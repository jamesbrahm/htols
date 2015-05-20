import os
import sys


def windows():
	()

def linux():
	if(not os.path.isdir("/opt"):
		os.mkdir("/opt")
	if(not os.path.isdir("/opt/htols"):
		os.mkdir("/opt/htols")
	os.system("cp HTOLSclient.pyc /opt/htols")
	os.system("cp liblinux.pyc /opt/htols")
	os.system("cp 


def main():
	plat = sys.platform

	if platform.startswith("linux"):
		linux()
	elif platform.startswith("win"):
		windows()
	else:
		print("Unrecognized platform")
		sys.exit()

