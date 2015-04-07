import subprocess
import os

def CMD(args):
	print(args)
	returnObj = [1, "score error"]
	return returnObj

def USER_PASSWORD_NOT(args):
	()

def USER_PASSWORD_IS(args):
	()

def USER_LOCKED(args):
	()
	
def USER_EXIST(args):
	user = args[1]
	points = args[2]
	out = runCMD("id -u "+user)
	if "no such user" in out:
		return [0, ""]
	return [points, "User "+user+" exists"]


def USER_NOT_EXIST(args):
	user = args[1]
	points = args[2]
	out = runCMD("id -u "+user)
	if "no such user" in out:
		return [points, "User "+user+" has been removed"]
	return [0, ""]

def USER_IN_GROUP(args):
	user = args[1]
	group = args[2]
	points = args[3]

	cmd = '''grep '^'''+group+'''' /etc/group | cut -d: -f4 '''
	membersList = runCMD(cmd)
	members = membersList.split(",")
	if user in members:
		return [points, user+" added to "+group+" group"]
	return [0, ""]

def USER_NOT_IN_GROUP(args):
	user = args[1]
	group = args[2]
	points = args[3]

	cmd = '''grep '^'''+group+'''' /etc/group | cut -d: -f4 '''
	membersList = runCMD(cmd)
	members = membersList.split(",")
	if user not in members:
		return [points, user+" removed from "+group+" group"]
	return [0, ""]

def MAX_PASS_AGE(args):
	value = args[1]
	points = args[2]
	f = open("/etc/login.defs", "r")
	flines = f.readlines()
	lines = stripComments(flines)
	relLines = []
	for item in lines:
		if "PASS_MAX_DAYS" in item:
			relLines.append(item)
	days = relLines[-1].split()[1]
	if(days <= value):
		return [points, "The maximum password age is "+str(value)+" days or less"]
	return [0, ""]

def SOFTWARE_INSTALLED(args):
	()

def SOFTWARE_NOT_INSTALLED(args):
	()

def SOFTWARE_NEWER(args):
	()

def LINE_EXIST(args):
	line = args[1]
	filename = args[2]
	message = args[3]
	points = args[4]
	f = open(filename, "r")
	flines = f.readlines()
	lines = stripComments(flines)
	for item in lines:
		if line in item:
			return [points, message]
	return [0, ""]

def LINE_NOT_EXIST(args):
	line = args[1]
	filename = args[2]
	message = args[3]
	points = args[4]
	f = open(filename, "r")
	flines = f.readlines()
	lines = stripComments(flines)
	found = 0
	for item in lines:
		if line in item:
			found +=1
	if(found == 0):
		return [points, message]
	return [0, ""]

def FILE_EXIST(args):
	filename = args[1]
	points = args[2]
	if(os.path.isfile(filename)):
		return [points, "File "+filename+" exists"]
	else:
		return [0, ""]

def FILE_NOT_EXIST(args):
	filename = args[1]
	points = args[2]
	if(not os.path.isfile(filename)):
		return [points, "File "+filename+" has been removed"]
	else:
		return [0, ""]

# Utility functions
def stripComments(flines):
	lines = []
	for item in flines:
		if("#" in item):
			lines.append(item[:item.index("#")])
		else:
			lines.append(item)
	return lines

def runCMD(cmd):
	out = subprocess.check_output(cmd, shell=True)
	text = out.decode("utf-8").strip()
	return text