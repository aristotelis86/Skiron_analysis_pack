from task_reader import Task
from skiron_reader import SkironData
import sys
from datetime import datetime

#############################################################
def main(verbose = False):
    """
    Master controller of the application.
    (For command line at least...)
    Responsible for parsing command line options 
    as well.
    """
    myargs = sys.argv[1:]
    nargs = len(myargs)
    actedon = 0
    dry = False
    timeit = False

    # If we do have arguments...
    if nargs > 0:
        for arg in myargs:
            # Check if the user explicitly asked for verbosity
            if arg[0] == '-':
                if arg.lower() == '-v':
                    verbose = True
                elif arg.lower() == '-dry':
                    dry = True
                elif arg.lower() == '-t':
                    timeit = True
                elif arg.lower() == '-h':
                    display_help()
                    if nargs > 1:
                        print('')
                        print('Execution terminated after showing help.')
                        print('If processing is needed, please remove "-h" flag and retry.')
                        print('Exiting...')
                        print('-------------------------------------------------------------')
                    return
                else:
                    print('Unrecognised flag passed, ignoring: {}'.format(arg))
        
        # Show banner
        welcome_message()

        # Start timer for reporting if necessary
        startTime = datetime.now()
        intervTime = startTime
        taskID = 0

        # Previous loop was to check for verbosity, now take action
        for arg in myargs:
            if arg[0] != '-':
                taskID += 1
                temp_task = Task(arg)
                if not temp_task.ok:
                    print('Task was not read correctly --> {}'.format(arg))
                    print('Continue with any remaining tasks...')
                    continue
                if verbose or dry:
                    temp_task.dump()

                # Get time to load task
                timenow = datetime.now()
                if timeit:
                    print('****Task {} loaded in {} (hh:mm:ss).****'.format(taskID, timenow - intervTime))

                if dry:
                    print('Finished dry run for Task {}.'.format(taskID))
                    continue
                
                # Measure action
                intervTime = datetime.now()
                temp_skiron = SkironData(temp_task)
                if not temp_skiron.ok:
                    print('Task could not load data correctly --> {}'.format(arg))
                    print('Continue with any remaining tasks...')
                    continue
                if verbose:
                    temp_skiron.dump_summary()

                timenow = datetime.now()
                if timeit:
                    print('****Data for task {} loaded in {} (hh:mm:ss).****'.format(taskID, timenow - intervTime))
                
                # Measure output timing
                intervTime = datetime.now()
                plots_ok = temp_skiron.create_plots()
                if not plots_ok:
                    print('Some or all of the plots were created...')
                
                stats_ok = temp_skiron.get_stats()
                if stats_ok < 0:
                    print('Some or all of the statistical indexes could not be calculated...')
                elif stats_ok > 0:
                    print('Statistics were not asked, so skipping...')

                timenow = datetime.now()
                if timeit:
                    print('****Output for task {} created in {} (hh:mm:ss).****'.format(taskID, timenow - intervTime))
                
                actedon += 1
    else:
        # Lack of arguments => exit...
        print('No conf files are given...')
        print('No demo mode at the moment, see correct usage below.')
        display_help()

    if actedon > 0:
        print('{} Task(s) were performed.'.format(actedon))
    else:
        print('No action taken.')

    timenow = datetime.now()
    if timeit:
        print('****The app finished in {} (hh:mm:ss).****'.format(timenow - startTime))

    print('Inspect previous messages for any errors/tasks undone...')
    return

def welcome_message():
    print('')
    print('*************************************************')
    print('            SKIRON data statistics               ')
    print('              and visualisation.                 ')
    print('*************************************************')
    print('')

def display_help():
    print('SKIRONANALYSIS Application:')
    print('Get basic statistics and figures for data in a SKIRON csv output file.')
    print('Usage:')
    print('skironanalysis batch.conf [batch2.conf ...] [-v, -t, -h, -dry]')
    print('')
    print('                -h:         Show this help message.                    ')
    print('                -v:         Turn on verbose mode. Multiple messages are')
    print('                            shown to the user.                         ')
    print('                -t:         Shows timings of each task/action.         ')
    print('              -dry:         Attempts to load the task(s). No further   ')
    print('                            action is taken (ie load/process data.)    ')
    
###############################################################
# Actual run part
if __name__ == "__main__":
    print('\n\n')
    main()
    print('End')
    print('-------------------------------------------------------------')




