from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox,QDialog
from UI.login import Ui_login
import common.utils as Utils
import sys,os,configparser

class CloseEventQDialog(QDialog):
    def closeEvent(self, event):
        sys.exit(-1)


class MesLoginView(CloseEventQDialog, QObject):

    def msgBox(self,info):
        qmsg = QMessageBox()
        qmsg.question(self,"警告",info,QMessageBox.Ok)
        # print(info)

    def loginInfoSave(self):
        login_cfg = os.path.join(Utils.getAppRootPath(), "user_cfg.ini")
        self.cfg.set("LoginInfo", "UserName", self.user_name)
        self.cfg.set("LoginInfo", "Password", Utils.aesEncrypt(self.password))
        self.cfg.write(open(login_cfg, "w"))

    def loginBtnCliked(self):
        if self.child.user_name_edit.text() is None or self.child.password_edit.text() is None:
            self.msgBox("请先输入完整的用户名和密码")
            return
        try:
            self.mes.setMESMode(self.child.checkBox.isChecked())
            self.mes.setTestMode(self.child.test_sel_rbutton.isChecked())
            self.user_name = self.child.user_name_edit.text()
            self.password = self.child.password_edit.text()
            self.mes.login(self.user_name, self.password)
            self.loginInfoSave()
            self.hide()
        except Exception as e:
            self.msgBox(str(e))

    def __init__(self, mes, config = None):
        QDialog.__init__(self)
        self.child = Ui_login()
        self.child.setupUi(self)

        self.mes = mes

        login_cfg = os.path.join(Utils.getAppRootPath(), "user_cfg.ini")
        self.cfg = configparser.ConfigParser(strict=False)
        self.cfg.optionxform = str
        self.cfg.clear()

        self.testModeEn = "0"
        self.user_name = ""
        self.password = ""
        self.child.checkBox.setChecked(True)

        try:
            self.cfg.read(login_cfg)
            self.user_name = self.cfg["LoginInfo"]["UserName"]
            self.password = Utils.aesDecrypt(self.cfg["LoginInfo"]["Password"])
            self.testModeEn = self.cfg["LoginInfo"]["TestModeEnable"]
        except Exception as e:
            if not self.cfg.has_section("LoginInfo"):
                self.cfg.add_section("LoginInfo")
            self.cfg.set("LoginInfo", "UserName", self.user_name)
            self.cfg.set("LoginInfo", "Password", Utils.aesEncrypt(self.password))
            self.cfg.set("LoginInfo", "TestModeEnable", self.testModeEn)
            self.cfg.write(open(login_cfg, "w+"))

        if self.testModeEn == "0":
            self.child.test_sel_rbutton.setVisible(False)
        else:
            self.child.test_sel_rbutton.setChecked(True)

        self.child.user_name_edit.setText(self.user_name)
        self.child.password_edit.setText(self.password)

        self.child.login_button.clicked.connect(self.loginBtnCliked)


