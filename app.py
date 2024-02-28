from flask import Flask, render_template, g, request, redirect, url_for, flash, jsonify
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt, generate_password_hash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_cors import CORS

from flask import current_app

from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, FloatField, IntegerField, IntegerRangeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from flask_wtf import FlaskForm

from datetime import timedelta, datetime
from config import DevelopmentConfig

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, create_engine, select
from sqlalchemy.event import listen
from sqlalchemy.pool import Pool
from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape, to_shape
from geoalchemy2 import functions as func

from sqlalchemy.sql import func

from shapely.geometry import shape, mapping
from shapely.ops import split
from shapely import wkt

import geopandas as gpd

import pycountry
import json
import logging
import flask_profiler
import time


from utilities.models_db import db 
from utilities.cn_to_db import cn_to_db
from utilities.random_hrus_generator import generate_random_hrus
from utilities.polygons_from_watershed_id import load_geometry_data, load_json_from_db
from utilities.models_db import Watershed, Zone, Lulc, User, UserData, Hru, Rainfall, CNumber
import json

# Initialize Flask app
app = Flask(__name__)
# Load the configuration from the config.py file --> in this case is the development configuration
app.config.from_object(DevelopmentConfig)
# db = SQLAlchemy(app) # Initialize SQLAlchemy database object


db.init_app(app)
migrate = Migrate(app, db)

# Super cool way to load the data from the csv file into the database 
@app.cli.command("load_data")
def loaddata_command():
    """Load data from CSV into database. Just run 'flask load_data' in the CLI"""
    cn_to_db('data_files/CN_table_clean.csv')
    print("Data loaded.")

@app.cli.command("create_random_hrus")
def create_random_hrus_command():
    """Create random HRUs. Just run 'flask create_random_hrus' in the CLI"""
    with current_app.app_context():
        generate_random_hrus()
    print("Random HRUs created and added to the db")
    

logging.basicConfig(level=logging.INFO)

CORS(app)
bcrypt = Bcrypt(app)

# Flask Login stuff

login_manager = LoginManager() # Initialize Flask Login object
login_manager.init_app(app) # Initialize Flask Login object with the app
login_manager.login_view = 'login' 

@login_manager.user_loader # This is a decorator that tells Flask Login how to load a user from the database
def load_user(user_id):  # This function is used to reload the user object from the user ID stored in the session
    return User.query.get(int(user_id)) 



with app.app_context():
    db.create_all()

# Form Classes are defined by creating a subclass of the FlaskForm i imported.
    
