#!/usr/bin/python

"""
@file JiraIssueMigrator/main.py
@author Roger Unwin
@brief the main file for the issue migrator program.
"""

from read_config import read_file
import sys
import csv

from x import importer

def main():
    """
    """
    settings = read_file("config.file")

    
    for k in sys.argv:
        key_val = k.lstrip('-').split('=')
        if len(key_val) > 1:
            settings['jira.' + key_val[0]] = key_val[1]
            #print "OVERRIDING CONFIGFILE - " + key_val[0] + '=' + key_val[1] + ""
        #print k
        if k == '--help':
            print   '--help : Prints this message\n' + \
                    '--url=[jira_url]  Sets the base url for accessing jira\n' + \
                    '--username=[username]  Sets the username to use\n' + \
                    '--password=[password]  Sets the password to use\n' + \
                    '--csv_file_name=[csv file name]  Sets the name of the CSV file to read\n' + \
                    '--reporter=[who is assigning the tasks]  Sets who is reporting the issues\n' + \
                    '--separator=[the character or string seperating fields in the csv file]  Sets the character(s) that are used as seperators in the input file\n' + \
                    '--quote_char=[the character used as a quote character]  Sets the character used as a quote character\n'
            exit()
    
    outputWriter = csv.writer(open('results-' + settings['jira.csv_file_name'], 'wb'), delimiter=settings["jira.separator"], quotechar=settings["jira.quote_char"], quoting=csv.QUOTE_MINIMAL)
    discovered_parsers = importer.get_parsers(settings, outputWriter)
    
    print "OPENING " + settings['jira.csv_file_name']
    file = open(settings['jira.csv_file_name'])
    
    csvReader = csv.reader(open(settings['jira.csv_file_name'], 'rb'), delimiter=settings["jira.separator"], quotechar=settings["jira.quote_char"])
    
    rejectWriter = csv.writer(open('reject-' + settings['jira.csv_file_name'], 'wb'), delimiter=settings["jira.separator"], quotechar=settings["jira.quote_char"], quoting=csv.QUOTE_MINIMAL)
    
    count = 0
    for tokens in csvReader:
        handled = False
        print str(tokens)
        for par in discovered_parsers:
            #print "PARSER = " + par.get_handler_name()
            if par.should_i_parse(tokens):
		#print "parsing with " + par.get_handler_name()
                if par.parse(tokens):
                    handled = True
                else:
                    if par.get_handler_name() == 'IT':
                        print par.get_handler_name() + " handler FAILED " 
                    
        if not handled:
            """
            """
            rejectWriter.writerow(tokens)
            if par.get_handler_name() == 'IT':
                print "LINE NOT HANDLED : " + str(tokens)

main()
