#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
#from models.review import Review
#from sqlalchemy import Column, String, Integer, FLOAT, ForeignKey
#from sqlalchemy.orm import relationship


class Place(BaseModel):
    """ A place to stay """
    #__tablename__ = "places"
    city_id = '' #Column(String(60), ForeignKey("cities.id"))
    user_id = '' #Column(String(60), ForeignKey("users.id"))
    user = '' #relationship("User")
    cities = '' #relationship("City")
    name = '' #Column(String(128))
    description = '' #Column(String(1024))
    number_rooms = 0 #Column(Integer, default=0)
    number_bathrooms = 0 #Column(Integer, default=0)
    max_guest = 0 #Column(Integer, default=0)
    price_by_night = 0 #Column(Integer, default=0)
    latitude = 0.0 #Column(FLOAT)
    longitude = 0.0 #Column(FLOAT)
    amenity_ids = []
    #reviews = relationship(
        #"Review",
        #backref="place",
        #cascade="all, delete-orphan",
    #)

    #@property
    #def reviews(self):
        #"""
        #reviews _summary_

        #Returns:
            #_type_: _description_
        #"""
        #from models import storage
        #return (
            #review
            #for review in storage.all(Review)
            #if review.place_id == self.id
        #)
