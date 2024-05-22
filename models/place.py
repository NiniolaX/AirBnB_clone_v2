#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey
from os import getenv
from sqlalchemy.orm import relationship
from models.review import Review


class Place(BaseModel, Base):
    """ A place to stay """
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        place_amenity = Table('place_amenity', Base.metadata,
                              Column('place_id', String(60),
                                     ForeignKey('places.id'),
                                     primary_key=True, nullable=False),
                              Column('amenity_id', String(60),
                                     ForeignKey('amenities.id'),
                                     primary_key=True, nullable=False))
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
        amenities = relationship('Amenity',
                                 secondary='place_amenity',
                                 back_populates='place_amenities',
                                 viewonly=False)

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
        amenity_ids = []

        @property
        def reviews(self):
            """
            Getter method for reviews associated with current place.
            Return:
                (list): List of Review instances with place_id equal to current
                        place's id.
            """
            from models import storage
            from models.review import Review
            review_instances = []
            for obj in storage.all(Review).values():
                if obj.place_id == self.id:
                    review_instances.append(obj)
            return review_instances

        @property
        def amenities(self):
            """ Getter method for amenities associated with place
            Return:
                (list): List of Amenity instances associated with place
            """
            from models import storage
            from models.amenity import Amenity
            amenity_list = []
            for amenity in storage.all(Amenity).values():
                if amenity.id in amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """ Setter method for amenities associated with place
            Args:
                (obj): Amenity object
            Return:
                None
            """
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
