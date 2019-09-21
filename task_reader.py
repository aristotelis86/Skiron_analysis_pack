"""
Module to define the Task class
responsible for parsing the input 
of users.
It performs sanity checks on what
is asked from the application.
"""
import os
import ntpath
from support_data import FILE, NODATA, VEC, SCAL, HISTO, SCATT, ROSE, HEAT, STATS, SERIES, SAVE, FTYPE, METEO, DPI, FIGSIZE, POS_ANS, FTYPES_ALLOWED
from support_data import KEYS_bool, KEYS_mult_num, KEYS_mult_str, KEYS_num, KEYS_str, NOKEY, NOKEY_val

def path_leaf(path):
    """
    Separate the filename and the full path.
    """
    head, tail = ntpath.split(path)
    return head, tail or ntpath.basename(head)

def key_in_keys(key):
    """
    Just a nice wrapper to check if key is in some the
    existing keys and get it back...
    """
    if key in KEYS_bool:
        return KEYS_bool
    if key in KEYS_mult_num:
        return KEYS_mult_num
    if key in KEYS_mult_str:
        return KEYS_mult_str
    if key in KEYS_num:
        return KEYS_num
    if key in KEYS_str:
        return KEYS_str
    
    return {}

def get_entry(line):
    """
    Read an entry from the conf file.
    """
    if not line.strip():
        print('Empty line, ignoring...')
        return NOKEY, NOKEY_val

    # Parse field name from values
    words = line.split('=')

    if len(words) < 2:
        # Just mentioning the field or some other weird setup
        if len(words) == 1:
            key = words[0].strip().lower()

            my_key_dict = key_in_keys(key)
            if my_key_dict:
                print('Field  {}  has no value, will default to {}'.format(key, my_key_dict[key]))
                return key, my_key_dict[key]
            else:
                print('Field  {}  is not recognised and will be ignored.'.format(key))
                return NOKEY, NOKEY_val
        else:
            print('Empty line, ignoring...')
            return NOKEY, NOKEY_val
    else:
        if len(words) > 2:
            print('Bad field combination:  {}'.format(line.strip()))
            print('Line will be ignored...')
            return NOKEY, NOKEY_val

        key = words[0].strip().lower()
        my_key_dict = key_in_keys(key)
        if not my_key_dict:
            print('Field  {}  is not recognised and will be ignored.'.format(key))
            return NOKEY, NOKEY_val

        values = words[1].strip()

        if ',' in values:
            mult_vals = values.split(',')
        else:
            mult_vals = values.split()
        
        mvals = []
        for val in mult_vals:
            mvals.append(val.strip())

        # if key == VEC and len(mult_vals) != 2:
        #     print('Bad field combination:  {}'.format(line.strip()))
        #     print('Line will be ignored...')
        #     return NOKEY, NOKEY_val
        
        # if key == SCAL and len(mult_vals) != 1:
        #     print('Bad field combination:  {}'.format(line.strip()))
        #     print('Line will be ignored...')
        #     return NOKEY, NOKEY_val

        return key, tuple(mvals)

def get_headers(fname):
    """
    Get the headers in the csv file.
    """
    headers = []
    with open(fname, 'r') as f:
        line = f.readline()
        words = line.split(',')

    for word in words:
        headers.append(word.strip().lower())
    return headers

