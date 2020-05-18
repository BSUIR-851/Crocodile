# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clientView.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(830, 680)
        Form.setMinimumSize(QtCore.QSize(830, 680))
        Form.setMaximumSize(QtCore.QSize(830, 680))
        self.gvBoard = QtWidgets.QGraphicsView(Form)
        self.gvBoard.setGeometry(QtCore.QRect(5, 5, 820, 540))
        self.gvBoard.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.gvBoard.setObjectName("gvBoard")
        self.pbClear = QtWidgets.QPushButton(Form)
        self.pbClear.setGeometry(QtCore.QRect(355, 560, 120, 40))
        self.pbClear.setObjectName("pbClear")
        self.lbConnectionImage = QtWidgets.QLabel(Form)
        self.lbConnectionImage.setGeometry(QtCore.QRect(680, 580, 51, 51))
        font = QtGui.QFont()
        font.setPointSize(55)
        self.lbConnectionImage.setFont(font)
        self.lbConnectionImage.setScaledContents(False)
        self.lbConnectionImage.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lbConnectionImage.setObjectName("lbConnectionImage")
        self.lbConnectionStatus = QtWidgets.QLabel(Form)
        self.lbConnectionStatus.setGeometry(QtCore.QRect(720, 610, 91, 16))
        self.lbConnectionStatus.setObjectName("lbConnectionStatus")
        self.pbGetColor = QtWidgets.QPushButton(Form)
        self.pbGetColor.setGeometry(QtCore.QRect(620, 570, 27, 27))
        self.pbGetColor.setIconSize(QtCore.QSize(16, 16))
        self.pbGetColor.setObjectName("pbGetColor")
        self.gvDotExample = QtWidgets.QGraphicsView(Form)
        self.gvDotExample.setEnabled(True)
        self.gvDotExample.setGeometry(QtCore.QRect(15, 550, 70, 70))
        self.gvDotExample.setAutoFillBackground(False)
        self.gvDotExample.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gvDotExample.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.gvDotExample.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.gvDotExample.setForegroundBrush(brush)
        self.gvDotExample.setObjectName("gvDotExample")
        self.vsThickness = QtWidgets.QSlider(Form)
        self.vsThickness.setGeometry(QtCore.QRect(85, 550, 20, 70))
        self.vsThickness.setMaximum(20)
        self.vsThickness.setProperty("value", 5)
        self.vsThickness.setOrientation(QtCore.Qt.Vertical)
        self.vsThickness.setObjectName("vsThickness")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Drawing machine"))
        self.pbClear.setText(_translate("Form", "Clear"))
        self.lbConnectionImage.setText(_translate("Form", "•"))
        self.lbConnectionStatus.setText(_translate("Form", "Not connected"))
        self.pbGetColor.setText(_translate("Form", "..."))
