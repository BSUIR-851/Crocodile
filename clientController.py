from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from clientView import Ui_Form
from colorpicker import colorPickerWidget

import threading
import sys
import socket
import struct
import datetime
import time
import logging
import cfg

#Create application
app = QtWidgets.QApplication(sys.argv)

#Create form and init UI
Form = QtWidgets.QMainWindow()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()

#Hook logic
class sceneDraw(QtWidgets.QGraphicsScene):

	def __init__(self, thickness, hostName, portNum):
		super().__init__()
		self.isPressedLeftMouse = False
		self.penThickness = thickness
		self.pen = QtGui.QPen(QtCore.Qt.black, self.penThickness)
		self.pen.setCapStyle(QtCore.Qt.RoundCap)
		self.pen.setJoinStyle(QtCore.Qt.MiterJoin)
		self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.hostName = hostName
		self.portNum = portNum
		self.servAddr = (self.hostName, self.portNum)
		self.penColor = object
		self.exampleScene = object
		self.examplePen = object


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
			self.sendData(line)

			self.addLine(self.pStartX, self.pStartY, self.pEndX + eps, self.pEndY + eps, self.pen)
		#	self.drawEllipse(self.pStartX, self.pStartY, self.penThickness, self.penThickness)

	def mouseMoveEvent(self, event):
		if self.isPressedLeftMouse:
			self.pEndX, self.pEndY = event.scenePos().x(), event.scenePos().y()

			line = [self.pStartX, self.pStartY, self.pEndX, self.pEndY]
			self.sendData(line)

			self.addLine(self.pStartX, self.pStartY, self.pEndX, self.pEndY, self.pen)

			self.pStartX, self.pStartY = self.pEndX, self.pEndY

	def mouseReleaseEvent(self, event):
		self.isPressedLeftMouse = False


def pbClear_onClick():
	ui.gvBoard.scene().clear()

def vsThickness_onValueChanged(scene, value):
	eps = 0.00000001
	scene.pen.setWidth(value)
	scene.penThickness = value
	scene.examplePen.setWidth(value)
	scene.exampleScene.clear()
	scene.exampleScene.addLine(0, 0, 0 + eps, 0 + eps, scene.examplePen)

@QtCore.pyqtSlot(list, object, int, int)
def drawLine(data, scene, thick, rgb):
	# lastThick = scene.pen.width()
	scene.pen.setWidth(thick)
	lastRgb = scene.penColor.rgb()

	scene.penColor.setRgb(rgb + 2**32)
	scene.pen.setColor(scene.penColor)
	eps = 0.00000001
	scene.addLine(data[0], data[1], data[2] + eps, data[3] + eps, scene.pen)

	scene.pen.setWidth(scene.penThickness)
	scene.penColor.setRgb(lastRgb)
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
	scene = sceneDraw(ui.vsThickness.value(), addr[0], addr[1])
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

def main():
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
	ui.pbClear.clicked.connect(pbClear_onClick)

	client = clientThread(scene, scene.clientSocket, ui.lbConnectionImage, ui.lbConnectionStatus, addr[0], addr[1])
	client.progressSignal.connect(drawLine)
	client.connectionImageSignal.connect(changeConnectionStatus)
	client.start()
	client.wait(1)


	sys.exit(app.exec_())

if __name__ == '__main__':
	main()