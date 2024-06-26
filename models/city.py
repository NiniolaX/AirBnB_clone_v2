#!/usr/bin/python3
""" City Module for HBNB project """
from os import getenv
from models.base_model import Base, BaseModel
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class for modelling city objects """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship('Place',
                              cascade='all, delete, delete-orphan',
                              backref='cities')
    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """Initializes the City model"""
        super().__init__(*args, **kwargs)
