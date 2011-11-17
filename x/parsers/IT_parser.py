
"""
@file JiraIssueMigrator/main.py
@author Roger Unwin
@brief this parses 'IT' lines and creates jira issues based on what it and the other parsers have found.

IT = item

        KNOWN ISSUE THAT ORIGIONAL ESTIMATE IS NOT PRESENT...
        https://jira.atlassian.com/browse/JRA-7624
        
"""

from x import importer
import SOAPpy
import time
import csv

class IT_parser(importer.Parser):
    
    def __init__(self):
        """
        """
        pass
    
    
    def parse(self, columns):
        settings = self.shared.settings
        outputWriter = self.shared.outputWriter




        issue = {}
        def col_num(col_name):
            return int(self.shared.settings['field_mappings.' + col_name])
            


	#print "checking col " + str(col_num("Iteration")) + "/" + str(len(columns)) + str(column)
	if len(columns) >= col_num("Iteration") and columns[ col_num("Iteration")] != self.shared.settings['jira.filter_value']:
	    print "Task did not match " + settings['jira.filter_value'] + " VALUE WAS " + columns[ col_num("Iteration")]
            outputWriter.writerow(columns)
	    return False

        #*3=Task
        # 2=New Feature
        # 1=Bug
        
        issue["task_type"] = 3 
        
        if len(columns) > col_num("Task"):
            issue["task_title"] = columns[col_num("Task")]
        else:
            print "TASK TITLE FAILED"
            outputWriter.writerow(columns)
            return False
        
        if len(columns) > col_num("Description"):
            issue["task_description"] = columns[col_num("Description")]
        else:
            print "DESCRIPTION FAILED"
            outputWriter.writerow(columns)
            return False

        if len(columns) > col_num("Support Developer") and columns[ col_num("Support Developer") ] != '':
            issue["task_description"] = issue["task_description"] + "\n\nSupport Developer: " + columns[col_num("Support Developer")]

        if len(columns) > col_num("Outcome") and columns[ col_num("Outcome") ] != '':
            issue["task_description"] = issue["task_description"] + "\n\nOutcome: " + columns[col_num("Outcome")]

        if len(columns) > col_num("Assignee"):
            #issue["task_assignee"] = settings['user_mappings.' + columns[ col_num("Assignee")].lower()]
            issue["task_assignee"] = columns[ col_num("Assignee")]
        else:
            print "ASSIGNEE FAILED"
            outputWriter.writerow(columns)
            return False
        
        issue["task_reporter"] = settings["jira.reporter"]
        
        if len(columns) > col_num("Risk (RTs)"):
            issue["task_risk"] = columns[col_num("Risk (RTs)")] # NEEDS TO BE PUT INTO A CUSTOM FIELD

        print "WHY ARE THERE NO AFFECTS VERSIONS OR FIX VERSIONS!!!!!"
        issue["task_affects_versions"] = ''
        for col in settings["Used_mappings.AffectsVersion"].split(','):
            if columns[int(col)].lower().find('x') >= 0:
                if issue["task_affects_versions"] != '':
                    issue["task_affects_versions"] += ', '
                issue["task_affects_versions"] += self.shared.columns[int(col)]
        issue["task_fix_versions"] = issue["task_affects_versions"]
        
        
        
        if len(columns) >  col_num("Design URL"):
            issue["task_design_url"] = columns[col_num("Design URL")] # add this as part of long task description
