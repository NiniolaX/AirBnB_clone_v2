#!/usr/bin/python3
""" City Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class for modelling city objects """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)


    def __init__(self, *args, **kwargs):
        """Initializes the City model"""
        from models import storage
        from models.state import State

        if 'name' not in kwargs or 'state_id' not in kwargs:
            return
        if f"State.{kwargs['state_id']}" not in storage.all(State).keys():
            return
        super().__init__(*args, **kwargs)
