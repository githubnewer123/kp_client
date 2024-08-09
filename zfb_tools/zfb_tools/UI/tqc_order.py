# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'order.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtWidgets
from common.utils import __SOFTERWARE_VERSION__
class Ui_OrderDialog(object):
    def setupUi(self, OrderDialog):
        OrderDialog.setObjectName("OrderDialog")
        OrderDialog.resize(940, 600)
        self.order_table_widget = QtWidgets.QTableWidget(OrderDialog)
        self.order_table_widget.setGeometry(QtCore.QRect(20, 20, 900, 480))
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
        self.ok_btn = QtWidgets.QPushButton(OrderDialog)
        self.ok_btn.setGeometry(QtCore.QRect(170, 520, 131, 51))
        self.ok_btn.setObjectName("ok_btn")
        self.exit_btn = QtWidgets.QPushButton(OrderDialog)
        self.exit_btn.setGeometry(QtCore.QRect(380, 520, 141, 51))
        self.exit_btn.setObjectName("exit_btn")

        self.retranslateUi(OrderDialog)
        QtCore.QMetaObject.connectSlotsByName(OrderDialog)

    def retranslateUi(self, OrderDialog):
        _translate = QtCore.QCoreApplication.translate
        OrderDialog.setWindowTitle(_translate("OrderDialog", "qc工具 "+ __SOFTERWARE_VERSION__))
        self.ok_btn.setText(_translate("OrderDialog", "确认选择"))
        self.exit_btn.setText(_translate("OrderDialog", "退出"))