#        else:
#            print "DESIGN URL FAILED"
#            return False
        
        if len(columns) > col_num("Priority") and columns[ col_num("Priority")] != '':
            issue["task_priority"] = settings["jira_priority." + settings["priorities." + columns[ col_num("Priority")]]]
            
            if len(columns) > col_num("Priority") and columns[col_num("Priority")] != '':
                issue["jira_task_priority"] = settings['priorities.' + columns[col_num("Priority")]]
            
        else:
            print "PRIORITY FAILED" + str(columns[ col_num("Priority")]) + str(col_num("Priority"))
            columns[col_num("Priority")] = '>' + columns[col_num("Priority")] + '<'
            print str(columns)
            print '---------'
            outputWriter.writerow(columns)
            return False
        
        if len(columns) > col_num("Work Days") and columns[ col_num("Work Days")] != '':
            issue["task_work_estimate_days"] = columns[col_num("Work Days")]
        else:
            print "WORK DAYS FAILED"
            outputWriter.writerow(columns)
            return False
        
        if len(columns) > col_num("Comments"):
            issue["task_comments"] = columns[col_num("Comments")]                             # perhaps add this as a comment
        
        if len(columns) > col_num("Possible Risks"):
            issue["task_possible_risks"] = columns[col_num("Possible Risks")]                            # add this as part of long task description
        
        
        
        customFields = []
        if self.shared.component_risks_RTs:
            customFields.append({'values': [self.shared.component_risks_RTs], 'customfieldId': 'customfield_10013', 'key': None})
            
        if "task_design_url" in issue and issue["task_design_url"] != '':
            customFields.append({'values': [issue["task_design_url"]], 'customfieldId': 'customfield_10010', 'key': None})
            
        
        new_issue = {'project': self.shared.control_account_subsystem,
                'type': str(issue["task_type"]),
                'summary': issue["task_title"],
                'description': issue["task_description"],
                'customFieldValues': customFields,
                'assignee': issue["task_assignee"],
                'reporter': issue["task_reporter"],
                'priority': issue["task_priority"]}
        
        
        # new code! add a version every time, let it fail if already there.
        try:
            soap.addVersion(auth, self.shared.control_account_subsystem, {'name': issue["task_affects_versions"]})
            print "1 ADDED new version " + issue["task_affects_versions"] + " to project " + self.shared.control_account_subsystem
        except:
            print "1 FAILED ADDED new version " + issue["task_affects_versions"] + " to project " + self.shared.control_account_subsystem

        try:    
             newissue = self.shared.soap.createIssue(self.shared.auth, new_issue)
             print "Created %s/browse/%s" % (settings["jira.url"], newissue['key'])

             columns[col_num("Jira Task Num")] = settings["jira.url"] + "/browse/" + newissue['key']
             outputWriter.writerow(columns)

             project = self.shared.soap.getProjectByKey(self.shared.auth, self.shared.control_account_subsystem)
             components = self.shared.soap.getComponents(self.shared.auth, str(project['key']))
             versions = self.shared.soap.getVersions(self.shared.auth, str(project['key']))
             component_list = []
             for row in components:
                 print str(row["name"].strip()) + ' ?= ' + str(self.shared.work_package_task_component)
                 if str(row["name"].strip()) == str(self.shared.work_package_task_component):
                     component_list.append(row["id"])
                     print self.shared.work_package_task_component + " MATCHED!!!!!!!!!!!!!!!!!!!!"
                     
             if component_list.count > 0:
                 self.shared.soap.updateIssue(self.shared.auth, newissue['key'], [{"id":"components", "values": component_list}])
        
             versions_list = []
             print "trying to match " + issue["task_affects_versions"]
             for row in versions:
                 my_versions_list = issue["task_affects_versions"].split(', ')
                 for my_ver in my_versions_list:
                     print "trying to match " + my_ver + " and " + row["name"].strip()
                     if row["name"].strip() == my_ver:
                         print "    Success"
                         versions_list.append(row["id"])
			 

			 
             if versions_list.count > 0:
                 self.shared.soap.updateIssue(self.shared.auth, newissue['key'], [{"id":"versions", "values":versions_list}])
             else:
                 print "It appears you didnt tell jira about the fix versions [" + str(issue["task_affects_versions"]) + "]"
		 
                 self.shared.soap.updateIssue(self.shared.auth, newissue['key'], [{"id":"fixVersions", "values":versions_list}])
		 
		 
             worklog = {'startDate': SOAPpy.dateTimeType(time.gmtime()[:6]), 'timeSpent':'1m', 'comment': 'Initial work estimate set'}
             self.shared.soap.addWorklogWithNewRemainingEstimate(self.shared.auth, newissue['key'], worklog, issue["task_work_estimate_days"] + "d")
        
        except Exception, e:
             print e
             outputWriter.writerow(columns)
             return False
    
        return True
        
    def should_i_parse(self, columns):
        if len(columns) > int(self.shared.settings['field_mappings.' + "Type"]) and columns[int(self.shared.settings['field_mappings.' + "Type"])].strip() == 'IT':
            return True
        return False

    def get_handler_name(self):
        return "IT"

foo = IT_parser()


