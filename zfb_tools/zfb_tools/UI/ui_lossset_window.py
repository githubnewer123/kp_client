# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_lossset_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LosssetMainWindow(object):
    def setupUi(self, LosssetMainWindow):
        LosssetMainWindow.setObjectName("LosssetMainWindow")
        LosssetMainWindow.resize(595, 559)
        self.centralwidget = QtWidgets.QWidget(LosssetMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 71, 31))
        self.label.setObjectName("label")
        self.imei_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.imei_edit.setGeometry(QtCore.QRect(90, 10, 221, 31))
        self.imei_edit.setObjectName("imei_edit")
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(240, 460, 111, 41))
        self.start_btn.setObjectName("start_btn")
        self.info_label = QtWidgets.QLabel(self.centralwidget)
        self.info_label.setGeometry(QtCore.QRect(10, 100, 561, 351))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(9)
        self.info_label.setFont(font)
        self.info_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.info_label.setWordWrap(True)
        self.info_label.setObjectName("info_label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(130, 60, 41, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 60, 51, 31))
        self.label_4.setObjectName("label_4")
        self.init_val_cbox = QtWidgets.QComboBox(self.centralwidget)
        self.init_val_cbox.setGeometry(QtCore.QRect(60, 60, 51, 31))
        self.init_val_cbox.setObjectName("init_val_cbox")
        self.throushold_cbox = QtWidgets.QComboBox(self.centralwidget)
        self.throushold_cbox.setGeometry(QtCore.QRect(170, 60, 61, 31))
        self.throushold_cbox.setObjectName("throushold_cbox")
        self.result_label = QtWidgets.QLabel(self.centralwidget)
        self.result_label.setGeometry(QtCore.QRect(440, 10, 101, 71))
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        self.result_label.setObjectName("result_label")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(250, 60, 41, 31))
        self.label_5.setObjectName("label_5")
        self.slot_cbox = QtWidgets.QComboBox(self.centralwidget)
        self.slot_cbox.setGeometry(QtCore.QRect(290, 60, 61, 31))
        self.slot_cbox.setObjectName("slot_cbox")
        LosssetMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LosssetMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 595, 26))
        self.menubar.setObjectName("menubar")
        LosssetMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LosssetMainWindow)
        self.statusbar.setObjectName("statusbar")
        LosssetMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LosssetMainWindow)
        QtCore.QMetaObject.connectSlotsByName(LosssetMainWindow)

    def retranslateUi(self, LosssetMainWindow):
        _translate = QtCore.QCoreApplication.translate
        LosssetMainWindow.setWindowTitle(_translate("LosssetMainWindow", "中云信安线损工具"))
        self.label.setText(_translate("LosssetMainWindow", "精板IMEI"))
        self.start_btn.setText(_translate("LosssetMainWindow", "开始"))
        self.info_label.setText(_translate("LosssetMainWindow", "TextLabel"))
        self.label_3.setText(_translate("LosssetMainWindow", "阈值"))
        self.label_4.setText(_translate("LosssetMainWindow", "初始值"))
        self.result_label.setText(_translate("LosssetMainWindow", "未开始"))
        self.label_5.setText(_translate("LosssetMainWindow", "SLOT"))

