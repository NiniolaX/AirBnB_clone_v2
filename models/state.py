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
        name = Column(String(128), nullable=False)
        from models.city import City
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes the State model"""
        if 'name' not in kwargs.keys():
            return
        super().__init__(*args, **kwargs)


    @property
    def cities(self):
        """Getter method for cities in the State"""
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            from models import storage
            from models.city import City
            cities = []
            for obj in storage.all(City).values():
                if cities.state_id == self.id:
                    cities.append(obj)
            return cities
