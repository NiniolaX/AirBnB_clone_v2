#!/usr/bin/python3
"""
Module containing New engine DBStorage specification
for using MySQL db for storage
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
import os
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class DBStorage:
    __engine = None
    __session = None

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
        if os.environ.get('HBNB_ENV') == 'test':
            """drop all tables"""
            pass

    def all(self, cls=None):
        """ Query current database section """
        classes = {
                'BaseModel': BaseModel, 'User': User,
                'Place': Place, 'State': State,
                'City': City, 'Amenity': Amenity,
                'Review': Review
                }
        if cls is not None:
            if cls in classes.values():
                results = self.__session.query(cls).all()
        else:
            results = self.__session.query(State, City).all()
        __objects = {}
        for obj in results:
            __objects[f"{obj.__class__.__name__}.{obj.id}"] = obj
            return __objects

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
