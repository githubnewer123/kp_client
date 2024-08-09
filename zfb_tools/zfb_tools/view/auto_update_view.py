from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject,Qt,QObject,pyqtSignal,QSize
from PyQt5.QtGui import QPixmap,QImage,QTransform,QPalette
from PyQt5.QtWidgets import QMessageBox,QDialog,QHeaderView
from UI.auto_update import Ui_update_dialog
from manager.app_update import AppUpdate
import sys,datetime,os,logging
import common.utils as Utils

class CloseEventQDialog(QDialog):
    def closeEvent(self, event):
        self.reject()

class AutoUpdateView(CloseEventQDialog, QObject):

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

        self.child.progressBar.setValue(val)
        if val == 100:
            self.msgBox("%s 文件下载完成, 按OK后重新打开新程序"%(self.select_version))
            # self.app_updater.createInk(Utils.getAppRootPath()+self.select_version, self.select_version+" - 快捷方式", Utils.getAppRootPath())
            # Utils.runExe(os.path.join(Utils.getAppRootPath(), self.select_version),self.select_version)
            self.reject()

    def checkVersionResult(self,result):
        logging.info(result)
        if result["res"] is False:
            self.msgBox(result["info"])
            self.reject()
        else:
            if result["version"] is None:
                self.accept()
                return

            if self.questionMsgBox("检测到新版本 %s，是否开始升级？"%(result["version"].replace(".zip",""))):
                logging.info("开始升级到版本： %s"%(result["version"]))
                self.child.update_info.setText("当前版本: %s\r\n目标版本: %s"%(Utils.getAppVersion(), result["version"].replace(".exe","").replace(".zip","")))
                self.select_version = result["version"]
                self.app_updater.download_progresss_signal.connect(self.downloadUpdate)
                self.app_updater.download(result["version"], './')
            else:
                self.accept()
                return

    def __init__(self, app_name = "CMBT"): #"TCTA"
        QDialog.__init__(self)
        self.child = Ui_update_dialog()
        self.child.setupUi(self)

        self.pre_val = 0
        self.select_version = ""

        self.app_updater = AppUpdate(app_name)
        self.app_updater.check_version_signal.connect(self.checkVersionResult)
        self.app_updater.checkVersion(Utils.getAppVersion())





