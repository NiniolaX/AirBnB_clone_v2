#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.user import User
import unittest
from os import getenv
from console import HBNBCommand
from models import storage

@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db',
                 'Test class not relevant to db storage')
class test_User(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.password), str)

@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db',
                         'Test class not relevant to db storage')
class test_User_with_db_storage(unittest.TestCase):
    """ Tests the User class with database storage engine """
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

    def test_user_inherits_from_Base(self):
        """ Tests that the User class inherits from Base """
        from sqlalchemy.ext.declarative import DeclarativeMeta
        self.assertIsInstance(User, DeclarativeMeta)

    def test_attr_tablename(self):
        """ Tests attribute tablename exists """
        self.assertTrue(hasattr(User, '__tablename__'))

    def test_user_creation_with_no_args(self):
        """ Tests user creation with no arguments """
        with self.assertRaises(Exception):
            self.console.do_create('User')

    def test_user_creation_with_email_only(self):
        """ Tests user creation with email only """
        with self.assertRaises(Exception):
            self.console.do_create('User email="user1@gmail.com"')

    def test_user_creation_with_email_and_passwd(self):
        """ Tests user creation with email and password only """
        initial_user_count = len(storage.all(User))
        self.console.do_create('User email="user01@gmail.com" password="123"')
        final_user_count = len(storage.all(User))
        self.assertEqual(initial_user_count, final_user_count - 1)

    def test_user_creation_with_all_arguments(self):
        """ Tests user creation with all required arguments """
        initial_user_count = len(storage.all(User))
        self.console.do_create('User email="love@gmail.com" password="123" first_name="Nini" last_name="Afinni"')
        final_user_count = len(storage.all(User))
        self.assertEqual(initial_user_count, final_user_count - 1)
