#!/usr/bin/python

# Sample Python client accessing JIRA via SOAP. By default, accesses
# http://jira.atlassian.com with a public account. Methods requiring
# more than basic user-level access are commented out. Change the URL
# and project/issue details for local testing.
#
# Note: This Python client only works with JIRA 3.3.1 and above (see
# http://jira.atlassian.com/browse/JRA-7321)
#
# Refer to the SOAP Javadoc to see what calls are available:
# http://docs.atlassian.com/software/jira/docs/api/rpc-jira-plugin/latest/com/atlassian/jira/rpc/soap/JiraSoapService.html
#
# Initially taken from the jira site, but modified to test things out
# This script is a great place to play and try new things....

import SOAPpy, getpass, datetime
import time


soap = SOAPpy.WSDL.Proxy('https://YOUR.SITE.HERE/jira/rpc/soap/jirasoapservice-v2?wsdl')

jirauser = raw_input("Username for jira [fred]: ")
passwd = getpass.getpass("Password for %s: " % jirauser)

# This prints available methods, but the WSDL doesn't include argument
# names so its fairly useless. Refer to the Javadoc URL above instead
#print 'Available methods: ', soap.methods.keys()

def listSOAPmethods():
	for key in soap.methods.keys():
	    print key, ': '
	    for param in soap.methods[key].inparams:
		print '\t', param.name.ljust(10), param.type
	    for param in soap.methods[key].outparams:
		print '\tOut: ', param.name.ljust(10), param.type


auth = soap.login(jirauser, passwd)
#listSOAPmethods()

issue = soap.getIssue(auth, 'CIDEVCOI-184')
print "Retrieved issue:", str(issue)


#-----------------
# Try to add a version
#versionInfo = {'name' : 'test version',
               #'releaseDate' : SOAPpy.dateTimeType(2008, 12, 25, 0, 0, 0, 3, 360, -1)}
#soap.addVersion(auth, 'CIDEVCOI', versionInfo)
try:
	soap.addVersion(auth, "CIDEVCOI", {'name': 'Version 1'})
except: 
	print "already there"



#-----------------


print "------------------------------"
project = soap.getProjectByKey(auth, 'CIDEVTEST')
print str(project)
print "##############################"
print project['id']
foo = soap.getComponents(auth, str(project['key']))
print str(foo)
print str(foo[1]['id'])
print str(foo[1]['name'])

bar = soap.getVersions(auth, str(project['key']))
print "VERSIONS = " + str(bar)

print"\n"
print bar[0]["name"]
print bar[1]["name"]
print bar[2]["name"]
print bar[3]["name"]
print bar[4]["name"]

exit()
print "-----------------"
# Note: if anyone can get timestamps to work, please let us know how!

baseurl = soap.getServerInfo(auth)['baseUrl']
"""
KNOWN ISSUE THAT ORIGIONAL ESTIMATE IS NOT PRESENT...
https://jira.atlassian.com/browse/JRA-7624

"""
customFields = []
customFields.append({'values': ['RI-99999, RI-88888'], 'customfieldId': 'customfield_10013', 'key': None})
customFields.append({'values': ['http://www.oceanobservatories.org/test'], 'customfieldId': 'customfield_10010', 'key': None})
newissue = soap.createIssue(auth, {'project': 'CIDEVTEST', 'type': '3',
				   'customFieldValues': customFields,
				'summary': 'Issue created with Python!', 'assignee': 'unwin', 'priority': '1', 'duedate': SOAPpy.dateTimeType(time.gmtime(1)[:6])})
print str(newissue)
print "Created %s/browse/%s" % (baseurl, newissue['key'])



#exit()



print "\n\n\ntrying to log work\n\n\n"

dt_today = SOAPpy.dateTimeType(time.gmtime(int("1"))[:6])
comment = 'testing'
worklog = {'startDate':dt_today, 'timeSpent':'1m', 'comment': comment}




