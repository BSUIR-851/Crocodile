from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread

from connectionCheck import checkConnectionThread

import socket
import datetime
import time
import struct

class clientThread(QThread):
	progressSignal = QtCore.pyqtSignal(list, object, int, int)
	connectionImageSignal = QtCore.pyqtSignal(object, object, bool)

	def __init__(self, scene, clientSocket, connectionImage, connectionText, hostName, portNum):
		super().__init__()
		self.scene = scene
		self.hostName = hostName
		self.portNum = portNum
		self.servAddr = (self.hostName, self.portNum)
		self.clientSocket = clientSocket
		self.connectionImage = connectionImage
		self.connectionText = connectionText
		self.logger = self.createLogger()
		self.checkConnection = checkConnectionThread(self.clientSocket, self.logger, self.servAddr)
		self.checkConnection.connectionStatusSignal.connect(self.connectionStatus)

	def createLogger(self):
		logger = logging.getLogger("client")
		logger.setLevel(logging.DEBUG)

		logFile = logging.FileHandler("client.log")
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		logFile.setFormatter(formatter)

		logger.addHandler(logFile)
		return logger

	def resetConnection(self):
		msg = '[{}] connection to {} lost'.format(datetime.datetime.now().time(), self.servAddr)
		logger.debug(msg)
		print(msg)
		self.connectionImageSignal.emit(self.connectionImage, self.connectionText, False)
		while True:
			try:
				self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.clientSocket.connect(self.servAddr)
				self.scene.clientSocket = self.clientSocket
				self.checkConnection.clientSocket = self.clientSocket
				self.connectionImageSignal.emit(self.connectionImage, self.connectionText, True)
				break
			except OSError:
				pass


	def startRecvData(self):
		self.checkConnection.start()
		self.checkConnection.wait(1)

		formatStringRecv = '=ffffiL'
		sizeFormatStringRecv = struct.calcsize(formatStringRecv)

		while True:
			try:
				isData = False
				checkData = False
				dataLen = 0
				binData = bytearray(0)

				while True:
					data = self.clientSocket.recv(1024)

					if not data:
						break

					if dataLen == 0:
						length = data[0:4]
						data = data[4:]
						dataLen = struct.unpack('i', length)[0]

					binData += data

					isData = True
					currLen = len(data)
					dataLen -= currLen
					if dataLen <= 4:
						break

				if isData:
					if (len(binData) == 4):
						self.connectionImageSignal.emit(self.connectionImage, self.connectionText, True)
						msg = '[{}] connection to {} confirmed'.format(datetime.datetime.now().time(), self.servAddr)
						logger.debug(msg)
						print(msg)

					elif (len(binData) % sizeFormatStringRecv) == 0:
						try:
							for i in range(len(binData) // sizeFormatStringRecv):
								data = list(struct.unpack(formatStringRecv, binData[i * sizeFormatStringRecv : (i + 1) * sizeFormatStringRecv]))
								msg = '[{}] recv: {}'.format(datetime.datetime.now().time(), data)
								logger.debug(msg)
								print(msg)
								self.progressSignal.emit(data, self.scene, data[-2], data[-1])

						except Exception as e:
							msg = '[{}] something gone wrong: {}'.format(datetime.datetime.now().time(), e)
							logger.error(msg)
							print(msg)
							continue

			except ConnectionResetError:
		#		print('hmm')
				self.resetConnection()

			except TimeoutError:
				self.resetConnection()

	@QtCore.pyqtSlot(bool)
	def connectionStatus(self, status):
		self.connectionImageSignal.emit(self.connectionImage, self.connectionText, status)

	def sendData(self, data):
		try:
			formatStringSend = '=iffffiL'

	#		print('send: {}'.format(data))
			data.append(self.pen.width())
			data.append(self.penColor.rgb())
			binData = struct.pack(formatStringSend, len(data) + 4, data[0], data[1], data[2], data[3], data[4], data[5])
			self.clientSocket.sendall(binData)
			msg = '[{}] send to {}: {}'.format(datetime.datetime.now().time(), self.servAddr, data)
			logger.debug(msg)
			print(msg)

		except Exception as e:
			msg = '[{}] something gone wrong: {}'.format(datetime.datetime.now().time(), e)
			logger.error(msg)
			print(msg)

	def run(self):
		try:
			self.clientSocket.connect(self.servAddr)
			self.startRecvData()

		except TimeoutError:
			self.resetConnection()
			self.startRecvData()

		except ConnectionRefusedError:
			self.resetConnection()
			self.startRecvData()

		finally:
			msg = '[{}] connection to {} closed'.format(datetime.datetime.now().time(), self.servAddr)
			logger.info(msg)
			print(msg)
			self.clientSocket.close()























