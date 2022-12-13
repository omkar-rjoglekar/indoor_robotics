# Imports
import glob
import argparse
import os

import rosbag

from parse_utils import *
from plot_utils import *
from cluster import *


# Main class for writing summaries
class SummaryWriter:
    def __init__(self, data_dir=None):
        """
        param: data_dir -> (string) root directory of rosbags; if None, searches current working directory
        Class Initializer
        Calls the parser function and generates pandas dataframes for easy summarization of data
        """
        if data_dir is None:
            files = glob.glob("./*.bag")
            print("Found {} rosbag files in working directory".format(len(files)))
        else:
            files = glob.glob(os.path.join(data_dir, "*.bag"))
            print("Found {} files in {}".format(len(files), data_dir))

        if len(files) == 0:
            raise FileNotFoundError("No rosbag files exist in the directory specified")

        print("Parsing all files into Pandas Dataframes")

        bag_list = [rosbag.Bag(file) for file in sorted(files)]
        self.flight_data = {}
        for i in range(len(bag_list)):
            self.flight_data['flight'+str(i)] = parse_flight_data(bag_list[i])
            bag_list[i].close()

        print("Done!")

    def summarize_altitude_stats(self):
        """
        plots altitude summary boxplot and writes to a csv file
        """
        for k, v in self.flight_data.items():
            print("Summarizing altitude statistics for {}".format(k))
            root_dir = os.path.join(os.getcwd(), "results")
            if not os.path.exists(root_dir):
                os.mkdir(root_dir)
            root_dir = os.path.join(root_dir, k)
            print("Writing results to {}".format(root_dir))
            if not os.path.exists(root_dir):
                os.mkdir(root_dir)

            altitude_stats = v.state[v.state["state"] == FLIGHT_STATES["Airborne"]].drop(["state"], axis=1)

            print("Creating time plot")
            time_plot = os.path.join(root_dir, "altitude_vs_time.png")
            save_time_plots(altitude_stats["altitude"], altitude_stats["time"], time_plot, "alt")
            print("Done!")

            altitude_stats = altitude_stats.drop(["time"], axis=1)
            summary_stats = altitude_stats.describe()

            print("Writing statistical summary to CSV file")
            csv_file = os.path.join(root_dir, "altitude_summary.csv")
            summary_stats.to_csv(csv_file)
            print("Done!")

            print("Creating boxplot")
            boxplot_file = os.path.join(root_dir, "altitude_summary.png")
            save_boxplots(altitude_stats, boxplot_file, "Altitude Boxplot")
            print("Done!")

        print("Altitude summary complete.")

    def summarize_imu_stats(self):
        """
        plots IMU summaries and writes csv file
        """
        for k, v in self.flight_data.items():
            print("Summarizing IMU data statistics for {}".format(k))
            root_dir = os.path.join(os.getcwd(), "results")
            if not os.path.exists(root_dir):
                os.mkdir(root_dir)
            root_dir = os.path.join(root_dir, k)
            print("Writing results to {}".format(root_dir))
            if not os.path.exists(root_dir):
                os.mkdir(root_dir)

            print("Writing statistical summary to CSV file")
            imu_stats = v.imu.drop(["time", "state"], axis=1)
            imu_acc_summary = imu_stats.describe()
            csv_file = os.path.join(root_dir, "imu_summary.csv")
            imu_acc_summary.to_csv(csv_file)
            print("Done!")

            print("Plotting summary box plots")
            boxplot_file = os.path.join(root_dir, "IMU_summary.png")
            save_boxplots(imu_stats.drop(["yaw"], axis=1), boxplot_file, "IMU boxplot")
            print("Done!")

            print("Starting K-Means clustering for {}".format(k))
            print("Optimizing cluster size using elbow method")
            run_elbow_method(imu_stats)

            k = input("Please enter the optimal cluster size:\n")

            clustering = run_kmeans(imu_stats, int(k))
            print("Clustering done!")

            print("Saving all IMU data time plots")
            for label in v.imu.drop(["time", "state"], axis=1).keys():
                filename = os.path.join(root_dir, label + "_vs_time.png")
                euler_angles = ["pitch", "roll", "yaw"]
                y_data = "acc" if label not in euler_angles else label

                save_time_plots(v.imu[label], v.imu["time"], filename, y_data, cluster_data=clustering)
            print("Done!")


def main(data_dir):
    """
    param: data_dir ->  location of .bag files on disk

    Runs all summarizations
    """
    summary_writer = SummaryWriter(data_dir)
    summary_writer.summarize_altitude_stats()
    summary_writer.summarize_imu_stats()


if __name__ == "__main__":
    """
    Usage: 1) python flight_summary.py  ====> For current working directory
           2) python flight_summary.py -r DATA_DIR  ====> look in DATA_DIR
           3) python flight_summary.py --root_dir DATA_DIR  ====> look in DATA_DIR
    """
    parser = argparse.ArgumentParser(description="Analyze and summarize all rosbag files in a specified directory")
    parser.add_argument("-r", "--root_dir", default=None, help="Directory of rosbag file location.")

    args = parser.parse_args()

    main(args.root_dir)

