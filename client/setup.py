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
	os.system("cp setTeam.py /opt/setTeam.py")

	if(os.path.isfile("/var/spool/cron/crontabs/root"):
		f = open("/var/spool/cron/crontabs/root"):
	


def main():
	plat = sys.platform

	if platform.startswith("linux"):
		linux()
	elif platform.startswith("win"):
		windows()
	else:
		print("Unrecognized platform")
		sys.exit()

