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
	cmd = 'net user'
	output = runCMD(cmd).split()[5:-4]
	if(user in output):
		return [points, "User "+user+" exists"]
	else:
		return [0, ""]

def USER_NOT_EXIST(args):
	user = args[1]
	points = args[2]
	cmd = 'net user'
	output = runCMD(cmd).split()[5:-4]
	if(user not in output):
		return [points, "User "+user+" does not exist"]
	else:
		return [0, ""]

def USER_IN_GROUP(args):
	user = args[1]
	group = args[2]
	points = args[3]
	cmd = 'net localgroup "'+group+'"'
	output = runCMD(cmd)
	outputlines = output.split("\n")
	linenum = outputlines.index('Members\r')
	usersingroup = [x.strip() for x in outputlines[linenum+3:-1]]
	if(user in usersingroup):
		return[points, "User "+user+" is in the "+group+" group"]
	else:
		return [0, ""]

def USER_NOT_IN_GROUP(args):
	user = args[1]
	group = args[2]
	points = args[3]
	cmd = 'net localgroup "'+group+'"'
	output = runCMD(cmd)
	outputlines = output.split("\n")
	linenum = outputlines.index('Members\r')
	usersingroup = [x.strip() for x in outputlines[linenum+3:-1]]
	if(user not in usersingroup):
		return[points, "User "+user+" is not in the "+group+" group"]
	else:
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

def SECURITY_SETTING_IS(args):
	setting = args[1]
	value = args[2]
	message = args[3]
	points = args[4]

	cmd = "secedit /export /cfg secedit.conf"
	runCMD(cmd)
	f = open(secedit.conf, "r")
	exported = f.readlines()
	theline = ""
	for line in exported:
		if(setting in line):
			theline = line
			break
	actualsetting = theline.split("=")[1].strip()
	if(setting[0] == "<"):
		if(actualsetting < setting[1:]):
			return [points, message]
	elif(setting[0] == ">"):
		if(actualsetting > setting[1:]):
			return [points, message]
	elif(setting == actualsetting):
		return [points, message]
	else:
		()
	return [0, ""]


def SECURITY_SETTING_NOT(args):
	message = args[3]
	points = args[4]
	returnstuff = SECURITY_SETTING_IS(args)
	if(returnstuff[1] == ""):
		return [points, message]

# Utility functions

def pushNotification(message):
	()

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