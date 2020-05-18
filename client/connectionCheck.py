from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread

import socket
import datetime
import time
import json

class checkConnectionThread(QThread):
	connectionStatusSignal = QtCore.pyqtSignal(bool)

	def __init__(self, clientSocket, logger, servAddr):
		super().__init__()
		self.clientSocket = clientSocket
		self.logger = logger
		self.servAddr = servAddr

	def run(self):
		dataJSON = {
			'success': True,
			'request': 'check',
		}
		binDataJSON = json.dumps(dataJSON).encode('UTF-8')
		binData = bytes([len(binDataJSON)]) + binDataJSON

		while True:
			try:
				self.clientSocket.sendall(binData)
				msg = '[{}] {}'.format(datetime.datetime.now().time(), dataJSON)

			except (ConnectionResetError, BrokenPipeError) as e:
				self.connectionStatusSignal.emit(False)
				msg = '[{}] connection to {} lost'.format(datetime.datetime.now().time(), self.servAddr)

			except Exception as e:
				msg = '[{}] {}'.format(datetime.datetime.now().time(), e)

			self.logger.debug(msg)
			print(msg)
			time.sleep(3)