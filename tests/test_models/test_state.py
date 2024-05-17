#!/usr/bin/python3
""" Unittests for State class """
from tests.test_models.test_base_model import test_basemodel
from models.state import State
from os import getenv
import unittest
from console import HBNBCommand
from models import storage


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db',
                 "State instance will not be created without name")
class test_state(test_basemodel):
    """ Tests the State class with file storage engine """

    def __init__(self, *args, **kwargs):
        """
        Run unittests of BaseModel on State as an instance of BaseModel
        """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ Test name attribute """
        new = self.value(name="California")
        self.assertEqual(type(new.name), str)

    def test_property_cities(self):
        """ Test attr cities of class """
        self.assertTrue(hasattr(self.value, 'cities'))

    def test_relationship_with_cities(self):
        """ Tests relationship between State and City """
        from models.city import City
        state = self.value(name='Texas')
        state.save()
        city = City(name='San_Jose', state_id=state.id)
        city.save()
        self.assertIn(city, state.cities)


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db',
                 "State instance will not be created without name")
class test_state_with_dbsStorage(unittest.TestCase):
    """ Tests State class with database storage engine """
    def setUp(self):
        """ Sets up resources for testing """
        self.console = HBNBCommand()

    def tearDown(self):
        """ Cleans up test resources and environment """
        from models.base_model import Base
        storage._DBStorage__session.rollback()
        objs = []
        for obj in storage.all().values():
            objs.append(obj)
        for obj in objs:
            try:
                obj.delete()
            except Exception as e:
                pass

    def test_state_inherits_from_Base(self):
        """ Tests that State class inherits from declarative base """
        from sqlalchemy.ext.declarative import DeclarativeMeta
        self.assertIsInstance(State, DeclarativeMeta)

    def test_attr_tablename(self):
        """ Tests that State class has attribute __tablename__ """
        self.assertTrue(hasattr(State, '__tablename__'))

    def test_property_cities(self):
        """ Tests that State class has attribute cities """
        self.assertTrue(hasattr(State, 'cities'))

    def test_relationship_cities(self):
        """ Tests the relationship between State and City """
        from models.city import City
        self.console.do_create('State name="Kwara"')
        state = max(storage.all(State).values(), key=lambda x: x.created_at)
        state.save()
        self.console.do_create(f'City name="Ilorin" state_id="{state.id}"')
        city = max(storage.all(City).values(), key=lambda x: x.created_at)
        city.save()
        self.assertIn(city, state.cities)

    def test_state_creation_without_name(self):
        """ Tests State instance creationw without name """
        with self.assertRaises(Exception):
            self.console.do_create('State')

    def test_state_creation_with_name(self):
        """ Test State instance creation with name """
        initial_state_count = len(storage.all(State).values())
        self.console.do_create('State name="Oyo"')
        final_state_count = len(storage.all(State).values())
        self.assertEqual(initial_state_count, final_state_count - 1)
