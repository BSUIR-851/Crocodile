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
	lenOfLen = 0
	binLength = b''
	
	while lenOfLen != 16:
		binLength += sock.recv(16 - lenOfLen)
		lenOfLen += len(binLength)
		if not binLength:
			break

	length = int.from_bytes(binLength, byteorder='big')

	while dataLen != length:
		binData += sock.recv(length - dataLen)
		dataLen += len(binData)
		if not binData:
			break
	
	return binData