"""
ddWorklogAndAutoAdjustRemainingEstimate : 
	in0        (u'http://www.w3.org/2001/XMLSchema', u'string')
	in1        (u'http://www.w3.org/2001/XMLSchema', u'string')
	in2        (u'http://beans.soap.rpc.jira.atlassian.com', u'RemoteWorklog')
	Out:  addWorklogAndAutoAdjustRemainingEstimateReturn (u'http://beans.soap.rpc.jira.atlassian.com', u'RemoteWorklog')
"""
#WORKS# soap.addWorklogAndAutoAdjustRemainingEstimate(auth, newissue['key'], worklog)

"""
updateWorklogWithNewRemainingEstimate : 
	in0        (u'http://www.w3.org/2001/XMLSchema', u'string')
	in1        (u'http://beans.soap.rpc.jira.atlassian.com', u'RemoteWorklog')
	in2        (u'http://www.w3.org/2001/XMLSchema', u'string')
"""
work_log = soap.getWorklogs(auth, newissue['key'])
print str(work_log)
#soap.updateWorklogWithNewRemainingEstimate(auth, [work_log], '55d')
soap.addWorklogWithNewRemainingEstimate(auth, newissue['key'], worklog, "1w")

print "\n\n\ndone trying to log work\n\n\n"








#print "\n\ntrying to set the remaining estimate\n"

#work_log = soap.getWorklogs(auth, newissue['key'])

#result = soap.addWorklogAndAutoAdjustRemainingEstimate(auth, newissue['key'], worklog, '1h')
print "\nafter trying to set the remaining estimate\n\n"



"""
PERL

SOAP::Data->type(
		RemoteWorklog => {
			startDate => $time, # like '2010-02-05T14:30:00Z'
			timeSpent => $hours, # like '2h30m'
			comment => $desc
		},
	)
	

"""




print "Adding comment.."
soap.addComment(auth, newissue['key'], {'body': 'Comment added with SOAP'})

print 'Updating issue..'
soap.updateIssue(auth, newissue['key'], [
		{"id": "summary", "values": ['[Updated] Issue created with Python'] },

		# Change issue type to 'New feature'
		{"id":"issuetype", "values":'2'},

		# Setting a custom field. The id (10010) is discoverable from
		# the database or URLs in the admin section

		{"id": "Risk Item", "values": ["RI-99999"] },

		{"id":"fixVersions", "values":['-1']}, #   WHAT SHOULD THE FIX VERSION BE?
		# Demonstrate setting a cascading selectlist:
		{"id": "customfield_10061", "values": ["10098"]},
		{"id": "customfield_10061_1", "values": ["10105"]},
		{"id": "duedate", "values": ["15/Nov/10"]}
# datetime.date.today().strftime("%d-%b-%y")}

		])

print 'Resolving issue..'
# Note: all fields prompted for in the transition (eg. assignee) need to
# be set, or they will become blank.
soap.progressWorkflowAction(auth, newissue['key'], '2', [
		{"id": "assignee", "values": "unwin" },
		{"id":"fixVersions", "values":['-1']},
		{"id": "resolution", "values": "2" }
		])


# Re. 'assignee' above, see http://jira.atlassian.com/browse/JRA-9018

# This works if you have the right permissions
#user = soap.createUser(auth, "testuser2", "testuser2", "SOAP-created user", "newuser@localhost")
#print "Created user ", user

#group = soap.getGroup(auth, "jira-developers")
# Adding a user to a group. Naming the parameters may be required (see
# http://jira.atlassian.com/browse/JRA-7971). You may experience other
# problems (see http://jira.atlassian.com/browse/JRA-7920).
#soap.addUserToGroup(token=auth, group=group, user=user)

# Adding a version to a project. If you figure out the syntax for the date please submit it back to Atlassian
#soap.addVersion(auth, "TST", {'name': 'Version 1'})


print "Done!"
