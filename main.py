import time, openvr
import trackerpositions
from matplotlib import pyplot as plt


trackerpositions.initialize_vr_system()

positions, rotations = trackerpositions.get_all_poses()

if __name__ == '__main__':


    # get base station poses
    pos1, rot1 = trackerpositions.get_base_station_pose(0)
    pos2, rot2 = trackerpositions.get_base_station_pose(1)
    pos3, rot3 = trackerpositions.get_base_station_pose(2)

    # 3d plot of base stations
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(pos1[0], pos1[2], pos1[1], c='r', marker='o')
    ax.scatter(pos2[0], pos2[2], pos2[1], c='b', marker='o')
    ax.scatter(pos3[0], pos3[2], pos3[1], c='g', marker='o')


    # Get position and rotation of the headset
    position, rotation = trackerpositions.get_headset_pose()

    # plot headset
    ax.scatter(position[0], position[2], position[1], c='k', marker='o')

    # Get position and rotation of the left controller
    position, rotation = trackerpositions.get_left_controller_pose()

    # plot left controller
    ax.scatter(position[0], position[2], position[1], c='y', marker='o')

    # Get position and rotation of the right controller
    position, rotation = trackerpositions.get_right_controller_pose()

    # plot right controller
    ax.scatter(position[0], position[2], position[1], c='m', marker='o')

    # plot hip tracker
    position, rotation = trackerpositions.get_tracker_pose(0)
    ax.scatter(position[0], position[2], position[1], c='c', marker='o')

    # plot left foot tracker
    position, rotation = trackerpositions.get_tracker_pose(1)
    ax.scatter(position[0], position[2], position[1], c='r', marker='o')

    # plot right foot tracker
    position, rotation = trackerpositions.get_tracker_pose(2)
    ax.scatter(position[0], position[2], position[1], c='b', marker='o')


    plt.show()

    while False:





        #position, rotation = trackerpositions.get_right_controller_pose()
        #print(f"Position - X: {position[0]:.2f}, Y: {position[1]:.2f}, Z: {position[2]:.2f}")
        #print(f"Rotation - X: {rotation[0]:.2f}, Y: {rotation[1]:.2f}, Z: {rotation[2]:.2f}")
        time.sleep(0.5)