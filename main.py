import time, openvr, requests, json, threading
import trackerpositions
import plot_data
import global_server as server
import roblox_user_id as roblox
import numpy as np
import easygui
from pystray import MenuItem as item
import pystray
from PIL import Image

#######################################################################################
# Setup and Configuration
#######################################################################################
# Port number for the webserver
webserver_port = 5002

# Display the plot in a window
display_plot = False

# Enable/disable headset
headset = True

# Enable/disable controllers
controllers = True

# Enable/disable trackers
trackers = True
# Number of trackers to be processed
num_trackers = 3

# Enable/disable base stations
base_stations = True
# Number of base stations to be processed
num_base_stations = 3

server.user_pin = 1234
server.user_id = 20504526 #roblox.get_user_id("mrfrogg1")

if __name__ == '__main__':

    input_list = ["Number of Trackers", "Number of Base Stations", "Your Designated Pin", "Roblox User ID or Username"]
    default_values = [3, 3, 1234, "mrfrogg1"]

    try:
        with open("stored_values.json", "r") as f:
            default_values = json.load(f)
    except:
        pass

    input_list = easygui.multenterbox("Enter the following information", "Input", input_list, default_values)

    num_trackers = int(input_list[0])
    num_base_stations = int(input_list[1])
    server.user_pin = int(input_list[2])
    user_id = input_list[3]
    if user_id.isnumeric():
        server.user_id = int(user_id)
    else:
        try:
            with open("user_id_cache.json", "r") as f:
                user_id_cache = json.load(f)
        except:
            user_id_cache = {}

        if user_id in user_id_cache:
            server.user_id = user_id_cache[user_id]

        else:
            server.user_id = roblox.get_user_id(user_id)
            user_id_cache[user_id] = server.user_id
            with open("user_id_cache.json", "w") as f:
                json.dump(user_id_cache, f)

    # save the inputted values as json file
    with open("stored_values.json", "w") as f:
        json.dump(input_list, f)


    # Initialize plot
    ax, fig = None, None
    if display_plot:
        ax, fig = plot_data.initialize_plot()

    # Initialize and run server
    server.port = webserver_port
    server.run_server()

    print("Started. Do not close this window, but you can minimize it.")
    #print(requests.get('http://connorpersonal.space:5002/vr/cache', params={'users':json.dumps([{'user_id':'20504526', 'pin':'1234'}])}).json())
    #time.sleep(9999)

    running = True



    def run_icon():

        def stop_running():
            global running
            running = False
            print("Stopped")
            icon.stop()

        image = Image.open("icon.ico")
        menu = (pystray.MenuItem('Quit', stop_running), )
        icon = pystray.Icon("name", image, "TrackerPosition", menu)
        icon.run()

    threading.Thread(target=run_icon).start()



    while running:


        list_of_objects = []

        def update_values(name, pos, rot, color):
            global list_of_objects

            # 1 stud is 0.28 meters, so divide by 0.28 to get the number of studs
            pos = np.array(pos) / 0.28
            # convert to list
            pos = pos.tolist()

            # convert rotation to radians
            rot = np.array(rot) * 180 / np.pi
            # convert to list
            rot = rot.tolist()



            list_of_objects.append({"position": pos, "rotation": rot, "color": color, "name": name})
            server.update_package(name, [pos, rot])

        if headset:
            # get headset position and rotation
            headset_position, headset_rotation = trackerpositions.get_headset_pose()
            update_values("headset", headset_position, headset_rotation, "k")

        if controllers:
            # get left controller position and rotation
            left_controller_position, left_controller_rotation = trackerpositions.get_left_controller_pose()
            update_values("left_controller", left_controller_position, left_controller_rotation, "r")

            # get right controller position and rotation
            right_controller_position, right_controller_rotation = trackerpositions.get_right_controller_pose()
            update_values("right_controller", right_controller_position, right_controller_rotation, "b")

        if trackers:
            # get all trackers position and rotation
            for i in range(num_trackers):
                try:
                    tracker_position, tracker_rotation = trackerpositions.get_tracker_pose(i)
                    update_values("tracker_" + str(i), tracker_position, tracker_rotation, "g")
                except:
                    pass

        if base_stations:
            # get all base stations position and rotation
            for i in range(num_base_stations):
                try:
                    base_station_position, base_station_rotation = trackerpositions.get_base_station_pose(i)
                    update_values("base_station_" + str(i), base_station_position, base_station_rotation, "y")
                except:
                    pass


        server.push_package()

        # Plot data if plot is True
        if display_plot:
            # update plot
            plot_data.update_plot(list_of_objects, ax)

            # draw
            plot_data.draw(fig)

        time.sleep(0.1)



