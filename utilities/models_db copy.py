from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, Date
from flask_login import UserMixin
from geoalchemy2 import Geometry
import datetime


db = SQLAlchemy()


class Watershed(db.Model):
    __tablename__ = 'watersheds'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False, unique=True)
    w_boundary = Column(Geometry('POLYGON')) 
    area = Column(Float, nullable = False)

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
    lm = Column(String, nullable=False)
    h_boundary = Column(Geometry('Polygon'))

class Rainfall(db.Model):
    __tablename__= 'rainfalls'
    id = Column(Integer, primary_key=True)
    watershed_id = Column(Integer, ForeignKey('watersheds.id'))
    date = Column(Date) 
    amount = Column(Float)


