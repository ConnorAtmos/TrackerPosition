import time, openvr, requests, json, threading
import trackerpositions
import plot_data
import global_server as server
import roblox_user_id as roblox
import numpy as np

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
#######################################################################################


if __name__ == '__main__':

    # Initialize plot
    ax, fig = None, None
    if display_plot:
        ax, fig = plot_data.initialize_plot()

    # Initialize and run server
    server.port = webserver_port
    server.run_server()

    print("Started")
    #print(requests.get('http://connorpersonal.space:5002/vr/cache', params={'users':json.dumps([{'user_id':'20504526', 'pin':'1234'}])}).json())
    #time.sleep(9999)

    while True:


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

        print("uh")
        time.sleep(0.1)



