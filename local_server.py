import flask

# This local server should send headset, controller, and base station positions and rotations to flask as json data.

port = 5000


def set_port(new_port):
    global port
    port = new_port


def get_port():
    global port
    return port


# create flask app
app = flask.Flask(__name__)

# create dictionary to store data
data = {}


def set_data(new_data):
    global data
    data = new_data


def get_data():
    global data
    return data


