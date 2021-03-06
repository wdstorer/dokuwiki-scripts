#!/usr/bin/env python
import pyodbc
import subprocess
import os
import confighelper

confighelper.testConfig(['Settings','MSSQL','Dokuwiki'])
appSettings = confighelper.getConfigSettings('Settings')
dbSettings = confighelper.getConfigSettings('MSSQL')
dokuSettings = confighelper.getConfigSettings('Dokuwiki')

#CONFIGURATION VARIABLES
tmpTextFile = appSettings['tempfile']
mssqlHost = dbSettings['host']
mssqlDB = dbSettings['database']
mssqlPort = dbSettings['port']
mssqlUser = dbSettings['username']
mssqlPass = dbSettings['password']
dokuwikiCLI = dokuSettings['clipath'] 
dokuwikiNS = dokuSettings['ns']
dokuwikiMSG = dokuSettings['msg']

#CONNECT TO MSSQL DATABASE
dbConnectionString = "DRIVER={FreeTDS};SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s" % (mssqlHost, mssqlPort, mssqlDB, mssqlUser, mssqlPass)

cnxn = pyodbc.connect(dbConnectionString)
cursor = cnxn.cursor()

cursor.execute("select * from webapps")

#EVALUATE DATABASE RECORDS AND CREATE WIKI PAGES
for row in cursor:
  pagename=(row.server + row.name + str(row.siteid)).translate(None,'. ').lower()
  environment = row.environment.lower()

  #SETUP THE DOKUWIKI PAGE  
  with open(tmpTextFile, 'a') as text_file:
    text_file.write("====%s====\n" % row.name) 
    text_file.write("  * Server: %s\n" % row.server)
    text_file.write("  * Instance Name: <nowiki>%s</nowiki>\n" % row.name)
    text_file.write("  * Webroot: <nowiki>%s</nowiki>\n" % row.webroot)
    #text_file.write("  * Bindings: %s\n" % row.bindings)
    text_file.write("  * Application Pools: <nowiki>%s</nowiki>\n" % row.apppool)
    text_file.write("  * Site ID: %s\n" % row.siteid)
    text_file.write("  * State: %s <sub>(state last updated %s)</sub>\n" % ((row.state=="Started" and "<hi #22b14c>" or "<hi #ed1c24>") + row.state + "</hi>", row.datechanged))

    text_file.write("  * Bindings:\n")
    for binding in row.bindings.split('|'):
      if len(binding.split(':')) > 2:
        if binding.split(':')[2] != "":
          text_file.write("    * %s:%s %s\n" % (binding.split(':')[0],binding.split(':')[1],(binding.split(':')[1]=="443" and "https://" or "http://") + binding.split(':')[2]))
        else:
          text_file.write("    * %s\n" % binding)
      else:
        text_file.write("    * %s\n" % binding)

    text_file.close()
  
  #GENERATE PAGE WITH DOKUWIKI PHP CLI
  proc = "php"
  procArgs = "%s commit -m \"%s\" %s %s:%s:%s" % (dokuwikiCLI, dokuwikiMSG, tmpTextFile, dokuwikiNS, environment, pagename)
  procFull = "%s %s" % (proc, procArgs)
  #print procArgs
  #print procFull
  subprocess.call(procFull, shell=True)  
  os.remove('/tmp/dwtmppage.txt')
