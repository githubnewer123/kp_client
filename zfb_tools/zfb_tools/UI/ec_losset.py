# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ec_losset.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ec_loss_dialog(object):
    def setupUi(self, ec_loss_dialog):
        ec_loss_dialog.setObjectName("ec_loss_dialog")
        ec_loss_dialog.resize(617, 401)
        self.info_label = QtWidgets.QLabel(ec_loss_dialog)
        self.info_label.setGeometry(QtCore.QRect(20, 20, 571, 351))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        self.info_label.setFont(font)
        self.info_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.info_label.setWordWrap(True)
        self.info_label.setObjectName("info_label")

        self.retranslateUi(ec_loss_dialog)
        QtCore.QMetaObject.connectSlotsByName(ec_loss_dialog)

    def retranslateUi(self, ec_loss_dialog):
        _translate = QtCore.QCoreApplication.translate
        ec_loss_dialog.setWindowTitle(_translate("ec_loss_dialog", "中云信安线损计算"))
        self.info_label.setText(_translate("ec_loss_dialog", "请放入第一块金版"))

