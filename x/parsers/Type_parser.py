"""
@file JiraIssueMigrator/Type_parser.py
@author Roger Unwin
@brief Simple parser, just grabs the column headings.

"""

from x import importer
import csv

class Type_parser(importer.Parser):
    
    def __init__(self):             
        """
        """
        pass
    
    def parse(self, columns):
        self.shared.columns = columns
        outputWriter = self.shared.outputWriter
        outputWriter.writerow(columns)
         
        return False # Return false, so this line always gets propagated to the rejects file
    
    def should_i_parse(self, columns):
        if len(columns) > int(self.shared.settings['field_mappings.' + "Type"]) and columns[int(self.shared.settings['field_mappings.' + "Type"])].strip() == 'Type':
        #if len(columns) > 1 and columns[1] == 'Type':
            return True
        return False

    def get_handler_name(self):
        return "Type"
    
foo = Type_parser()
