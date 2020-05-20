from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from clientView import Ui_Form
from colorpicker import colorPickerWidget

from client.client import clientThread

import sys
import socket
import cfg
import re

#Create application
app = QtWidgets.QApplication(sys.argv)

#Create form and init UI
Form = QtWidgets.QMainWindow()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()

#Hook logic
class sceneDraw(QtWidgets.QGraphicsScene):
	def __init__(self, thickness, host):
		super().__init__()
		self.isPressedLeftMouse = False

		self.penThickness = thickness
		self.pen = QtGui.QPen(QtCore.Qt.black, self.penThickness)
		self.pen.setCapStyle(QtCore.Qt.RoundCap)
		self.pen.setJoinStyle(QtCore.Qt.MiterJoin)

		self.hostName = host[0]
		self.portNum = host[1]
		self.servAddr = (self.hostName, self.portNum)

		self.penColor = object
		self.exampleScene = object
		self.examplePen = object

		self.sceneClient = object


	def drawEllipse(self, x, y, w, h):
		ellipse = QtWidgets.QGraphicsEllipseItem(x, y, w-1, h-1)
		transform = QtGui.QTransform()
		transform.translate(-(w-1)/2, -(h-1)/2)
		ellipse.setTransform(transform)
		ellipse.setBrush(QtCore.Qt.black)
		self.addItem(ellipse)

	def mousePressEvent(self, event):
		if (event.button() == QtCore.Qt.LeftButton):
			eps = 0.00000001
			self.isPressedLeftMouse = True
			self.pStartX, self.pStartY = event.scenePos().x(), event.scenePos().y()
			self.pEndX, self.pEndY = self.pStartX, self.pStartY

			line = [self.pStartX, self.pStartY, self.pEndX, self.pEndY]
			self.sceneClient.sendData(line)

			self.addLine(self.pStartX, self.pStartY, self.pEndX + eps, self.pEndY + eps, self.pen)
		#	self.drawEllipse(self.pStartX, self.pStartY, self.penThickness, self.penThickness)

	def mouseMoveEvent(self, event):
		if self.isPressedLeftMouse:
			self.pEndX, self.pEndY = event.scenePos().x(), event.scenePos().y()

			line = [self.pStartX, self.pStartY, self.pEndX, self.pEndY]
			self.sceneClient.sendData(line)

			self.addLine(self.pStartX, self.pStartY, self.pEndX, self.pEndY, self.pen)

			self.pStartX, self.pStartY = self.pEndX, self.pEndY

	def mouseReleaseEvent(self, event):
		self.isPressedLeftMouse = False


def pbClear_onClick(scene):
	ui.gvBoard.scene().clear()
	dataJSON = {
		'success': True,
		'request': 'clear',
		'data': 'clear',
	}
	scene.sceneClient.sendAnotherData(dataJSON)

def vsThickness_onValueChanged(scene, value):
	eps = 0.00000001
	scene.pen.setWidth(value)
	scene.penThickness = value
	scene.examplePen.setWidth(value)
	scene.exampleScene.clear()
	scene.exampleScene.addLine(0, 0, 0 + eps, 0 + eps, scene.examplePen)

@QtCore.pyqtSlot(list, object, dict)
def drawLine(scene, data):
	lastData = {
		'width': scene.pen.width(),
		'red': scene.penColor.red(),
		'green': scene.penColor.green(),
		'blue': scene.penColor.blue(),
		'alpha': scene.penColor.alpha(),
	}
	scene.pen.setWidth(data['width'])

	scene.penColor.setRed(data['rgba']['red'])
	scene.penColor.setGreen(data['rgba']['green'])
	scene.penColor.setBlue(data['rgba']['blue'])
	scene.penColor.setAlpha(data['rgba']['alpha'])
	scene.pen.setColor(scene.penColor)
	eps = 0.00000001
	scene.addLine(data['start_x'], data['start_y'], data['end_x'] + eps, data['end_y'] + eps, scene.pen)

	scene.pen.setWidth(lastData['width'])
	scene.penColor.setRed(lastData['red'])
	scene.penColor.setGreen(lastData['green'])
	scene.penColor.setBlue(lastData['blue'])
	scene.penColor.setAlpha(lastData['alpha'])
	scene.pen.setColor(scene.penColor)

@QtCore.pyqtSlot(object, object, bool)
def changeConnectionStatus(image, text, status):
	if status:
		image.setStyleSheet("color: rgb(0, 255, 0)")
		text.setText("Connected")
	else:
		image.setStyleSheet("color: rgb(255, 0, 0)")
		text.setText("Disconnected")


def boardSetting(addr):
	scene = sceneDraw(ui.vsThickness.value(), addr)
	ui.gvBoard.setScene(scene)
	scene.setSceneRect(0, 0, ui.gvBoard.width()-5, ui.gvBoard.height()-5)
	return scene

def getColor(scene):
	eps = 0.00000001
	color = QtWidgets.QColorDialog.getColor()
	scene.penColor = color
	scene.pen.setColor(scene.penColor)
	scene.examplePen.setColor(scene.penColor)
	scene.exampleScene.clear()
	scene.exampleScene.addLine(0, 0, 0 + eps, 0 + eps, scene.examplePen)
	# print(color.getRgb())

@QtCore.pyqtSlot(object, tuple)
def setColor(scene, color):
	scene.penColor = QtGui.QColor(color[0], color[1], color[2])
	scene.pen.setColor(scene.penColor)

