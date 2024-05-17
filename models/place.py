#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from os import getenv
from sqlalchemy.orm import relationship
from models.review import Review


class Place(BaseModel, Base):
    """ A place to stay """
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review',
                               cascade='all, delete, delete-orphan',
                               backref='place')

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0

        @property
        def reviews(self):
            """
            Getter method for reviews associated with current place.
            Return: 
                List of Review instances with place_id equal to current
                place_id
            """
            from models import storage
            from models.review import Review
            review_instances = []
            for obj in storage.all(Review).values():
                if obj.place_id == self.id:
                    review_instances.append(obj)
            return review_instances

