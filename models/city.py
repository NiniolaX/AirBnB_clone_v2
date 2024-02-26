#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey


class City(BaseModel, Base):
    """ The city class for modelling city objects """
    __tablename__ = 'cities'
    name = Column(String(128), default='', nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
