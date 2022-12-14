import os
import pandas as pd


def get_statistical_summary(df):
    description = df.describe()
    kurtosis = pd.DataFrame(df.kurtosis()).transpose().rename(index={0: "kurtosis"})
    skew = pd.DataFrame(df.skew()).transpose().rename(index={0: "skew"})
    summary_stats = pd.concat((description, kurtosis, skew))

    return summary_stats


def generate_results_directory(name):
    root_dir = os.path.join(os.getcwd(), "results")
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
    root_dir = os.path.join(root_dir, name)
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)

    return root_dir
