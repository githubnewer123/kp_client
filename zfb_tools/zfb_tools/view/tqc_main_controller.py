import datetime
import json
import os
import threading
import time
import serial
from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject,Qt,QObject,pyqtSignal,QSize
from PyQt5.QtGui import QPixmap,QImage,QTransform,QPalette
from PyQt5.QtWidgets import QMessageBox,QDialog,QHeaderView
from UI.tqc_main import Ui_CheckDialog
from mes.tba_tqc_tool import universalTool
import sys
from mes.tqc_check_mysql import check_station



class CloseEventQDialog(QDialog):
    def closeEvent(self, event):
        print("self.close")
        sys.exit(-1)

class CheckView(CloseEventQDialog, QObject):
    pruduct_result_signal = pyqtSignal(dict)
    setItem_result_signal = pyqtSignal(dict)
    edit_result_signal = pyqtSignal(bool)
    def order_check(self):
        self.label_change("等待", "yellow")
        self.edit_change(False)
        self.child.change_button.update()
        for i in range(self.processTotalCount):
            for j in range(7):
                ditem = QtWidgets.QTableWidgetItem()
                ditem.setText("")
                ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.item_change(i, j, ditem)
        threading.Thread(target=self.order_mes).start()
    def order_mes(self):
        self.child.time_label.setText("")
        imei = str(self.child.entry_edit.text()).replace("\n","")
        chipId = ""
        line_item_name = ["processName","chipId","imei","createTime"]
        self.child.order_table_widget.setColumnCount(7)
        self.child.order_table_widget.setRowCount(self.processTotalCount)
        ts = datetime.datetime.now()
        state = True
        empty = False


        for i in range(self.processTotalCount):
            res = self.mes.checkmodle(self.order_id,"imei",i+1,[imei])
            if res == False:
                self.label_change("联网失败1", "red")
                self.edit_change(True)
                return
            if res["data"] != {}:
                if res["data"][imei]["imei"] != "" and len(res["data"][imei]["chipId"]) == 27:
                    chipId = res["data"][imei]["chipId"]
                    break

        res_list = []
        if imei != "" or chipId != "":
            for i in range(self.processTotalCount):
                res_list.append(self.mes.checkmodle(self.order_id,"imei", i + 1, [imei]))
                print(res_list)
                if res_list[-1] == False:
                    self.label_change("联网失败2", "red")
                    self.edit_change(True)
                    return
                if res_list[i]["data"] == {}:
                    res_list[i] = self.mes.checkmodle(self.order_id,"chipid", i + 1, [chipId])
                    if res_list[i] == False:
                        self.label_change("联网失败3", "red")
                        self.edit_change(True)
                        return
        if res_list == []:
            self.label_change("无效数据", "red")
            self.edit_change(True)
            return
        # if res_list == res_list_mark:
        #     self.label_change("无效数据", "red")
        #     self.edit_change(True)
        #     return
        process = check_station().check(self.order_id,imei)
        for i in range(self.processTotalCount):
            if res_list[i] == {'msg': 'success', 'code': 0, 'data': {}} and self.orderinfo[i] != "no_check":
                empty = True
                state = False
                for x in range(7):
                    ditem = QtWidgets.QTableWidgetItem()
                    ditem.setText("无")
                    ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.item_change(i, x, ditem)
            elif self.orderinfo[i] == "no_check":
                for x in range(7):
                    ditem = QtWidgets.QTableWidgetItem()
                    ditem.setText("不检测")
                    ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.item_change(i, x, ditem)
            else:
                info = res_list[i]["data"].keys()
                info = res_list[i]["data"][list(info)[0]]
                if info["processTestInfo"] != None:
                    infos = str(info["processTestInfo"]).replace("'","\"")
                    processTestInfo = json.loads(infos)
                else:
                    processTestInfo = info["processTestInfo"]
                for j in range(len(line_item_name)):
                    ditem = QtWidgets.QTableWidgetItem()
                    ditem.setText(str(info[line_item_name[j]]))
                    ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.item_change(i, j, ditem)
                print(info)
                ditem = QtWidgets.QTableWidgetItem()
                try:
                    if process[i][0] != "无" or None:
                        ditem.setText(process[i][0])
                    else:
                        ditem.setText("无")
                except:
                    ditem.setText("无")
                ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.item_change(i, len(line_item_name), ditem)

                ditem = QtWidgets.QTableWidgetItem()
                try:
                    if process[i][1] != "无" or None:
                        ditem.setText(process[i][1])
                    else:
                        ditem.setText("无")
                except:
                    ditem.setText("无")
                ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.item_change(i, len(line_item_name)+1, ditem)

                ditem = QtWidgets.QTableWidgetItem()
                if info["processResult"]:
                    ditem.setText("成功")
                else:
                    state = False
                    ditem.setText("失败")
                ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.item_change(i, len(line_item_name)+2, ditem)
                # ditem = QtWidgets.QTableWidgetItem()
                # ditem.setText(str(processTestInfo))
                # ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                # self.item_change(i, len(line_item_name)+3, ditem)



        if not empty:
            ch = []
            im = []
            ti = []
            csn = []
            psn = []
            for i in range(self.processTotalCount):
                if self.orderinfo[i] != "no_check":
                    info = res_list[i]["data"].keys()
                    info = res_list[i]["data"][list(info)[0]]
                    ch.append(info["chipId"])
                    im.append(info["imei"])
                    ti.append(info["createTime"])
                    csn.append(process[0])
                    psn.append(process[1])
            for i in range(1,len(ch)):
                if ch[i]!= ch[i-1]:
                    self.label_change("错误:chipId", "red")
                    self.edit_change(True)
                    self.child.time_label.setText("%.2f" % float((datetime.datetime.now() - ts).total_seconds()) + "s")
                    self.num_add()
                    return
                if im[i]!= im[i-1] and im[i-1] != None:
                    self.label_change("错误:imei", "red")
                    self.edit_change(True)
                    self.child.time_label.setText("%.2f"%float((datetime.datetime.now()-ts).total_seconds())+"s")
                    self.num_add()
                    return

                if ti[i] <= ti[i - 1]:
                    self.label_change("错误:time", "red")
                    self.edit_change(True)
                    self.child.time_label.setText("%.2f"%float((datetime.datetime.now()-ts).total_seconds())+"s")
                    self.num_add()
                    return
                # if csn[i] != psn[i-1] :
                #     self.label_change("错误:工位", "red")
                #     self.edit_change(True)
                #     self.child.time_label.setText("%.2f"%float((datetime.datetime.now()-ts).total_seconds())+"s")
                #     self.num_add()
                #     return
        if state:
            self.label_change("成功","green")

        else:
            self.label_change("错误:工序","red")

        self.num_add()

        self.child.order_table_widget.item(0, 0)

        self.edit_change(True)
        self.child.time_label.setText("%.2f"%float((datetime.datetime.now()-ts).total_seconds())+"s")




    def chipId_check(self,log):
        try:
            if log["chipId"] != "" :
                return log["chipId"]
            else:
                return False
        except:
            return False

    def reset_num(self):
        self.num = 0
        self.un.write_setting("num",0,"check_cofig.json")
        self.child.nlabel.setText(str(self.num))

    def num_add(self):
        self.num += 1
        self.un.write_setting("num", self.num,"check_cofig.json")
        self.child.nlabel.setText(str(self.num))

    def setItem_emit(self,data):
        row = data["row"]
        column = data["column"]
        text = data["text"]
        self.child.order_table_widget.setItem(row, column, text)
    def edit_change(self,bl):
        self.edit_result_signal.emit(bl)
    def edit_emit(self,bl):
        self.child.entry_edit.setEnabled(bl)
        self.child.sumbit_button.setEnabled(bl)
        if bl:
            self.child.entry_edit.setText("")
            self.child.entry_edit.setFocus()
    def label_emit(self,data):
        self.child.change_button.setText(data["text"])
        self.child.change_button.setStyleSheet("background-color: " + data["color"])
    def label_change(self,text,color):
        data = {"color": color, "text": text}
        self.pruduct_result_signal.emit(data)
        # self.child.change_button.setText(text)
        # self.child.change_button.setStyleSheet("background-color: "+ color)
    def item_change(self,row,column,text):
        data = {}
        data["row"] = row
        data["column"] = column
        data["text"] = text
        self.setItem_result_signal.emit(data)

    def __init__(self, mes,order,orderinfo):
        QDialog.__init__(self)
        self.child = Ui_CheckDialog()
        self.child.setupUi(self)
        self.order_id = order.order_id
        self.change_mark = "imei"
        self.orderinfo = orderinfo
        column_item_name = ["工序名称","chipId","imei","上传时间","上传工位","前道工位","工序结果"]

        self.mes = mes
        self.orders = self.mes.getOrderList()
        self.order_id = self.mes.getActiveOrder().order_id
        for i,order in enumerate(self.orders):
            if order.getOrderDict()["orderId"] == self.order_id:
                orderc = order.getOrderDict()["orderConfig"]
                break
        orderc = json.loads(orderc)
        self.processTotalCount = int(3)
        self.un = universalTool()

        if not os.path.isfile("check_cofig.json"):
            set_file = {}
            json.dump(set_file, open("check_cofig.json", "w"))
            self.un.write_setting("num",0,"check_cofig.json")
        self.num = int(self.un.read_setting("num","check_cofig.json"))
        self.child.nlabel.setText(str(self.num))




        # self.child.order_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.child.order_table_widget.setColumnCount(len(column_item_name))

        self.child.order_table_widget.setColumnWidth(0, 80)
        self.child.order_table_widget.setColumnWidth(1, 250)
        self.child.order_table_widget.setColumnWidth(2, 150)
        self.child.order_table_widget.setColumnWidth(3, 170)
        self.child.order_table_widget.setColumnWidth(4, 100)
        self.child.order_table_widget.setColumnWidth(5, 100)
        self.child.order_table_widget.setColumnWidth(6, 100)
        self.child.order_table_widget.setColumnWidth(7, 2000)
        self.child.order_table_widget.setHorizontalHeaderLabels(column_item_name)

        self.child.order_table_widget.setVerticalHeaderLabels([str(i+1) for i in range(len(self.orders))])

        self.child.reset_button.clicked.connect(self.reset_num)
        self.child.sumbit_button.clicked.connect(self.order_check)
        self.pruduct_result_signal.connect(self.label_emit)
        self.setItem_result_signal.connect(self.setItem_emit)
        self.edit_result_signal.connect(self.edit_emit)











