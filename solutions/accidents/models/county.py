from the_app import db
from sqlalchemy import Column, Integer, String, Float
from geoalchemy2 import Geometry
from marshmallow import fields, Schema

class CountyModel(db.Model):
    r"""A db model for spatial extents and country information."""

    __tablename__ = 'county'

    county_id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(60))
    area_code = Column(String(3))
    description = Column(String(50))
    file_name = Column(String(50))
    number = Column(Float)
    number0 = Column(Float)
    polygon_id = Column(Integer)
    unit_id = Column(Integer)
    code = Column(String(9))
    hectares = Column(Float)
    area = Column(Float)
    type_code = Column(String(2))
    description0 = Column(String(25))
    type_code0 = Column(String(3), nullable = True)
    description1 = Column(String(25), nullable = True)
    geom = Column(Geometry('MULTIPOLYGON', 27700))

# class CountyQuerySchema(Schema):
#     r"""A serialization schema for County records."""

