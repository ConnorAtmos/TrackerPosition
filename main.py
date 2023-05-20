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

# Testing mode tests the integrity of the tracking system and outputs it into a file (testing.py)
# NOTE: Testing mode will not start the server or plot data until the test is complete
# 1000 entries takes about 10 seconds
testing_mode = False
#######################################################################################

if __name__ == '__main__':

    # Testing mode tests the integrity of the tracking system and outputs it into a file
    if testing_mode:
        import testing
        testing.run_test()

    # Initialize plot
    if display_plot:
        ax, fig = plot_data.initialize_plot()

    # Initialize and run server
    local_server.port = webserver_port
    local_server.run_server()

    while True:

        list_of_objects = []

        # get headset position and rotation
        headset_position, headset_rotation = trackerpositions.get_headset_pose()
        list_of_objects.append({"position": headset_position, "rotation": headset_rotation, "color": "k", "name": "headset"})

        local_server.update_package("headset", [headset_position, headset_rotation])

        # Plot data if plot is True
        if display_plot:
            # update plot
            plot_data.update_plot(list_of_objects, ax)

            # draw
            plot_data.draw(fig)

        time.sleep(0.1)



