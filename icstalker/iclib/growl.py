#!/usr/bin/python
#
# Script written by Legoktm, 2011
# Released into the Public Domain on November, 16, 2011
# This product comes with no warranty of any sort.
# Enjoy!
#
from commands import getoutput
def notify(string, program=False):
	if not program:
		command = 'growlnotify Python -m "%s"' %string
	else:
		command = 'growlnotify "%s" -m "%s"' %(program, string)
	getoutput(command)

def notifyold(string):
	#THIS IS THE OLD METHOD. YOU SHOULD ONLY USE THIS IF YOU DO NOT HAVE growlnotify INSTALLED.
	print"""]9;%s
""" %string
