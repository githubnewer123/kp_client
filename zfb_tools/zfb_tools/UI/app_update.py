# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app_update.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AppUpdateDialog(object):
    def setupUi(self, AppUpdateDialog):
        AppUpdateDialog.setObjectName("AppUpdateDialog")
        AppUpdateDialog.resize(762, 544)
        self.app_update_widget = QtWidgets.QTableWidget(AppUpdateDialog)
        self.app_update_widget.setGeometry(QtCore.QRect(20, 0, 731, 451))
        self.app_update_widget.setAcceptDrops(True)
        self.app_update_widget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.app_update_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.app_update_widget.setProperty("showDropIndicator", False)
        self.app_update_widget.setDragDropOverwriteMode(False)
        self.app_update_widget.setAlternatingRowColors(False)
        self.app_update_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.app_update_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.app_update_widget.setShowGrid(False)
        self.app_update_widget.setGridStyle(QtCore.Qt.NoPen)
        self.app_update_widget.setWordWrap(False)
        self.app_update_widget.setCornerButtonEnabled(False)
        self.app_update_widget.setObjectName("app_update_widget")
        self.app_update_widget.setColumnCount(0)
        self.app_update_widget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.app_update_widget.setVerticalHeaderItem(0, item)
        self.app_update_widget.verticalHeader().setVisible(True)
        self.download_btn = QtWidgets.QPushButton(AppUpdateDialog)
        self.download_btn.setGeometry(QtCore.QRect(210, 470, 131, 51))
        self.download_btn.setObjectName("download_btn")
        self.exit_btn = QtWidgets.QPushButton(AppUpdateDialog)
        self.exit_btn.setGeometry(QtCore.QRect(400, 470, 141, 51))
        self.exit_btn.setObjectName("exit_btn")

        self.retranslateUi(AppUpdateDialog)
        QtCore.QMetaObject.connectSlotsByName(AppUpdateDialog)

    def retranslateUi(self, AppUpdateDialog):
        _translate = QtCore.QCoreApplication.translate
        AppUpdateDialog.setWindowTitle(_translate("AppUpdateDialog", "版本升级"))
        self.download_btn.setText(_translate("AppUpdateDialog", "下载"))
        self.exit_btn.setText(_translate("AppUpdateDialog", "退出"))

