"""
Module to define the reader class and functionality
for the csv files provided by SKIRON.
"""

import numpy as np
import csv
import os
from task_reader import Task, VEC, SCAL, FILE, HISTO, SCATT, ROSE, HEAT, STATS, SERIES, SAVE, FTYPE, METEO
from support_data import DIR, MAG, MEAN, MIN, MAX, MEDIAN, STD, PRCTILES, COV, RECORDS, ptiles, STAT_ID
import skiron_fig_lib as sflib

def get_mag_dir(x, y, origin = False):
    """
    Given the vector components,
    it calculates the magnitude
    and bearing (in degrees 0 to 360) of 
    the vector.
    """
    speed = np.sqrt(x**2 + y**2)
    if origin:
        direction = 180.0 * (-0.5 * np.pi - np.arctan2(y,x)) / np.pi
    else:
        direction = 180.0 * (0.5 * np.pi - np.arctan2(y,x)) / np.pi
    if direction < 0.0:
        direction += 360.0
    return speed, direction
    
def get_dir_simple(x,y):
    return 180.0 * np.arctan2(y,x) / np.pi

############################################################
class SkironData:
    def __init__(self, task = None):
        """
        Constructor to create an instance of the data in memory.
        Various headers are given to combine data properly.
        """
        self.ok = False
        print('Entering SkironData reader...')

        if not task:
            print('No task present...')
            print('Exiting Skiron data reader...')
            return

        self.task = task
        self.fname = task.opt_dict[FILE]
        self.vecHeads = task.opt_dict[VEC]
        self.scalHeads = task.opt_dict[SCAL]
        self.data = {}
        self.stats = {}
        self.totRecords = 0
        self.validRecords = 0

        if not self.fname:
            print('Filename is not given...')
            print('Exiting Skiron data reader...')
            return
        
        if (not self.vecHeads) and (not self.scalHeads):
            print('No headers to look for...')
            print('Exiting Skiron data reader...')
            return
        
        # Read data to memory
        temp_data = self.get_data_dict(vecHeads = self.vecHeads, scalHeads = self.scalHeads)
        
        # Organise data according to user input (headers)
        self.organise_data(temp_data)

        self.ok = True
        print('Skiron data read from csv OK.')
        return

    def dump_summary(self):
        """
        For development - produce a summary of contents.
        """
        print('--------------------------------------------')
        print('                Data Summary                ')
        print('--------------------------------------------')
        print('File:                 {}'.format(self.fname))
        print('Total Records:        {}'.format(self.totRecords))
        print('Valid Records:        {}'.format(self.validRecords))
        print('Columns to process:   {}'.format(len(self.scalHeads) + 2 * len(self.vecHeads)))

        print('')
        return

    def get_data_dict(self, vecHeads = None, scalHeads = None):
        """
        Reads meteo data into dictionary
        (assumes SKIRON csv output format).
        """
        with open(self.fname,'r') as csvfile:
            csvData = csv.DictReader(csvfile)
            nrow = 0
            for row_dummy in csvData:
                nrow += 1
            
            self.totRecords = nrow

        dd = {}
        # Concatenate heads...
        myHeads = []
        if scalHeads:
            for item in scalHeads:
                myHeads.append(item)
        if vecHeads:
            for item in vecHeads:
                for sub in item:
                    myHeads.append(sub)

        # Initialise the arrays in the dictionary
        for hd in myHeads:
            dd[hd] = np.zeros(nrow)
            
        with open(self.fname,'r') as csvfile:
            csvData = csv.DictReader(csvfile)
            
            # Get the data
            icount = 0
            for row in csvData:
                try:
                    for name in myHeads:
                        dd[name][icount] = float(row[name])
                    icount += 1
                except:
                    print('Failed to convert to float.')
                
            self.validRecords = icount
        return dd

    def organise_data(self, mydata):
        """
        Gather data in a more suitable way for
        further processing.
        """
        for item in self.scalHeads:
            self.data[item] = mydata[item][0:self.validRecords]

        orig_dir = not self.task.opt_dict[METEO]
        for tup in self.vecHeads:
            self.data[tup] = {}
            for sub in tup:
                self.data[tup][sub] = mydata[sub][0:self.validRecords]
            
            self.data[tup][MAG] = np.zeros_like(self.data[tup][tup[0]])
            self.data[tup][DIR] = np.zeros_like(self.data[tup][tup[0]])
            for ij in range(len(self.data[tup][DIR])):
                x = self.data[tup][tup[0]][ij]
                y = self.data[tup][tup[1]][ij]
                self.data[tup][MAG][ij], self.data[tup][DIR][ij] = get_mag_dir(x, y, origin = orig_dir)
        return

    def get_stats(self):
        """
        Calculates some basic statistical indexes
        for the 1D (and some 2D) arrays.
        """
        print('Starting statistical indexes calculation...')
        if not self.task.opt_dict[STATS]:
            return 1

        if self.scalHeads:
            for item in self.scalHeads:
                self.stats[item] = {}

                self.stats[item][MEAN] = np.mean(self.data[item]) 
                self.stats[item][MAX] = np.max(self.data[item]) 
                self.stats[item][MIN] = np.min(self.data[item]) 
                self.stats[item][MEDIAN] = np.median(self.data[item]) 
                self.stats[item][STD] = np.std(self.data[item])
                self.stats[item][RECORDS] = self.validRecords
                self.stats[item][PRCTILES] = []
                for pp in ptiles:
                    self.stats[item][PRCTILES].append(np.percentile(self.data[item], pp))
        
        if self.vecHeads:
            for item1 in self.vecHeads:
                for item2 in item1:
                    self.stats[item2] = {}

                    self.stats[item2][MEAN] = np.mean(self.data[item1][item2]) 
                    self.stats[item2][MAX] = np.max(self.data[item1][item2]) 
                    self.stats[item2][MIN] = np.min(self.data[item1][item2]) 
                    self.stats[item2][MEDIAN] = np.median(self.data[item1][item2]) 
                    self.stats[item2][STD] = np.std(self.data[item1][item2])
                    self.stats[item2][RECORDS] = self.validRecords
                    self.stats[item2][PRCTILES] = []
                    for pp in ptiles:
                        self.stats[item2][PRCTILES].append(np.percentile(self.data[item1][item2], pp))
            
                self.stats[item1] = {}
                self.stats[item1][RECORDS] = self.validRecords
                self.stats[item1][COV] = np.cov(self.data[item1][item1[0]], self.data[item1][item1[1]])

        # Save the statistics in file
        filename = os.path.join(self.task.opt_dict[SAVE], 'statistics.csv')
        self.write_statistics(filename)
        
        print('Statistical indexes calculation finished.')
        return 0

    def write_statistics(self, fname):
        """
        Write statistic indexes for the each set of data.
        """
        myheads = []
        if self.vecHeads:
            for item1 in self.vecHeads:
                myheads.append(item1)
                for item2 in item1:
                    myheads.append(item2)
        
        if self.scalHeads:
            for item in self.scalHeads:
                myheads.append(item)
        
        with open(fname, 'w') as f:
            f.write(' ;')
            for hd in myheads:
                f.write('{};'.format(hd))
            f.write('\n')

            for st in STAT_ID:
                if st == PRCTILES:
                    ic = 0
                    for pp in ptiles:
                        ptitle = '{}th pctile'.format(pp)
                        f.write('{};'.format(ptitle))    
                        for hd in myheads:
                            if st in self.stats[hd]:
                                val = self.stats[hd][st][ic]
                            else:
                                val = 'null'
                            f.write('{};'.format(val))
                        ic += 1
                        f.write('\n')
                elif st == COV:
                    f.write('{};'.format(st))
                    for hd in myheads:
                        if st in self.stats[hd]:
                            val = self.stats[hd][st][0,1]
                        else:
                            val = 'null'

                        f.write('{};'.format(val))
                    f.write('\n')
                else:
                    f.write('{};'.format(st))
                    for hd in myheads:
                        if st in self.stats[hd]:
                            val = self.stats[hd][st]
                        else:
                            val = 'null'

                        f.write('{};'.format(val))
                    f.write('\n')
        return

    def create_plots(self):
        """
        Contoller for creating and saving all the necessary plots
        from this data structure.
        """
        print('Attempting to create figures...')
        if self.task.opt_dict[HISTO]:
            # Create histograms
            self.plot_histo()

        if self.task.opt_dict[SCATT]:
            # Create scatter plots
            self.plot_scatter()

        if self.task.opt_dict[HEAT]:
            # Create heatmaps
            self.plot_heat()

        if self.task.opt_dict[ROSE]:
            # Create rose diagrams
            self.plot_rose()
        
        if self.task.opt_dict[SERIES]:
            # Create timeseries graph
            self.plot_timeseries()

        print('Exiting figure creator controller.')
        return True
    

    def plot_scatter(self):
        """
        Responsible for creating scatter plots of 2D data.
        """
        if self.vecHeads:
            for item in self.vecHeads:
                fileName = []
                for figtype in self.task.opt_dict[FTYPE]:
                    fileName.append(os.path.join(self.task.opt_dict[SAVE], 'scatter_{}_{}.{}'.format(item[0], item[1], figtype)))

                mtitle, mxlabel, mylabel, mlegend = sflib.get_fig_decorations_from_header(item, SCATT)
                sflib.plot_scatter(fileName, self.data[item][item[0]], self.data[item][item[1]], title = mtitle, xlabel = mxlabel, ylabel = mylabel, dpi = 150, marker = '.', markSize = 0.6, figsize = (10,10))
                
        return 0

    def plot_histo(self):
        """
        Responsible for creating histograms of 1D data.
        """
        if self.vecHeads:
            for item in self.vecHeads:
                for sub in item:
                    fileName = []
                    for figtype in self.task.opt_dict[FTYPE]:
                        fileName.append(os.path.join(self.task.opt_dict[SAVE], 'histogram_{}.{}'.format(sub, figtype)))

                    mtitle, mxlabel, mylabel, mlegend = sflib.get_fig_decorations_from_header(sub, HISTO)
                    sflib.plot_histogram(fileName, self.data[item][sub], bins = 10, title = mtitle, xlabel = mxlabel, ylabel = mylabel, dpi = 150, figsize = (10,10))
                
                fileName_mag = []
                fileName_dir = []
                for figtype in self.task.opt_dict[FTYPE]:
                    fileName_mag.append(os.path.join(self.task.opt_dict[SAVE], 'histogram_{}_{}_mag.{}'.format(item[0], item[1], figtype))) 
                    fileName_dir.append(os.path.join(self.task.opt_dict[SAVE], 'histogram_{}_{}_dir.{}'.format(item[0], item[1], figtype)))

                mtitle, mxlabel, mylabel, mlegend = sflib.get_fig_decorations_from_header(item, HISTO, special = MAG)
                sflib.plot_histogram(fileName_mag, self.data[item][MAG], bins = 10, title = mtitle, xlabel = mxlabel, ylabel = mylabel, dpi = 150, figsize = (10,10))

                mtitle, mxlabel, mylabel, mlegend = sflib.get_fig_decorations_from_header(item, HISTO, special = DIR)
                sflib.plot_histogram(fileName_dir, self.data[item][DIR], bins = 10, title = mtitle, xlabel = mxlabel, ylabel = mylabel, dpi = 150, figsize = (10,10))

        if self.scalHeads:
            for item in self.scalHeads:
                fileName = []
                for figtype in self.task.opt_dict[FTYPE]:
                    fileName.append(os.path.join(self.task.opt_dict[SAVE], 'histogram_{}.{}'.format(item, figtype)))

                mtitle, mxlabel, mylabel, mlegend = sflib.get_fig_decorations_from_header(item, HISTO)
                sflib.plot_histogram(fileName, self.data[item], bins = 10, title = mtitle, xlabel = mxlabel, ylabel = mylabel, dpi = 150, figsize = (10,10))
                
        return 0

    def plot_heat(self):
        """
        Responsible for creating heatmaps of 2D data.
        """
        if self.vecHeads:
            for item in self.vecHeads:
                fileName = []
                for figtype in self.task.opt_dict[FTYPE]:
                    fileName.append(os.path.join(self.task.opt_dict[SAVE], 'heatmap_{}_{}.{}'.format(item[0], item[1], figtype)))

                mtitle, mxlabel, mylabel, mlegend = sflib.get_fig_decorations_from_header(item, HEAT)
                #print(fileName)
        return 0

    def plot_rose(self):
        """
        Responsible for creating rose diagrams of 2D vector data.
        """
        if self.vecHeads:
            for item in self.vecHeads:
                fileName = []
                for figtype in self.task.opt_dict[FTYPE]:
                    fileName.append(os.path.join(self.task.opt_dict[SAVE], 'rose_{}_{}.{}'.format(item[0], item[1], figtype)))

                mtitle, mxlabel, mylabel, mlegend = sflib.get_fig_decorations_from_header(item, ROSE)
                #print(fileName)
        return 0
    
    def plot_timeseries(self):
        """
        Responsible for visualising timeseries of data.
        """
        if self.vecHeads:
            for item in self.vecHeads:
                for sub in item:
                    fileName = []
                    for figtype in self.task.opt_dict[FTYPE]:
                        fileName.append(os.path.join(self.task.opt_dict[SAVE], 'timeseries_{}.{}'.format(sub, figtype)))

                    mtitle, mxlabel, mylabel, mlegend = sflib.get_fig_decorations_from_header(sub, SERIES)
                    sflib.plot_timeseries(fileName, self.data[item][sub], title = mtitle, xlabel = mxlabel, ylabel = mylabel, dpi = 150, figsize = (10,10))
                
                fileName_mag = []
                fileName_dir = []
                for figtype in self.task.opt_dict[FTYPE]:
                    fileName_mag.append(os.path.join(self.task.opt_dict[SAVE], 'timeseries_{}_{}_mag.{}'.format(item[0], item[1], figtype))) 
                    fileName_dir.append(os.path.join(self.task.opt_dict[SAVE], 'timeseries_{}_{}_dir.{}'.format(item[0], item[1], figtype)))

                mtitle, mxlabel, mylabel, mlegend = sflib.get_fig_decorations_from_header(item, SERIES, special = MAG)
                sflib.plot_timeseries(fileName_mag, self.data[item][MAG], title = mtitle, xlabel = mxlabel, ylabel = mylabel, dpi = 150, figsize = (10,10))

                mtitle, mxlabel, mylabel, mlegend = sflib.get_fig_decorations_from_header(item, SERIES, special = DIR)
                sflib.plot_timeseries(fileName_dir, self.data[item][DIR], title = mtitle, xlabel = mxlabel, ylabel = mylabel, dpi = 150, figsize = (10,10))

        if self.scalHeads:
            for item in self.scalHeads:
                fileName = []
                for figtype in self.task.opt_dict[FTYPE]:
                    fileName.append(os.path.join(self.task.opt_dict[SAVE], 'timeseries_{}.{}'.format(item, figtype)))

                mtitle, mxlabel, mylabel, mlegend = sflib.get_fig_decorations_from_header(item, SERIES)
                sflib.plot_timeseries(fileName, self.data[item], title = mtitle, xlabel = mxlabel, ylabel = mylabel, dpi = 150, figsize = (10,10))
                #print(fileName)
        return 0
        

