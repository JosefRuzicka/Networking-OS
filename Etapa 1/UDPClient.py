# Adapted from https://www.binarytides.com/programming-udp-sockets-in-python/

'''
	udp socket client
'''

from FileManager import FileManager
import queue
import os.path  # for opening files
import socket	# for sockets
import sys		# for exit

def send_package(msg_to_send, sock, host, port):
	message_received = False
	while(not message_received):
		sock.sendto(msg_to_send, (host, port))
		try:
			d = s.recvfrom(1024)
			reply = d[0]
			addr  = d[1]
			message_received = True
		except socket.timeout:
			continue
		
		if(message_received and len(reply) == 4):
			message_received = False

	return reply, addr

# create dgram udp socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.settimeout(10)
except socket.error:
	print ('Failed to create socket')
	sys.exit()

host = '127.0.0.1'  # Standard loopback interface address (localhost)
port = 65432     # Port to listen on

fileManager = FileManager()

# Access to server
while(1) :
	# Ask user for user and password.
	print('ingrese su usuario o "1" para salir del sistema')
	user = str(input())
	if (user == '1'):
		print('Saliendo del sistema')
		sys.exit()
	print('Ingrese su contrasena')
	password = str(input())

	# build message.
	messageToBeSent = user + ',' + str(password)
	message_received = False

	# send credentials to server.
	s.sendto(str.encode(messageToBeSent), (host, port))

	# receive data from client (data, addr)
	
	try:
		d = s.recvfrom(1024)
		reply = d[0]
		addr  = d[1]
		message_received = True
	except socket.timeout:
		continue

	if(message_received):
			# if message was correctly received by server.
			# bytes.decode parses the bytes to string.
			print ('Server reply : ' + bytes.decode(reply))
			reply = bytes.decode(reply)

			# grant access to user or not.
			if (reply == 'Acceso otorgado'):
				break

# open file.
while(1) :
	print('Ingrese el nombre del archivo que utilizara o una opcion.')
	print('1) Crear un nuevo archivo.')
	print('2) Salir del sistema.')
	file = input()

	# 1) Create new file
	if (file == 1):
		print('Digite el nombre del nuevo archivo')
		file = input()
		fileManager.create_file(file)

	# 2) Close Client.
	elif (file == 2):
		print('Saliendo del sistema.')
		sys.exit()

	# if file exists, open it and show user menu.
	if (os.path.isfile(file)):
		userDataBase = fileManager.csv_enqueue_lines(file)
		break
	else:
		print ('El archivo no existe.')

# while data is being added.
while(1) :
	print('Digite el numero que correspone a la opcion que desea realizar.')
	print('1) Agregar datos al archivo.')
	print('2) Enviar datos al servidor.')
	print('3) Salir del sistema.')
	userInput = input()

	# 1 add data to file
	if (userInput == '1'): 
		print ('Ingrese la informacion de vacunacion (111111111,22,33,44)')
		userData = str(input())
		print (userData)
		fileManager.csv_write_file(file, userData)
		userDataBase.put(str(userData))

	# 2 Send file data to server
	elif (userInput == '2'):
		break

	# 3 Close client.
	elif (userInput == '3'):
		print('Saliendo del sistema')
		sys.exit()
	
	else :
		print('Seleccione una opcion valida (1-3).')


# while data is being sent and received to and from server.
sentMessagesCount = 0
messageSize = 18 # in bytes.
messagesToBeSent = (userDataBase.qsize())
packageSize = 10 # lines

while(sentMessagesCount < messagesToBeSent) :
	try :
		# Set the whole string
		# str.encode parses the string to bytes.
		# 117000951,01,02,03,0000,0026,0001,0000
		# disconect
		msgCounter = 0
		messageToBeSent = ''

		while( msgCounter < packageSize and not userDataBase.empty()):
			messageToBeSent += userDataBase.get()
			msgCounter += 1

		bytes_to_send = str.encode(messageToBeSent)
		bytes_to_send += sentMessagesCount.to_bytes(4,byteorder='big') + messagesToBeSent.to_bytes(4,byteorder='big') + messageSize.to_bytes(4,byteorder='big') + msgCounter.to_bytes(4,byteorder='big')
		
		reply, addr = send_package(bytes_to_send,s,host,port)

		# if message was correctly received by server.
		# bytes.decode parses the bytes to string.

		if(len(reply) == 16):
			receivedBytesStart = int.from_bytes(reply[:4], 'big')
			receivedBytesFinish = int.from_bytes(reply[4:8], 'big')
			bytesToBeReceived = int.from_bytes(reply[8:12], 'big')
			arrivedPackage = int.from_bytes(reply[12:16], 'big')

			if(receivedBytesFinish == msgCounter*messageSize):
				print(f"Successfully sent {sentMessagesCount+msgCounter} packs of {messagesToBeSent}")
				sentMessagesCount += msgCounter

		# close client once all messages have been sent.
		if (sentMessagesCount == messagesToBeSent):
			# send stop listening signal to close server.
			s.sendto(str.encode("disconnect"), (host, port))
			break
	
	except socket.error as msg:
		print ('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
		sys.exit()