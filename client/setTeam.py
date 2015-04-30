#!/usr/bin/env python3
import sys
import time

startTime = str(int(time.time()))

quit = 0
while quit == 0:
	teamName = input("Enter your team name EXACTLY: ")
	ans = input('Is your team name "'+teamName+'"? [y/n]')
	if(ans.lower() == "y"):
		quit = 1

if(sys.platform.startswith("win")):
	f = open("teamID", "w")
	f.write(startTime)
	f.write("\n")
	f.write(teamName)
	f.write("\n")
elif(sys.platform.startswith("linux")):
	f = open("teamID", "w")
	f.write(startTime)
	f.write("\n")
	f.write(teamName)
	f.write("\n")

else:
	()