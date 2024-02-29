#!/usr/bin/python3
""" Unittest for the BaseModel class """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 "BaseModel class not mapped to database")
class test_basemodel(unittest.TestCase):
    """ Tests the BaseModel class """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ Sets up test resources """
        pass

    def tearDown(self):
        """ Cleans up test resources """
        try:
            os.remove('file.json')
        except:
            pass

    def test_default(self):
        """ Test object instantiation """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ Tests object recreation with its dictionary representation """
        i = self.value()
        copy = i.to_dict()
        new = self.value(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ Tests object creation with keyword arguments """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = self.value(**copy)

    def test_save(self):
        """ Tests the save public class method """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ Tests the __str__ private class method """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ Tests the to_dict public class method """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """ Tests object creation with invalid dictionary """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    @unittest.skip("Not relevant for obj creation with parameters in console")
    def test_kwargs_one(self):
        """ Test object creation with dictionary argument """
        n = {'Name': 'test'}
        with self.assertRaises(KeyError):
            new = self.value(**n)

    def test_id(self):
        """ Tests the id instance attribute"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ Tests the created_at instance attribute """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """ Tests the updated_at instance attribute """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = self.value(**n)
        self.assertFalse(new.created_at == new.updated_at)

    def test_delete(self):
        """ Tests the delete method """
        from models import storage
        new = self.value()
        new.save()
        self.assertIn(new, storage.all().values())
        new.delete()
        self.assertNotIn(new, storage.all().values())