############################################################
class Task:
    def __init__(self, filename = None):
        """
        Constructor - aborting if nothing 
        is entered (ie no demo mode).
        """
        self.ok = False
        print('')
        print('------> Entering Task creator...')

        if not filename:
            print('Error: no filename provided!')
            print('Please retry...')
            print('Exiting task. <------ ')
            return

        # Get the full path and name of the file in one string
        fullname = os.path.abspath(filename) 

        # Check if the conf file exists
        if not os.path.exists(fullname):
            print('Error: The conf file does not exist!')
            print('Please retry...')
            print('Exiting task. <------')
            return

        # Store for later use
        self.fullname = fullname
        self.fpath, self.fname = path_leaf(fullname)

        # Initialise options dictionary
        self.init_opt_dict()

        # Read the conf file and extract info
        self.conf_reader()

        # Validate the input from the user
        ok = self.validate_conf()
        if not ok:
            print('Error: Some of the contents of ')
            print('         {}'.format(self.fullname))
            print('       are not valid!') 
            print('Please retry...')
            print('Exiting task. <------')
            return
        
        self.ok = True
        print('Task created OK. <------')
        return

    def init_opt_dict(self):
        """
        Get the keys and default values
        to proceed with the task.
        """
        self.opt_dict = {}
        for key in KEYS_bool.keys():
            self.opt_dict[key] = KEYS_bool[key]
        
        for key in KEYS_mult_num.keys():
            self.opt_dict[key] = KEYS_mult_num[key]

        for key in KEYS_mult_str.keys():
            self.opt_dict[key] = KEYS_mult_str[key]

        for key in KEYS_num.keys():
            self.opt_dict[key] = KEYS_num[key]
        
        for key in KEYS_str.keys():
            self.opt_dict[key] = KEYS_str[key]
        return

    def dump(self):
        """
        Just for debugging.
        Printing the dictionary.
        """
        print('--------------------------------------------')
        print('                Task Summary                ')
        print('--------------------------------------------')
        print('Fullpath to conf file:    {}'.format(self.fullname))
        print('Path of conf file:        {}'.format(self.fpath))
        print('Name of conf file:        {}'.format(self.fname))
        print('*********************')
        print('(Key       :  Value)  ')
        for kk in self.opt_dict.keys():
            print('{:<9s}  :  {}'.format(kk, self.opt_dict[kk]))
        print('============================================')
        print('')
        return

    def set_value(self, key, val):
        """
        Set the value to the field in an appropriate way.
        """
        if isinstance(val, tuple):
            if key in KEYS_bool:
                uopt = val[0].lower()
                if uopt in POS_ANS:
                    self.opt_dict[key] = True
                else:
                    self.opt_dict[key] = False
            elif key in KEYS_str:
                self.opt_dict[key] = val[0]
            elif key in KEYS_num:
                try:
                    self.opt_dict[key] = float(val[0])
                except:
                    print('Using default {}:{}'.format(key, KEYS_num[key]))
                    self.opt_dict[key] = KEYS_num[key]
            elif key in KEYS_mult_str:
                self.opt_dict[key].append(val[0:])
            elif key in KEYS_mult_num:
                temp_list = []
                for item in val:
                    try:
                        temp_list.append(float(item))
                    except:
                        print('Could not add {} to {}'.format(item, key))
                
                self.opt_dict[key] = tuple(temp_list)
        elif isinstance(val, int) or isinstance(val, float):
            if key in KEYS_num:
                self.opt_dict[key] = val
            else:
                print('Could not associate {} with numeric fields...'.format(key))
            
        elif isinstance(val, list):
            print('Unable to handle lists in task_reader.set_values()...')
        else:
            print('No method to handle {}:{}'.format(key, val))

        return

    def conf_reader(self):
        """
        Read the contents of the conf file.
        """
        with open(self.fullname, 'r') as f:
            lines = f.readlines()

        for line in lines:
            key, vals = get_entry(line)

            if key != NOKEY:
                self.set_value(key, vals)
        return
    
    def validate_conf(self):
        """
        Responsible for validating the contents 
        of the conf file.
        """
        if not self.opt_dict[FILE]:
            print('SKIRON csv filename is missing!')
            return False

        # Adjust the full name of the csv file
        temp_path = os.path.join(self.fpath, self.opt_dict[FILE])
        if not os.path.exists(temp_path):
            print('SKIRON csv file does not exist: {}'.format(temp_path))
            return False
        
        self.opt_dict[FILE] = temp_path

        # # Check for nodata value input and default to something...
        # if not self.opt_dict[NODATA]:
        #     print('No user input for NODATA value.')
        #     print('Default to {}'.format(KEYS_mult_str[NODATA]))
        #     self.opt_dict[NODATA].append(KEYS_mult_str[NODATA])
        
        # Get the headers of the csv
        headers = get_headers(self.opt_dict[FILE])

        # Convert to lowercase the header input from the user
        # and count how many are valid.
        scount = 0
        temp_list = self.opt_dict[SCAL]
        self.opt_dict[SCAL] = []
        for item in temp_list:
            
            if len(item) != 1:
                print('Bad request for scalar field, will consider leftmost entry only from {}'.format(item))
            
            item1 = item[0].lower()
            if item1 in headers:
                self.opt_dict[SCAL].append(item1)
                scount += 1
            else:
                print('Removing {}'.format(item))
        
        vcount = 0
        temp_list = self.opt_dict[VEC]
        self.opt_dict[VEC] = []
        for item in temp_list:
            if len(item) < 2:
                print('Ignoring {}'.format(item))
                continue
            elif len(item) > 2:
                print('Bad request for vector field, will consider the first two different entries from {}'.format(item))

            cc = 0
            last = ''
            temp_tup = []
            for subitem in item:
                current = subitem.lower()
                if cc != 0:
                    if (current != last) and (current in headers):
                        temp_tup.append(current)
                        last = current
                        cc += 1
                else:
                    if current in headers:
                        temp_tup.append(current)
                        last = current
                        cc += 1

                if cc == 2:
                    self.opt_dict[VEC].append(tuple(temp_tup))
                    vcount += 1
                    continue
            
        if scount + vcount < 1:
            print('No valid header input found in the conf file!')
            return False
        
        # Get unique elements...
        if vcount > 0:
            self.opt_dict[VEC] = list(set(self.opt_dict[VEC]))
        if scount > 0:
            self.opt_dict[SCAL] = list(set(self.opt_dict[SCAL]))

        # Check if any output is actually requested
        outcount = 0
        if self.opt_dict[HISTO]:
            outcount += 1
        if self.opt_dict[SCATT]:
            outcount += 1
        if self.opt_dict[ROSE]:
            outcount += 1
        if self.opt_dict[HEAT]:
            outcount += 1
        if self.opt_dict[SERIES]:
            outcount += 1
        if self.opt_dict[STATS]:
            outcount += 1
        if not outcount:
            print('No output is actually requested!')
            return False
        
        # Check if any folders need to be created for output
        temp_path = os.path.join(self.fpath, self.opt_dict[SAVE])
        if not os.path.exists(temp_path):
            print('Output folder does not exist, but will attempt creating...')
            os.makedirs(temp_path)
            if not os.path.exists(temp_path):
                print('Output folder could NOT be created...')
                print('Possible cause: Lack of writing rights in some of the folders in the path.')
                return False
        self.opt_dict[SAVE] = temp_path

        # Check for valid output figure filetypes
        temp_list = self.opt_dict[FTYPE]
        for ftype in temp_list:
            if not (ftype in FTYPES_ALLOWED):
                self.opt_dict[FTYPE].remove(ftype)

        if len(self.opt_dict[FTYPE]) < 1:
            print('No valid output format given...')
            print('Default to  {}'.format(KEYS_mult_str[FTYPE][0]))
            self.opt_dict[FTYPE] = KEYS_mult_str[FTYPE]

        # Check for the rest of options...
        self.opt_dict[DPI] = int(self.opt_dict[DPI])
        if self.opt_dict[DPI] < 80 or self.opt_dict[DPI] > 350:
            print('Unusually small or large value for DPI detected...')
            print('Will default to {}'.format(KEYS_num[DPI]))
            self.opt_dict[DPI] = KEYS_num[DPI]

        # Ensure figsize has two values
        if isinstance(self.opt_dict[FIGSIZE], tuple):
            if len(self.opt_dict[FIGSIZE]) == 1:
                self.opt_dict[FIGSIZE] = tuple([self.opt_dict[FIGSIZE][0], self.opt_dict[FIGSIZE][0]])
            elif len(self.opt_dict[FIGSIZE]) > 2:
                print('Bad format for figsize, will consider first two args only...')
                self.opt_dict[FIGSIZE] = tuple([self.opt_dict[FIGSIZE][0], self.opt_dict[FIGSIZE][1]])
        else:
            print('Unknown format for figsize...')
            print('Will default to {}'.format(KEYS_mult_num[FIGSIZE]))
            self.opt_dict[FIGSIZE] = KEYS_mult_num[FIGSIZE]

        return True



        
 
    




        
        

