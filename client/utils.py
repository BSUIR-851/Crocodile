import json
import logging

def createLogger(name):
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)

	logFile = logging.FileHandler(name + ".log")
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	logFile.setFormatter(formatter)

	logger.addHandler(logFile)
	return logger

def getBinaryJson(dataJSON):
	binDataJSON = json.dumps(dataJSON).encode('UTF-8')
	binData = len(binDataJSON).to_bytes(16, byteorder='big') + binDataJSON
	return binData

def getJson(binData):
	return json.loads(binData.decode('utf-8'))

def read(sock):
	binData = b''
	dataLen = 0
	length = -1
	
	while len(binData) != length:
		data = sock.recv(1024)
		
		if not data:
			break

		if dataLen == 0:
			length = data[0:16]
			data = data[16:]
			dataLen = int.from_bytes(length, byteorder='big')
			length = dataLen

		binData += data
		currLen = len(data)
		dataLen -= currLen

	return binData

