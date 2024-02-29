#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import Base, BaseModel
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
                              cascade='all, delete, delete-orphan')
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes the State model"""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """Getter method for cities in the State"""
            from models import storage
            from models.city import City
            city_instances = []
            for obj in storage.all(City).values():
                if obj.state_id == self.id:
                    city_instances.append(obj)
            return city_instances