class RegistrationForm(FlaskForm):
    name =  StringField("Your name", validators=[DataRequired()])
    last_name = StringField("Your last name", validators=[DataRequired()])
    username = StringField("Choose a username", validators=[DataRequired()])
    organization = StringField("Your organization")
    email = StringField('Email', validators=[DataRequired(), Email()])
    country = SelectField('Country', choices=[(country.name, country.name) for country in pycountry.countries])
    language = SelectField('Preferred language', choices=['English', 'French','Spanish'], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    newsletter = BooleanField('Want to hear from us?')
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Log in")



class ZoneForm(FlaskForm):

    type = StringField('Name for the zone', validators=[
        DataRequired()
    ])

    slope = IntegerField('Slope of the land', validators=[
        DataRequired(), 
        NumberRange(
            min=0, 
            max=100, 
            message='The slope value should be expressed in percentage and it can have a minimum of 0 and a maximum of 100'
            )
    ])

    hsg = SelectField('Hydrological Soil Group', 
        choices=[
            ('a', 'Group A'),
            ('b', 'Group B'),
            ('c', 'Group C'),
            ('d', 'Group D')
        ]
    )

    amc = SelectField('Antecedent Moisture Condition',
        choices=[
            (1, 'Dry'),
            (2, 'Average'),
            (3, 'Moist')
        ],
        validators=[
            DataRequired()
        ])   
    
    submit = SubmitField('Save Zone')

class LulcForm(FlaskForm):
    # TODO:use htmx to do it dynamic field selection updates! https://htmx.org/examples/value-select/
    
    type = SelectField(
        'Land Use Type',
        validators=[
            DataRequired()
        ],
        choices=[
            ('fallow', 'Fallow'),
            ('row crops', 'Row crops'),
            ('small grain', 'Small grains'),
            ('close-seeded or broadcast legumes or rotation meadow', 'Close-seeded or broadcast legumes or rotation meadow'),
            ('pasture, grassland, or range- continuous forage for grazing', 'Pasture, grassland, or range- continuous forage for grazing'),
            ('meadow-continuous grass, generally mowed for hay', 'Meadow-continuous grass, generally mowed for hay'),
            ('brush-brush-forbs-grass mixture, with brush the major element','Brush-brush-forbs-grass mixture, with brush the major element'),
            ('woods-grass comb. (orchard/tree farm)','Woods-grass combination (Orchard/Tree farm)'),
            ('woods','Woods'),
            ('farmstead-buildings, lanes, driveways and lots','farmstead-buildings, lanes, driveways and lots'),
            ('dirt roads','Dirt roads'),
            ('gravel roads','Gravel roads')
        ]
    )

    submit = SubmitField('Save LULC unit')


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

    
@app.route('/', methods=['GET','POST'])
def index():

    reg_form = RegistrationForm()
    log_form = LoginForm()
    
    return render_template('index.html', log_form=log_form, reg_form=reg_form)

@app.route('/sidebar')
def sidebar():
    reg_form = RegistrationForm()
    log_form = LoginForm()
    return render_template('snippets/sidebar.html', reg_form=reg_form, log_form=log_form)

@app.route('/register', methods=['GET','POST'])
def register():
    reg_form = RegistrationForm()
    log_form = LoginForm()
    try: 
        hashed_password = bcrypt.generate_password_hash(reg_form.password.data).decode('utf-8') # decode is needed to convert the hashed password to a string
        user = User(email=reg_form.email.data, # Create an instance of the class User with attributes from the form
                    pwd=hashed_password, 
                    username = reg_form.username.data
                    )
        db.session.add(user) # Add the instance to the database
        db.session.commit() # Commit the changes to the database

        user_data = UserData(user_id=user.id, # Create an instance of the class UserData with attributes from the form
                            name=reg_form.name.data,
                            last_name=reg_form.last_name.data,
                            organization=reg_form.organization.data,
                            country=reg_form.country.data,
                            lang=reg_form.language.data,
                            news=reg_form.newsletter.data,
                            datereg=datetime.now() # datetime.now() is a function that returns the current date and time
                            )
        
        db.session.add(user_data) 
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success') # Flash a message to the user

        return render_template('index.html', reg_form=reg_form, log_form=log_form)

    except Exception as e: # If something goes wrong, print the error and flash a message to the user
        print(f"An error occurred: {e}")
        flash('An error occurred. Please try again.', 'danger')
        return render_template('index.html', reg_form=reg_form, log_form=log_form)

@app.route('/login', methods=['GET','POST'])
def login():
    log_form = LoginForm()
    reg_form = RegistrationForm()

    if log_form.validate_on_submit():
        user = User.query.filter_by(email=log_form.email.data).first()
        if user and bcrypt.check_password_hash(user.pwd, log_form.password.data):
            # If the user exists and the password is correct, log the user in with the login_user function from Flask Login
            login_user(user)
            flash('You have been logged in!', 'success')
            print(f"LOGGED IN as: {current_user.email} ")
            return render_template('index.html', log_form=log_form, reg_form=reg_form)
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('index.html', log_form=log_form, reg_form=reg_form )

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))


# @app.route('/watershed', methods=['GET'])
# def watershed():
    
#     return render_template('snippets/watershed.html', wsd = wsd)

