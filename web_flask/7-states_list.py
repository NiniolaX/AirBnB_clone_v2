#!/usr/bin/python3
""" Script starts a web flask application listening on 0.0.0.0 port 5000
Routes:
    /states_list: Displays a HTML page with the list of all State objects
                 present in `DBStorage` sorted by name (A-Z)
"""
from flask import Flask, render_template
from os import getenv


if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """ Close the database session after each request. """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ Returns a template listing all states in `DBStorage` """
    from models.state import State
    storage.reload()
    states = list(storage.all(State).values())
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
