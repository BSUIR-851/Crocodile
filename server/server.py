from utils import *
from words import *

import socket
import datetime
import threading
import sys
import random
import time

#LOGGER
logger = createLogger("server")

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
msg = '[{}] new secret word: {}'.format(datetime.datetime.now().time(), secretWord)
logger.info(msg)
print(msg)


def delete(strAddress):
	global currDrawer
	msg = '[{}] {} disconnected'.format(datetime.datetime.now().time(), strAddress)
	logger.info(msg)
	print(msg)
	clients[strAddress]['connection'].close()
	del clients[strAddress]
	if currDrawer == strAddress:
		currDrawer = ''

def deleteSelf(strAddress):
	delete(strAddress)
	sys.exit()

def deleteClient(strAddress):
	t = clients[strAddress]['thread']
	delete(strAddress)
	t.join(1)

def deleteClients():
	for client in toDelete:
		deleteClient(client)

def getNewSecretWord():
	global secretWord
	random.shuffle(words)
	secretWord = words[0]
	msg = '[{}] new secret word: {}'.format(datetime.datetime.now().time(), secretWord)
	logger.info(msg)
	print(msg)
	return secretWord
'''
def getNewDrawer():
	moveNum += 1
	clientsAddr = clients.keys()
	currDrawer = clientsAddr[moveNum % len(clients)]
	secretWord = getNewSecretWord()
	return currDrawer
'''
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
		toDelete.clear()


def startRecvRequests(connection, address):
	global currDrawer
	global secretWord
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
					msg = '[{}] {} from {}: {}'.format(datetime.datetime.now().time(), dataJSON['request'], address, dataJSON['data'])
					logger.debug(msg)
					print(msg)

					if dataJSON['request'] == 'check':
						dataJSON['data'] = {}
						dataJSON['data']['amount_of_connected'] = len(clients)
						dataJSON['data']['isLive'] = bool(currDrawer)
						if dataJSON['data']['isLive']:
							dataJSON['data']['drawer'] = clients[currDrawer]['nickname']
						else:
							dataJSON['data']['drawer'] = ''

						dataJSON['data']['isYouDrawer'] = address == currDrawer
						dataJSON['data']['secretWord'] = secretWord

						binData = getBinaryJson(dataJSON)
						connection.sendall(binData)
						msg = '[{}] {} to {} confirmed'.format(datetime.datetime.now().time(), dataJSON['request'], address)
						logger.debug(msg)
						print(msg)

					elif dataJSON['request'] == 'nickname':
						clients[address]['nickname'] = dataJSON['data']

					elif dataJSON['request'] == 'answer':
						if dataJSON['data'] == secretWord.upper():
							# finish drawing after guessing word
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

							time.sleep(2)

							# notify all players about guessing word
							currDrawer = address
							answer = secretWord
							winner = clients[address]['nickname']
							dataJSON = {
								'success': True,
								'request': 'drawer',
								'data': {
									'drawer': clients[address]['nickname'],
									'answer': answer,
									'winner': winner,
								},
							}
							binData = getBinaryJson(dataJSON)
							sendCoordsToClients(binData, dataJSON, address)

							# send new secret word to new drawer
							secretWord = getNewSecretWord()
							dataJSON = {
								'success': True,
								'request': 'start',
								'data': {
									'secretWord': secretWord,
								},
							}
							binData = getBinaryJson(dataJSON)
							connection.sendall(binData)
							msg = '[{}] to {}: {}'.format(datetime.datetime.now().time(), address, dataJSON['data'])
							logger.debug(msg)
							print(msg)

					elif dataJSON['request'] == 'send':
						sendCoordsToClients(binData, dataJSON, address)

					elif dataJSON['request'] == 'clear':
						sendCoordsToClients(binData, dataJSON, address)

					elif dataJSON['request'] == 'firstStart':
						currDrawer = address


			else:
				connection.close()
				deleteSelf(address)

		except (ConnectionResetError, socket.timeout, TimeoutError, ConnectionRefusedError) as e:
			connection.close()
			deleteSelf(address)
				

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























