#!/usr/bin/env python

#SOME CONFIG SPECIFIC FUNCTIONS

from ConfigParser import SafeConfigParser
import io

configFile = "config.ini"

def testConfig(sectionList):
  parser=SafeConfigParser()
  parser.read(configFile)

  #TEST THAT CONFIG FILE EXISTS
  found = parser.read(configFile)
  if len(found) == 0:
    print "Config file [%s] not found" % configFile
    exit()

  #TEST THAT REQUIRED SECTIONS EXIST
  for section in sectionList:
    if parser.has_section(section) == False:
      print "Missing section %s" % section
      exit()

def getConfigSettings(strSection):
  parser=SafeConfigParser()
  parser.read(configFile)
  return dict(parser.items(strSection))

def outputConfig():
  #OUTPUT ALL VALUES
  parser = SafeConfigParser()
  parser.read(configFile)

  print "*********************************"
  print "Config file found"
  print "*********************************"
  print
  print "Values:"
  print
  for section in parser.sections():
    print 'Section:', section
    #print '  Options:', parser.options(section)
    for name, value in parser.items(section):
      print '  %s = %s' % (name, value)

  print

#testConfig()
#outputConfig()

#dbSettings = getConfigSettings('MSSQL')
#dokuSettings = getConfigSettings('Dokuwiki')

#print dbSettings
#print dokuSettings

#print parser.get('Dokuwiki','CLIPath')
#print parser.get('Dokuwiki','MSG')

