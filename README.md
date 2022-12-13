# Indoor Robotics - Interview coding assignment

## Summary
This repository reads rosbag files in the current working directory 
OR a specified directory. Each rosbag file contains flight data from the IMU,
SONAR and state data. This code summarizes the IMU acceleration statistics 
as well as the euler orientation statistics to a CSV file. It also runs
K-Means on the IMU data to understand the states of motion of the drone.
It generates the time series plots and boxplots wherever relevant.
More details are available in `Algo Student Programming task.pdf`.

## Code files
- The main file is `flight_summary.py`. You can run it in one 
of the following 3 ways from the command line:

  1. `python flight_summary.py` ====> For current working directory
  2. `python flight_summary.py -r DATA_DIR` ====> look in DATA_DIR
  3. `python flight_summary.py --root_dir DATA_DIR` ====> look in DATA_DIR


- `cluster.py` - contains helper functions to run K-Means with elbow method
- `parse_utils.py` - contains utility functions to parse the rosbag files
- `plot_utils.py` - contains utility functions to generate all required plots

## Directories
- `results` - Contains all the summary plots and CSV files. 
Contains a subdirectory for each independent flight.
