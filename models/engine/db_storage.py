#!/usr/bin/python3
"""
Module containing New engine DBStorage specification
for using MySQL db for storage
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
import os
from models import amenity, base_model, city, place, review, state, user


class DBStorage:
    __engine = None
    __session = None

    __classes = {
                'BaseModel': base_model.BaseModel, 'User': user.User,
                'Place': place.Place, 'State': state.State,
                'City': city.City, 'Amenity': amenity.Amenity,
                'Review': review.Review
                }

    def __init__(self):
        """
        __init__ Class constructor
        """
        host = os.environ["HBNB_MYSQL_HOST"]
        user = os.environ["HBNB_MYSQL_USER"]
        passwd = os.environ["HBNB_MYSQL_PWD"]
        db = os.environ["HBNB_MYSQL_DB"]
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}"
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

    def all(self, cls=None):
        if cls is not None:
            if cls in self.__classes.keys():
                pass
        else:
            pass

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
