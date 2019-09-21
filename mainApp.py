from task_reader import Task
from skiron_reader import SkironData
import sys

#############################################################
def main(verbose = True):
    """
    Master controller of the application.
    (For command line at least...)
    Responsible for parsing command line options 
    as well.
    """
    myargs = sys.argv[1:]
    nargs = len(myargs)
    actedon = 0

    # If we do have arguments...
    if nargs > 0:
        for arg in myargs:
            # Check if the user explicitly asked for verbosity
            if arg[0] == '-':
                if arg.lower() == '-v1':
                    verbose = True
                elif arg.lower() == '-v0':
                    verbose = False
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

        # Previous loop was to check for verbosity, now take action
        for arg in myargs:
            if arg[0] != '-':
                temp_task = Task(arg)
                if not temp_task.ok:
                    print('Task was not read correctly --> {}'.format(arg))
                    print('Continue with any remaining tasks...')
                    continue
                if verbose:
                    temp_task.dump()
                
                temp_skiron = SkironData(temp_task)
                if not temp_skiron.ok:
                    print('Task could not load data correctly --> {}'.format(arg))
                    print('Continue with any remaining tasks...')
                    continue
                if verbose:
                    temp_skiron.dump_summary()
                
                plots_ok = temp_skiron.create_plots()
                if not plots_ok:
                    print('Some or all of the plots were created...')
                
                stats_ok = temp_skiron.get_stats()
                if stats_ok < 0:
                    print('Some or all of the statistical indexes could not be calculated...')
                elif stats_ok > 0:
                    print('Statistics were not asked, so skipping...')

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

    print('Inspect previous messages for any errors/tasks undone...')
    print('End')
    print('-------------------------------------------------------------')
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
    print('skironanalysis batch.conf [batch2.conf ...] [-v0, -v1, -h]')

###############################################################
# Actual run part
if __name__ == "__main__":
    print('\n\n')
    main()




