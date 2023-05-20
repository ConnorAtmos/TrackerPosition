from matplotlib import pyplot as plt

#######################################################################################
# How to use this file
#######################################################################################
# This file is a library of functions that can be used to plot data in 3D space.
# To use this file, import it into your own file like this:
# import plot_data
#######################################################################################

#######################################################################################
# What this file does
#######################################################################################
# This file is used to plot data in 3D space using matplotlib in real time.
# It can be used to plot the headset, controllers, base stations, and trackers.
#######################################################################################

#######################################################################################
# Steps in main.py:
#######################################################################################

# 1. Import plot_data.py
# ex:
# import plot_data

# 2. Initialize plot
# ex:
# ax, fig = plot_data.initialize_plot()

# 3. Plot data
# ex:
# list_of_objects = []
# headset_position, headset_rotation = trackerpositions.get_headset_pose()
# list_of_objects.append({"position": headset_position, "rotation": headset_rotation, "color": "k", "name": "headset"})
# plot_data.update_plot(list_of_objects, ax)

# 4. Draw
# ex:
# plot_data.draw(fig)
#
#######################################################################################


#######################################################################################
# Full Example:
#######################################################################################
# import time, openvr
# import trackerpositions
# import plot_data
#
#
# if __name__ == '__main__':
#
#     ax, fig = plot_data.initialize_plot()
#
#     while True:
#
#         list_of_objects = []
#
#         # get headset position and rotation
#         headset_position, headset_rotation = trackerpositions.get_headset_pose()
#         list_of_objects.append({"position": headset_position, "rotation": headset_rotation, "color": "k", "name": "headset"})
#
#         # update plot
#         plot_data.update_plot(list_of_objects, ax)
#
#         # draw
#         plot_data.draw(fig)
#
#         time.sleep(0.1)
#
#######################################################################################

def update_ax(ax):
    ax.set_xlabel('X', fontsize=14)
    ax.set_ylabel('Z', fontsize=14)
    ax.set_zlabel('Y', fontsize=14)

def initialize_plot():
    plt.ion()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    plt.title("3D Space", fontsize=20)

    return ax, fig
def update_plot(list_of_objects, ax):
    ax.clear()
    update_ax(ax)

    for object in list_of_objects:
        ax.scatter(object["position"][0], object["position"][2], object["position"][1], marker='o', color=object["color"])

        # plot the text, but center it on the point, but offset it above the point
        ax.text(object["position"][0], object["position"][2], object["position"][1], object["name"], fontsize=10, horizontalalignment='center', verticalalignment='bottom', color='k', zorder=1)


def draw(fig):
    # update plot
    # drawing updated values
    fig.canvas.draw()

    # This will run the GUI event
    # loop until all UI events
    # currently waiting have been processed
    fig.canvas.flush_events()
