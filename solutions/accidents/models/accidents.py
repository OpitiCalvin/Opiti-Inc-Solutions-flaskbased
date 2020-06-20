from the_app import db
from sqlalchemy import Column, Integer, String, Float, Time, Date
from geoalchemy2 import Geometry

class AccidentModel(db.Model):
    r"""A db model for accident records."""

    __tablename__ = "accident"

    accident_id = Column(Integer, primary_key=True, autoincrement=True)
    accident_index = Column(String(20))
    location_easting_osgr = Column(Integer)
    location_northing_osgr = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)
    police_force = Column(Integer)
    accident_severity = Column(Integer)
    number_of_vehicles = Column(Integer)
    number_of_casualties = Column(Integer)
    date = Column(Date)
    day_of_week = Column(Integer)
    time = Column(Time)
    geom = Column(Geometry('POINT', 27700), nullable = True)