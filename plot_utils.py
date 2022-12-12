import matplotlib.pyplot as plt
import seaborn as sns

MAX_AVG_HUMAN_HEIGHT = 1.7


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


def save_time_plots(data_y, data_x, filename, y_value, show=False):
    if (filename[-4:] != ".png") & (filename[-4:] != ".jpg"):
        raise ValueError("Plots can only be saved as PNG or JPG")

    fig = plt.figure()
    plt.plot(data_x, data_y, label="Drone altitude")
    max_ht = [MAX_AVG_HUMAN_HEIGHT for i in range(len(data_x))]
    plt.plot(data_x, max_ht, 'k--', label="Average human height")
    plt.fill_between(data_x, y1=0, y2=MAX_AVG_HUMAN_HEIGHT, color='r', alpha=0.3)
    plt.text(47, 0.5, "DANGER ZONE", color='r', fontsize=22)
    plt.xlabel("Time(sec)")
    plt.ylabel(y_value)
    plt.title(y_value + " vs Time(sec)")
    plt.legend()
    plt.grid()
    fig.savefig(filename)
    if show:
        plt.show()
    else:
        plt.close(fig)
