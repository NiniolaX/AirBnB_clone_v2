#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False, default='')
        from models import City
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes the State model"""
        super().__init__(*args, **kwargs)
