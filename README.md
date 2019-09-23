# Skiron_analysis_pack

This is a tool to process output (timeseries) csv files produced by SKIRON weather and dust modelling system.

It is able to produce basic statistical indexes such as:
- *Minimum value*
- *Maximum value*
- *Mean value*
- *Median*
- *Standard deviation*
- *Percentiles*
- *Covariance* (2D components)
- *Number of valid records*

Additionally, multiple figures can be created:
- *Timeseries*
- *Histograms*
- *Scatter plots* (2D only)
- *Heatmaps* (2D only, polar coord displayed)
- *Rose charts* (2D only, polar coord displayed)

## Usage
The main script (`mainApp.py`) expects at least one text file summarising the task to be completed. If multiple tasks are needed, then multiple task files can be passed to the script. The task file is plain text, and uses the (`field = value(s)`) convention. An example task file is given as *example.conf*. The extension of the file can be arbitrary (not checked for validation).

The script also accepts switches to enable certain functionality, such as timing the code or increasing verbosity. For further details, please see the examples below.

## Task file format
The general format of this text file follows the (`field = value(s)`) convention. The full list of available options with a brief explanation and any default and accepted values follows:
- **file**: provides the path to the csv file. The path should be relative to the task file. For example, the task file is in  ~/Documents/task1.conf and the csv in ~/Documents/data/mycsv.csv. The entry should be file=data/mycsv.csv. The default value is empty and the path should not contain empty spaces. Only one entry of this field is allowed.
- **vec**: provides the headers to the vector data separated by comma. For example, vec=u_m1ll, v_m1ll. The default value is empty. It accepts two headers only. If more headers are provided, the application will choose the first two, non-matching headers. If it fails, it will ignore the entry. The entry will also be ignored if the headers are not both present in the csv. Multiple vec fields can be included, in case more than one vector series are to be processed.
- **scal**: provides the headers to the scalar data. For example, scal=air_m1ll. The default value is empty. It accepts one header only. If more headers are provided, the application will ignore the entry. The entry will also be ignored if the header is not present in the csv. Multiple scal fields can be included, in case more than one scalar series are to be processed.
- **datetime**: provides the header of the date-time data. This will be used for data filtering (see **timefrom** and **timeto** fields). If the header is not in the csv, date filtering is disabled for this task.
- **timefrom**: provides the date from which the data are to be included in processing (this date included). Default value is empty and results to data being included from the start of the csv. Multiple date formats accepted (DD/MM/YYYY, preferable).
- **timeto**: provides the date until which the data are to be included in processing (this date included). Default value is empty and results to data being included unitl the end of the csv. Multiple date formats accepted (DD/MM/YYYY, preferable).
- **histo**: Flag to enable output of histograms. Default is *false*, so no output of histograms. To enable it, any of the following is accepted: *1*, *t*, *y*, *yes* and *true* (case insensitive). Anything else will turn it off. Histograms are produced for all scalar variables and for each component of vectors (including magnitude and direction).
- **scatter**: Flag to enable output of scatter plots. Default is *false*, so no output of plots. To enable it, any of the following is accepted: *1*, *t*, *y*, *yes* and *true* (case insensitive). Anything else will turn it off. Scatter plots are produced for vector variables only (*not* including magnitude and direction).
- **rose**: Flag to enable output of rose charts. Default is *false*, so no output of charts. To enable it, any of the following is accepted: *1*, *t*, *y*, *yes* and *true* (case insensitive). Anything else will turn it off. Rose charts are produced for vector variables only (magnitude and direction *only*).
- **heat**: Flag to enable output of heatmaps. Default is *false*, so no output of heatmaps. To enable it, any of the following is accepted: *1*, *t*, *y*, *yes* and *true* (case insensitive). Anything else will turn it off. Heatmaps are produced for vector variables only (magnitude and direction *only*).
- **series**: Flag to enable output of timeseries. Default is *false*, so no output of timeseries. To enable it, any of the following is accepted: *1*, *t*, *y*, *yes* and *true* (case insensitive). Anything else will turn it off. Timeseries are produced for all scalar variables and for each component of vectors (including magnitude and direction).
- **stats**: Flag to enable output of statistics. Default is *false*, so no output. To enable it, any of the following is accepted: *1*, *t*, *y*, *yes* and *true* (case insensitive). Anything else will turn it off. The values are stored in the file *statistics.csv*.
- **save**: provides the path to the folder to save all the output (both figures and statistics). The path should be relative to the task file, similarly to the **file** field. The default value is empty and the path should not contain empty spaces. Only one entry of this field is allowed. If the folder does not exist, it will be created, along with any parent folders needed. 
- **ftype**: passes the image file types to be used for saving the figures. More than one entries can be entered (comma-separated). Default value is *png*, but it also accepts any combination of *eps*, *pdf*, *ps* and *svg*.

When attempting to load one or more task files, the application will try to recover from certain failures. If it fails to recover, any remaining tasks will continue normally. Emtpy lines and entries not recognised are ignored by default and do not affect the run. You may or may not leave space around the `=` sign between the field and its value.

## Dependencies
The application is compatible with Python 3 (built with 3.7.3). The libraries loaded are the following:
- os
- sys
- ntpath
- datetime
- dateutil
- csv
- numpy
- matplotlib
- windrose

## Examples
#### Example 1:
Process data using the task file ~/mytask.conf. Requesting as much information as possible and timing of the run:

`python3 mainApp.py -v -t ~/mytask.conf`

#### Example 2:
Process multiple data using the task files ~/mytask1.conf and ~/Document/tasks/task2.conf. Requesting as much information as possible:

`python3 mainApp.py -v ~/mytas1k.conf ~/Document/tasks/task2.conf`

#### Example 3:
Ask for help on the usage:

`python3 mainApp.py -h`

The order of the arguments is not important. In case there is a frozen version of the code, replace `python3 mainApp.py` with `skironanalysis`. 

