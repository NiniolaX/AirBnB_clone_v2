#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Table, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv


class Amenity(BaseModel, Base):
    """ Amenity class for modelling Amenity objects """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship('Place',
                                       secondary='place_amenity',
                                       back_populates='amenities')
    else:
        name = ""
