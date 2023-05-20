import time, openvr
import trackerpositions
import plot_data
import local_server

#######################################################################################
# Setup and Configuration
#######################################################################################
# Port number for the webserver
webserver_port = 5002

# Display the plot in a window
display_plot = False

# Enable/disable headset
headset = False

# Enable/disable controllers
controllers = False

# Enable/disable trackers
trackers = True
# Number of trackers to be processed
num_trackers = 12

# Enable/disable base stations
base_stations = True
# Number of base stations to be processed
num_base_stations = 12
#######################################################################################


if __name__ == '__main__':

    # Initialize plot
    ax, fig = None, None
    if display_plot:
        ax, fig = plot_data.initialize_plot()

    # Initialize and run server
    local_server.port = webserver_port
    local_server.run_server()

    while True:

        list_of_objects = []


        def update_values(name, pos, rot, color):
            global list_of_objects
            list_of_objects.append({"position": pos, "rotation": rot, "color": color, "name": name})
            local_server.update_package(name, [pos, rot])

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



        # Plot data if plot is True
        if display_plot:
            # update plot
            plot_data.update_plot(list_of_objects, ax)

            # draw
            plot_data.draw(fig)

        time.sleep(0.1)



