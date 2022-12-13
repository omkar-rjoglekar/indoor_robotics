from sklearn.cluster import KMeans
from plot_utils import elbow_plot
import pandas as pd


def run_elbow_method(X):
    """
    param: X -> pandas dataframe of features
    Plots elbow plot of no. of clusters vs inertia
    """
    K = range(2, 15)
    ssd = []
    for k in K:
        kmeans = KMeans(n_clusters=k, max_iter=1000, n_init='auto')
        clustering = kmeans.fit(X)
        ssd.append(clustering.inertia_)

    elbow_plot(ssd, K)


def run_kmeans(X, k):
    """
    param: X -> pandas dataframe of features
    param: k -> optimal number of clusters
    returns: clustering -> pandas dataframe of the IMU data clustering
    """
    kmeans = KMeans(n_clusters=k, max_iter=1000, n_init='auto')
    clustering = kmeans.fit(X)

    clustering = pd.DataFrame(clustering.labels_, columns=["Drone orientation"])

    return clustering
