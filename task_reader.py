"""
Module to define the Task class
responsible for parsing the input 
of users.
It performs sanity checks on what
is asked from the application.
"""
import os
import ntpath
from support_data import FILE, NODATA, VEC, SCAL, HISTO, SCATT, ROSE, HEAT, STATS, SAVE, FTYPE, METEO, NOKEY, KEYS, INIT_DICT, DEF_VALS, POS_ANS, FTYPES_ALLOWED

def path_leaf(path):
    """
    Separate the filename and the full path.
    """
    head, tail = ntpath.split(path)
    return head, tail or ntpath.basename(head)

def get_entry(line):
    """
    Read an entry from the conf file.
    """
    if not line.strip():
        print('Empty line, ignoring...')
        return NOKEY, DEF_VALS[NOKEY]

    words = line.split('=')

    if len(words) < 2:
        if len(words) == 1:
            key = words[0].strip().lower()
            if key in KEYS:
                print('Field  {}  has no value, will default to {}'.format(key, DEF_VALS[key]))
                return key, DEF_VALS[key]
            else:
                print('Field  {}  is not recognised and will be ignored.'.format(key))
                return NOKEY, DEF_VALS[NOKEY]
        else:
            print('Empty line, ignoring...')
            return NOKEY, DEF_VALS[NOKEY]
    else:
        if len(words) > 2:
            print('Bad field combination:  {}'.format(line.strip()))
            print('Line will be ignored...')
            return NOKEY, DEF_VALS[NOKEY]

        key = words[0].strip().lower()
        if not (key in KEYS):
            print('Field  {}  is not recognised and will be ignored.'.format(key))
            return NOKEY, DEF_VALS[NOKEY]

        values = words[1].strip()

        if ',' in values:
            mult_vals = values.split(',')
        else:
            mult_vals = values.split()
        
        mvals = []
        for val in mult_vals:
            mvals.append(val.strip())

        if key == VEC and len(mult_vals) != 2:
            print('Bad field combination:  {}'.format(line.strip()))
            print('Line will be ignored...')
            return NOKEY, DEF_VALS[NOKEY]
        
        if key == SCAL and len(mult_vals) != 1:
            print('Bad field combination:  {}'.format(line.strip()))
            print('Line will be ignored...')
            return NOKEY, DEF_VALS[NOKEY]

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
        print('Entering Task creator...')

        if not filename:
            print('Error: no filename provided!')
            print('Please retry...')
            print('Exiting task')
            return

        # Get the full path and name of the file in one string
        fullname = os.path.abspath(filename) 

        # Check if the conf file exists
        if not os.path.exists(fullname):
            print('Error: The conf file does not exist!')
            print('Please retry...')
            print('Exiting task')
            return

        # Store for later use
        self.fullname = fullname
        self.fpath, self.fname = path_leaf(fullname)

        self.opt_dict = INIT_DICT

        # Read the conf file and extract info
        self.conf_reader()

        # Validate the input from the user
        ok = self.validate_conf()
        if not ok:
            print('Error: Some of the contents of ')
            print('         {}'.format(self.fullname))
            print('       are not valid!') 
            print('Please retry...')
            print('Exiting task')
            return
        
        self.ok = True
        print('Task created OK.')
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
        print('Key        :  Value   pairs')
        for kk in self.opt_dict.keys():
            print('{:<9s}  :  {}'.format(kk, self.opt_dict[kk]))

        print('')
        return

    def set_value(self, key, val):
        """
        Set the value to the field in an appropriate way.
        """
        n = len(val)
        if key == VEC or key == SCAL:
            if n == 1:
                self.opt_dict[key].append(val[0])
            else:
                self.opt_dict[key].append(val[0:])
        elif key == NODATA or key == FTYPE:
            if n == 1:
                self.opt_dict[key].append(val[0])
            else:
                for ij in range(n):
                    self.opt_dict[key].append(val[ij])
        elif key == SAVE or key == FILE:
            self.opt_dict[key] = val[0]
        else:
            uopt = val[0].lower()
            if uopt in POS_ANS:
                self.opt_dict[key] = True
            else:
                self.opt_dict[key] = False

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

        # Check for nodata value input and default to something...
        if not self.opt_dict[NODATA]:
            print('No user input for NODATA value.')
            print('Default to {}'.format(DEF_VALS[NODATA]))
            self.opt_dict[NODATA].append(DEF_VALS[NODATA])
        
        # Get the headers of the csv
        headers = get_headers(self.opt_dict[FILE])

        # Convert to lowercase the header input from the user
        # and count how many are valid.
        scount = 0
        temp_list = self.opt_dict[SCAL]
        for item in temp_list:
            item = item.lower()
            if item in headers:
                scount += 1
            else:
                print('Removing {}'.format(item))
                self.opt_dict[SCAL].remove(item)
        
        vcount = 0
        temp_list = self.opt_dict[VEC]
        for item in temp_list:
            cc = 0
            for subitem in item:
                subitem = subitem.lower()
                if subitem in headers:
                    cc += 1
            if cc > 1:
                vcount += 1
            else:
                print('Removing {}'.format(item))
                self.opt_dict[VEC].remove(item)
        
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
            print('Default to  {}'.format(DEF_VALS[FTYPE][0]))
            self.opt_dict[FTYPE] = DEF_VALS[FTYPE]

        return True



        
 
    




        
        

