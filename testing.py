import time, openvr
import trackerpositions
from matplotlib import pyplot as plt
import numpy as np

#######################################################################################
# How to use this file
#######################################################################################
# Right click on this file and click "Run 'testing'", or type
# "python testing.py" in the terminal.
#######################################################################################

#######################################################################################
# What this file does
#######################################################################################
# This file is used to grab entries from the trackers, headset, and base stations and put them in a list.
# an entry is a dictionary with the following format:
# {
#   "name": "headset",
#   "position": [x, y, z],
#   "rotation": [x, y, z, w]
# }

# The list of entries is then used to calculate the standard deviation of the position and rotation of each object.
# This is used to determine how much the objects are moving, rotating, and vibrating.
# It will then print out the standard deviation of each object and output it to a file.
#######################################################################################

#######################################################################################
# Setup and Configuration
#######################################################################################
# How many entries to grab
num_entries = 1000
# How long to wait between each entry (in seconds)
time_between_entries = 0.01

# Track base stations?
base_stations = True
# Number of base stations
num_base_stations = 3

# Track trackers?
trackers = True
# Number of trackers
num_trackers = 3
#######################################################################################

def get_distance(pos1, pos2):
    return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 + (pos1[2]-pos2[2])**2)**0.5

def calculate_standard_deviation(list_data):
    mean = sum(list_data)/len(list_data)


used_object_names = []
def update_plot(ax, object_name, pos_rot_tuple):
    global used_object_names

    if object_name not in used_object_names:
        used_object_names.append(object_name)
        ax.scatter(pos_rot_tuple[0][0], pos_rot_tuple[0][2], pos_rot_tuple[0][1], marker='o')

        # plot the text, but center it on the point, but offset it above the point
        ax.text(pos_rot_tuple[0][0], pos_rot_tuple[0][2], pos_rot_tuple[0][1], object_name, fontsize=10, horizontalalignment='center', verticalalignment='bottom', color='k', zorder=1)

