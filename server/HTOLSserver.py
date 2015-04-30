import socket
import time
import sys
import os
import multiprocessing
import xml.etree.ElementTree

def handleConn(conn, addr):

	conn.send(b'What is your name?')
	teamName = conn.recv(1024).decode("utf-8")

	conn.send(b'What is your quest?')
	imageName = conn.recv(1024).decode("utf-8")

	conn.send(b'What is your favorite color?')
	if(conn.recv(1024) != b'Blue'):
		conn.close()
		return 1

	timeString = time.strftime("%Y-%m-%d--%H-%M-%S")
	path = teamName+"/"+imageName+"/"
	if(not os.path.exists(path)):
		os.makedirs(path)
	scoreReport = open(path+timeString+".html", "wb")


	buff = conn.recv(1024)
	while buff:
		scoreReport.write(buff)
		buff = conn.recv(1024)
	scoreReport.close()

	scoreReport = open(path+timeString+".html", "r")
	score = scoreReport.readlines()[-1][4:-3]
	scoreReport.close()

	print(teamName, imageName, "{"+str(addr[0])+"} =",score,"at "+time.strftime("%H:%M:%S"))

	conn.close()

def startListen():
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(("127.0.0.1",9999))
		sock.listen(1)

		while True:
			conn, addr = sock.accept()
			handleConn(conn, addr)

			conn.close()
	except:
		print("there was a problem")
		print(sys.exc_info())
		sock.close()


def probeTeam(team):
	for server in team.findall("server"):
		


def probe(host):
	return "blah"


def stripComments(flines):
	lines = []
	for item in flines:
		if("#" in item):
			uncommented = item[:item.index("#")] 
			if(uncommented.strip() != ""):
				lines.append(uncommented)
		else:
			if(item.strip() != ""):
				lines.append(item)
	return lines


def main():
	f = open("htols.conf")
	conf = stripComments(f.readlines())
	f.close()

	listen = 0
	probeInterval = 60
	pointsPer = 2

	xmlTree = xml.etree.ElementTree.parse("config.xml")
	root = xmlTree.getroot()

	if(root.find("settings").find("listen").text.strip() == "1"):
		listener = multiprocessing.Process(target=startListen)
		listener.start()

	probeInterval = int(root.find("settings").find("probeInterval").text.strip()) 
	if(probeInterval > 0):
		while True:
			print(probeInterval)
			print("probing")
			for team in root.findall("team"):
				probeTeam(team)
			time.sleep(probeInterval)






main()
