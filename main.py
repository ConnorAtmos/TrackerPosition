import openvr, time
import numpy as np
import matplotlib.pyplot as plt

def matrix_to_euler_angles(rotation_matrix):
    # Convert rotation matrix to Euler angles (X-Y-Z, extrinsic rotations)
    sy = np.sqrt(rotation_matrix[0][0] * rotation_matrix[0][0] + rotation_matrix[1][0] * rotation_matrix[1][0])
    singular = sy < 1e-6
    if not singular:
        x = np.arctan2(rotation_matrix[2][1], rotation_matrix[2][2])
        y = np.arctan2(-rotation_matrix[2][0], sy)
        z = np.arctan2(rotation_matrix[1][0], rotation_matrix[0][0])
    else:
        x = np.arctan2(-rotation_matrix[1][2], rotation_matrix[1][1])
        y = np.arctan2(-rotation_matrix[2][0], sy)
        z = 0.0
    return np.degrees(x), np.degrees(y), np.degrees(z)

def get_headset_pose():
    vr_system = openvr.init(openvr.VRApplication_Background)
    poses = vr_system.getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding, 0, openvr.k_unMaxTrackedDeviceCount)
    hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]

    # Extract position and rotation from hmd_pose
    position = hmd_pose.mDeviceToAbsoluteTracking[0][3], hmd_pose.mDeviceToAbsoluteTracking[1][3], hmd_pose.mDeviceToAbsoluteTracking[2][3]
    rotation = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            rotation[i][j] = hmd_pose.mDeviceToAbsoluteTracking[i][j]

    openvr.shutdown()

    rotation = matrix_to_euler_angles(rotation)

    return position, rotation


if __name__ == '__main__':
    while True:
        position, rotation = get_headset_pose()
        print(f"Position - X: {position[0]:.2f}, Y: {position[1]:.2f}, Z: {position[2]:.2f}")
        print(f"Rotation - X: {rotation[0]:.2f}, Y: {rotation[1]:.2f}, Z: {rotation[2]:.2f}")
        time.sleep(0.5)