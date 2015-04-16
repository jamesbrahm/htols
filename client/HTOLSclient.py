# Imports
import subprocess
import codecs
import argparse
import sys
import datetime
import time
import socket
import os

# Conditional imports
platform = sys.platform
if platform.startswith("linux"):
	import liblinux as score
elif platform.startswith("win"):
	import libwindows as score
else:
	print("Unrecognized platform")

def argstuff():
	parser = argparse.ArgumentParser()
	parser.add_argument("TARGET")
	global args
	args = parser.parse_args()

# Obfuscation
def dec(line):
	reversed = line[::-1]
	decoded = codecs.decode(reversed, "hex").decode("utf-8")
	return decoded

def scoreVuln(vuln):  # The master scoring function
	global pointGainLines
	global pointLossLines
	global totalScore
	global totalVDL
	unstrippedArgs = vuln.split(";")
	args = []
	for arg in unstrippedArgs:
		args.append(arg.strip())
	if(int(args[-1]) > 0):
		totalVDL += 1

	returnObj = [0, "score error"]
	# Sample 
	if(args[0] == "CMD"):
		returnObj = score.CMD(args)
	
	# User stuff
	elif(args[0] == "USER_PASSWORD_NOT"):
		returnObj = score.USER_PASSWORD_NOT(args)
	elif(args[0] == "USER_PASSWORD_IS"):
		returnObj = score.USER_PASSWORD_IS(args)
	elif(args[0] == "USER_LOCKED"):
		returnObj = score.USER_LOCKED(args)
	elif(args[0] == "USER_EXIST"):
		returnObj = score.USER_EXIST(args)
	elif(args[0] == "USER_NOT_EXIST"):
		returnObj = score.USER_NOT_EXIST(args)
	elif(args[0] == "USER_IN_GROUP"):
		returnObj = score.USER_IN_GROUP(args)
	elif(args[0] == "USER_NOT_IN_GROUP"):
		returnObj = score.USER_NOT_IN_GROUP(args)

	# Password Policy
	elif(args[0] == "MAX_PASS_AGE"):
		returnObj = score.MAX_PASS_AGE(args)

	# Software
	elif(args[0] == "SOFTWARE_INSTALLED"):
		returnObj = score.SOFTWARE_INSTALLED(args)
	elif(args[0] == "SOFTWARE_NOT_INSTALLED"):
		returnObj = score.SOFTWARE_NOT_INSTALLED(args)
	elif(args[0] == "SOFTWARE_NEWER"):
		returnObj = score.SOFTWARE_NEWER(args)

	# File Operations
	elif(args[0] == "LINE_EXIST"):
		returnObj = score.LINE_EXIST(args)
	elif(args[0] == "LINE_NOT_EXIST"):
		returnObj = score.LINE_NOT_EXIST(args)
	elif(args[0] == "FILE_CONTAIN"):
		returnObj = score.CMD(args)
	elif(args[0] == "FILE_NOT_CONTAIN"):
		returnObj = score.CMD(args)
	elif(args[0] == "FILE_EXIST"):
		returnObj = score.FILE_EXIST(args)
	elif(args[0] == "FILE_NOT_EXIST"):
		returnObj = score.FILE_NOT_EXIST(args)

	# Extra
	elif(args[0] == "CMD"):
		returnObj = score.CMD(args)
	else:
		returnObj = [1, "VDL not recognized"]		

	returnObj[0] = int(returnObj[0])
	totalScore += returnObj[0]

	if(returnObj[0] > 0):
		pointGainLines.append(str(returnObj[0]) + ": "+returnObj[1])
	elif(returnObj[0] < 0):
		pointLossLines.append(returnObj[1])
	else:
		() # No match




