import datetime
import hashlib
import signal
import subprocess
import threading
import time
import uuid

import psutil
import serial
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QMetaObject, Qt, QObject, QRegExp, pyqtSignal
from PyQt5.QtGui import QPixmap,QImage,QTransform,QPalette,QRegExpValidator
from PyQt5.QtWidgets import QMessageBox,QDialog,QHeaderView
import sys,os

from UI.tba_main import Ui_DownloadDialog
from mes import mes

from mes.tba_tqc_tool import port
from mes.tba_tqc_tool import universalTool
from common.utils import __SOFTERWARE_VERSION__

TOOL_DATA = {
    "commitid":"",
    "count":0,
    "successCount":0,
    "failCount":0,
    "orderId":"",
    "startTs":"",
    "endTs":"",
    "prodectId":"",
    "processTotalCount":3,
    "processName":"烧录",
    "processSequence":1,
    "stationNumber":"",
    "processList":[]
}

TOOL_DATA_DICT = {
    "processFlag":1,
    "processTestInfo":"",
    "realEst":0,
    "est":0,
    "logZip": "",
    "processResult":0,
    "remark":"",
    "sn":"",
    "imei":"",
    "mac":"",
    "chipId":""
}
global STATION
class CloseEventQDialog(QDialog):
    def closeEvent(self, event):
        print("self.close")
        sys.exit(-1)

