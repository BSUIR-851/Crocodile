from utils import *

import socket
import datetime
import threading
import sys

#SERVER DATA
host = ''
port = 49100
addr = (host, port)
clients = {}

#CREATE LOGGER
logger = createLogger("server")

def deleteSelf(strAddress):
	del clients[strAddress]
	sys.exit()

def deleteClient(strAddress):
	t = clients[strAddress][1]
	del clients[strAddress]
	t.join(1)

def sendCoords(binData, dataJSON, client_address, connAndThread):
	global clients 

	connection = connAndThread[0]

	try:
		connection.sendall(binData)
		msg = '[{}] send to {}: {}'.format(datetime.datetime.now().time(), client_address, dataJSON['data'])
		logger.debug(msg)

	except (OSError, socket.timeout, TimeoutError, ConnectionRefusedError, BrokenPipeError) as e:
		deleteClient(client_address)
		msg = '[{}] {} disconnected'.format(datetime.datetime.now().time(), client_address)
		logger.info(msg)

	except Exception as e:
		msg = '[{}] something gone wrong: {}'.format(datetime.datetime.now().time(), e)
		logger.error(msg)

	print(msg)


def sendCoordsToClients(binData, dataJSON, address):

	for client_address, connAndThread in lients.items():
		if client_address != address:
			sendCoords(binData, dataJSON, client_address, connAndThread)


def startRecvRequests(connection, address):
	msg = '[{}] connected by {}'.format(datetime.datetime.now().time(), address)
	logger.info(msg)
	print(msg)

	while True:
		try:
			binData = read(connection)
			if binData:
				dataJSON = getJson(binData)
				if dataJSON['success']:
					if dataJSON['request'] == 'check':
						binData = getBinaryJson(dataJSON)
						connection.sendall(binData)
						msg = '[{}] {} to {} confirmed'.format(datetime.datetime.now().time(), dataJSON['request'], address)
						logger.debug(msg)
						print(msg)

					elif dataJSON['request'] == 'send':
						binData = getBinaryJson(dataJSON)
						msg = '[{}] from {}: {}'.format(datetime.datetime.now().time(), address, dataJSON['data'])
						logger.debug(msg)
						print(msg)
						sendCoordsToClients(binData, dataJSON, address)

			else:
				msg = '[{}] {} disconnected'.format(datetime.datetime.now().time(), address)
				logger.info(msg)
				connection.close()
				deleteSelf(address)

		except (socket.timeout, TimeoutError, ConnectionRefusedError) as e:
			pass
				

def main():
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serverSocket.bind(addr)
	serverSocket.listen()
	msg = '[{}] ready'.format(datetime.datetime.now().time())
	logger.info(msg)
	print(msg)

	while True:
		connection, address = serverSocket.accept()
		strAddress = address[0] + ':' + str(address[1])
		if strAddress not in clients:
			t = threading.Thread(target = startRecvRequests, args = (connection, strAddress))
			clients[strAddress] = (connection, t)
			t.start()

	for thread in clients.values():
		thread.join()

	serverSocket.close()

if __name__ == '__main__':
	main()
