def createColors(scene):
	colors = [(0, 0, 0), 	   (255, 255, 255),
			  (109, 109, 109), (255, 196, 219),
			  (56, 220, 198),  (45, 177, 25),
		  	  (19, 0, 255),    (128, 0, 201),
			  (24, 192, 26),   (244, 228, 11),
			  (255, 224, 163), (253, 123, 8),
			  (251, 0, 8),     (91, 32, 11)
	]
	pbX = 15
	pbY = 635
	pbW = 27
	pbH = 27
	colorPicker = colorPickerWidget(Form, scene, pbX, pbY, pbW, pbH, colors, len(colors))
	ui.pbGetColor.setGeometry(QtCore.QRect(colorPicker.lastX + pbW , pbY - 4, pbW + 14, pbH + 9))
	ui.pbGetColor.setCursor(QtCore.Qt.PointingHandCursor)

def createExampleScene(scene, startValue, startColor):
	eps = 0.00000001
	exampleScene = QtWidgets.QGraphicsScene()
	ui.gvDotExample.setScene(exampleScene)
	examplePen = QtGui.QPen(QtCore.Qt.black, startValue)
	examplePen.setColor(QtGui.QColor(startColor[0], startColor[1], startColor[2]))
	examplePen.setCapStyle(QtCore.Qt.RoundCap)
	exampleScene.addLine(0, 0, 0 + eps, 0 + eps, examplePen)
	scene.exampleScene = exampleScene
	scene.examplePen = examplePen

@QtCore.pyqtSlot(object)
def clearScene(scene):
	scene.clear()

def pbSendNickname_onClick(scene):
	nickname = ui.leNickname.text()
	dataJSON = {
		'success': True,
		'request': 'nickname',
		'data': nickname,
	}
	scene.sceneClient.sendAnotherData(dataJSON)
	scene.sceneClient.nickname = nickname
	ui.lbNickname.setText(nickname)
	Form.hide()
	Form.show()

# СДЕЛАТЬ ЗАПУСК ИГРЫ!!!!
def pbSendAnswer_onClick(scene):
	text = ui.leAnswer.text()
	text = re.sub(r'\s+', ' ', text)
	text = text.strip()
	if text == 'start':

	dataJSON = {
		'success': True,
		'request': 'firstStart',
		'data': nickname,
	}
	scene.sceneClient.sendAnotherData(dataJSON)
	scene.sceneClient.nickname = nickname
	ui.lbNickname.setText(nickname)

@QtCore.pyqtSlot(int)
def setAmountOfPlayers(amount):
	ui.lbPlayers.setText(str(amount))

@QtCore.pyqtSlot(dict)
def recvStartHandler(data):
	ui.lbSecretWord.setText("Секретное слово: " + data['secretWord'])
	ui.gvBoard.setEnabled(True)
	ui.pbClear.setEnabled(True)
	ui.leAnswer.setEnabled(False)
	ui.leSendAnswer.setEnabled(False)
	Form.hide()
	Form.show()

	msgBox = QtWidgets.QMessageBox()
	msgBox.setText("Вы - ведущий!")
	msgBox.setInformativeText(
		"Вы были выбраны случайным образом!\n" +
		"Секретное слово: " + str(data['secretWord'])
	)
	msgBox.exec_()


@QtCore.pyqtSlot()
def recvFinishHandler():
	ui.gvBoard.setEnabled(False)
	ui.pbClear.setEnabled(False)
	ui.lbSecretWord.clear()
	ui.leAnswer.setEnabled(True)
	ui.leSendAnswer.setEnabled(True)
	Form.hide()
	Form.show()

@QtCore.pyqtSlot(dict)
def recvDrawerHandler(data):
	msgBox = QtWidgets.QMessageBox()
	if data['isWin']:
		msgBox.setText("Поздравляю! Вы отгадали слово!")
	else:
		msgBox.setText("Секретное слово было угадано.")

	msgBox.setInformativeText(
		"Победитель: " + str(dataJSON['winner']) +
		"\nОтвет: " + str(dataJSON['answer']) + 
		"\nСледующий ведущий: " + str(dataJSON['drawer'])
	)
	msgBox.exec_()

def main():
	ui.lbNickname.setText(socket.gethostname())
	ui.leNickname.setText(socket.gethostname())
	ui.vsThickness.setRange(0, 50)
	ui.lbConnectionImage.setStyleSheet("color: rgb(255, 0, 0)")
	ui.lbConnectionStatus.setText("Disconnected")

	host, port = cfg.getValues('addr.conf', ['address'], ['host', 'port'])
	
	addr = (host, port)
	scene = boardSetting(addr)

	startColor = (0, 0, 0)
	setColor(scene, startColor)
	createExampleScene(scene, ui.vsThickness.value(), startColor)
	createColors(scene)

	ui.pbGetColor.clicked.connect(lambda: getColor(scene))

	ui.vsThickness.valueChanged.connect(lambda: vsThickness_onValueChanged(scene, ui.vsThickness.value()))
	ui.pbClear.clicked.connect(lambda: pbClear_onClick(scene))
	ui.pbSendNickname.clicked.connect(lambda: pbSendNickname_onClick(scene))
	ui.pbSendAnswer.clicked.connect(lambda: pbSendAnswer_onClick(scene))

	client = clientThread(scene, ui.lbConnectionImage, ui.lbConnectionStatus, addr)
	client.progressSignal.connect(drawLine)
	client.connectionImageSignal.connect(changeConnectionStatus)
	client.clearSignal.connect(clearScene)
	client.amountOfPlayersSignal.connect(setAmountOfPlayers)
	client.recvStartSignal.connect(recvStartHandler)
	client.recvFinishSignal.connect(recvFinishHandler)
	client.drawerSignal.connect(recvDrawerHandler)
	scene.sceneClient = client
	client.start()
	client.wait(1)

	pbSendNickname_onClick(scene)

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()