import socket
import time
import sys
import os

def handleConn(conn, addr):
	print("Handling connection from "+str(addr))

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
	print("done")
	conn.close()



def main():
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


main()