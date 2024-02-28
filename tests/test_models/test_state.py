#!/usr/bin/python3
""" Unittests for State class """
from tests.test_models.test_base_model import test_basemodel
from models.state import State
import os


class test_state(test_basemodel):
    """ Tests the State class """

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
