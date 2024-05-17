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
        storage.reload()
        self.console = HBNBCommand()

    def tearDown(self):
        """ Cleans up test resources """
        self.cur.close()
        self.db.close()

    def test_all_with_class(self):
        """ Tests all method with class """
        self.cur.execute("SELECT COUNT(*) FROM states;")
        states_count = self.cur.fetchone()[0]
        self.assertEqual(states_count, len(storage.all(State)))

    def test_all_without_class(self):
        """ Tests all method without class """
        tables = ['states', 'cities']
        obj_count = 0;
        for table in tables:
            self.cur.execute(f'SELECT COUNT(*) FROM {table}')
            obj_count += self.cur.fetchone()[0]
        self.assertEqual(obj_count, len(storage.all()))

    def test_new(self):
        """ Tests the new method """
        self.console.do_create('State name="Osun"')
        state = max(storage.all(State).values(), key=lambda x: x.created_at)
        storage.new(state)
        self.assertIn(state, storage.all().values())
        state.delete()

    def test_save(self):
        """ Tests the save method """
        self.cur.execute('SELECT COUNT(*) FROM states')
        initial_count = self.cur.fetchone()[0]
        self.console.do_create('State name="Abuja"')
        state = max(storage.all(State).values(), key=lambda x: x.created_at)
        self.assertIn(state, storage.all().values())
        storage.close()  # SQL alchemy didn't reload his 'Session' so close
        self.cur.execute('SELECT COUNT(*) FROM states')
        final_count = self.cur.fetchone()[0]
        self.assertNotEqual(initial_count, final_count)
        state.delete()
