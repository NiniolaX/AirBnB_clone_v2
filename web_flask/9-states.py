#!/usr/bin/python3
""" Script starts a web flask application listening on 0.0.0.0 port 5000
Routes:
    /states_list: Displays a HTML page with the list of all State objects
        sorted by name (A-Z)
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def state():
    """ Returns a template displaying all states """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda x: x.name)
    return render_template('7-states_list.html', states=sorted_states)


@app.route('/states/<id>', strict_slashes=False)
def cities_in_states(id):
    """ Returns a template displaying the cities in a state
    Args:
        (str): id of state whose cities are to be displayed
    """
    states = storage.all(State)
    state_id = f'State.{id}'
    if state_id in states:
        state = states.get(state_id)
        sorted_cities = sorted(state.cities, key=lambda x: x.name)
    else:
        state = None
        sorted_cities = None
    return render_template('9-states.html', state=state, cities=sorted_cities)


@app.teardown_appcontext
def teardown_db(exception):
    """ Close the database session after each request. """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
