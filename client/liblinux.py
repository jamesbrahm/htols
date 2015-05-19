import subprocess
import os
import crypt

def CMD(args):
	print(args)
	returnObj = [1, "score error"]
	return returnObj

def TEST1():
	var = "morgan"

def TEST2():
	print(var)

def USER_PASSWORD_NOT(args):
	user = args[1]
	password = args[2]
	points = args[3]
	cmd = '''awk -F: '($1 == "'''+user+'''") {print}' /etc/shadow '''
	shadowLine = runCMD(cmd)
	salt = shadowLine.split(":")[1].split("$")[2]
	shadowhash = shadowLine.split(":")[1]
	testhash = crypt.crypt(password, "$6$"+salt)
	if(testhash != shadowhash):
		return[points, "User "+user+" has a new password"]
	return [0, ""]

def USER_PASSWORD_IS(args):
	user = args[1]
	password = args[2]
	points = args[3]
	cmd = '''awk -F: '($1 == "'''+user+'''") {print}' /etc/shadow '''
	shadowLine = runCMD(cmd)
	salt = shadowLine.split(":")[1].split("$")[2]
	shadowhash = shadowLine.split(":")[1]
	testhash = crypt.crypt(password, "$6$"+salt)
	if(testhash == shadowhash):
		return[points, "User "+user+" has the correct password"]
	return [0, ""]
 

def USER_LOCKED(args):
	user = args[1]
	points = args[2]

	cmd = "passwd -S "+user
	out = runCMD(cmd)
	status = out.split()[1]
	if "L" in status:
		return [points, "User "+user+" locked"]
	return [0, ""]
	
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

def SOFTWARE_INSTALLED(args):
	package = args[1]
	points = args[2]
	softwareInstalled = runCMD("dpkg --get-selections | grep -v deinstall")
	for item in softwareInstalled:
		if (item.split()[0] == package):
			return [points, "Package "+package+" is installed"]
	return [0, ""]

def SOFTWARE_NOT_INSTALLED(args):
	package = args[1]
	points = args[2]
	softwareInstalled = runCMD("dpkg --get-selections | grep -v deinstall")
	softwareInstalled = softwareInstalled.split("\n")
	for item in softwareInstalled:
		if (item.split()[0] == package):
			return [0, ""]
	return [points, "Package "+package+" is has been removed"]

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


# Security Policies
def SECURITY_POLICY(args):
	()

# helper functions
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


# Other functions

def pushNotification(message):
	message = message.strip()
	cmd = 'notify-send "'+message+'"'
	os.system(cmd)