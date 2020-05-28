import MySQLdb
import csv
import json
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET 
import re
import sshtunnel

ENDL = '\n'
TAB = '\t'

dbCredentialsDirectory = 'settings\\'

ignoreCaseReplaceSpanStart = re.compile('<span class="field-item">', re.IGNORECASE)
ignoreCaseReplaceSpanEnd = re.compile("</span>", re.IGNORECASE)

def getDBConnectionInformation(databaseInfoAlias):
   dbConnectionInformation = []
   
   credentialsFileHandle = open(dbCredentialsDirectory + databaseInfoAlias + ".json", mode='r')
   credentialsDataJSON = json.loads(credentialsFileHandle.read())
   credentialsFileHandle.close()
   
   dbConnectionInformation[0] = credentialsDataJSON.get("hostname")
   dbConnectionInformation[1] = credentialsDataJSON.get("port")
   dbConnectionInformation[2] = credentialsDataJSON.get("database")
   dbConnectionInformation[3] = credentialsDataJSON.get("user")
   dbConnectionInformation[4] = credentialsDataJSON.get("password")

   return dbConnectionInformation

def saveDBConnectionInformation(databaseInfoAlias, dbConnectionInformation):
   credentials = {}
   credentials["hostname"] = dbConnectionInformation[0]
   credentials["port"] = dbConnectionInformation[1]
   credentials["database"] = dbConnectionInformation[2]
   credentials["user"] = dbConnectionInformation[3]
   credentials["password"] = dbConnectionInformation[4]
   credentialsDataJSON = json.dumps(credentials, sort_keys=False, indent=3)
   
   credentialsFileHandle = open(dbCredentialsDirectory + databaseInfoAlias + ".json", mode='w+')
   credentialsFileHandle.write(credentialsDataJSON)
   credentialsFileHandle.close()

def connectToMySQL(dbConnectionInformation):
   dbHost = dbConnectionInformation[0]
   dbPort = dbConnectionInformation[1]
   dbDatabase = dbConnectionInformation[2]
   dbUser = dbConnectionInformation[3]
   dbPassword = dbConnectionInformation[4]
    
   conn = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPassword, database=dbDatabase, port=dbPort)
    
   return conn

databaseInfoAlias = "database_alias_and_filename"
saveDBConnectionInformation(databaseInfoAlias, dbConnectionInformation)
dbConnectionInformation = getDBConnectionInformation(databaseInfoAlias)
