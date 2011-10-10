
"""
@file JiraIssueMigrator/importer.py
@author Roger Unwin
@brief this file inventories and returns an array of line parsers
"""

from x import parsers

from zope import interface
from twisted import plugin
import SOAPpy

class IParser(interface.Interface):
    
    def parse(self, columns):
        """
        all classes implementing IParser privide a method parse with
        @param columns
        """
    
    def should_i_parse(self, columns):
        """
        """
        
    def get_handler_name(self):
        """
        """
        
        
class Parser(object):
    interface.implements(plugin.IPlugin, IParser)

    def parse(self, columns):
        pass
    
    def should_i_parse(self, columns):
        pass
    
    def get_handler_name(self):
        pass

class Shared():
    pass
    
def get_parsers(settings, outputWriter):
    ps = plugin.getPlugins(IParser, package=parsers)
    
    discovered_parsers = []
    shared = Shared()
    shared.settings = settings
    shared.outputWriter = outputWriter # pass in the output writer to handle the output CSV file with jira links
    ### Should really initialize the soap elsewhere, but this is just too convienent.
    print settings['jira.url'] + '/rpc/soap/jirasoapservice-v2?wsdl'
    shared.soap = SOAPpy.WSDL.Proxy(settings['jira.url'] + '/rpc/soap/jirasoapservice-v2?wsdl')

    shared.auth = shared.soap.login(settings['jira.username'], settings['jira.password'])
    for p in ps:
        p.shared = shared
        
        print "DISCOVERED " + p.get_handler_name() + " PARSER"
        discovered_parsers.append(p)
    return(discovered_parsers)
    