def main():

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    plt.title("3D Space", fontsize=20)

    ax.set_xlabel('X', fontsize=14)
    ax.set_ylabel('-Z (flipped)', fontsize=14)
    ax.set_zlabel('Y', fontsize=14)

    package = {}

    def update_package(object_name, pos_rot_tuple):

        # multiply by 1000 to convert from meters to millimeters (pos only)
        pos_rot_tuple = (np.array(pos_rot_tuple[0])*1000, pos_rot_tuple[1])

        # flip z axis
        pos_rot_tuple[0][2] = -pos_rot_tuple[0][2]

        if object_name not in package:
            package[object_name] = {}

        if "position" not in package[object_name]:
            package[object_name]["position"] = []

        if "rotation" not in package[object_name]:
            package[object_name]["rotation"] = []

        print(object_name, pos_rot_tuple)

        package[object_name]["position"].append(pos_rot_tuple[0])
        package[object_name]["rotation"].append(pos_rot_tuple[1])

        update_plot(ax, object_name, pos_rot_tuple)



    for i in range(num_entries):

        print("Entry {}".format(i))

        # headset
        update_package("headset", trackerpositions.get_headset_pose())

        # controllers
        update_package("lcontroller", trackerpositions.get_left_controller_pose())
        update_package("rcontroller", trackerpositions.get_right_controller_pose())

        # base stations
        if base_stations:
            for j in range(num_base_stations):
                update_package("basestation{}".format(j), trackerpositions.get_base_station_pose(j))

        # trackers
        if trackers:
            for j in range(num_trackers):
                update_package("tracker{}".format(j), trackerpositions.get_tracker_pose(j))

        time.sleep(time_between_entries)

    plt.show()

    #save the plot as a png
    fig.savefig("3dplot.png")

    # go through all package data and remove duplicates for each object
    for object_name in package:
        for pos_rot_key, pos_rot_values in package[object_name].items():
            print("Evaluating object: ", object_name, " for key: ", pos_rot_key)
            for i in range(len(pos_rot_values)-1, -1, -1):

                if i != 0:
                    for j in range(i):
                        if np.array_equal(pos_rot_values[i], pos_rot_values[j]):
                            print("Removing duplicate: ", pos_rot_values[i])
                            del pos_rot_values[i]
                            break


    # get average position and rotation of each object
    package_averages = {}

    for object_name in package:
        package_averages[object_name] = {}

        for pos_rot_key, pos_rot_values in package[object_name].items():
            package_averages[object_name][pos_rot_key] = np.average(pos_rot_values, axis=0)

    print("Package averages: ", package_averages)

    # get a list of the distances of each point from the average
    package_distances = {}

    for object_name in package:
        package_distances[object_name] = {}

        for pos_rot_key, pos_rot_values in package[object_name].items():
            package_distances[object_name][pos_rot_key] = []

            for pos_rot_value in pos_rot_values:

                if pos_rot_key == "rotation":
                    # if it's rotation, cap the distance at 180 degrees. If it's more than 180 degrees, subtract 360 degrees and take the absolute value

                    dist = get_distance(pos_rot_value, package_averages[object_name][pos_rot_key])

                    if dist > 180:
                        dist = abs(dist - 360)

                    package_distances[object_name][pos_rot_key].append(dist)

                else:
                    package_distances[object_name][pos_rot_key].append(get_distance(pos_rot_value, package_averages[object_name][pos_rot_key]))

    print("Package distances: ", package_distances)

    # get average distance from the list of distances
    package_average_distances = {}

    for object_name in package:
        package_average_distances[object_name] = {}

        for pos_rot_key, pos_rot_values in package_distances[object_name].items():
            package_average_distances[object_name][pos_rot_key] = np.average(pos_rot_values)

    print("Package average distances: ", package_average_distances)

    # get the standard deviation of the distances
    package_standard_deviations = {}

    for object_name in package:
        package_standard_deviations[object_name] = {}

        for pos_rot_key, pos_rot_values in package_distances[object_name].items():
            package_standard_deviations[object_name][pos_rot_key] = np.std(pos_rot_values)

    print("Package standard deviations: ", package_standard_deviations)

    # get maximum distance from average for each object
    package_max_distances = {}

    for object_name in package:
        package_max_distances[object_name] = {}

        for pos_rot_key, pos_rot_values in package_distances[object_name].items():
            package_max_distances[object_name][pos_rot_key] = max(pos_rot_values)

    print("Package max distances: ", package_max_distances)

    # worse 1% of data, then get the average of that
    package_worse_1_percent = {}

    for object_name in package:
        package_worse_1_percent[object_name] = {}

        for pos_rot_key, pos_rot_values in package_distances[object_name].items():
            package_worse_1_percent[object_name][pos_rot_key] = np.average(sorted(pos_rot_values)[-int(len(pos_rot_values)*0.01):])


    print("Package worse 1%: ", package_worse_1_percent)

    # Save all the data to a csv file
    with open('data.csv', 'w') as f:

        f.write("Object Name, Average Position Distance, Distance Standard Deviation, Max Position Distance, Worse 1% Position Distance, Average Rotation Distance, Standard Deviation, Max Rotation Distance, Worse 1% Rotation Distance\n")

        for object_name in package:
            f.write(object_name + ",")
            f.write(str(package_average_distances[object_name]["position"]) + ",")
            f.write(str(package_standard_deviations[object_name]["position"]) + ",")
            f.write(str(package_max_distances[object_name]["position"]) + ",")
            f.write(str(package_worse_1_percent[object_name]["position"]) + ",")
            f.write(str(package_average_distances[object_name]["rotation"]) + ",")
            f.write(str(package_standard_deviations[object_name]["rotation"]) + ",")
            f.write(str(package_max_distances[object_name]["rotation"]) + ",")
            f.write(str(package_worse_1_percent[object_name]["rotation"]) + "\n")


def run_test():
    main()



if __name__ == '__main__':
    main()
