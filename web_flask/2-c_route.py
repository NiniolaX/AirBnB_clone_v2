#!/usr/bin/python3
""" This script starts a Flask web application listening on 0.0.0.0, port 5000
Routes:
    /: display “Hello HBNB!”
    /hbnb: display “HBNB”
    /c/<text>: display “C ” followed by the value of the text variable
"""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_route():
    """ Returns "Hello HBNB!" """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb_route():
    """ Returns "HBNB" """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """ Displays 'C' followed by the value of the text variable """
    return f'C {escape(text)}'.replace('_', ' ')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
