# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'order.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject,Qt,QObject,pyqtSignal,QSize
from PyQt5.QtGui import QPixmap,QImage,QTransform,QPalette
from PyQt5.QtWidgets import QMessageBox,QDialog,QHeaderView
from common.utils import __SOFTERWARE_VERSION__



class Ui_CheckDialog(object):
    def setupUi(self, CheckDialog):
        CheckDialog.setObjectName("CheckDialog")
        CheckDialog.resize(1050, 600)
        self.entry_edit = QtWidgets.QLineEdit(CheckDialog)
        self.entry_edit.setGeometry(QtCore.QRect(20, 10, 300, 50))
        self.entry_edit.setFont(QFont("Timers", 20))
        self.sumbit_button = QtWidgets.QPushButton(CheckDialog)
        self.sumbit_button.setGeometry(QtCore.QRect(320, 10, 100, 50))
        self.sumbit_button.setFont(QFont("Timers", 20))

        self.nlabel = QtWidgets.QLabel(CheckDialog)
        self.nlabel.setGeometry(QtCore.QRect(440, 10, 50, 50))
        self.nlabel.setFont(QFont("Timers", 20))
        self.reset_button = QtWidgets.QPushButton(CheckDialog)
        self.reset_button.setGeometry(QtCore.QRect(500, 10, 100, 50))
        self.reset_button.setFont(QFont("Timers", 20))

        self.time_label = QtWidgets.QLabel(CheckDialog)
        self.time_label.setGeometry(QtCore.QRect(650, 10, 100, 50))
        self.time_label.setFont(QFont("Timers", 20))
        self.time_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.change_button = QtWidgets.QLabel(CheckDialog)
        self.change_button.setGeometry(QtCore.QRect(800, 10, 200, 50))
        self.change_button.setFont(QFont("Timers", 20))
        self.change_button.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.change_button.setStyleSheet("background-color: yellow")
        self.order_table_widget = QtWidgets.QTableWidget(CheckDialog)
        self.order_table_widget.setGeometry(QtCore.QRect(20, 70, 1000, 480))
        self.order_table_widget.setAcceptDrops(True)
        self.order_table_widget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.order_table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.order_table_widget.setProperty("showDropIndicator", False)
        self.order_table_widget.setDragDropOverwriteMode(False)
        self.order_table_widget.setAlternatingRowColors(False)
        self.order_table_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.order_table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.order_table_widget.setShowGrid(False)
        self.order_table_widget.setGridStyle(QtCore.Qt.NoPen)
        self.order_table_widget.setWordWrap(False)
        self.order_table_widget.setCornerButtonEnabled(False)
        self.order_table_widget.setObjectName("order_table_widget")
        self.order_table_widget.setColumnCount(0)
        self.order_table_widget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.order_table_widget.setVerticalHeaderItem(0, item)
        self.order_table_widget.verticalHeader().setVisible(True)

        self.retranslateUi(CheckDialog)
        QtCore.QMetaObject.connectSlotsByName(CheckDialog)

    def retranslateUi(self, CheckDialog):
        _translate = QtCore.QCoreApplication.translate
        CheckDialog.setWindowTitle(_translate("CheckDialog", "qc工具 "+ __SOFTERWARE_VERSION__))
        self.nlabel.setText(_translate("CheckDialog", "imei"))
        self.sumbit_button.setText(_translate("CheckDialog", "查询"))
        self.reset_button.setText(_translate("CheckDialog", "重置"))
        self.change_button.setText(_translate("CheckDialog", "等待"))


