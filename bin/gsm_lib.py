#/usr/bin/env python

"""
gsm_lib.py

    Stores a collection of utility functions used by
        generate_subject_map.py and generate_subject_map_input.py
"""

__author__      = ""
__copyright__   = "Copyright 2014, University of Florida"
__license__     = "BSD 3-Clause"
__version__     = "0.1"
__email__       = ""
__status__      = "Development"

import json
import pprint
import os
import sys
import datetime
import contextlib
import tempfile
import shutil

# This addresses the issues with relative paths
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

sys.path.insert(0, proj_root+'bin/utils/')
from GSMLogger import GSMLogger


'''
Sort element tree based on three given indices.

Keyword argument: data
sorting is based on study_id, form name, then timestamp, ascending order
'''
def sort_element_tree(data):
    # this element holds the subjects that are being sorted
    container = data.getroot()
    container[:] = sorted(container, key=getkey)


'''
Helper function for sorting. Returns keys to sort on.

Keyword argument: elem
returns the corresponding tuple study_id, form_name, timestamp
'''
def getkey(elem):
    research_subject_id = elem.findtext("research_subject_id")
    yob = elem.findtext("yob")
    return (research_subject_id,yob)


'''
Write ElementTree to a file
    takes file_name as input
'''
def write_element_tree_to_file(element_tree, file_name):
    #gsmlogger.logger.debug('Writing ElementTree to %s', file_name)
    element_tree.write(file_name, encoding="us-ascii", xml_declaration=True,method="xml")


'''
Read the config data from setup.json
'''
def read_config(configuration_directory, setup_json):
    conf_file = configuration_directory + setup_json

    # check if the path is valid
    if not os.path.exists(conf_file):
        raise GSMLogger().LogException("Invalid path specified for conf file: " + setup_json)

    try:
        json_data = open(conf_file)
    except IOError:
        #raise logger.error
        print "file " + conf_file + " could not be opened"
        raise

    setup = json.load(json_data)
    json_data.close()

    # test for required parameters
    required_parameters = ['source_data_schema_file', 'site_catalog',
                    'system_log_file']

    for parameter in required_parameters:
        if not parameter in setup:
            raise GSMLogger().LogException("read_config: required parameter, "
                + parameter  + "', is not set in " + conf_file)

    # test for required files but only for the parameters that are set
    files = ['source_data_schema_file', 'site_catalog']
    for item in files:
        if item in setup:
            if(item == 'system_log_file'):
                file_path = proj_root + 'log/'
                if not os.path.exists(file_path):
                    try:
                        os.makedirs(file_path)
                    except OSError:
                        print "Unable to create folder: " + file_path
            else:
                file_path = configuration_directory + setup[item]

            if not os.path.exists(file_path):
                print 'Checking existence of file: ' + file_path
                raise GSMLogger().LogException("read_config: " + item
                    + " file, '" + setup[item] + "', specified in " + conf_file + " does not exist")
    return setup



'''
Helper function for parsing undefined strings
'''
def handle_blanks(s):
    return '' if s is None else s.strip()


'''
Create a folder name with the following format:
    ./out/out_YYYY_mm_dd:00:11:22
'''
def create_temp_dir_debug(existing_folder = './out') :
    prefix = 'out_' + datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    mydir = existing_folder + '/' + prefix
    os.mkdir(mydir)
    return mydir

'''
If do_keep_gen_files = True
    create a path like './out/out_YYYY_mm_dd:00:11:22'
else
    create a path using system provided location for a file
'''
def get_temp_path(do_keep_gen_files) :
    if do_keep_gen_files :
        return create_temp_dir_debug() + '/'
    else :
        return tempfile.mkdtemp('/')


def parse_host_and_port(raw):
    """Returns a tuple comprising hostname and port number from raw text"""
    host_and_port = raw.split(':')
    if len(host_and_port) == 2:
        return host_and_port
    else:
        return raw, None
