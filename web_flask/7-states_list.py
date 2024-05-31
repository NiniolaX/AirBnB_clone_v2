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


# Configure Jinja2 environment
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ Returns a template displaying all states """
    states = sorted(storage.all(State).values(), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(error):
    """ Close the database session after each request. """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
