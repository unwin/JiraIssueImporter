
"""
@file JiraIssueMigrator/SV_parser.py
@author Roger Unwin
@brief this parses 'SV' lines and sets persistent variables based on what it finds.

SV = work package
"""

from x import importer
import csv

class SV_parser(importer.Parser):
    
    def __init__(self):
        """
        """
        pass
    def parse(self, columns):
        settings = self.shared.settings
        outputWriter = self.shared.outputWriter
        outputWriter.writerow(columns)




        if len(columns) > int(settings["field_mappings.Task"]):
            print "*************\n*************" + str(columns[int(settings["field_mappings.OOI_CATEGORY_NUMBER"])]) + ' ' + str(columns[int(settings["field_mappings.Task"])])
            self.shared.work_package_task_component = str(columns[int(settings["field_mappings.OOI_CATEGORY_NUMBER"])]) + ' ' + str(columns[int(settings["field_mappings.Task"])])

  
        if len(columns) > int(settings["field_mappings.Task"]):
            self.shared.work_package_task = columns[int(settings["field_mappings.Task"])]

        if len(columns) > int(settings["field_mappings.Description"]):
            self.shared.work_package_description = columns[int(settings["field_mappings.Description"])]
        else:
            self.shared.work_package_description = ''
            
        if len(columns) > int(settings["field_mappings.Risk (RTs)"]):    
            self.shared.component_risks_RTs = columns[int(settings["field_mappings.Risk (RTs)"])]
        else:
            self.shared.component_risks_RTs = ''
            
        if len(columns) > int(settings["field_mappings.Possible Risks"]):    
            self.shared.component_possible_risks = columns[int(settings["field_mappings.Possible Risks"])]
        else:
            self.shared.component_possible_risks = ''
            
        return False # Return false, so this line always gets propagated to the rejects file
    
    def should_i_parse(self, columns):
        if len(columns) > int(self.shared.settings['field_mappings.' + "Type"]) and columns[int(self.shared.settings['field_mappings.' + "Type"])].strip() == 'SV':
            return True
        return False

    def get_handler_name(self):
        return "SV"
    
foo = SV_parser()
