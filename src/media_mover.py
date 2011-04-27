#!/usr/bin/python

"""media_mover.py
used to move media files around.
"""

__author__ = "Scott Truger (http://wwww.truger.net)"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2010/05 $"
__copyright__ = "Copyright (c) 2010 Scott Truger"
__license__ = "Python"

from shutil import copy2
import ConfigParser
import datetime
import fileinput
import os
import sys

class MediaMover:
    "moves media files from one dir to another"
  
    def __init__(self, debugOutput = False):
        self._debug = debugOutput
  
    def findFiles(self, fileType, searchPath):
        """finds files of the given type recursivly in the given path.
          Returns the path of the files found in an array.
          fileType is the extension of the file including '.', ex: '.avi'"""
        foundFiles = []
        for root, dirs, files in os.walk(searchPath):
    	for elem in files:
    	  if (os.path.splitext(elem)[1] == fileType):
    	    foundFiles.append(os.path.join(root, elem))
        return foundFiles
    
  def copyFiles(self, fileList, storePath, log, dateTime):
    """moves files in fileList to storePath.
      checks the log if file has been previously moved.
      processed files are logged in log."""
    if(self._debug): print "starting file copy"
    
    logFile = open(log, "r")
    l = logFile.read()
    logFile.close()
    
    f = open(log, "a")
    
    for item in fileList:
      index = l.find(item)
      if (index == -1):
	if (self._debug): print "copying file - " + item
	copy2(item, storePath)
	f.write(item + " - move - " + str(dateTime) + "\n")
      else:
	if (self._debug): print "found file - " + item
    f.close
    
  def unrarFiles(self, fileList, storePath, log, dateTime):
    """ calls the system unrar command for the archives in fileList.
      the files are stored in storePath.
      each processed archive is logged in log"""
    if (self._debug): print "starting rar processesing"
    
    logFile = open(log, "r")
    l = logFile.read()
    logFile.close()
    
    f = open(logFilePath, "a")
    
    for archive in fileList:
      index = l.find(archive)
      if (index == -1):
	if (self._debug): print "unrar file - " + archive
	
	command = "unrar e -y -inul %s %s" % (archive, storePath) 
	os.system(command)
	f.write(archive + " - unrar - " + str(dateTime) + "\n")
      else:
	if (self._debug): print "found archive - " + archive
    
    f.close
      
if __name__ == "__main__":
    debug = True 
    
    c = ConfigParser.ConfigParser()
    c.read('settings.cfg')
    
    searchPath = c.get('File Locations','searchPath')
    storePath = c.get('File Locations','storePath')
    logFilePath = c.get('File Locations','logFilePath')
    
    if (debug):
      print "config setttings"
      print searchPath
      print storePath
      print logFilePath
    
    curdate = datetime.datetime.now()
    
    m = MediaMover(debug)
    
    #file lists of files
    rarFiles = m.findFiles(".rar", searchPath)
    aviFiles = m.findFiles(".avi", searchPath)
    
    #unrar files
    m.unrarFiles(rarFiles, storePath, logFilePath, curdate)
    
    #copy avi files
    m.copyFiles(aviFiles, storePath, logFilePath, curdate)
    
    if (debug):
      f = open(logFilePath, "r")
      print "finished processing"
      print "_________ log _________"
      print f.read()
      print "_______________________"
      f.close()
  
  
