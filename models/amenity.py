#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from os import getenv


class Amenity(BaseModel):
    """ Amenity class for modelling Amenity objects """
#    if getenv('HBNB_TYPE_STORAGE') == 'db':
#        __tablename__ = amenities
#        name = Column(String(128), nullable=False)
#    else:
    name = ""
