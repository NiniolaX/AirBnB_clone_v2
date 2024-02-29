#!/usr/bin/python3
""" Unittests for State class """
from tests.test_models.test_base_model import test_basemodel
from models.state import State
import os
import unittest
from console import HBNBCommand
from models import storage


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
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

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                         "State instance will not be created without name")
class test_state_with_dbStorage(unittest.TestCase):
    """ Tests State class with database storage engine """
    def setUp(self):
        """ Sets up resources for testing """
        pass
