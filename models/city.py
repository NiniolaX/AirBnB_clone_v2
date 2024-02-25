#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey, relationship


class City(BaseModel, Base):
    """ The city class for modelling city objects """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(ForeignKey("states.id"), String(60), nullable=False)
    places = relationship(
        "Place",
        backref="user",
        cascade="all, delete-orphan",
    )
