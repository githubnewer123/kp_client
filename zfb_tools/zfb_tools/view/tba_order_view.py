import hashlib
import os
import shutil
import threading
import time
import zipfile

import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject,Qt,QObject,pyqtSignal,QSize
from PyQt5.QtGui import QPixmap,QImage,QTransform,QPalette
from PyQt5.QtWidgets import QMessageBox,QDialog,QHeaderView
from UI.order import Ui_OrderDialog
import sys
from common.utils import __TBA_VERSION__


from mes.tba_tqc_tool import universalTool
from UI.tba_order import *


class CloseEventQDialog(QDialog):
    def closeEvent(self, event):
        print("self.close")
        sys.exit(-1)

class OrderView(CloseEventQDialog, QObject):
    upload_result_signal = pyqtSignal(str)
    button_result_signal = pyqtSignal(bool)
    msgbox_result_signal = pyqtSignal(str)
    label_result_signal = pyqtSignal(str)

    def msgBox(self, info):
        print(info)
        qmsg = QMessageBox()
        qmsg.question(self, "警告", info, QMessageBox.Ok)

    def questionMsgBox(self, info):
        res = QMessageBox.question(self, "注意", info, QMessageBox.Yes | QMessageBox.No)
        return True if (QMessageBox.Yes == res) else False


    def file_upload(self,url,path,types):
        try:
            print(url,path,types)
            response = requests.get(url, stream=True)
            size = 0
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            with open(path, 'wb') as file:  # 显示进度条
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    self.progressBar_emit(int(size / content_size * 100),types)
                    print((int(size / content_size * 100)))
            if types == "aboot":
                self.unpack()
        except Exception:
            return False

        return True

    def unpack(self):
        fzip = zipfile.ZipFile(r"aboot/aboot.zip", 'r')
        for file in fzip.namelist():
            fzip.extract(file, "aboot")

    def aboot_check(self,aboot_md5,aboot_url):
        if os.path.isdir("aboot"):
            if os.path.isfile("aboot/aboot.zip"):
                if self.md5("aboot/aboot.zip") != aboot_md5:
                    self.label_emit("aboot")
                    shutil.rmtree("aboot")
                    os.mkdir("aboot")
                    self.file_upload(aboot_url,"aboot\\aboot.zip","aboot")
            else:
                self.label_emit("aboot")
                shutil.rmtree("aboot")
                os.mkdir("aboot")
                self.file_upload(aboot_url, "aboot\\aboot.zip", "aboot")

        else:
            self.label_emit("aboot")
            os.mkdir("aboot")
            self.file_upload(aboot_url, "aboot\\aboot.zip", "aboot")

    def fw_check(self,md5,url):
        res = self.check_file_md5(md5)
        if res:
            universalTool().write_setting("path", res,"setting.json")
            return True
        self.label_emit("fw")
        self.file_upload(url,"aboot\\bin\\fw.zip","fw")
        universalTool().write_setting("path", "bin\\fw.zip","setting.json")




    def down_init(self,order):
        fail = []
        url = ""
        md5 = ""
        aboot_url = ""
        aboot_md5 = ""
        if not os.path.isfile("setting.json"):
            fail.append("setting_none")
            universalTool().init_setting()

        for ele in order["list"]:
            if ele["elementEntity"]["zyxaElementCategoryEntity"]["category"] == "固件":
                self.name = ele["versionName"]
                url = ele["downloadUrl"]
                md5 = ele["hash"]
            if ele["elementEntity"]["zyxaElementCategoryEntity"]["category"] == "Aboot":
                aboot_url = ele["downloadUrl"]
                aboot_md5 = ele["hash"]



        if url == "" or md5 == "" or aboot_url=="" or aboot_md5 == "":
            self.msgBox("订单设置错误")
            return False


        self.aboot_check(aboot_md5,aboot_url)
        self.fw_check(md5,url)

        return True

    def md5(self,file_name):
        try:
            file_object = open(file_name, 'rb')
        except Exception:
            return
        file_content = file_object.read()
        file_object.close()
        file_md5 = hashlib.md5(file_content)
        return file_md5.hexdigest()

    def check_file_md5(self,md5):
        try:
            if not os.path.isdir("aboot\\bin"):
                os.mkdir("aboot\\bin")
            for i in os.listdir("aboot\\bin"):
                if self.md5("aboot\\bin\\" + i) == md5:
                    return "bin\\" + i
            return False
        except:
            self.box_emit("aboot缺失")
            sys.exit()




    def selectBtnOnClicked(self):


        items = self.child.order_table_widget.selectedItems()
        if len(items) == 0:
            self.box_emit("请选择一个生产订单后再确认")
            self.button_emit(True)
            return
        station = self.child.station_num_cbox.currentText()
        if station == "":
            self.box_emit("请输入工位号再确认")
            self.button_emit(True)
            return
        order = self.orders[items[1].row()]
        info = "请确认是否开始以下新的订单？\r\nMES工单: %s\r\n项目名称: %s\r\n产品编码: %s\r\n" \
               "产品版本: %s\r\n项目版本: %s\r\n生产数量: %s"% \
               (order.order_id, order.project_name, order.erp_material_id, order.material_id,order.project_version,order.product_total)

        self.order_cache = universalTool().read_setting("order_cache","setting.json")
        self.mes.setActiceOrder(items[2].text())

        if self.order_cache != "" and items[2].text() != self.order_cache:
            if self.questionMsgBox(info) is False:
                self.button_emit(True)
                return
        self.button_emit(False)
        threading.Thread(target=self.selectBtnOnClicked_th).start()

    def selectBtnOnClicked_th(self):
        items = self.child.order_table_widget.selectedItems()
        order = self.mes.getOrderInfo(items[2].text())
        self.down_init(order)
        station = self.child.station_num_cbox.currentText()
        if items[2].text() != self.order_cache:
            universalTool().write_setting("order_cache", items[2].text(),"setting.json")
            universalTool().write_setting("success_num", 0,"setting.json")
            universalTool().write_setting("fail_num", 0,"setting.json")
        universalTool().write_setting("station", station,"setting.json")

        self.orderinfo = 0
        for i in self.mes.orderlist:
            if i.order_id == items[2].text():
                if i.download_process != None:
                    self.orderinfo += 1
                if i.cal_process != None:
                    self.orderinfo += 1
                if i.nst_process != None:
                    self.orderinfo += 1

        self.hide()

    def progressBar_emit(self,num,types):
        s = str(num)+" "+types
        self.upload_result_signal.emit(s)

    def progressBar_change(self,s):
        num = int(s.split(" ")[0])
        types = str(s.split(" ")[1])
        if types == "fw":
            self.child.progressBar.setValue(num)
        elif types == "aboot":
            self.child.aboot_progressBar.setValue(num)

    def box_emit(self,string):
        self.msgbox_result_signal.emit(string)

    def box_change(self,string):
        print("box",string)
        self.msgBox(string)

    def button_emit(self,bl):
        self.button_result_signal.emit(bl)

    def button_change(self,bl):
        self.child.ok_btn.setEnabled(bl)
        self.child.exit_btn.setEnabled(bl)
        self.child.label_n.setVisible(bl)
        self.child.station_num_cbox.setEnabled(bl)
        self.name = ""

    def label_emit(self,name):
        self.label_result_signal.emit(name)

    def label_change(self,name):
        if name == "fw":
            self.child.label_n.setVisible(False)
        elif name == "aboot":
            self.child.label_x.setVisible(False)


    def __init__(self, mes):
        QDialog.__init__(self)
        self.child = Ui_OrderDialog()
        self.child.setupUi(self)

        column_item_name = ["项目名称","工具版本","订单号","物料编码","订单版本","生产数量"]
        line_item_name = ["projectName","orderId","orderId","materialCode",  "projectVersionName", "num"]

        self.mes = mes
        self.orders = self.mes.getOrderList()





        # self.child.order_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.child.order_table_widget.setColumnCount(len(column_item_name))
        self.child.order_table_widget.setRowCount(len(self.orders))
        self.child.order_table_widget.setColumnWidth(0, 80)
        self.child.order_table_widget.setColumnWidth(1, 100)
        self.child.order_table_widget.setColumnWidth(2, 150)
        self.child.order_table_widget.setColumnWidth(3, 150)
        self.child.order_table_widget.setColumnWidth(4, 300)
        self.child.order_table_widget.setColumnWidth(5, 80)
        self.child.order_table_widget.setHorizontalHeaderLabels(column_item_name)

        self.child.station_num_cbox.addItems(["%02d"%(i) for i in range(1,50)])
        station = universalTool().read_setting("station","setting.json")
        if station:
            self.child.station_num_cbox.setCurrentText(station)

        self.child.order_table_widget.setVerticalHeaderLabels([str(i+1) for i in range(len(self.orders))])


        for idx,order in enumerate(self.orders):
            # check box

            for i in range(len(line_item_name)):
                ditem = QtWidgets.QTableWidgetItem()
                ditem.setText(str(order.getOrderDict()[line_item_name[i]]))
                ditem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.child.order_table_widget.setItem(idx, i, ditem)

            ditem = QtWidgets.QTableWidgetItem()
            ditem.setText(__TBA_VERSION__)
            ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.child.order_table_widget.setItem(idx, 1, ditem)


        self.child.ok_btn.clicked.connect(self.selectBtnOnClicked)
        self.child.exit_btn.clicked.connect(sys.exit)
        self.button_result_signal.connect(self.button_change)
        self.upload_result_signal.connect(self.progressBar_change)
        self.msgbox_result_signal.connect(self.box_change)
        self.label_result_signal.connect(self.label_change)






