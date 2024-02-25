#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String, relationship


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = "reviews"
    place_id = Column(String(60), ForeignKey("places.id"))
    user_id = Column(String(60), ForeignKey("users.id"))
    text = Column(String(1024))
    user = relationship("User")
    place = relationship("Place")
