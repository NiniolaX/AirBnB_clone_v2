#!/usr/bin/python3
""" Script starts a web flask application listening on 0.0.0.0 port 5000
Routes:
    /states_list: Displays a HTML page with the list of all State objects
        sorted by name (A-Z)
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def load_hbnb_filters():
    """ Returns a dynamic clone of the AirBnB web app
    """
    # Get states
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda x: x.name)
    # Extract cities by state into a dictionary
    cities_by_state = {}
    for state in states:
        sorted_cities = sorted(state.cities, key=lambda x: x.name)
        cities_by_state[state.id] = sorted_cities
    # Extract amenities
    amenities = storage.all(Amenity).values()
    sorted_amenities = sorted(amenities, key=lambda x: x.name)
    # Render template
    return render_template('10-hbnb_filters.html',
                           states=sorted_states,
                           cities_by_state=cities_by_state,
                           amenities=sorted_amenities)


@app.teardown_appcontext
def teardown_db(exception):
    """ Close the database session after each request. """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
