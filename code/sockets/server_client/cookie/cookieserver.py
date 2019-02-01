import socket

host = ''
port = 12345

storedValue = "hi there"

def setupServer():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("socket created")

	try:
		s.bind((host, port))

	except socket.error as msg:
		print(msg)

	print("socket bind completed")
	return s


def setupConnection():
	s.listen(2)
	conn, address = s.accept()
	print("connected to:" + address[0] + ":"  + str(address[1]))
	return conn


def GET():
	reply = storedValue
	return reply

def REPEAT():
	reply = dataMessage
	return reply

def dataTransfer():
	while True:
		data = con.recv(1024)
		data = data.decode('utf-8')


		dataMessage = data.split('  ', 1)
		command = dataMessage[0]

		if command == 'GET':
			reply = GET()
		elif command == 'REPEAT':
			reply = REPEAT()
		elif command == 'EXIT':
			print("our client has left us")
			break
		elif command == 'KILL':
			PRINT("OUR SERVER IS SHUTTING DOWN")
			s.close()
			break
		else:
			reply = 'UNKNOWN COMMAND'

		conn.sendall(str.encode(reply))
		print("data has been sent")
	conn.close()


s = setupServer()

while True:
	try:
		conn = setupConnection()
		dataTransfer(conn)

	except:
		break

