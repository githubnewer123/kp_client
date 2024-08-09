import datetime
import hashlib
import subprocess
import threading
import time

import serial
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QMetaObject, Qt, QObject, QRegExp, pyqtSignal
from PyQt5.QtGui import QPixmap,QImage,QTransform,QPalette,QRegExpValidator
from PyQt5.QtWidgets import QMessageBox,QDialog,QHeaderView
import sys,os

from UI.tba_main import Ui_DownloadDialog

from mes.tba_tqc_tool import port
from mes.tba_tqc_tool import universalTool

class CloseEventQDialog(QDialog):
    def closeEvent(self, event):
        print("self.close")
        sys.exit(-1)

class BurnView(CloseEventQDialog, QObject):
    pruduct_result_signal = pyqtSignal(dict)

    def msgBox(self,info):
        qmsg = QMessageBox()
        # qmsg.setWindowIcon()
        qmsg.question(self,"警告",info,QMessageBox.Ok)

    def msgBoxError(self,info):
        qmsg = QMessageBox()
        qmsg.critical(self,"错误",info,QMessageBox.Ok)

    def loop(self):
        self.port_list = []
        self.s = 0
        while True:
            if self.mark:
                return
            ports = port().serial_List()
            if self.port_list == []:
                self.port_list = ports
                for i in range(0,len(self.port_list)):
                    self.label_change("block",i,"yellow",self.port_list[i]["text"])
                    self.s = int(i/self.width)+i%self.width
            for i in range(0, len(ports)):
                k = 0
                for j in range(0, len(self.port_list)):
                    if self.port_list[j]["location"] == ports[i]["location"]:
                        self.port_list[j] = ports[i]
                        self.label_change("block",j, self.port_list[j]["color"], self.port_list[j]["text"])
                        k = 1
                        break
                if k == 0:
                    self.s += 1
                    if self.s >= 24:
                        break
                    self.port_list.append(ports[i])
                    self.label_change("block",len(self.port_list)-1, self.port_list[len(self.port_list)-1]["color"], self.port_list[len(self.port_list)-1]["text"])
            for i in range(0, len(self.port_list)):
                k = 0
                for j in range(0, len(ports)):
                    if self.port_list[i]["location"] == ports[j]["location"]:
                        self.label_change("block",i, self.port_list[i]["color"], text=self.port_list[i]["text"])
                        k = 1
                        break
                if k == 0 and self.port_list[i]["location"] != "":
                    self.port_list[i]["text"] = "未连接"
                    self.port_list[i]["color"] = "gray"
                    self.label_change("block",i, self.port_list[i]["color"], text=self.port_list[i]["text"])
            time.sleep(1)

    def skip(self):
        if self.port_list == []:
            self.port_list = [{'text': '', 'name': ' ASR Serial Download Device', 'location': "", 'color': '', 'label': '', 'state': '', 'thread': ''}]
            self.label_change("block",0,"white","未录入")
            return
        self.s += 1
        if self.s>=24:
            return
        po = {'text': '', 'name': ' ASR Serial Download Device', 'location': "", 'color': '', 'label': "", 'state': '', 'thread': ''}
        self.port_list.append(po)
        self.label_change("block",len(self.port_list) - 1,"white","未录入")

    def entrys(self):
        if len(self.port_list) == 0:
            self.msgBox("不能为空")
            return
        writedata = []
        for i in self.port_list:
            writedata.append(i["location"])
        universalTool().write_setting("calibration",writedata,"setting.json")
        self.mark = True
        sys.exit()

    def quit(self):
        if self.clo:
            sys.exit()

    def closeEvent(self, event):
        self.mark = True
        self.clo = True


    def label_change(self, type, id, color, text):
        color = self.bg_change(color)
        data = {"type": type, "id": id, "color": color, "text": text}
        self.pruduct_result_signal.emit(data)

    def bg_change(self,bg):
        if bg == "white":
            return "rgb(255, 255, 255)"
        elif bg == "red":
            return "rgb(255, 0, 0)"
        elif bg == "yellow":
            return "rgb(255, 255, 0)"
        elif bg == "green":
            return "rgb(0, 255, 0)"
        elif bg == "gray":
            return "rgb(205,200,177)"

    def downloadChange(self, res):
        if res["type"] == "block":
            color = res["color"]
            text = res["text"]
            rc = res["id"]
            self.child.Label_list[rc].setText(text)
            self.child.Label_list[rc].setStyleSheet("background-color: " + color + ";border:2px solid #014F84")
        else:
            self.child.main_label.setText(res["text"])
            self.child.main_label.setStyleSheet("background-color: " + res["color"])

    def __init__(self,mes,name):
        QDialog.__init__(self)
        self.child = Ui_DownloadDialog()
        self.child.setupUi(self)
        self.width = 6
        self.mes = mes
        self.mark = False

        self.order = self.mes.getActiveOrder()
        self.child.skip_button.setText("跳过")
        self.child.end_button.setText("录入")

        self.port_list_UI = {}
        self.address = universalTool().read_setting("calibration","setting.json")
        station = universalTool().read_setting("station","setting.json")

        for i in range(24):
            port_list_block = port().port_Initialize()
            if i < len(self.address) and self.address[i] != "":
                port_list_block["text"] = "未连接"
                port_list_block["name"] = "未连接"
                if ":" in self.address[i]:
                    port_list_block["location"] = self.address[i].split(":")[0]
                else:
                    port_list_block["location"] = self.address[i]
                port_list_block["color"] = "grey"
                port_list_block["state"] = "wait burn"
                self.port_list_UI[str(i)] = port_list_block
            else:
                port_list_block["text"] = str(i+1)+" 未录入"
                port_list_block["name"] = "未录入"
                port_list_block["location"] = ""
                port_list_block["color"] = "white"
                port_list_block["state"] = "not config"
                self.port_list_UI[str(i)] = port_list_block

        project_v = str(self.order.project_version).replace("\n","")
        project_n = ""
        for x in range(int(len(project_v)/13)):
                project_n += project_v[int(x*13):int((x+1)*13)]+"\n"
        project_n += project_v[int((x+1)*13):]
        self.child.order_num_label.setText(self.order.order_id)
        self.child.product_ver_label.setText(project_n)
        self.child.project_name_label.setText(self.order.project_name)
        self.child.product_count_label.setText(str(self.order.product_total))
        self.child.material_code_label.setText(self.order.material_id)
        self.child.erp_material_id_label.setText(self.order.erp_material_id)
        self.child.station_code_label.setText(station)
        self.child.fw_code_label.setText(name)
        # self.child.num_code_label_XX.setVisible(False)
        # self.child.success_code_label_XX.setVisible(False)
        # self.child.fail_code_label_XX.setVisible(False)
        self.child.numBox.setVisible(False)


        self.child.main_label.setText("校准")
        self.child.skip_button.clicked.connect(self.skip)
        self.child.end_button.clicked.connect(self.entrys)
        self.pruduct_result_signal.connect(self.downloadChange)

        threading.Thread(target=self.loop).start()















