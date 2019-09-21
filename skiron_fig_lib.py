from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.ticker as tkr
import numpy as np
from support_data import description_dict, units_dict, level_dict, graph_types, SCATT, HISTO, ROSE, HEAT, SERIES, MAG, DIR

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plot_scatter(filename, xdata, ydata, title = None, xlabel = None, ylabel = None, dpi = 150, marker = '.', markSize = 0.6, figsize = (10,10), tfont = 17, lfont = 14):
    """
    Plots scatter graph for x- and y-components
    of the required field.
    """
    fig = plt.figure(figsize = figsize)
    plt.plot(xdata, ydata, marker, Markersize = markSize)
    if title:
        plt.title(title, fontsize = tfont)
    if xlabel:
        plt.xlabel(xlabel, fontsize = lfont)
    if ylabel:
        plt.ylabel(ylabel, fontsize = lfont)
    plt.axis('square')

    cfont = max([8, lfont-2])
    plt.xticks(fontsize = cfont)
    plt.yticks(fontsize = cfont)

    plt.grid()
    
    if isinstance(filename, list):
        for item in filename:
            fig.savefig(item, dpi = dpi)
    else:
        fig.savefig(filename, dpi = dpi)
    plt.close()
    return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plot_histogram(filename, mydata, bins = 10, title = None, xlabel = None, ylabel = None, dpi = 150, figsize = (10,10), tfont = 17, lfont = 14):
    """
    Plots a histogram for scalar timeseries.
    """
    fig = plt.figure(figsize = figsize)
    plt.hist(mydata, bins = bins)
    if title:
        plt.title(title, fontsize = tfont)
    if xlabel:
        plt.xlabel(xlabel, fontsize = lfont)
    if ylabel:
        plt.ylabel(ylabel, fontsize = lfont)
    
    cfont = max([8, lfont-2])
    plt.xticks(fontsize = cfont)
    plt.yticks(fontsize = cfont)

    if isinstance(filename, list):
        for item in filename:
            fig.savefig(item, dpi = dpi)
    else:
        fig.savefig(filename, dpi = dpi)
    plt.close()
    return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plot_timeseries(filename, mydata, title = None, xlabel = None, ylabel = None, dpi = 150, figsize = (10,10), tfont = 17, lfont = 14):
    """
    Plots the timeseries.
    """
    fig = plt.figure(figsize = figsize)
    plt.plot(mydata)
    if title:
        plt.title(title, fontsize = tfont)
    if xlabel:
        plt.xlabel(xlabel, fontsize = lfont)
    if ylabel:
        plt.ylabel(ylabel, fontsize = lfont)
    
    cfont = max([8, lfont-2])
    plt.xticks(fontsize = cfont)
    plt.yticks(fontsize = cfont)
    
    plt.grid()

    if isinstance(filename, list):
        for item in filename:
            fig.savefig(item, dpi = dpi)
    else:
        fig.savefig(filename, dpi = dpi)
    plt.close()
    return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plot_heatmap(filename, xdata, ydata, binx, biny, title = None, xlabel = None, ylabel = None, dpi = 150, figsize = (10,10), tfont = 17, lfont = 14):
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
    if total == 0:
        print('Not enough data to produce heatmap, exiting...')
        return 
    nx, nxbins = np.histogram(xdata, bins = binx)
    ny, nybins = np.histogram(ydata, bins = biny)

    temp_x = np.zeros(total)
    temp_y = np.zeros(total)

    for ij in range(total):
        temp_x[ij] = get_bin_id(nxbins, xdata[ij])
        temp_y[ij] = get_bin_id(nybins, ydata[ij])

    table2d = np.zeros((len(nybins)-1,len(nxbins)-1))

    for ij in range(len(temp_x)):
        table2d[int(temp_y[ij])-1, int(temp_x[ij])-1] += 1

    x_labels = []
    y_labels = []
    for ij in range(len(nxbins)-1):
        x_labels.append('{:.2f}'.format(0.5*(nxbins[ij] + nxbins[ij+1])))
    
    for ij in range(len(nybins)-1):
        y_labels.append('{:.1f}'.format(0.5*(nybins[ij] + nybins[ij+1])))

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
        ax.set_title(title, fontsize = tfont)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize = lfont)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize = lfont)

    ylims = ax.get_yticks()
    rr = ylims[1] - ylims[0]
    ax.set_ylim(ylims[0] - rr/2., ylims[-1] + rr/2.)

    cfont = max([8, lfont-2])
    ax.tick_params(axis = 'both', which = 'major', labelsize = cfont)
    
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    for i in range(len(nxbins)-1):
        for j in range(len(nybins)-1):
            text = ax.text(i, j, int(100.0*table2d[j, i]/total), ha="center", va="center", color="w")
    fig.tight_layout()
    
    if isinstance(filename, list):
        for item in filename:
            fig.savefig(item, dpi = dpi)
    else:
        fig.savefig(filename, dpi = dpi)
    plt.close()
    return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plot_roses(filename, vdir, mag, nsector = 16, bins = 10, title = None, legtitle = None, dpi = 150, figsize = (10,10), tfont = 17, lfont = 14):
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
        ax.set_title("{}".format(title), position = (0.5, 1.1), fontsize = tfont)
    
    cfont = max([8, lfont-2])
    ax.tick_params(axis = 'both', which = 'major', labelsize = cfont)

    ax.set_legend()
    if legtitle:
        ax.legend(title='{}'.format(legtitle), loc = (0.0, 0.0))
    #used to pretty up the printing around of wind occurent frequencies
    tictic = ax.get_yticks()
    ax.set_yticks(np.arange(0, tictic[-1], tictic[-1]/len(tictic)))
    ax.yaxis.set_major_formatter(tkr.FormatStrFormatter('%2.0f'))

    if isinstance(filename, list):
        for item in filename:
            fig.savefig(item, dpi = dpi)
    else:
        fig.savefig(filename, dpi = dpi)
    plt.close()
    return 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def get_fig_decorations_from_header(header, figtype, special = None):
    """
    Analyses the content of the header
    and produces various strings to be 
    used as a part of title, x and y 
    labels and the legend in figures.
    """
    title = '{} of '.format(graph_types.get(figtype, 'Unknown fig. type'))
    if isinstance(header, tuple):
        title += 'Wind '

        partOne = header[0]
        partTwo = header[1]
        parts = partOne.split('_')
        parts2 = partTwo.split('_')

        title += '@ {}'.format(level_dict.get(parts[1].lower(), 'some level'))

        if figtype == HISTO:
            if special:
                xlabel = '{} ({})'.format(description_dict.get(special, 'unknown var'), units_dict.get(special, 'units'))
            else:
                xlabel = '{} ({})'.format(description_dict.get(parts[0].lower(), 'unknown var'), units_dict.get(parts[0].lower(), 'units'))
            ylabel = 'Absolute frequency (#)'
            legend = 'Legend'
        elif figtype == SERIES:
            xlabel = 'records (#)'
            if special:
                ylabel = '{} ({})'.format(description_dict.get(special, 'unknown var'), units_dict.get(special, 'units'))
            else:
                ylabel = '{} ({})'.format(description_dict.get(parts[0].lower(), 'unknown var'), units_dict.get(parts[0].lower(), 'units'))
            legend = 'Legend'
        elif figtype == SCATT:
            xlabel = '{} ({})'.format(description_dict.get(parts[0].lower(), 'unknown var'), units_dict.get(parts[0].lower(), 'units'))
            ylabel = '{} ({})'.format(description_dict.get(parts2[0].lower(), 'unknown var'), units_dict.get(parts2[0].lower(), 'units'))
            legend = 'Legend'
        elif figtype == HEAT:
            if special:
                xlabel = '{} ({})'.format(description_dict.get(MAG, 'unknown var'), units_dict.get(MAG, 'units'))
                ylabel = '{} ({})'.format(description_dict.get(DIR, 'unknown var'), units_dict.get(DIR, 'units'))
            else:
                xlabel = '{} ({})'.format(description_dict.get(parts[0].lower(), 'unknown var'), units_dict.get(parts[0].lower(), 'units'))
                ylabel = '{} ({})'.format(description_dict.get(parts2[0].lower(), 'unknown var'), units_dict.get(parts2[0].lower(), 'units'))
            legend = 'Legend'
        elif figtype == ROSE:
            xlabel = 'xlabel'
            ylabel = 'ylabel'
            legend = '{} ({})'.format(description_dict.get(MAG, 'unknown var'), units_dict.get(MAG, 'units'))
        else:
            print('figtype {} not recognised'.format(figtype))
            xlabel = 'xlabel'
            ylabel = 'ylabel'
            legend = 'Legend'

    else:
        parts = header.split('_')
        if len(parts) > 1:
            title += '{} @ {}'.format(description_dict.get(parts[0].lower(), 'Unknown variable'), level_dict.get(parts[1].lower(), 'some level'))
        else:
            title += '{} @ {}'.format(description_dict.get(parts[0].lower(), 'Unknown variable'), 'some level')
        
        if figtype == HISTO:
            xlabel = '{} ({})'.format(description_dict.get(parts[0].lower(), 'unknown var'), units_dict.get(parts[0].lower(), 'units'))
            ylabel = 'Absolute frequency (#)'
            legend = 'Legend'
        elif figtype == SERIES:
            xlabel = 'records (#)'
            ylabel = '{} ({})'.format(description_dict.get(parts[0].lower(), 'unknown var'), units_dict.get(parts[0].lower(), 'units'))
            legend = 'Legend'
        else:
            print('figtype {} not recognised'.format(figtype))
            xlabel = 'xlabel'
            ylabel = 'ylabel'
            legend = 'Legend'

    return title, xlabel, ylabel, legend