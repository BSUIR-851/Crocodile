from utils import *
from words import *

import socket
import datetime
import threading
import sys
import random
import time

#SERVER DATA
host = ''
port = 49100
addr = (host, port)
clients = {}
toDelete = []

#GAME DATA
moveNum = 0
currDrawer = ''
words = getWords('words.txt')
random.shuffle(words)
secretWord = words[0]

#LOGGER
logger = createLogger("server")

def deleteSelf(strAddress):
	del clients[strAddress]
	sys.exit()

def deleteClient(strAddress):
	t = clients[strAddress]['thread']
	del clients[strAddress]
	t.join(1)

def deleteClients():
	for client in toDelete:
		deleteClient(client)
	toDelete.clear()

def getNewSecretWord():
	random.shuffle(words)
	secretWord = words[0]
	return secretWord

def getNewDrawer():
	moveNum += 1
	clientsAddr = clients.keys()
	currDrawer = clientsAddr[moveNum % len(clients)]
	secretWord = getNewSecretWord()
	return currDrawer

def sendCoords(binData, dataJSON, client_address, connAndThread):

	connection = connAndThread['connection']

	try:
		connection.sendall(binData)
		msg = '[{}] send to {}: {}'.format(datetime.datetime.now().time(), client_address, dataJSON['data'])
		logger.debug(msg)

	except (OSError, socket.timeout, TimeoutError, ConnectionRefusedError, BrokenPipeError) as e:
		toDelete.append(client_address)
		msg = '[{}] {} disconnected'.format(datetime.datetime.now().time(), client_address)
		logger.info(msg)

	except Exception as e:
		msg = '[{}] something gone wrong: {}'.format(datetime.datetime.now().time(), e)
		logger.error(msg)

	print(msg)


def sendCoordsToClients(binData, dataJSON, address):
	for client_address, connAndThread in clients.items():
		if client_address != address:
			sendCoords(binData, dataJSON, client_address, connAndThread)

	if toDelete:
		deleteClients()



def startRecvRequests(connection, address):
	msg = '[{}] connected by {}'.format(datetime.datetime.now().time(), address)
	logger.info(msg)
	print(msg)

	while True:
		try:
			binData = read(connection)
			if binData:
				dataJSON = getJson(binData)
				binData = getBinaryJson(dataJSON)

				if dataJSON['success']:
					if dataJSON['request'] == 'check':
						dataJSON['amount_of_connected'] = len(clients)
						binData = getBinaryJson(dataJSON)
						connection.sendall(binData)
						msg = '[{}] {} to {} confirmed'.format(datetime.datetime.now().time(), dataJSON['request'], address)
						logger.debug(msg)
						print(msg)

					elif dataJSON['request'] == 'nickname':
						msg = '[{}] from {}: {}'.format(datetime.datetime.now().time(), address, dataJSON['data'])
						clients[address]['nickname'] = dataJSON['data']
						logger.debug(msg)
						print(msg)

					elif dataJSON['request'] == 'answer':
						if dataJSON['data'] == secretWord:
							msg = '[{}] answer from {}: {}'.format(datetime.datetime.now().time(), address, dataJSON['data'])
							logger.debug(msg)
							print(msg)

							answer = secretWord
							winner = clients[address]['nickname']
							oldDrawer = currDrawer

							dataJSON = {
								'success': True,
								'request': 'finish',
								'data': 'finish',
							}
							binData = getBinaryJson(dataJSON)
							clients[oldDrawer]['connection'].sendall(binData)
							msg = '[{}] to {}: {}'.format(datetime.datetime.now().time(), address, dataJSON['data'])
							logger.debug(msg)
							print(msg)

							newDrawer = getNewDrawer()

							time.sleep(2)

							dataJSON = {
								'success': True,
								'request': 'drawer',
								'data': {
									'drawer': clients[newDrawer]['nickname'],
									'answer': answer,
									'winner': winner,
									'isWin': False,
								},
							}
							binData = getBinaryJson(dataJSON)
							sendCoordsToClients(binData, dataJSON, address)

							dataJSON = {
								'success': True,
								'request': 'start',
								'data': {
									'secretWord': secretWord,
								},
							}
							binData = getBinaryJson(dataJSON)
							clients[newDrawer]['connection'].sendall(binData)
							msg = '[{}] to {}: {}'.format(datetime.datetime.now().time(), address, dataJSON['data'])
							logger.debug(msg)
							print(msg)

							dataJSON['data']['isWin'] = True
							binData = getBinaryJson(dataJSON)
							connection.sendall(binData)
							msg = '[{}] win to {}: {}'.format(datetime.datetime.now().time(), address, dataJSON['data'])
							logger.debug(msg)
							print(msg)

					elif dataJSON['request'] == 'send':
						msg = '[{}] from {}: {}'.format(datetime.datetime.now().time(), address, dataJSON['data'])
						logger.debug(msg)
						print(msg)
						sendCoordsToClients(binData, dataJSON, address)

					elif dataJSON['request'] == 'clear':
						msg = '[{}] from {}: {}'.format(datetime.datetime.now().time(), address, dataJSON['data'])
						logger.debug(msg)
						print(msg)
						sendCoordsToClients(binData, dataJSON, address)

					elif dataJSON['request'] == 'firstStart':
						msg = '[{}] from {}: {}'.format(datetime.datetime.now().time(), address, dataJSON['data'])
						logger.debug(msg)
						print(msg)


			else:
				msg = '[{}] {} disconnected'.format(datetime.datetime.now().time(), address)
				logger.info(msg)
				print(msg)
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
			clients[strAddress] = {}
			clients[strAddress]['connection'] = connection
			clients[strAddress]['thread'] = t
			t.start()

	for thread in clients.values():
		thread.join()

	serverSocket.close()

if __name__ == '__main__':
	main()
























