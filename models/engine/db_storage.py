#!/usr/bin/python3
"""
Module containing new engine DBStorage specification
for using MySQL db for storage
"""
import os

class DBStorage:
    """ Class for configuring database storage engine """
    from models.base_model import BaseModel
    from models.user import User
    from models.place import Place
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.review import Review

    __engine = None
    __session = None

    __classes = {
                'BaseModel': BaseModel, 'User': User,
                'Place': Place, 'State': State,
                'City': City, 'Amenity': Amenity,
                'Review': Review
                }

    def __init__(self):
        """
        __init__ Class constructor
        """
        from sqlalchemy import create_engine
        host = os.environ["HBNB_MYSQL_HOST"]
        user = os.environ["HBNB_MYSQL_USER"]
        passwd = os.environ["HBNB_MYSQL_PWD"]
        db = os.environ["HBNB_MYSQL_DB"]
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}"
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)
        if os.environ.get('HBNB_ENV') == 'test':
            """drop all tables"""
            Base.metadata.dropall(bind=self.__engine)

    def all(self, cls=None):
        """ Query current database section """
        if cls is not None:
            if cls in self.__classes.values():
                results = self.__session.query(cls).all()
        else:
            from sqlalchemy import union_all
            # Build the union query using union_all function
            union_query = union_all(*[self.__session.query(table)
                                    for table in self.__classes.values()]
                                    )
            results = self.__session.execute(union_query)

        __objects = {}
        for obj in results:
            __objects[f"{obj.__class__.__name__}.{obj.id}"] = obj
        return __objects

    def new(self, obj):
        """ Adds an object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commits all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes object from the current database session """
        if obj is not None:
            from sqlalchemy.orm import delete
            self.__session.delete(obj)

    def reload(self):
        """ Creates all tables in the database and the current db session """
        from models.base_model import Base
        from sqlalchemy.orm import sessionmaker, scoped_session
        Base.metadata.create_all(bind=self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
