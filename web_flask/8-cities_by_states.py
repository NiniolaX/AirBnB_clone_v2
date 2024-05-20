#!/usr/bin/python3
""" Script starts a web flask application listening on 0.0.0.0 port 5000
Routes:
    /cities_by_states: Displays a HTML page with the list of all city objects
        by state
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_state():
    """ Returns a template displaying all cities by their states """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda x: x.name)
    cities_dict = {}
    for state in states:
        sorted_cities = sorted(state.cities, key=lambda x: x.name)
        cities_dict[state.id] = sorted_cities
    return render_template('8-cities_by_states.html', states=sorted_states,
                           cities_dict=cities_dict)


@app.teardown_appcontext
def teardown_db(exception):
    """ Close the database session after each request. """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
