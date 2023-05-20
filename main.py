import time, openvr
import trackerpositions
import plot_data

if __name__ == '__main__':

    ax, fig = plot_data.initialize_plot()

    while True:

        list_of_objects = []

        # get headset position and rotation
        headset_position, headset_rotation = trackerpositions.get_headset_pose()
        list_of_objects.append({"position": headset_position, "rotation": headset_rotation, "color": "k", "name": "headset"})

        # update plot
        plot_data.update_plot(list_of_objects, ax)

        # draw
        plot_data.draw(fig)

        time.sleep(0.1)



