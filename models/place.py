#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage
from models.review import Review
from sqlalchemy import Column, String, Integer, FLOAT, ForeignKey, relationship


class Place(BaseModel):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"))
    user_id = Column(String(60), ForeignKey("users.id"))
    user = relationship("User")
    cities = relationship("City")
    name = Column(String(128))
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(FLOAT)
    longitude = Column(FLOAT)
    amenity_ids = []
    reviews = relationship(
        "Review",
        backref="place",
        cascade="all, delete-orphan",
    )

    @property
    def reviews(self):
        return [review for review in storage.all(Review) if review.place_id == self.id]
