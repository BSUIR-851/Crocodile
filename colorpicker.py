from PyQt5 import QtCore, QtGui, QtWidgets

class coloredPushButton(QtWidgets.QPushButton):
	btnID = int
	color = tuple
	scene = object

	def pbOnClick(self):
		eps = 0.00000001
		self.scene.penColor = QtGui.QColor(self.color[0], self.color[1], self.color[2])
		self.scene.pen.setColor(self.scene.penColor)
		self.scene.examplePen.setColor(self.scene.penColor)
		self.scene.exampleScene.clear()
		self.scene.exampleScene.addLine(0, 0, 0 + eps, 0 + eps, self.scene.examplePen)


class colorPickerWidget(QtCore.QObject):

	def __init__(self, parent, scene, x, y, w, h, colors, in1row):
		super().__init__()
		self.parent = parent
		self.scene = scene
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.colors = colors
		self.in1row = in1row
		self.createButtonnedColors(self.x, self.y, self.w, self.h, self.colors, self.in1row)

	def setStyle(self, button, color):
		button.setStyleSheet('QPushButton'
							 '{'
							 'background-color: rgb('+str(color[0])+','+str(color[1])+','+str(color[2])+');'
							 'border-radius: 3px;\n'
							 '}'
							 'QPushButton:hover'
							 '{'
							 'border: 1px solid black;\n'
							 '}'
							 'QPushButton:pressed'
							 '{'
							 ';\n'
							 '}')

	def createButtonnedColors(self, x, y, w, h, colors, in1row):
		i = 0
		offsetY = 0
		spacing = 3
		while i < len(colors):
			if (i % in1row == 0) and (i < len(colors)):
				coloredButton = coloredPushButton(self.parent)
				coloredButton.btnID = i
				coloredButton.scene = self.scene
				new_x = x
				new_y = y + offsetY * (h + spacing)
				coloredButton.setGeometry(QtCore.QRect(new_x, new_y, w, h))
				coloredButton.color = colors[i]
				self.setStyle(coloredButton, colors[i])
				coloredButton.setCursor(QtCore.Qt.PointingHandCursor)
				coloredButton.show()
				coloredButton.clicked.connect(coloredButton.pbOnClick)
				i += 1

			offsetX = 1
			while (i  % in1row != 0) and (i < len(colors)):
				coloredButton = coloredPushButton(self.parent)
				coloredButton.btnID = i
				coloredButton.scene = self.scene
				new_x = x + offsetX * (w + spacing)
				new_y = y + offsetY * (h + spacing)
				coloredButton.setGeometry(QtCore.QRect(new_x, new_y, w, h))
				coloredButton.color = colors[i]
				self.setStyle(coloredButton, colors[i])
				coloredButton.setCursor(QtCore.Qt.PointingHandCursor)
				coloredButton.show()
				coloredButton.clicked.connect(coloredButton.pbOnClick)
				i += 1
				offsetX += 1

			offsetY += 1
		self.lastX = new_x

				

			

