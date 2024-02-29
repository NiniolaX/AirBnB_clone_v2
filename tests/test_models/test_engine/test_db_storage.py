#!/usr/bin/python3
""" Unittest for DBStorage class """
import unittest
import MySQLdb
import os
from console import HBNBCommand
from models.state import State
from models import storage


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "Not applicable to file storage tests")
class test_dbStorage(unittest.TestCase):
    """ Class to test database storage """
    def setUp(self):
        """ Set up test resources """
        self.db = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'),
                                     port=3306,
                                     user=os.getenv('HBNB_MYSQL_USER'),
                                     passwd=os.getenv('HBNB_MYSQL_PWD'),
                                     database=os.getenv('HBNB_MYSQL_DB')
                )
        self.cur = self.db.cursor()
        self.console = HBNBCommand()

    def tearDown(self):
        """ Cleans up test resources """
        self.cur.close()
        self.db.close()
        if os.path.exists('file.json'):
            os.remove('file.json')

    def test_all_with_class(self):
        """ Tests all method with class """
        self.cur.execute("SELECT COUNT(*) FROM states;")
        states_count = self.cur.fetchone()[0]
        self.assertEqual(states_count, len(storage.all(State)))

    def test_all_without_class(self):
        """ Tests all method without class """
        from models.city import City
        tables = {'State': State, 'City': City}
        query = "SELECT COUNT(*) FROM %s;"
        obj_count = 0;
        for table in tables.values():
            result = self.cur.execute(query, (table,))
            obj_count = obj_count + result.fetchone()[0]
        self.assertEqual(obj_count, len(storage.all()))
