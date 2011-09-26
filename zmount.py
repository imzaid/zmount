#!/usr/bin/python

##################################
# zmount.py
# 
# ABOUT:
#	zmount is a shell script written in python to 
#	make ease of connectivity to an SSH/SFTP server
#	in the terminal through the MacFuse connection
#	manager 
#
# PREREQUISITES:
#	- MacFuse
#	- SSHFS
#	- custom "list" file
#		ex: ([#] denotes line #)
#		[1]name:example1, port:27, user:user, ip:192.168.0.113, rdir:/var/www/, ldir:/mount/example, volname:example
#		[2]name:google,   port:,   user:gusr, ip:google.com,    rdir:/,         ldir:/mount/google,  volname:google
#		[3]name:apple,    port:73, user:appl, ip:apple.com,     rdir:,          ldir:/mount/apple,   volname:apple
#

from os import system as cmd
from sys import argv as args
import types

##################################
# Config
path = ''				# Insert Path to File here
fyle = 'list'			# Insert List File here
listFile = path+fyle	# Combine the two

def myException(x):
	print x
	raise SystemExit
##################################
# Basic Help Menu
def defHelp():
	myException(" No arguments provided - Usage %s <option>\n for a list of commands: %s -h"%(args[0],args[0]))
##################################
# Full Help Menu
def showHelp(l):
	#myException(" Couldn't find that one, Here's some help")
	helpHeader = "---------------------------------------------------"
	print helpHeader+"\nMacFuse-SSHFS Mounter Command line interface\n"+helpHeader
	print "\n  To connect to a specific server you must type:"
	print "\t%s <option>\n"%args[0]
	print "  Or to Disconnect from a specific server you must type:"
	print "\t%s -<option>\n"%args[0]
	print "  Where <option> is:"
	list = sortList(l)
	for i in list:
		print "\t%s"%i[0]
##################################
# Dictionary List into a Sorted Array
def sortList(l):
	listItems = l.items()
	returnItems = [ [v[0],v[1]] for v in listItems ]
	returnItems.sort()
	return returnItems

##################################
# Make a Dictionary of Items to Connect to, from the file given in the config above
# fileToList(listFile)
def fileToList(l):
	infile = open(l,"r")
	list = {}
	for line in infile.readlines():
		if line.find(",") != -1 and line[0] != "#":
			lineArray = line.split(",")
			listItem = ""
			for la in lineArray:
				cellName,cellValue = la.split(":")
				if cellName == "name":
					listItem = cellValue
					list[listItem] = {}
				else:
					list[listItem][cellName.strip()] = cellValue.strip("\n")
	return list

##################################
# Build a Connection/Mount String
# buildConnect(key,list)
def buildConnect(key,list):
	print "connecting to %s"%key
	ret = "sshfs "
	keys = ['port', 'user', 'ip', 'rdir', 'ldir', 'volname']
	keys_dict = {
		'port':		'-p%s ',
		'user':		'%s@',
		'ip':		'%s:',
		'rdir':		['%s ', ' '],
		'ldir':		'%s ',
		'volname':	'-o volname=%s'
	}
	for k in keys:
		if list.has_key(k):
			if list[k] != '':
				if isinstance(keys_dict[k], types.ListType):
					ret += keys_dict[k][0]%list[k]
				else:
					ret += keys_dict[k]%list[k]
			else:
				if isinstance(keys_dict[k], types.ListType):
					ret += keys_dict[k][1]
	print ret
	return ret

##################################
# Build a Disconnection/Unmount String
# buildDisconnect(key,mount)
def buildDisconnect(key, mount):
	print "disconnecting from %s"%key
	return "umount " + mount

##################################
# Get Disconnect/Connect String and Run Command
# mounter(key, list, disconnect)
def mounter(key,list,disconnect):
	if disconnect:
		run = buildDisconnect(key,list["ldir"])
	else:
		run = buildConnect(key,list)
	cmd(run)

##################################
# Main program
if __name__=="__main__":
	try: 	key = args[1]				# Is there an argument available?
	except:	defHelp()				#	if exception thrown, run Basic Help
	list = fileToList(listFile)			# get list/dict file
	disconnect = key[0] == "-"			# are we disconnecting?
	key = key.lstrip("-")				# strip the disconnect character from string
	if(list.has_key(key)):				# does the list have the key?
		mounter(key, list[key], disconnect)	#	yes -> mount/unmount it
	else:
		showHelp(list)				#	no  -> show list of keys