class DownloadView(CloseEventQDialog, QObject):
    pruduct_result_signal = pyqtSignal(dict)
    num_result_signal = pyqtSignal(int)
    msgbox_result_signal = pyqtSignal(str)
    def msgBox(self,info):
        qmsg = QMessageBox()
        qmsg.question(self,"警告",info,QMessageBox.Ok)

    def msgBoxError(self,info):
        qmsg = QMessageBox()
        qmsg.critical(self,"错误",info,QMessageBox.Ok)

    def md5(self,file_name):
        try:
            file_object = open(file_name, 'rb')
        except Exception:
            return
        file_content = file_object.read()
        file_object.close()
        file_md5 = hashlib.md5(file_content)
        return file_md5.hexdigest()

    def main_loop(self):
        while True:
            if self.run_mark:
                return
            self.wait_loop()
            self.burn_loop()
            self.end_loop()

    def wait_loop(self):
        run = True
        time_out_start = False
        self.stime = time.time()
        print("wait_loop>>>start")
        while True:
            if self.run_mark:
                return

            time.sleep(1)#防止卡死
            self.port_list = port().serial_List()
            for i in range(0, len(self.port_list)):
                for j in range(24):  # 刷新地址池中已存在并连接的COM口
                    if self.port_list_UI[j]["location"] == self.port_list[i]["location"]:
                        self.port_list[i]["state"] = self.port_list_UI[j]["state"]
                        self.port_list_UI[j] = self.port_list[i]
                        if self.port_list[i]["name"] == " ASR Serial Download Device" and self.port_list_UI[j]["state"] == "wait burn":
                            print("wait_loop>>>prepare_collect")
                            self.label_change("block",j, self.port_list_UI[j]["color"], "等待烧录")
                            self.port_list_UI[j]["state"] = "burning"
                            time_out_start = True
                            self.stime = time.time()
            for i in range(0, len(self.address)):
                identifier = False
                for j in range(0, len(self.port_list)):  # 激活地址池中存在并在此连接的COM口
                    if self.port_list_UI[i]["location"] == self.port_list[j]["location"]:
                        self.port_list[j]["state"] = self.port_list_UI[i]["state"]
                        self.port_list_UI[i] = self.port_list[j]
                        identifier = True
                        break
                if not identifier and self.port_list_UI[i]["state"] != "fail end":  # 关闭地址池中存在并未连接的COM口
                    self.port_list_UI[i]["text"] = "未连接"
                    self.port_list_UI[i]["color"] = "grey"
                    if self.port_list_UI[i]["state"] == "wait burn":
                        self.label_change("block",i, self.port_list_UI[i]["color"], self.port_list_UI[i]["text"])
            for i in range(0, len(self.address)):
                if self.port_list_UI[i]["state"] == "fail end" and self.port_list_UI[i]["text"] != "未连接":
                    self.port_list_UI[i]["state"] = "burning"
                    self.label_change("block",i, "yellow", "等待烧录")
                if self.port_list_UI[i]["state"] == "burning" and self.port_list_UI[i]["text"] == "未连接":
                    self.port_list_UI[i]["state"] = "fail end"
                    self.label_change("block",i, "red", "烧录失败,硬件被取出")
                if self.port_list_UI[i]["text"] == "未连接" and time.time() - self.stime > self.link_time_out and self.port_list_UI[i]["state"] == "wait burn" and time_out_start:
                    self.label_change("block",i, "red", "硬件插入超时")
                    self.port_list_UI[i]["state"] = "fail end"
            identifier = False
            for i in range(0, len(self.address)):
                if self.port_list_UI[i]["state"] == "wait burn":
                    identifier = True
            if not identifier:
                if run:
                    run = False
                else:
                    print("wait_loop>>>end")
                    break

    def burn_loop(self):
        global TOOL_DATA
        global TOOL_DATA_DICT
        if self.run_mark:
            return
        TOOL_DATA["startTs"] = datetime.datetime.now()
        # .strftime('%Y-%m-%d %H:%M:%S.%f')
        for i in range(0,len(self.port_list_UI)):
            cd = TOOL_DATA_DICT.copy()
            TOOL_DATA["processList"].append(cd)
        # print("collect_loop>>>star")
        for i in range(0, len(self.port_list_UI)):
            if self.port_list_UI[i]["state"] == "burning":
                self.label_change("block",i, self.port_list_UI[i]["color"], "烧录中")
                self.port_list_UI[i]["thread"]=threading.Thread(target=self.burn, args=(i,))
                self.port_list_UI[i]["thread"].start()
        # print("collect_loop>>>thread_end")
        self.stime = time.time()
        identifier_one = False
        while True:
            if self.run_mark:
                return
            identifier_two = False
            time.sleep(1)
            if time.time() - self.stime > self.burn_time_out:
                # print("collect_loop>>>time_out")
                self.getAllPid()
                for i in range(0, len(self.address)):
                    if self.port_list_UI[i]["state"] == "burning":
                        if TOOL_DATA["processList"][i]["chipId"] != "":
                            TOOL_DATA["failCount"] += 1
                            TOOL_DATA["processList"][i]["processResult"] = 0
                            TOOL_DATA["processList"][i]["processFlag"] = 1
                            TOOL_DATA["processList"][i]["realEst"] = float(
                                (datetime.datetime.now() - TOOL_DATA["startTs"]).total_seconds())
                            TOOL_DATA["processList"][i]["remark"] = "烧录超时"
                            self.fail_num += 1
                            self.num_change()
                            if self.reset:
                                self.label_change("block", i, "red", "被重置")
                                TOOL_DATA["processList"][i]["remark"] = "被重置"
                        if not self.reset:
                            self.label_change("block",i, "red", "烧录失败,超时")
                        self.port_list_UI[i]["state"] = "fail end"
                break
            for i in range(0, len(self.address)):
                if self.port_list_UI[i]["state"] == "burn end" and not identifier_one:
                    self.stime = time.time() - self.burn_success_time_out+self.burn_success_time_out
                    identifier_one = True
            for i in range(0,len(self.address)):
                if self.port_list_UI[i]["state"] == "burning":
                    identifier_two = True
            if not identifier_two :

                # print("collect_loop>>>end")
                break

    def end_loop(self):
        if self.run_mark:
            return
        global TOOL_DATA
        self.label_change("main_label", 0, "yellow", "结束")
        TOOL_DATA["endTs"] = datetime.datetime.now()
        for i in TOOL_DATA["processList"]:
            i["est"] = float((TOOL_DATA["endTs"]-TOOL_DATA["startTs"]).total_seconds())
        TOOL_DATA["startTs"] = TOOL_DATA["startTs"].strftime('%Y-%m-%d %H:%M:%S.%f')
        TOOL_DATA["endTs"] = TOOL_DATA["endTs"].strftime('%Y-%m-%d %H:%M:%S.%f')
        processList_l = len(TOOL_DATA["processList"])
        i = 0
        while i<processList_l:
            if self.run_mark:
                return
            if TOOL_DATA["processList"][i]["chipId"] == "":
                del TOOL_DATA["processList"][i]
                processList_l -= 1
                continue
            i += 1
        TOOL_DATA["count"] = len(TOOL_DATA["processList"])
        if not TOOL_DATA["processList"] == []:
            self.mes.postProductData(TOOL_DATA)
        TOOL_DATA["processList"] = []
        TOOL_DATA["successCount"] = 0
        TOOL_DATA["failCount"] = 0
        while True:
            if self.run_mark:
                return
            ports = port().serial_List()
            if len(ports) == 0:
                break
        self.label_change("main_label", 0, "yellow", "等待")
        while True:
            if self.run_mark:
                return
            ports = port().serial_List()
            if len(ports) > 0:
                break
        for i in range(0,len(self.address)):
            if self.address[i] != "":
                self.port_list_UI[i]["state"] = "wait burn"
        self.reset = False
        self.label_change("main_label", 0, "yellow", "正进行")

    def burn(self,id):
        global TOOL_DATA
        TOOL_DATA["processList"][id]["processTestInfo"] = str({"tool_version":__SOFTERWARE_VERSION__}).replace("\'","\"")
        stime = time.time()
        lists = []
        for s in range(0, 1000):
            lists.append(str(s))
        com = self.port_list_UI[id]["text"]
        progress = 0
        cmd = "adownload.exe -q -f -u -s 3686400 -p " + com + " " + self.path_file
        ret = subprocess.Popen(cmd, shell=True,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               cwd=r"aboot")
        for i in iter(ret.stdout.readline, b""):
            if "[INFO: EFuse     ]" in i.decode().strip():
                for j in i.decode().strip().replace(",","").split(" "):
                    if j in lists:
                        le = 3-len(j)
                        for k in range(0,le):
                            j = "0"+j
                        TOOL_DATA["processList"][id]["chipId"] += j
            if i.decode().strip()[0:12] == "\"progress\" :":
                if int(i.decode().strip()[12:].rstrip(",")) == 100:
                    progress = 100
                if progress ==100 and int(i.decode().strip()[12:].rstrip(",")) == 0:
                    TOOL_DATA["successCount"] += 1
                    TOOL_DATA["processList"][id]["processResult"] = 1
                    if self.burn_processTotalCount == 1:
                        TOOL_DATA["processList"][id]["processFlag"] = 0
                    else:
                        TOOL_DATA["processList"][id]["processFlag"] = 2
                    if TOOL_DATA["processTotalCount"] == self.burn_processTotalCount:
                        TOOL_DATA["processList"][id]["processFlag"] = 1
                    TOOL_DATA["processList"][id]["realEst"] = float((datetime.datetime.now()-TOOL_DATA["startTs"]).total_seconds())
                    self.label_change("block",id, "green", "烧录成功")
                    self.success_num += 1
                    self.num_change()
                    self.port_list_UI[id]["state"] = "burn end"
                    break
                self.label_change("block",id, "yellow", "烧录中"+i.decode().strip()[12:].rstrip(",")+"%")
            elif str(i.decode().strip().split(" ")[1:]) == "['aboot', 'download', 'engine', 'stopped', 'successfully.']" and progress != 100:
                TOOL_DATA["failCount"] += 1
                TOOL_DATA["processList"][id]["processResult"] = 0
                TOOL_DATA["processList"][id]["processFlag"] = 1
                TOOL_DATA["processList"][id]["realEst"] = float((datetime.datetime.now() - TOOL_DATA["startTs"]).total_seconds())
                TOOL_DATA["processList"][id]["remark"] = "烧录中断"
                self.fail_num += 1
                self.num_change()
                self.label_change("block",id, "red", "烧录中途停止")
                self.port_list_UI[id]["state"] = "burn end"
                break

    def box_emit(self,string):
        self.msgbox_result_signal.emit(string)

    def box_change(self,string):
        self.msgBox(string)

    def label_change(self,type, id, color, text):
        if color == None:
            color = "grey"
        color = self.bg_change(color)
        data = {"type":type,"id":id,"color":color,"text":text}
        self.pruduct_result_signal.emit(data)

    def label_emit(self,data):
        if data["type"] == "block":
            color = data["color"]
            text = data["text"]
            rc = data["id"]
            self.child.Label_list[rc].setText(str(rc)+" "+text)
            self.child.Label_list[rc].setStyleSheet("background-color: " + color + ";border:2px solid #014F84")
        else:
            self.child.main_label.setText(data["text"])
            self.child.main_label.setStyleSheet("background-color: " + data["color"])

    def num_change(self):
        self.num_result_signal.emit(1)

    def num_emit(self,int):
        self.child.success_code_label.setText(str(self.success_num))
        self.child.fail_code_label.setText(str(self.fail_num))
        self.child.num_code_label.setText(str(self.success_num+self.fail_num))
        universalTool().write_setting("fail_num",self.fail_num,"setting.json")
        universalTool().write_setting("success_num",self.success_num,"setting.json")

    def getAllPid(self):
        try:
            pid_dict = {}
            pids = psutil.pids()
            for pid in pids:
                p = psutil.Process(pid)
                pid_dict[pid] = p.name()
            for t in pid_dict.keys():
                if pid_dict[t] == "adownload.exe":
                    kill_pid = os.kill(t, signal.SIGABRT)
        except Exception as a:
            pass

    def reset_run(self):
        self.getAllPid()
        self.stime = time.time()-int(self.burn_time_out)
        self.id = []
        self.reset = True
        for k in range(0, len(self.address)):
            self.id.append("wait")
        self.label_change("main_label",0,"yellow","已重置")
        for s in range(0,len(self.address)):
            if self.port_list_UI[s]["state"] != "not config":
                self.label_change("block",s,"red","已重置")

    def ca(self):
        self.reset_run()

        self.run_mark = True
        self.hide()


    def bg_change(self,bg):
        if bg == "white":
            return "rgb(255, 255, 255)"
        elif bg == "red":
            return "rgb(255, 0, 0)"
        elif bg == "yellow":
            return "rgb(255, 255, 0)"
        elif bg == "green":
            return "rgb(0, 128, 0)"
        elif bg == "grey":
            return "rgb(205,200,177)"

    # def aboot_th_stop(self):

    def string_len_n(self,name):
        name_n = ""
        for x in range(int(len(name)/20)):
                name_n += name[int(x*20):int((x+1)*20)]+"\n"
        name_n += name[int((x+1)*20):]
        return name_n

    def quit(self):
        if self.clo:
            sys.exit()
    def closeEvent(self, event):
        self.clo = True
        self.run_mark = True
        self.getAllPid()

    def __init__(self, order,mes,name,orderinfo):
        QDialog.__init__(self)
        self.child = Ui_DownloadDialog()
        self.child.setupUi(self)
        self.fail_num = universalTool().read_setting("fail_num","setting.json")
        self.success_num = universalTool().read_setting("success_num","setting.json")
        self.run_mark = False
        self.clo = False
        self.path_file = universalTool().read_setting("path","setting.json")
        self.mes = mes
        self.order = self.mes.getActiveOrder()
        self.burn_processTotalCount = 1
        self.port_list_UI = []
        self.address = universalTool().read_setting("calibration","setting.json")
        self.link_time_out = 10
        self.burn_time_out = 80
        self.burn_success_time_out = 90
        self.reset = False
        self.orderinfo = orderinfo
        global TOOL_DATA
        # print(order)
        # TOOL_DATA["processTotalCount"] = order["processTotalCount"]
        # self.burn_processTotalCount = 1
        # for i in order["process"]:
        #     if "proc_burn" == i:
        #         break
        #     self.burn_processTotalCount += 1
        # TOOL_DATA["processSequence"] = self.burn_processTotalCount

        self.station = universalTool().read_setting("station","setting.json")

        TOOL_DATA["commitid"] = str(uuid.uuid1())
        TOOL_DATA["orderId"] = self.order.order_id
        TOOL_DATA["stationNumber"] = self.station
        TOOL_DATA["processTotalCount"] = self.orderinfo

        print(TOOL_DATA["processTotalCount"],"processTotalCount")



        for i in range(24):
            port_list_block = port().port_Initialize()
            if i < len(self.address) and self.address[i] != "":
                port_list_block["text"] = str(i+1)+"未连接"
                port_list_block["name"] = "未连接"
                if ":" in self.address[i]:
                    port_list_block["location"] = self.address[i].split(":")[0]
                else:
                    port_list_block["location"] = self.address[i]
                port_list_block["color"] = "grey"
                port_list_block["state"] = "wait burn"
                self.port_list_UI.append(port_list_block)
            else:
                port_list_block["text"] = str(i+1)+" 未录入"
                port_list_block["name"] = "未录入"
                port_list_block["location"] = ""
                port_list_block["color"] = "white"
                port_list_block["state"] = "not config"
                self.port_list_UI.append(port_list_block)

        verison = str(self.order.project_version).replace("\n","")

        self.child.order_num_label.setText(self.order.order_id)
        self.child.product_ver_label.setText(self.string_len_n(verison))
        self.child.project_name_label.setText(self.order.project_name)
        self.child.product_count_label.setText(str(self.order.product_total))
        self.child.material_code_label.setText(self.order.material_id)
        self.child.erp_material_id_label.setText(self.order.erp_material_id)
        self.child.station_code_label.setText(self.station)
        self.child.num_code_label.setText(str(self.success_num+self.fail_num))
        self.child.success_code_label.setText(str(self.success_num))
        self.child.fail_code_label.setText(str(self.fail_num))
        self.child.fw_code_label.setText(name)



        self.child.main_label.setVisible(True)
        self.child.main_label.setText("等待")
        self.child.end_button.setText("重置")
        self.child.skip_button.setText("校准")

        self.pruduct_result_signal.connect(self.label_emit)
        self.num_result_signal.connect(self.num_emit)
        self.child.skip_button.clicked.connect(self.ca)
        self.child.end_button.clicked.connect(self.reset_run)
        self.msgbox_result_signal.connect(self.box_change)

        for i in range(24):
            if self.port_list_UI[i]["color"] == "":
                self.port_list_UI[i]["color"] = "white"
            self.label_change("block",i,self.port_list_UI[i]["color"],"未录入")

        self.th = threading.Thread(target=self.main_loop).start()


















