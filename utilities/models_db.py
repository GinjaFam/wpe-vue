from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, Date
from flask_login import UserMixin
from geoalchemy2 import Geometry


db = SQLAlchemy()


class User(db.Model, UserMixin): #UserMixin is needed by Flask Login. to do its magic
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    pwd = Column(String, nullable =False)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)

class UserData(db.Model):
    __tablename__= 'user_data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    organization = Column(String, nullable=True)
    datereg = Column(DateTime, nullable=False)
    country = Column(String, nullable=True)
    lang = Column(String, nullable=True)
    news = Column(Boolean, nullable=True)
    
class Watershed(db.Model):
    __tablename__ = 'watersheds'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False, unique=True)
    w_boundary = Column(Geometry('POLYGON')) 
    area = Column(Float, nullable = False)

# class Zone(db.Model):
#     __tablename__= 'zones'
#     id = Column(Integer, primary_key=True)
#     watershed_id = Column(Integer, ForeignKey('watersheds.id'))
#     z_type = Column(String, nullable=False)
#     z_boundary = Column(Geometry('Polygon'))
    
class Zone(db.Model):
    __tablename__= 'zones'
    id = Column(Integer, primary_key=True)
    watershed_id = Column(Integer, ForeignKey('watersheds.id'))
    z_type = Column(String, nullable=False)
    #TODO: make nullable=True
    z_hsg = Column(String)
    z_slope = Column(Float)
    z_amc = Column(Integer)
    z_boundary = Column(Geometry('Polygon'))


class Lulc(db.Model):
    __tablename__= 'lulcs'
    id = Column(Integer, primary_key=True)
    watershed_id = Column(Integer, ForeignKey('watersheds.id'))
    zone_id = Column(Integer, ForeignKey('zones.id'))
    l_type = Column(String, nullable=False)
    l_boundary = Column(Geometry('Polygon'))

class Hru(db.Model):
    __tablename__= 'hrus'
    id = Column(Integer, primary_key=True)
    watershed_id = Column(Integer, ForeignKey('watersheds.id'))
    zone_id = Column(Integer, ForeignKey('zones.id'))
    lulc_id = Column(Integer, ForeignKey('lulcs.id'))
    slope = Column(Float, nullable=False)
    amc = Column(Integer, nullable=False)
    hsg = Column(Integer, nullable=False)
    cn = Column(Integer, nullable=False)
    h_boundary = Column(Geometry('Polygon'))

class Mock(db.Model):
    __tablename__= 'mocks'
    id = Column(Integer, primary_key=True)
    watershed_id = Column(Integer)
    zone_id = Column(Integer)
    lulc_id = Column(Integer)
    slope = Column(Float, nullable=False)
    amc = Column(Integer, nullable=False)
    hsg = Column(Integer, nullable=False)
    cn = Column(Integer, nullable=False)
    h_boundary = Column(Geometry('Polygon'))


class Rainfall(db.Model):
    __tablename__= 'rainfalls'
    id = Column(Integer, primary_key=True)
    watershed_id = Column(Integer, ForeignKey('watersheds.id'))
    date = Column(Date) 
    amount = Column(Float)


class CNumber(db.Model):
    __tablename__ = 'cnumbers'
    id = Column(Integer, primary_key=True)
    l_type = Column(String)
    treatment = Column(String)
    h_condition = Column(String)
    hsg_a = Column(Integer)
    hsg_b = Column(Integer)
    hsg_c = Column(Integer)
    hsg_d = Column(Integer)
    


