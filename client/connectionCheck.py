from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread

from client.utils import *

import datetime
import time

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

		binData = getBinaryJson(dataJSON)

		while True:
			try:
				self.clientSocket.sendall(binData)
				msg = '[{}] {} to {}'.format(datetime.datetime.now().time(), dataJSON['request'], self.servAddr)
				self.logger.debug(msg)

			except (ConnectionResetError, BrokenPipeError) as e:
				self.connectionStatusSignal.emit(False)
				msg = '[{}] {} to {} failed'.format(datetime.datetime.now().time(), dataJSON['request'], self.servAddr)
				self.logger.error(msg)

			except Exception as e:
				msg = '[{}] {}'.format(datetime.datetime.now().time(), e)
				self.logger.error(msg)

			print(msg)
			time.sleep(3)