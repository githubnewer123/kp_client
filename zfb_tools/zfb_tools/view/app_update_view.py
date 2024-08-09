from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject,Qt,QObject,pyqtSignal,QSize
from PyQt5.QtGui import QPixmap,QImage,QTransform,QPalette
from PyQt5.QtWidgets import QMessageBox,QDialog,QHeaderView
from UI.app_update import Ui_AppUpdateDialog
from manager.app_update import AppUpdate
import sys,datetime,os
import common.utils as Utils

class CloseEventQDialog(QDialog):
    def closeEvent(self, event):
        self.accept()

class AppUpdateView(CloseEventQDialog, QObject):

    def questionMsgBox(self, info):
        res = QMessageBox.question(self, "注意", info, QMessageBox.Yes | QMessageBox.No)
        return True if (QMessageBox.Yes == res) else False

    def msgBox(self,info):
        qmsg = QMessageBox()
        qmsg.question(self,"警告",info,QMessageBox.Ok)

    def downloadUpdate(self, val):
        if self.pre_val == val:
            return
        self.pre_val = val

        ditem = self.child.app_update_widget.selectedItems()[3]
        if val == 100:
            ditem.setText("完成")
            self.msgBox("%s 文件下载完成, 按OK后退出程序!请重新从桌面快捷方式打开程序"%(self.select_version))
            self.app_updater.createInk(Utils.getAppRootPath()+self.select_version, self.select_version+" - 快捷方式", Utils.getAppRootPath())
            Utils.runExe(os.path.join(Utils.getAppRootPath(), self.select_version),self.select_version)
            self.reject()
        else:
            ditem.setText(str(val)+"%")

    def downloadBtnOnClicked(self):
        self.child.download_btn.setEnabled(False)
        items = self.child.app_update_widget.selectedItems()
        if len(items) == 0:
            self.msgBox("请选择一个版本后开始下载！")
            return
        print("开始下载文件: "+ items[0].text())
        self.select_version = items[0].text()
        self.app_updater.download_progresss_signal.connect(self.downloadUpdate)
        self.app_updater.download(items[0].text(), "./")

    def versionInfoUpdate(self, result):
        column_item_name = ["工具名称", "文件大小", "上传时间", "下载进度"]
        if result["res"] is False:
            self.msgBox("无法获取软件版本列表")
            self.hide()
            return

        # self.child.order_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.child.app_update_widget.setColumnCount(len(column_item_name))
        self.child.app_update_widget.setRowCount(len(self.app_updater.version_list))
        self.child.app_update_widget.setColumnWidth(0, 200)
        self.child.app_update_widget.setColumnWidth(1, 80)
        self.child.app_update_widget.setColumnWidth(2, 220)
        self.child.app_update_widget.setColumnWidth(3, 100)
        self.child.app_update_widget.setHorizontalHeaderLabels(column_item_name)
        print(self.app_updater.version_list)
        self.child.app_update_widget.setVerticalHeaderLabels(
            [str(i + 1) for i in range(len(self.app_updater.version_list))])

        for idx, ver in enumerate(self.app_updater.version_list):
            # exe name
            ditem = QtWidgets.QTableWidgetItem()
            ditem.setText(str(ver))
            ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.child.app_update_widget.setItem(idx, 0, ditem)

            # file size
            meta = self.app_updater.getFileMeta(ver)
            ditem = QtWidgets.QTableWidgetItem()
            ditem.setText(str(meta.content_length))
            ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.child.app_update_widget.setItem(idx, 1, ditem)

            ditem = QtWidgets.QTableWidgetItem()
            create_time = datetime.datetime.fromtimestamp(meta.last_modified).strftime('%Y-%m-%d %H:%M:%S')
            ditem.setText(create_time)
            ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.child.app_update_widget.setItem(idx, 2, ditem)

            ditem = QtWidgets.QTableWidgetItem()
            ditem.setText("0")
            ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.child.app_update_widget.setItem(idx, 3, ditem)
        #
        self.child.download_btn.clicked.connect(self.downloadBtnOnClicked)
        self.child.exit_btn.clicked.connect(super().accept)

    def __init__(self):
        QDialog.__init__(self)
        self.child = Ui_AppUpdateDialog()
        self.child.setupUi(self)

        self.pre_val = 0
        self.select_version = ""

        try:
            self.app_updater = AppUpdate("TCTA")
            self.app_updater.check_version_signal.connect(self.versionInfoUpdate)
            self.app_updater.checkVersion(Utils.getAppVersion())


            # self.child.app_update_widget.clicked.connect(self.widgetOnClicked)
        except Exception as e:
            self.msgBox(str(e))
            self.hide()





