import matplotlib.pyplot as plt
import seaborn as sns


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
    plt.plot(data_x, data_y, 'r-')
    plt.xlabel("Time(sec)")
    plt.ylabel(y_value)
    plt.title(y_value + " vs Time(sec)")
    plt.grid()
    fig.savefig(filename)
    if show:
        plt.show()
    else:
        plt.close(fig)
