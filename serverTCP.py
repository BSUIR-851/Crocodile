import socket
import struct
import datetime
import threading
import logging

logger = logging.getLogger("server")
logger.setLevel(logging.DEBUG)

logFile = logging.FileHandler("server.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logFile.setFormatter(formatter)

logger.addHandler(logFile)

def sendCoords(clients, addr, connection, coords, listData):
	try:
		connection.sendall(coords)
		msg = '[{}] send to {}: {}'.format(datetime.datetime.now().time(), addr, listData)
		logger.debug(msg)
		print(msg)

	except BrokenPipeError:
		t = clients[addr][1]
		del clients[addr]
		t.join(1)
		msg = '[{}] {} disconnected'.format(datetime.datetime.now().time(), addr)
		logger.info(msg)
		print(msg)

	except Exception as e:
		msg = '[{}] something gone wrong: {}'.format(datetime.datetime.now().time(), e)
		logger.error(msg)
		print(msg)


def sendCoordsToClients(clients, coords, currAddress, listData):
	new_clients = clients.copy()
	for addr, connAndThr in new_clients.items():
		if connAndThr[0] != new_clients[currAddress][0]:
			sendCoords(clients, addr, connAndThr[0], coords, listData)

def createConnect(clients, connection, address):
	msg = '[{}] connected by {}'.format(datetime.datetime.now().time(), address)
	logger.info(msg)
	print(msg)
	
	formatStringRecv = '=ffffiL'
	sizeFormatStringRecv = struct.calcsize(formatStringRecv)

	formatStringSend = '=iffffiL'

	while True:
		isData = False
		checkData = False
		dataLen = 0
		binData = bytearray(0)

		while True:
			data = connection.recv(1024)
			if not data:
				break

			if dataLen == 0:
				length = data[0:4]
				data = data[4:]
				dataLen = struct.unpack('=i', length)[0]

			binData += data

			isData = True
			currLen = len(data)
			dataLen -= currLen
			if dataLen <= 4:
				break

		if isData:
			if len(binData) == 4:
				try:
					listData = list(struct.unpack('=i', binData))
					listData = struct.pack('=ii', len(listData) + 4, listData[0])
					connection.sendall(listData)
					msg = '[{}] check connection from: {}'.format(datetime.datetime.now().time(), address)
					logger.debug(msg)
					print(msg)

				except Exception as e:
					msg = '[{}] something gone wrong: {}'.format(datetime.datetime.now().time(), e)
					logger.error(msg)
					print(msg)

			elif (len(binData) % sizeFormatStringRecv) == 0:
				try:
					for i in range(len(binData) // sizeFormatStringRecv):
						listData = list(struct.unpack(formatStringRecv, binData[i * sizeFormatStringRecv : (i + 1) * sizeFormatStringRecv]))
						msg = '[{}] recv ({}): {}'.format(datetime.datetime.now().time(), address, listData)
						logger.debug(msg)
						print(msg)

						listBinData = struct.pack(formatStringSend, len(listData) + 4, listData[0], listData[1], listData[2], listData[3], listData[4], listData[5])
						sendCoordsToClients(clients, listBinData, address, listData)

				except Exception as e:
					msg = '[{}] something gone wrong: {}'.format(datetime.datetime.now().time(), e)
					logger.error(msg)
					print(msg)
				

def main():
	clients = {}
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serverSocket.bind(('', 49100))
	serverSocket.listen()
	msg = '[{}] ready'.format(datetime.datetime.now().time())
	logger.info(msg)
	print(msg)

	while True:
		connection, address = serverSocket.accept()
		if address not in clients:
			t = threading.Thread(target = createConnect, args = (clients, connection, address))
			clients[address] = (connection, t)
			t.start()

	serverSocket.close()

if __name__ == '__main__':
	main()