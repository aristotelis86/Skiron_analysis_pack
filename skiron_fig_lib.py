from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.ticker as tkr
import numpy as np

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plot_scatter(filename, xdata, ydata, title = None, xlabel = None, ylabel = None, dpi = 150, marker = '.', markSize = 0.6, figsize = (10,10)):
    """
    Plots scatter graph for x- and y-components
    of the required field.
    """
    fig = plt.figure(figsize = figsize)
    plt.plot(xdata, ydata, marker, Markersize = markSize)
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.axis('square')
    
    if filename is list:
        for item in filename:
            fig.savefig(item, dpi = dpi)
    else:
        fig.savefig(filename, dpi = dpi)
    plt.close()
    return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plot_histogram(filename, mydata, bins = 10, title = None, xlabel = None, ylabel = None, dpi = 150, figsize = (10,10)):
    """
    Plots a histogram for scalar timeseries.
    """
    fig = plt.figure(figsize = figsize)
    plt.hist(mydata, bins = bins)
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)

    if filename is list:
        for item in filename:
            fig.savefig(item, dpi = dpi)
    else:
        fig.savefig(filename, dpi = dpi)
    plt.close()
    return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def get_heatmap(filename, xdata, ydata, binx, biny, title = None, xlabel = None, ylabel = None, dpi = 150, figsize = (10,10)):
    """
    Present variables as a 2D heatmap
    to correlate magnitude and direction.
    """
    def get_bin_id(mybins, vv):
        for ibin in range(len(mybins)-1):
            if vv >= mybins[ibin] and vv < mybins[ibin+1]:
                return ibin + 1
        return 0
    total = len(xdata)
    nx, nxbins = np.histogram(xdata, bins = binx)
    ny, nybins = np.histogram(ydata, bins = biny)

    temp_x = np.zeros(total)
    temp_y = np.zeros(total)

    for ij in range(total):
        temp_x[ij] = get_bin_id(nxbins, xdata[ij])
        temp_y[ij] = get_bin_id(nybins, ydata[ij])

    table2d = np.zeros((len(nxbins)-1,len(nybins)-1))

    for ij in range(len(temp_x)):
        table2d[int(temp_x[ij])-1, int(temp_y[ij])-1] += 1

    x_labels = []
    y_labels = []
    for ij in range(len(nxbins)-1):
        x_labels.append('{:.1f}'.format(0.5*(nxbins[ij] + nxbins[ij+1])))
    
    for ij in range(len(nybins)-1):
        y_labels.append('{:.2f}'.format(0.5*(nxbins[ij] + nxbins[ij+1])))

    fig, ax = plt.subplots()
    fig.set_size_inches(figsize[0], figsize[1])
    im = ax.imshow(table2d)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(x_labels)))
    ax.set_yticks(np.arange(len(y_labels)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)
    if title:
        ax.set_title(title)
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    for i in range(len(nxbins)-1):
        for j in range(len(nybins)-1):
            text = ax.text(i, j, int(100.0*table2d[j, i]/total), ha="center", va="center", color="w")
    fig.tight_layout()
    
    if filename is list:
        for item in filename:
            fig.savefig(item, dpi = dpi)
    else:
        fig.savefig(filename, dpi = dpi)
    plt.close()
    return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plot_roses(filename, vdir, mag, nsector = 16, bins = 10, title = None, legtitle = None, dpi = 150, figsize = (10,10)):
    """
    Plots the rose chart 
    from wind data and
    saves it to png file.
    """
    fig = plt.figure(figsize = figsize)
    # [left, bottom, width, height] as a fraction of total figure size
    right_rectangle = [0.05, 0.05, 0.85, 0.8]

    ax = WindroseAxes(fig, right_rectangle)
    fig.add_axes(ax)
    # ax.bar(wind['dir'], wind['sp'], normed=True, opening=0.9, edgecolor='white', bins=np.logspace(-1,1.3, 10), nsector=16)
    # ax.bar(wind['dir'], wind['sp'], normed=True, opening=0.9, edgecolor='white', bins=np.linspace(0,max(wind['sp']), 10), nsector=16)
    ax.bar(vdir, mag, normed = True, opening = 0.9, edgecolor = 'white', bins = bins, nsector = nsector)
    if title:
        ax.set_title("{}".format(title), position = (0.5, 1.1))

    ax.set_legend()
    if legtitle:
        ax.legend(title='{}'.format(legtitle), loc = (0.0, 0.0))
    #used to pretty up the printing around of wind occurent frequencies
    tictic = ax.get_yticks()
    ax.set_yticks(np.arange(0, tictic[-1], tictic[-1]/len(tictic)))
    ax.yaxis.set_major_formatter(tkr.FormatStrFormatter('%2.0f'))

    if filename is list:
        for item in filename:
            fig.savefig(item, dpi = dpi)
    else:
        fig.savefig(filename, dpi = dpi)
    plt.close()
    return 0
