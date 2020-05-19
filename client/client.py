from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread

from client.connectionCheck import checkConnectionThread

from client.utils import *

import socket
import datetime

class clientThread(QThread):
	progressSignal = QtCore.pyqtSignal(object, dict)
	connectionImageSignal = QtCore.pyqtSignal(object, object, bool)

	def __init__(self, scene, connectionImage, connectionText, servAddr):
		super().__init__()
		self.scene = scene

		self.servAddr = servAddr
		self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.connectionImage = connectionImage
		self.connectionText = connectionText

		self.logger = createLogger("client")

		self.checkConnection = checkConnectionThread(self.clientSocket, self.logger, self.servAddr)
		self.checkConnection.connectionStatusSignal.connect(self.connectionStatus)

	def resetConnection(self):
		msg = '[{}] connection to {} lost'.format(datetime.datetime.now().time(), self.servAddr)
		self.logger.debug(msg)
		print(msg)
		self.connectionImageSignal.emit(self.connectionImage, self.connectionText, False)
		while True:
			try:
				self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.clientSocket.connect(self.servAddr)
				self.checkConnection.clientSocket = self.clientSocket
				self.connectionImageSignal.emit(self.connectionImage, self.connectionText, True)
				break
			except OSError:
				continue


	def startRecvData(self):
		try:
			self.clientSocket.connect(self.servAddr)
		except (OSError, socket.timeout, TimeoutError, ConnectionRefusedError) as e:
			self.resetConnection()

		self.checkConnection.start()
		self.checkConnection.wait(1)

		while True:
			try:
				binData = read(self.clientSocket)
				dataJSON = getJson(binData)

				if dataJSON['success']:
					if dataJSON['request'] == 'check':
						self.connectionImageSignal.emit(self.connectionImage, self.connectionText, True)
						msg = '[{}] {} to {} confirmed'.format(datetime.datetime.now().time(), dataJSON['request'], self.servAddr)

					elif dataJSON['request'] == 'send':
						msg = '[{}] {}'.format(datetime.datetime.now().time(), dataJSON['data'])
						self.progressSignal.emit(self.scene, dataJSON['data'])

					self.logger.debug(msg)
					print(msg)

			except (OSError, socket.timeout, TimeoutError, ConnectionRefusedError) as e:
				self.resetConnection()

	@QtCore.pyqtSlot(bool)
	def connectionStatus(self, status):
		self.connectionImageSignal.emit(self.connectionImage, self.connectionText, status)

	def sendData(self, data):
		try:
			dataJSON = {
				'success': True,
				'request': 'send',
				'data': {
					'start_x': data[0],
					'start_y': data[1],
					'end_x': data[2],
					'end_y': data[3],
					'width': self.scene.pen.width(),
					'rgba': {
						'red': self.scene.penColor.red(),
						'green': self.scene.penColor.green(),
						'blue': self.scene.penColor.blue(),
						'alpha': self.scene.penColor.alpha(),
					},
				},
			}
			binData = getBinaryJson(dataJSON)

			self.clientSocket.sendall(binData)
			msg = '[{}] send to {}: {}'.format(datetime.datetime.now().time(), self.servAddr, dataJSON['data'])
			self.logger.debug(msg)
			print(msg)

		except (socket.timeout, TimeoutError, ConnectionRefusedError) as e:
			self.resetConnection()

		except Exception as e:
			msg = '[{}] {}'.format(datetime.datetime.now().time(), e)
			self.logger.error(msg)
			print(msg)

	def run(self):
		try:
			self.startRecvData()

		finally:
			msg = '[{}] connection to {} closed'.format(datetime.datetime.now().time(), self.servAddr)
			self.logger.info(msg)
			print(msg)
			self.clientSocket.close()


if __name__ == '__main__':
	print("fff")




















