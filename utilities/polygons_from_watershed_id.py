from flask import session, jsonify
from sqlalchemy import select
import json
from shapely.geometry import mapping
from geoalchemy2.shape import to_shape

from utilities.models_db import Watershed, Zone, Lulc, Hru

def load_geometry_data(db: any, db_table_name:str, watershed_id=None) -> list[dict]:
    """
    Loads polygon data from a specified db table related to a given watershed.
    If the watershed_id is not provided, it is retrieved from the session.

    Args:
    db: Database session object
    db_table_name: String name of the db table (options: 'watersheds', 'zones', 'lulcs', 'hrus')
    watershed_id: Optional, the ID of the watershed

    Returns:
    list of dicts: Each dict contains data for one feature related to the watershed
    """
    # Mapping of string table names to actual table classes
    table_mapping = {
        'watersheds': {'class': Watershed, 'boundary_col': 'w_boundary'},
        'zones': {'class': Zone, 'boundary_col': 'z_boundary'},
        'lulcs': {'class': Lulc, 'boundary_col': 'l_boundary'},
        'hrus': {'class': Hru, 'boundary_col': 'h_boundary'}
    }

    # Get the table class from the mapping
    db_table_info = table_mapping.get(db_table_name)
    if not db_table_info:
        raise ValueError(f"Unknown db table name: {db_table_name}")

    db_table_class = db_table_info['class']
    boundary_column_name = db_table_info['boundary_col']

    # Special handling for 'watersheds' table since it uses 'id' instead of 'watershed_id'
    if db_table_name == 'watersheds':
        if not watershed_id:
            return None
        stmt = select(db_table_class).where(db_table_class.id == watershed_id)
    else:
        # For other tables, retrieve 'watershed_id' from session if not provided
        if not watershed_id:
            watershed_id = session.get('ws_id')

        if not watershed_id:
            return None

        stmt = select(db_table_class).where(db_table_class.watershed_id == watershed_id)

    response = db.session.execute(stmt)
    
    # Fetch all rows at once instead of using .first()
    rows = response.fetchall()
    
    # Check if there are no rows
    if not rows:
        return []

    geometries = []
    features = []

    for row in rows:
        feature = row[0]  # Assuming the first column is the desired feature

        shapely_geom = to_shape(getattr(feature, boundary_column_name))
        geometries.append(shapely_geom)
        geojson_dict = mapping(shapely_geom)
        geojson_string = json.dumps(geojson_dict)

        # Add other relevant attributes from the feature as needed
        feature_data = {
            "id": feature.id,
            "geojson": geojson_string
            # Include other attributes here
        }
        features.append(feature_data)

    # # return features
    return features

def load_json_from_db(db:any, db_table_name:str, watershed_id=None) -> list[dict]:
    """
    Loads data from a specified db table related to a given watershed and
    returns all attributes for each feature.
    If the watershed_id is not provided, it is retrieved from the session.
    
    Args:
    db: Database session object
    db_table_name: String name of the db table (options: 'watersheds', 'zones', 'lulcs', 'hrus')
    watershed_id: Optional, the ID of the watershed
    
    Returns:
    list of dicts: Each dict contains all attributes for one feature related to the watershed
    """
    # Mapping of string table names to actual table classes
    table_mapping = {
        'watersheds': {'class': Watershed, 'boundary_col': 'w_boundary'},
        'zones': {'class': Zone, 'boundary_col': 'z_boundary'},
        'lulcs': {'class': Lulc, 'boundary_col': 'l_boundary'},
        'hrus': {'class': Hru, 'boundary_col': 'h_boundary'}
    }
    
    # Get the table class from the mapping
    db_table_info = table_mapping.get(db_table_name)
    if not db_table_info:
        raise ValueError(f"Unknown db table name: {db_table_name}")
    
    db_table_class = db_table_info['class']
    boundary_column_name = db_table_info['boundary_col']
    
    # Special handling for 'watersheds' table since it uses 'id' instead of 'watershed_id'
    if db_table_name == 'watersheds':
        if not watershed_id:
            return None
        stmt = select(db_table_class).where(db_table_class.id == watershed_id)
    else:
        # For other tables, retrieve 'watershed_id' from session if not provided
        if not watershed_id:
            watershed_id = session.get('ws_id')
        
        if not watershed_id:
            return None
        
        stmt = select(db_table_class).where(db_table_class.watershed_id == watershed_id)
    
    # Execute the query
    response = db.session.execute(stmt)
    
    # Fetch all rows at once
    rows = response.fetchall()
    
    # Check if there are no rows
    if not rows:
        return []
    
    features = []

    # Go through each row and create a dictionary of all column values
    for row in rows:
        feature = row[0]  # Assuming the first column is the desired feature
        feature_data = {"type": "Feature"}

        properties = {}
        geojson = None

        # Use ORM descriptor to get all columns for the feature's class
        for column in feature.__table__.columns:
            # Convert geometry to GeoJSON if it's the boundary column
            if column.name == boundary_column_name:
                shapely_geom = to_shape(getattr(feature, column.name))
                geojson = mapping(shapely_geom)
            else:
                # Add other attributes to the properties dictionary
                properties[column.name] = getattr(feature, column.name)

        feature_data["properties"] = properties
        feature_data["geometry"] = geojson

        features.append(feature_data)

    return features