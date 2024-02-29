#!/usr/bin/python3
"""
Module containing new engine DBStorage specification
for using MySQL db for storage
"""
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City

classes = {
    'State': State,
    'City': City,
}


class DBStorage:
    """ Class for configuring database storage engine """
    __engine = None
    __session = None

    def __init__(self):
        """
        __init__ Class constructor
        """
        from os import getenv
        from sqlalchemy import create_engine
        host = getenv("HBNB_MYSQL_HOST")
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}"
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            """drop all tables"""
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """ Query current database section

        Args:
            cls(str): Name of class whose table is to be queried (optional)

        Return:
            __objects(dict): Format: <class-name.obj-id> = obj
        """
        if not self.__session:
            self.reload()

        objects = {}
        
        if cls:
            # Save all objects of class 'cls' in database to objects
            for obj in self.__session.query(cls).all():
                objects[f"{obj.__class__.__name__}.{obj.id}"] = obj
        else:
            # Save all objects in database to objects
            for class_ in classes.values():
                for obj in self.__session.query(class_).all():
                    objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

        return objects

    def new(self, obj):
        """ Adds an object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commits all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes object from the current database session """
        if obj is not None:
            from sqlalchemy import delete
            self.__session.delete(obj)

    def reload(self):
        """ Creates all tables in the database and the current db session """
        from sqlalchemy.orm import sessionmaker, scoped_session
        session_factory = sessionmaker(self.__engine,
                                       expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_factory)
