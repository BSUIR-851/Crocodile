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
        Form.resize(1200, 680)
        Form.setMinimumSize(QtCore.QSize(1200, 680))
        Form.setMaximumSize(QtCore.QSize(1200, 680))
        self.gvBoard = QtWidgets.QGraphicsView(Form)
        self.gvBoard.setEnabled(False)
        self.gvBoard.setGeometry(QtCore.QRect(5, 5, 820, 540))
        self.gvBoard.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.gvBoard.setObjectName("gvBoard")
        self.pbClear = QtWidgets.QPushButton(Form)
        self.pbClear.setEnabled(False)
        self.pbClear.setGeometry(QtCore.QRect(355, 560, 120, 40))
        self.pbClear.setObjectName("pbClear")
        self.lbConnectionImage = QtWidgets.QLabel(Form)
        self.lbConnectionImage.setGeometry(QtCore.QRect(695, 598, 20, 40))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.lbConnectionImage.setFont(font)
        self.lbConnectionImage.setLineWidth(1)
        self.lbConnectionImage.setScaledContents(False)
        self.lbConnectionImage.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
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
        self.leNickname = QtWidgets.QLineEdit(Form)
        self.leNickname.setGeometry(QtCore.QRect(840, 120, 241, 30))
        self.leNickname.setObjectName("leNickname")
        self.pbSendNickname = QtWidgets.QPushButton(Form)
        self.pbSendNickname.setGeometry(QtCore.QRect(1085, 116, 110, 40))
        self.pbSendNickname.setObjectName("pbSendNickname")
        self.lbSendNickname = QtWidgets.QLabel(Form)
        self.lbSendNickname.setGeometry(QtCore.QRect(845, 100, 101, 16))
        self.lbSendNickname.setObjectName("lbSendNickname")
        self.lbNicknameHeader = QtWidgets.QLabel(Form)
        self.lbNicknameHeader.setGeometry(QtCore.QRect(845, 10, 95, 21))
        self.lbNicknameHeader.setObjectName("lbNicknameHeader")
        self.lbNickname = QtWidgets.QLabel(Form)
        self.lbNickname.setGeometry(QtCore.QRect(940, 10, 251, 21))
        self.lbNickname.setText("")
        self.lbNickname.setObjectName("lbNickname")
        self.lbDrawingHeader = QtWidgets.QLabel(Form)
        self.lbDrawingHeader.setGeometry(QtCore.QRect(845, 40, 95, 21))
        self.lbDrawingHeader.setObjectName("lbDrawingHeader")
        self.lbDrawer = QtWidgets.QLabel(Form)
        self.lbDrawer.setGeometry(QtCore.QRect(940, 40, 251, 21))
        self.lbDrawer.setText("")
        self.lbDrawer.setObjectName("lbDrawer")
        self.leSendAnswer = QtWidgets.QLineEdit(Form)
        self.leSendAnswer.setEnabled(False)
        self.leSendAnswer.setGeometry(QtCore.QRect(840, 190, 241, 30))
        self.leSendAnswer.setObjectName("leSendAnswer")
        self.pbSendAnswer = QtWidgets.QPushButton(Form)
        self.pbSendAnswer.setEnabled(False)
        self.pbSendAnswer.setGeometry(QtCore.QRect(1085, 186, 110, 40))
        self.pbSendAnswer.setObjectName("pbSendAnswer")
        self.lbSendAnswer = QtWidgets.QLabel(Form)
        self.lbSendAnswer.setGeometry(QtCore.QRect(845, 170, 101, 16))
        self.lbSendAnswer.setObjectName("lbSendAnswer")
        self.lbPlayersHeader = QtWidgets.QLabel(Form)
        self.lbPlayersHeader.setGeometry(QtCore.QRect(690, 550, 51, 21))
        self.lbPlayersHeader.setObjectName("lbPlayersHeader")
        self.lbPlayers = QtWidgets.QLabel(Form)
        self.lbPlayers.setGeometry(QtCore.QRect(745, 550, 75, 21))
        self.lbPlayers.setText("")
        self.lbPlayers.setAlignment(QtCore.Qt.AlignCenter)
        self.lbPlayers.setObjectName("lbPlayers")
        self.lbSecretWord = QtWidgets.QLabel(Form)
        self.lbSecretWord.setGeometry(QtCore.QRect(845, 70, 350, 21))
        self.lbSecretWord.setText("")
        self.lbSecretWord.setObjectName("lbSecretWord")
        self.pbStartGame = QtWidgets.QPushButton(Form)
        self.pbStartGame.setGeometry(QtCore.QRect(320, 560, 191, 41))
        self.pbStartGame.setObjectName("pbStartGame")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Drawing machine"))
        self.pbClear.setText(_translate("Form", "Clear"))
        self.lbConnectionImage.setText(_translate("Form", "⚫"))
        self.lbConnectionStatus.setText(_translate("Form", "Not connected"))
        self.pbGetColor.setText(_translate("Form", "..."))
        self.pbSendNickname.setText(_translate("Form", "Send"))
        self.lbSendNickname.setText(_translate("Form", "Send nickname:"))
        self.lbNicknameHeader.setText(_translate("Form", "Your nickname:"))
        self.lbDrawingHeader.setText(_translate("Form", "Drawing:"))
        self.pbSendAnswer.setText(_translate("Form", "Send"))
        self.lbSendAnswer.setText(_translate("Form", "Send answer:"))
        self.lbPlayersHeader.setText(_translate("Form", "Players:"))
        self.pbStartGame.setText(_translate("Form", "Start game"))
