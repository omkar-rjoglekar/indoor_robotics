# Imports
import glob
import os
import argparse

import rosbag
import seaborn as sns

from parse_utils import *
from plot_utils import *


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

        print("Done!")

    def summarize_altitude_stats(self):
        """
        plots altitude summary boxplot and writes to a csv file
        """
        for k, v in self.flight_data.items():
            print("Summarizing altitude statistics for {}".format(k))
            root_dir = os.path.join(os.getcwd(), "results", k)
            print("Writing results to {}".format(root_dir))
            if not os.path.exists(root_dir):
                os.mkdir(root_dir)

            altitude_stats = v.state[v.state["state"] == FLIGHT_STATES["Airborne"]].drop(["state"], axis=1)

            time_plot = os.path.join(root_dir, "altitude_vs_time.png")
            save_time_plots(altitude_stats["altitude"], altitude_stats["time"], time_plot, "Altitude(m)")
            print("Saved time plot!")

            altitude_stats = altitude_stats.drop(["time"], axis=1)
            summary_stats = altitude_stats.describe()

            csv_file = os.path.join(root_dir, "altitude_summary.csv")
            summary_stats.to_csv(csv_file)
            print("CSV file written!")

            boxplot_file = os.path.join(root_dir, "altitude_summary.png")
            save_boxplots(altitude_stats, boxplot_file, "Altitude Boxplot")
            print("Boxplot saved!")


if __name__ == "__main__":
    """
    Usage: 1) python flight_summary.py  ====> For current working directory
           2) python flight_summary.py -r DATA_DIR  ====> look in DATA_DIR
           3) python flight_summary.py --root_dir DATA_DIR  ====> look in DATA_DIR
    """
    parser = argparse.ArgumentParser(description="Analyze and summarize all rosbag files in a specified directory")
    parser.add_argument("-r", "--root_dir", default=None, help="Directory of rosbag file location.")

    args = parser.parse_args()
    summary_writer = SummaryWriter(args.root_dir)
    summary_writer.summarize_altitude_stats()