# in this route the user can load the watersheds that are already saved in the db
@app.route('/ws_load', methods=['GET','POST'])
def ws_load():
    ''' 
    Get the existing watersheds from the database for the logged in user and create a geojson. 
    If the user clicks on the load button, the watershed id is loaded in the session and a message is flashed to the user. 
    If the user clicks on the remove button, the watershed is removed from the database.

    It expects a GET request when the page is loaded and a POST request when the user clicks on the load button.

    '''
    print(f'ws_load:------------------->hello route')
    stmt = select(Watershed).where(Watershed.user_id == current_user.id)
    watershedsUser = db.session.execute(stmt)
    print(watershedsUser)
    #Create an empty list where to append the watersheds with the for loop
    wsd = []
    print(f'ws_load:-------------------> the watersheds are: {wsd}')

    # Loop through the query results and append the watersheds to the list
    # TODO: the block below could be abstracted away with a function
    # if wsd is empty, return a message to the user
    if not watershedsUser:
        pass
        # flash("No Watershed Found")
        # return "No Watershed Found", 404
    else:
        for row in watershedsUser:
            watershed = row.Watershed
            # Convert the geom attribute to a Shapely geometry
            shapely_geom = to_shape(watershed.w_boundary)
            # Convert the Shapely geometry to GeoJSON
            geojson_geom = json.dumps(mapping(shapely_geom))            
            area = None
            if isinstance(watershed.area, float):
                area = round(watershed.area, 2)

            wsd.append({
                "id": watershed.id,
                "user_id": watershed.user_id,
                "name": watershed.name,
                "geojson": geojson_geom,
                "area": area,
                })
        
    # if the request method is GET  
    if request.method == 'GET' and 'HX-Request' in request.headers:
        print("HTMX Request Received", request.headers.get('HX-Trigger'))
        trigger = request.headers.get('HX-Trigger', None)
        if trigger == 'wsLoad':
            return render_template('snippets/ws_load.html',wsd=wsd)
    
    elif request.method == 'POST' and request.form['status'] == 'loaded':
            # save to a variable the watershed from the post request
            watershed_id = request.form['watershed_id']
            # store the loaded watershed in a variable
            wsd = Watershed.query.filter_by(id=watershed_id).first()            
            # save to the session the watershed id
            session['watershed_id'] = watershed_id
            flash('Watershed loaded successfully! Proceed to Zone delineation', 'success')
            return render_template('snippets/ws_loaded.html', wsd=wsd) #render_template('snippets/ws_load_success.html')
    
    
    return render_template('snippets/ws_load.html',wsd=wsd)

@app.route('/ws_remove', methods=['POST'])
def ws_remove():
    '''
    This route removes the watershed from the database. Before deleting the watershed, it asks the user to confirm the action.
    '''
    # TODO: Add a confirmation message to the user before deleting the watershed
    # FIXME: Get the user_id from the session not from the form

    # Get the id of the watershed to remove from the request
    watershed_id = request.form['watershed_id']
    # Query the watershed from the database
    watershed = Watershed.query.filter_by(id=watershed_id).first()
    # Delete the watershed from the database
    db.session.delete(watershed)
    db.session.commit()
    db.session.close()
    # Return a success message
    message = "Watershed removed successfully!"
    flash(message)
    return redirect(url_for('ws_load'))

@app.route('/ws_unload', methods=['POST'])
def ws_unload():
    '''
    Tbhis route unloads the watershed from the session, when clicking the unload button 
    '''
    #unload the watershed from the session
    session.pop('watershed_id', None)
    # Return a success message
    message = "Watershed unloaded successfully!"
    flash(message)
    return redirect(url_for('ws_load'))

@app.route('/ws_draw', methods=['GET'])
def ws_draw():
    '''
    This route allows the user to draw a new watershed
    '''
    return render_template('snippets/ws_draw.html')

@app.route('/ws_save', methods=['POST'])
def ws_save():
    ''' 
    This route saves the watershed to the database. It expects a POST request with the geojson data.
    '''
    # Get the geojson from the request
    geojson_str = request.form['geojsonData']
    # Convert the geojson to a Python dictionary
    geojson = json.loads(geojson_str)
    # Convert the geojson to a Shapely geometry
    shapely_geom = shape(geojson['geometry'])
    # Convert the Shapely geometry to a GeoAlchemy2 geometry
    geom = from_shape(shapely_geom, srid=4326)
    # Calculate the area of the watershed
    area = shapely_geom.area
    # Create a new watershed object
    watershed = Watershed(user_id=current_user.id, 
                        name=geojson['properties']['name'], 
                        w_boundary=geom, 
                        area=area)
    # Add the watershed to the database
    db.session.add(watershed)
    db.session.commit()
    db.session.close()  # Close the session
    # Return a success message
    message = "Watershed saved successfully!"
    flash(message)
    return render_template('snippets/ws_load.html', message=message)

