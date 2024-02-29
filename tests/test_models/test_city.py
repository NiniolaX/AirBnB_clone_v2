#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.city import City
import os
import unittest


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "City instance will not be created without name & state_id")
class test_City(test_basemodel):
    """ Tests the City class """

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
