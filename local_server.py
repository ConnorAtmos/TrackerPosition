import flask
import threading

#######################################################################################
# How to use this file
#######################################################################################
# This file is used to create a local server that can be used to send data to a web browser.
# To use this file, import it into your own file like this:
# import local_server
#######################################################################################

#######################################################################################
# Steps in main.py:
#######################################################################################
# 1. Import local_server.py
# ex:
# import local_server
#
# 2. Set the port number
# ex:
# port = 5000
#
# 3. Run the server
# ex:
# local_server.port = port
# local_server.run_server()
#
# 4. Update the package
# ex:
# headset_position, headset_rotation = trackerpositions.get_headset_pose()
# local_server.update_package("headset", [headset_position, headset_rotation])

# To stop the server, use this:
# local_server.stop_server()
#
#######################################################################################



#######################################################################################
# Setup and Configuration
#######################################################################################
# Default port number for the webserver, if not specified
port = 5000
#######################################################################################

user_id = None
user_pin = None

package = {}
def update_package(object_name, pos_rot_tuple):
    global package

    if object_name not in package:
        package[object_name] = {}

    package[object_name]["position"] = pos_rot_tuple[0]
    package[object_name]["rotation"] = pos_rot_tuple[1]


app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return flask.jsonify(package)

# run the server
thread = None
def run_server():
    global thread

    if thread is not None:
        return

    # Create a thread for the flask app
    thread = threading.Thread(target=app.run, kwargs={'port': port})

    # Start the thread
    thread.start()

def stop_server():
    global thread

    if thread is None:
        return

    # Stop the thread
    thread.join()

    # Clear the thread variable
    thread = None

