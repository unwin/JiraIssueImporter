
"""
@file JiraIssueMigrator/C_parser.py
@author Roger Unwin
@brief this parses 'W' lines and sets persistent variables based on what it finds.

C = control account
""" 
from x import importer
import csv


class C_parser(importer.Parser):
    
    def __init__(self):
        """
        """
        pass
    
    def parse(self, columns):
        settings = self.shared.settings
        outputWriter = self.shared.outputWriter
        outputWriter.writerow(columns)
        # 1.2.3.12.1,C,Common Operating Infrastructure - Release 1
        if len(columns) > int(settings["field_mappings.OOI_CATEGORY_NUMBER"]):
            self.shared.control_account_WBS_number = columns[int(settings["field_mappings.OOI_CATEGORY_NUMBER"])]
        else:
            self.shared.control_account_WBS_number = ''
            
        if len(columns) > int(settings["field_mappings.Task"]):
            self.shared.control_account_WBS_description = columns[int(settings["field_mappings.Task"])]
            self.shared.control_account_subsystem = settings['Projects.' + columns[int(settings["field_mappings.Task"])]]
        else:
            self.shared.control_account_WBS_description = ''
            self.shared.control_account_subsystem = ''
            
        return False # Return false, so this line always gets propagated to the rejects file
    
    def should_i_parse(self, columns):
        if len(columns) > int(self.shared.settings['field_mappings.' + "Type"]) and columns[int(self.shared.settings['field_mappings.' + "Type"])].strip() == 'C':
        #if len(columns) > 1 and columns[1].strip() == 'C':
            return True
        return False

    def get_handler_name(self):
        return "C"
    
foo = C_parser()
