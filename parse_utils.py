# Imports
from collections import namedtuple

import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R

# define the types of available summaries
SUMMARY_TYPES = ["imu", "state"]

# create a named tuple to store both types of data
FlightData = namedtuple("FlightData", SUMMARY_TYPES)

# define global state mapping
FLIGHT_STATES = {'Docked': 0,
                 'Detaching': 1,
                 'DetachingFinal': 2,
                 'Airborne': 3,
                 'Docking': 4,
                 'DockingFinal': 5}


# Define helper functions to parse rosbag files
def from_quaternion(quaternion):
    """
    param: quaternion -> tuple(x,y,z,w)
    returns: euler orientations, roll(x) and pitch(y)
    """
    r = R.from_quat(quaternion)
    euler = r.as_euler('xyz', degrees=True)

    return euler[0], euler[1]


def normalize_time(clock_array):
    """
    param: clock_array -> numpy array of wall time
    returns: flight time starting at 0 (secs)
    """
    return (clock_array - clock_array.min()).tolist()


def check_altitude_validity(message):
    """
    param: message -> sensor_msg
    returns: True if (min_range <= value <= max_range) else False
    """
    return (message.range >= message.min_range) & (message.range <= message.max_range)


def parse_flight_data(bag):
    """
    param: bag -> rosbag.Bag object
    returns: namedtuple FlightData(IMU = pandas dataframe with relevant IMU data,
                                    STATE = pandas dataframe with relevant state data)
    """
    wall_time = []
    topics = []
    msgs = []
    for topic, msg, t in bag.read_messages():
        wall_time.append(t.to_sec())
        topics.append(topic)
        msgs.append(msg)

    wall_time = normalize_time(np.array(wall_time))

    imu_df = {"time": [],
              "linear_acc_x": [],
              "linear_acc_y": [],
              "linear_acc_z": [],
              "pitch": [],
              "roll": [],
              "state": []}

    state_df = {"time": [],
                "state": [],
                "altitude": []}

    cur_state = 0
    for i in range(len(wall_time)):
        if topics[i] == '/indoor/status':
            cur_state = FLIGHT_STATES[msgs[i].stateStr]
        elif topics[i] == '/imu_data':
            imu_df["time"].append(wall_time[i])

            imu_df["linear_acc_x"].append(msgs[i].linear_acceleration.x)
            imu_df["linear_acc_y"].append(msgs[i].linear_acceleration.y)
            imu_df["linear_acc_z"].append(msgs[i].linear_acceleration.z)

            imu_df["state"].append(cur_state)

            quat = [msgs[i].orientation.x,
                    msgs[i].orientation.y,
                    msgs[i].orientation.z,
                    msgs[i].orientation.w]

            roll, pitch = from_quaternion(quat)
            imu_df["roll"].append(roll)
            imu_df["pitch"].append(pitch)
        else:
            if check_altitude_validity(msgs[i]):
                state_df["time"].append(wall_time[i])
                state_df["state"].append(cur_state)
                state_df["altitude"].append(msgs[i].range)

    state_df = pd.DataFrame(state_df)
    imu_df = pd.DataFrame(imu_df)

    return FlightData(imu=imu_df, state=state_df)