# Score Report stuff
def genReport():
	global pointGainLines
	global pointLossLines
	global totalScore
	global totalVDL
	global teamName
	global startTime

	# Time
	secdiff = int(time.time()) - startTime
	timediff = str(datetime.timedelta(seconds=secdiff))

	reportlines = []
	reportlines.append("<html> <header> <title> HTOLS Scoring Report </title </header>")
	reportlines.append('<body bgcolor=black text=#00FF00>')
	reportlines.append('<style> body{font-family:monospace}</style>')
	reportlines.append("<center> <h1> HTOLS Scoring Report </h1>")
	reportlines.append("<h2> Team "+teamName+" </h2>")
	reportlines.append("<p> Generated at: "+str(datetime.datetime.now())+"</p>")
	reportlines.append("<p> Running time: "+timediff+"</p>")
	reportlines.append("<h3> Score: "+str(totalScore)+"</h3> </center> <br>")
	reportlines.append("<br> <h3> "+str(len(pointGainLines))+" out of "+str(totalVDL)+" issues fixed</h3>")
	for item in pointGainLines:
		reportlines.append(item + " <br>")

	if(len(pointLossLines) == 1):
		reportlines.append("<h3> "+str(len(pointLossLines))+" penalty assessed</h3>")
	else:
		reportlines.append("<h3> "+str(len(pointLossLines))+" penalties assessed</h3>")

	for item in pointLossLines:
		reportlines.append(item + " <br>")

	reportlines.append("</body> </html>")
	reportlines.append("\n<!--"+str(totalScore)+"-->")


	reportFile = open("ScoreReport.html", "w")
	for line in reportlines:
		reportFile.write(line)
	reportFile.close()

	# Notify
	if(totalScore > oldScore):
		score.pushNotification("You have gained points!  Score: "+str(totalScore))
	if(totalScore < oldScore):
		score.pushNotification("You have lost points.  Score: "+str(totalScore))

	result = sendRemoteReport()

def sendRemoteReport():
	global teamName
	global imageName
	global args
	if(args.TARGET == "local"):
		return 0



	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((args.TARGET, 9999))

	# Handshake
	print(sock.recv(1024))
	sock.send(bytes(teamName, "utf-8"))
	print(sock.recv(1024))
	sock.send(bytes(imageName, "utf-8"))
	print(sock.recv(1024))
	sock.send(b'Blue')

	scoreReport = open("ScoreReport.html", "rb")
	buff = scoreReport.read(1024)

	while buff:
		sock.send(buff)
		buff = scoreReport.read(1024)
	scoreReport.close()
	print("done")
	sock.close()



# Misc

def getScoringData():
	global imageName

	files = os.listdir(".")
	for f in files:
		if(f.endswith(".dat")):
			filename = f
			break

	imageName = filename[:-4]

	vdlFile = open(filename, "r")
	enclines = vdlFile.readlines()
	vdlLines = []
	for line in enclines:
		line = line.rstrip()
		vdlLines.append(dec(line))

	# DEBUG CODE GOES HERE #
	# NOT FOR PRODUCTION USE #
	vdlLines.append("LINE_EXIST; dog; /bears; dog bear; 4")
	vdlLines.append("LINE_NOT_EXIST; dog; /bears; no dog bear; 4")
	vdlLines.append("MAX_PASS_AGE; 99999999; 7")
	vdlLines.append("USER_IN_GROUP; jbrahm; adm; 9")
	vdlLines.append("USER_NOT_IN_GROUP; mwagner; adm; 4")
	vdlLines.append("USER_EXIST; jbrahm; 5")

	# END DEBUG CODE #

	return vdlLines

def main():
	argstuff()
	vdlLines = getScoringData()
	global pointGainLines
	pointGainLines = []
	global pointLossLines
	pointLossLines = []
	global totalScore
	totalScore = 0
	global oldScore
	f = open("ScoreReport.html")
	scoreLine = f.readlines()[-1]
	f.close()
	score = scoreLine[4:]
	oldScore = int(score[:-3])


	global totalVDL
	totalVDL = 0

	global teamName
	global startTime
	f = open("teamID", "r")
	flines = f.readlines()
	startTime = int(flines[0].strip())
	teamName = flines[1].strip()

	for line in vdlLines:
		scoreVuln(line)

	genReport()

	
if __name__ == '__main__':
	main()