@app.route('/ws_upload')
def ws_upload():
    # TODO: Add a form to upload the file
    return render_template('snippets/ws_load.html')

@app.route('/ws_auto') 
def ws_auto():
    # TODO: add the function to automatically delineate the watershed
    return render_template('snippets/ws_load.html')

# Routes to handle the zones polygons

@app.route('/zones', methods=['GET'])
def zones():
    return render_template('snippets/zones.html')

@app.route('/z_load', methods=['GET','POST'])
def z_load():
    '''
    This route loads the watershed already in the db 
    If no Watershed is loaded in the session, it returns a message
    If a watershed is loaded, it searches the corresponding zone  in the db and loads it in the frontend
   

    If no watershed is loaded in the session, it flashes a message to the user 
    If zones already exists for the watershed, it loads them in the map.
    If no zones exists, it flashes a message to the user and allows to draw a new zone.
    '''
    # Safe access to the session data
    
    watershed_id = session.get('watershed_id')
    print(f"z_load--------->>THE WATERSHED ID IS: {watershed_id}")
    wsd = None
    zn = None
    wsd = load_geometry_data(db, 'watersheds', watershed_id)

    z_form = ZoneForm()

    if request.method == 'GET':
        if wsd is None:
            flash("No Watershed Found")
            return "No Watershed Found", 404
        else:
            zn = load_json_from_db(db,'zones',watershed_id)
            print(f"z_load--------->>THE ZONES ARE: {zn}")
            if not zn:
                zn=[]
                flash("There are no zones for this watershed. Please draw a new zone")
                return render_template('snippets/z_load.html', current_route='z_load', wsd_loaded = wsd, zn_loaded=zn, z_form=z_form)
            else:
                messages = [f"the loaded watershed is {wsd[0]['id']}"]
                return render_template('snippets/z_load.html', messages=messages, zn_loaded=zn, wsd_loaded = wsd, z_form=z_form)
    
    elif request.method == 'POST':

        data = request.form['zPolygonData']
        jsonData = json.loads(data)        
        shapely_geom = shape(jsonData['geometry'])
        geom = from_shape(shapely_geom, srid=4326)
        # Create a new watershed object
        zone = Zone(watershed_id = watershed_id,
                            z_type = z_form.type.data,
                            z_hsg = z_form.hsg.data,
                            z_slope =  z_form.slope.data,
                            z_amc = z_form.amc.data,
                            z_boundary = geom)
        # Add the watershed to the database
        db.session.add(zone)
        db.session.commit()
        db.session.close()  # Close the session
        # Return a success message
        message = "Zone saved successfully!"
        flash(message)
        zn = load_json_from_db(db,'zones',watershed_id)
        return render_template('snippets/z_table.html', zn_loaded=zn, wsd_loaded = wsd)


# Route allows user to draw or modify and then save a new watershed zone
@app.route('/z_draw', methods=['POST'])
def z_draw():
    # get the data from the frontend fetch post request and store it in a variable
    ws_id = session.get('watershed_id')
    polygon_data = request.get_json()

    print(f"z_draw--------->>THE Line LOADED IS: {polygon_data}")
    # Just focus on the geometry bit of the feature
    polygon = shape(polygon_data['geometry'])
    print(f"z_draw--------->>THE saheply line LOADED IS: {polygon}")

    z_features = load_geometry_data(db, 'zones', ws_id)
    print('Features print: -------->>:',z_features)
    # TODO: Draw the polygons feature 

    return jsonify({"status": "success", "message": "Line processed"})

