#!/usr/bin/python3
""" This script starts a Flask web application listening on 0.0.0.0, port 5000
Routes:
    /: display “Hello HBNB!”
    /hbnb: display “HBNB”
    /c/<text>: display “C ” followed by the value of the 'text' variable
    /python/<text>: display “Python ”, followed by the value of the 'text'
        variable
    /number/<n>: displays "n is a number" only if n is an integer
    /number_template/<n>: display a HTML page only if n is an integer
"""
from flask import Flask
from markupsafe import escape
from flask import render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """ Returns "Hello HBNB!" """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Returns "HBNB" """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """ Returns a string 'C' followed by the value of the 'text' variable
    Args:
        text(str) -String to be displayed with 'C'
    """
    return f'C {escape(text)}'.replace('_', ' ')


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    """ Returns a string 'Python' followed by the value of text
    Args:
        text(str) - String to be displayed with 'Python', default is 'is cool'
    """
    return f'Python {escape(text)}'.replace('_', ' ')


@app.route('/number/<int:n>/', strict_slashes=False)
def number(n):
    """ Returns the text "n is a number" only if n is an integer
    Args:
        n: A value which is an integer or not
    """
    return f"{escape(n)} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """ Returns an HTML page containing variable n, only if n is an integer
    Args:
        n: Integer to be displayed on page
    """
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
