#!/usr/bin/python3
""" Unittests for the City model """
from tests.test_models.test_base_model import test_basemodel
from models.city import City
import os
import unittest
from models import storage
from console import HBNBCommand


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "City instance will not be created without name & state_id")
class test_city(test_basemodel):
    """ Tests the City model """

    def __init__(self, *args, **kwargs):
        """ Calls base_model tests on State """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """ Tests id attribute """
        new = self.value()
        self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """ Tests name attribute """
        new = self.value()
        self.assertEqual(type(new.name), str)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "Test class only needed for database storage use case")
class test_city_with_dbstorage(unittest.TestCase):
    """ Tests the City model with database storage """
    def setUp(self):
        """ Sets up resources and environment for testing """
        self.console = HBNBCommand()

    def tearDown(self):
        """ Cleans up resources and environment used in testing """
        if os.path.exists('file.json'):
            os.remove('file.json')
        storage._DBStorage__session.rollback()

    def test_city_inherits_from_Base(self):
        """ Tests that City class inherits from declarative_base class """
        from sqlalchemy.ext.declarative import DeclarativeMeta
        self.assertIsInstance(City, DeclarativeMeta)

    def test_city_has_attr_tablename(self):
        """ Tests that City class has attr __tablename__"""
        self.assertTrue(hasattr(City, '__tablename__'))

    def test_city_creation_with_name_and_state_id(self):
        """ Tests city creation with name and state_id """
        from models.state import State
        initial_state_count = len(storage.all(State))
        self.console.do_create('State name="Lagos"')
        # Extract recently created state object
        new_state = max(storage.all(State).values(),
                        key=lambda x: x.created_at)
        self.console.do_create(f'City name="Wuse" state_id="{new_state.id}"')
        final_state_count = len(storage.all(State))
        self.assertEqual(initial_state_count, final_state_count - 1)

    def test_city_creation_with_no_arguments(self):
        """ Tests city creation without name and state_id in db storage """
        with self.assertRaises(Exception):
            self.console.do_create('City')

    def test_city_creation_with_name_only(self):
        """ Tests city creation with name only in db storage """
        with self.assertRaises(Exception):
            self.console.do_create('City name="Wuse"')

    def test_city_creation_with_state_id_only(self):
        """ Tests city creation with state_id only"""
        self.console.do_create('State name="Abuja"')
        # Extract id of recently created state
        new_state = max(storage.all().values(),
                        key=lambda x: x.created_at)
        with self.assertRaises(Exception):
            self.console.do_create(f"City state_id={self.new_state.id}")
