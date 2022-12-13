import matplotlib.pyplot as plt
import seaborn as sns
import os

AVG_HUMAN_HEIGHT = 1.7
TIME_PLOTS = {"alt": "Altitude(m)",
              "acc": "IMU acceleration(m/s^2)",
              "roll": "Roll(deg)",
              "pitch": "Pitch(deg)",
              "yaw": "Yaw(deg)"}


def save_boxplots(data, filename, title, show=False):
    if (filename[-4:] != ".png") & (filename[-4:] != ".jpg"):
        raise ValueError("Plots can only be saved as PNG or JPG")

    fig = plt.figure()
    sns.violinplot(data)
    plt.title(title)
    fig.savefig(filename)
    if show:
        plt.show()
    else:
        plt.close(fig)


def save_time_plots(data_y, data_x, filename, y_value, show=False, cluster_data=None):
    if (filename[-4:] != ".png") & (filename[-4:] != ".jpg"):
        raise ValueError("Plots can only be saved as PNG or JPG")
    if y_value not in TIME_PLOTS.keys():
        raise ValueError("Time plot only defined for {}".format(TIME_PLOTS))

    fig = plt.figure()
    if y_value == "alt":
        plt.plot(data_x, data_y)
        max_ht = [AVG_HUMAN_HEIGHT for i in range(len(data_x))]
        plt.plot(data_x, max_ht, 'k--')
        plt.fill_between(data_x, y1=0, y2=AVG_HUMAN_HEIGHT, color='r', alpha=0.3)
        plt.text(47, 0.5, "DANGER ZONE", color='r', fontsize=22)
        plt.legend(["Drone altitude", "Average human height"])
    else:
        if cluster_data is None:
            raise ValueError("Require cluster data to color plot")

        sns.scatterplot(x=data_x, y=data_y,
                        hue=cluster_data["Drone orientation"],
                        palette='Set1')

    plt_title = os.path.splitext(os.path.split(filename)[1])[0]
    plt.xlabel("Time(sec)")
    plt.ylabel(TIME_PLOTS[y_value])
    plt.title(plt_title)
    plt.grid()
    fig.savefig(filename)
    if show:
        plt.show()
    else:
        plt.close(fig)


def elbow_plot(ssd_list, K):
    fig = plt.figure()
    plt.plot(K, ssd_list, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')
    plt.show()
