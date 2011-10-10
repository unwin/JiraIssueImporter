
"""
@file JiraIssueMigrator/CO_parser.py
@author Roger Unwin
@brief this parses 'CO' lines and sets persistent variables based on what it finds.

CO = release task
"""

from x import importer
import csv


class CO_parser(importer.Parser):
    
    def __init__(self):
        """
        """
        pass
    
    def parse(self, columns):
        settings = self.shared.settings
        outputWriter = self.shared.outputWriter
        outputWriter.writerow(columns)
 
        if len(columns) > int(settings["field_mappings.Task"]):
            self.shared.release_task_task_title = columns[int(settings["field_mappings.Task"])]
        else:
            self.shared.release_task_task_title = ''

        if len(columns) > int(settings["field_mappings.Description"]):
            self.shared.release_task_description = columns[int(settings["field_mappings.Description"])]
        else:
            self.shared.release_task_description = ''

        #Risk (RTs)
        
        if len(columns) > int(settings["field_mappings.Risk (RTs)"]) and str(columns[int(settings["field_mappings.Risk (RTs)"])].lower).startswith("ri-"):
            self.shared.release_task_risk_rts = columns[int(settings["field_mappings.Risk (RTs)"])]
           
        else:
            self.shared.release_task_risk_rts = ''
            
        return False # Return false, so this line always gets propagated to the rejects file
    
    def should_i_parse(self, columns):
        if len(columns) > int(self.shared.settings['field_mappings.' + "Type"]) and columns[int(self.shared.settings['field_mappings.' + "Type"])].strip() == 'CO':
            return True
        return False

    def get_handler_name(self):
        return "CO"
    
foo = CO_parser()