@app.route('/z_remove', methods=['DELETE'])
def z_remove():
    '''
    This route removes a zone from the database. Before deleting the watershed, it asks the user to confirm the action.
    '''
    watershed_id = session.get('watershed_id')
    wsd = load_geometry_data(db, 'watersheds', watershed_id)
    zn = load_json_from_db(db,'zones',watershed_id)
    # Get the id of the zone to remove from the request
    print(f'zn_remove:-------> request content type:{request.content_type}')
    print(f'zn_remove:-------> request forma data:{request.form}')
    zone_id = request.form.get('id')
    print(f'zn_remove:-------> id of zone to remove:{zone_id}')
    # Query the watershed from the database
    zone_to_remove = Zone.query.filter_by(id=zone_id).first()
    # Delete the watershed from the database
    db.session.delete(zone_to_remove)
    db.session.commit()
    db.session.close()
    # Return a success message
    message = "Zone removed successfully!"
    flash(message)
    return render_template('snippets/z_load.html', wsd_loaded = wsd, zn_loaded=zn)

@app.route('/z_edit', methods=['PUT'])
def z_edit():
    # TODO: Add z_edit route and related functionalities
    pass



#Routes to handle the LULC polygons

@app.route('/lulc', methods=['GET'])
def lulc():
    return render_template('snippets/lulc.html')

# Route to load LULC already in the db for the loaded watershed
@app.route('/l_load', methods=['GET','POST'])
def l_load():
    '''
    This route loads the lulc sub-units already in the db 
    If no Watershed is loaded in the session, it returns a message
    If a watershed is loaded, it searches the corresponding lulc sub-unit/s and passes it to the frontend
   
    If lulc sub-unit/s already exist/s for the watershed, it loads them in the map.
    If no lulc sub-unit/s exist/s yet, it flashes a message to the user and allows to draw a new zone.
    '''
    watershed_id = session.get('watershed_id')    
    wsd = None
    zn = None
    l = []

    wsd = load_geometry_data(db, 'watersheds', watershed_id)
    zn = load_json_from_db(db,'zones', watershed_id)


    lform = LulcForm()

    if request.method == 'GET':
        if wsd is None:
            flash("No Watershed Found")
            return "No Watershed Found", 404
        elif zn is None:
            flash("No Zone Found")
            return "No Zone Found", 404
        else:
            l = load_json_from_db(db,'lulcs',watershed_id)
            if not l:
                l = []
                flash("There are no lulc sub-units for this watershed. Please draw a new zone")
                
            messages = [f"the loaded watershed is {wsd[0]['id']}"] #TODO add zns too?
            print(f"l_load --------> The lulc sub-units are: {l}")
            return render_template('snippets/l_load.html', messages=messages, wsd_loaded = wsd, l_loaded=l, zn_loaded=zn, lform=lform)

    elif request.method == 'POST':
        z_id = []
        data = request.form['lPolygonData']
        jsonData = json.loads(data)
        shapely_geom = shape(jsonData['geometry'])
        geom = from_shape(shapely_geom, srid=4326)

        point_on_surface = db.session.query(func.ST_PointOnSurface(geom)).scalar()

        # Find the zone_id of the corresponding zone that contains the point
        zone = db.session.query(Zone).filter(func.ST_Contains(Zone.z_boundary, point_on_surface)).first()
        if zone:
            z_id = zone.id
    
        lulc = Lulc(watershed_id=watershed_id,
                    zone_id= z_id,
                    l_type=lform.type.data, 
                    l_boundary=geom,
                    )
        db.session.add(lulc)
        db.session.commit()
        db.session.close()  
        message = "Lulc sub-unit saved successfully!"
        flash(message)
        l = load_json_from_db(db,'lulcs',watershed_id)
        return render_template('snippets/l_load.html', wsd_loaded = wsd, l_loaded=l, zn_loaded=zn, lform=lform)

