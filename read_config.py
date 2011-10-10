"""
@file JiraIssueMigrator/read_config.py
@author Roger Unwin
@brief this module reads a config file, and returns a dict of section.label = value
"""

import re

def read_file(fn):
    values = {}
    file = open(fn)
    last_section = 'default'
    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            line = re.sub('#.*', '', line.strip())
            vals = line.split('=', 2)
            
            if (len(vals) == 1) :
                vals[0] = re.sub('[\[\]]', '', vals[0].strip())
                if (vals[0] != ''):
                    last_section = vals[0].strip()
            else:
                values[last_section + '.' + vals[0].strip()] = vals[1].strip()
    return values