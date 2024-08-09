# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auto_update.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_update_dialog(object):
    def setupUi(self, update_dialog):
        update_dialog.setObjectName("update_dialog")
        update_dialog.resize(688, 300)
        self.progressBar = QtWidgets.QProgressBar(update_dialog)
        self.progressBar.setGeometry(QtCore.QRect(20, 230, 651, 51))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(20)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.update_info = QtWidgets.QLabel(update_dialog)
        self.update_info.setGeometry(QtCore.QRect(40, 50, 381, 91))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(18)
        self.update_info.setFont(font)
        self.update_info.setObjectName("update_info")

        self.retranslateUi(update_dialog)
        QtCore.QMetaObject.connectSlotsByName(update_dialog)

    def retranslateUi(self, update_dialog):
        _translate = QtCore.QCoreApplication.translate
        update_dialog.setWindowTitle(_translate("update_dialog", "软件版本更新"))
        self.update_info.setText(_translate("update_dialog", "检查软件版本..."))