@app.route('/l_remove', methods=['DELETE'])
def l_remove():
    '''
    This route removes a lulc sub-unit from the database. Before deleting the sub-unit, it asks the user to confirm the action.
    '''
    watershed_id = session.get('watershed_id')
    wsd = load_geometry_data(db, 'watersheds', watershed_id)
    zn = load_json_from_db(db,'zones', watershed_id)
    l = load_json_from_db(db, 'lulcs', watershed_id)
    # Get the id of the zone to remove from the request
    print(f'l_remove:-------> request content type:{request.content_type}')
    print(f'l_remove:-------> request forma data:{request.form}')
    l_id = request.form.get('id')
    print(f'zn_remove:-------> id of zone to remove:{l_id}')
    # Query the watershed from the database
    lulc_to_remove = Lulc.query.filter_by(id=l_id).first()
    # Delete the watershed from the database
    db.session.delete(lulc_to_remove)
    db.session.commit()
    db.session.close()
    # Return a success message
    message = "LULC sub-unit removed successfully!"
    flash(message)
    return render_template('snippets/l_load.html', wsd_loaded = wsd, zn_loaded=zn, l_loaded = l)



@app.route('/hrus', methods=['GET'])
def hrus():
    return render_template('snippets/hrus.html')

# Route to load HRUs already in the db for the loaded watershed
@app.route('/h_load', methods=['GET','POST'])
def h_load():
    '''
    This route loads the hrus sub-units already in the db 
    If no Watershed is loaded in the session, it returns a message
    If a watershed is loaded, it searches the corresponding hrus sub-unit/s and passes it to the frontend
   
    If hrus sub-unit/s already exist/s for the watershed, it loads them in the map.
    If no hrus sub-unit/s exist/s yet, it flashes a message to the user and allows to draw a new hru sub-unit.
    '''

    #TODO: rename the table from swcs to hrus

    # Safe access to the session data
    watershed_id = session.get('watershed_id')
   
    print(f"h_load --------> THE WATERSHED ID IS: {watershed_id}")
    
    wsd = None
    zn = None
    l = []
    h = []

    wsd = load_geometry_data(db, 'watersheds', watershed_id)
    print(f"h_load --------> THE ws IS: {wsd}")

    zn = load_json_from_db(db,'zones', watershed_id)
    print(f"h_load --------> THE zns are: {zn}")

    l = load_json_from_db(db, 'lulcs', watershed_id)
    print(f"h_load --------> THE lulcs are: {l}")

    # hru_form = HruForm()
    

    if request.method == 'GET':
        if wsd is None:
            flash("No Watershed Found")
            return "No Watershed Found", 404
        elif zn is None:
            flash("No Zone Found")
            return "No Zone Found", 404
        elif l is None:
            flash("No LULC found")
            return "No LULC found", 404
        else:
            h = load_json_from_db(db,'hrus',watershed_id) # TODO: change database from swcs to hrus
            print(f"h_load GET--------> THE h from the load_json_from_db is: {h}")

            if not h:
                h=[]
                flash("There are no HRUs sub-units for this watershed. Please draw a new one")
                
            messages = [f"the loaded watershed is {wsd[0]['id']}"] #TODO add zns too?
            print(f"\n h_load GET --------> The HRUs are: {h} \n")
            return render_template('snippets/h_load.html', messages=messages, wsd_loaded = wsd, l_loaded=l, zn_loaded=zn, h_loaded=h)

    elif request.method == 'POST':
        z_id = []
        l_id = []

        data = request.form['hPolygonData'] #TODO: Same name in the hidden input field of the form html
        print(f'\n h_load POST ----------> hru polygon data is:{data} \n')


        jsonData = json.loads(data)

        print(f'h_load POST----------> the drawn hru polygon is:{jsonData}')
        
        shapely_geom = shape(jsonData['geometry'])
        # Convert the Shapely geometry to a GeoAlchemy2 geometry
        geom = from_shape(shapely_geom, srid=4326)
        print(f'\n h_load POST----------> the geom hru polygon to load is:{geom}\n')

        # Calculate ST_PointOnSurface for the HRU polygon
        point_on_surface = db.session.query(func.ST_PointOnSurface(geom)).scalar()

        # Find the zone_id of the corresponding zone that contains the point
        zone = db.session.query(Zone).filter(func.ST_Contains(Zone.z_boundary, point_on_surface)).first()
        if zone:
            z_id = zone.id

        print(f'h_load ----------> the z_id is:{z_id}')
        

        # Find the lulc_id of the corresponding LULC that contains the point
        lulc = db.session.query(Lulc).filter(func.ST_Contains(Lulc.l_boundary, point_on_surface)).first()
        if lulc:
            l_id = lulc.id
        print(f'h_load ----------> the l_id is:{l_id}')

        # Create a new watershed object
        hru = Hru(watershed_id=watershed_id,
                            zone_id= z_id,
                            lulc_id= l_id,
                            h_boundary=geom,
                    )
        # Add the watershed to the database
        db.session.add(hru)
        db.session.commit()
        db.session.close()  # Close the session
        # Return a success message
        message = "HRU sub-unit saved successfully!"
        flash(message)
        return render_template('snippets/h_load.html', wsd_loaded = wsd, l_loaded=l, zn_loaded=zn, h_loaded=h)


@app.route('/identify_polygon', methods=['POST'])
def identify_polygon():
    point = request.get_json()
    point_geometry = shape(point['geometry'])
    point_wkt = wkt.dumps(point_geometry)  # Convert to WKT
    # Convert the WKT string to a geometry and set the SRID to 4326
    point_geom = func.ST_SetSRID(func.ST_GeomFromText(point_wkt), 4326)


    intersecting_lulc = Lulc.query.filter(Lulc.l_boundary.ST_Intersects(point_geom)).first()
    print(f'identify_polygon:-------> intersecting_lulc:{intersecting_lulc}')
    if intersecting_lulc:
        lulc_name = intersecting_lulc.l_type
        print(f'identify_polygon:-------> lulc_name:{lulc_name}')
        treatment_options = CNumber.query.filter_by(l_type=lulc_name).distinct(CNumber.treatment).all()
        print(f'identify_polygon:-------> treatment options query result:{treatment_options}')
        # list comprehension to get the treatment options
        options = [option.treatment_options for option in treatment_options]
        print(f'identify_polygon:-------> treatment options list:{options}')
        return json.dumps(options)
    else:
        return json.dumps('No intersecting zone found')
    
# @app.route('/l_remove', methods=['DELETE'])
# def l_remove():
#     '''
#     This route removes a lulc sub-unit from the database. Before deleting the sub-unit, it asks the user to confirm the action.
#     '''
#     watershed_id = session.get('watershed_id')
#     wsd = load_geometry_data(db, 'watersheds', watershed_id)
#     zn = load_json_from_db(db,'zones', watershed_id)
#     l = load_json_from_db(db, 'lulcs', watershed_id)
#     # Get the id of the zone to remove from the request
#     print(f'l_remove:-------> request content type:{request.content_type}')
#     print(f'l_remove:-------> request forma data:{request.form}')
#     l_id = request.form.get('id')
#     print(f'zn_remove:-------> id of zone to remove:{l_id}')
#     # Query the watershed from the database
#     lulc_to_remove = Lulc.query.filter_by(id=l_id).first()
#     # Delete the watershed from the database
#     db.session.delete(lulc_to_remove)
#     db.session.commit()
#     db.session.close()
#     # Return a success message
#     message = "LULC sub-unit removed successfully!"
#     flash(message)
#     return render_template('snippets/l_load.html', wsd_loaded = wsd, zn_loaded=zn, l_loaded = l)


# Routes to handle the SWC polygons



# Route to load SWC already in the db for the loaded watershed
@app.route('/load_swc', methods=['GET','POST'])
def load_swc():
    pass

# Route allows user to draw or modify and then save a new watershed SWC
@app.route('/draw_swc', methods=['GET','POST'])
def draw_swc():
    pass

@app.route('/get-hydrological-conditions')
def get_hydro_conditions():
    lulc_id = request.args.get('lulc_id')
    land_use = None
    # get the land use type from the database
    with app.app_context():
        conn = db.engine.connect()
        land_use = Lulc.query.filter_by(id=lulc_id).first()
        conn.close()
    return jsonify(land_use)

if __name__ == '__main__':
    app.run(debug=True, 
            host='0.0.0.0', 
            port=5000,
            )
    