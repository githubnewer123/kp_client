from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject,Qt,QObject,pyqtSignal,QSize
from PyQt5.QtGui import QPixmap,QImage,QTransform,QPalette
from PyQt5.QtWidgets import QMessageBox,QDialog,QHeaderView
from UI.tqc_order import Ui_OrderDialog
import sys
from UI.tqc_main import *
from common.utils import __TQC_VERSION__

class CloseEventQDialog(QDialog):
    def closeEvent(self, event):
        print("self.close")
        sys.exit(-1)

class OrderView(CloseEventQDialog, QObject):

    def msgBox(self,info):
        qmsg = QMessageBox()
        qmsg.question(self,"警告",info,QMessageBox.Ok)

    def selectBtnOnClicked(self):
        items = self.child.order_table_widget.selectedItems()
        if len(items) == 0:
            self.msgBox("请选择一个生产订单后再确认")
            return

        self.mes.setActiceOrder(items[2].text())
        self.orderinfo = []
        for i in self.mes.orderlist:
            if i.order_id == items[2].text():
                if i.download_process != None:
                    self.orderinfo.append("burn")
                else:
                    self.orderinfo.append("no_check")
                if i.cal_process != None:
                    self.orderinfo.append("calibration")
                else:
                    self.orderinfo.append("no_check")
                if i.nst_process != None:
                    self.orderinfo.append("test")
                else:
                    self.orderinfo.append("no_check")

        self.hide()

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

        self.child.order_table_widget.setVerticalHeaderLabels([str(i+1) for i in range(len(self.orders))])

        for idx,order in enumerate(self.orders):
            # check box
            # ditem = QtWidgets.QTableWidgetItem()
            # ditem.setText("可选")
            # ditem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            # self.child.order_table_widget.setItem(idx, 0, ditem)
            for i in range(len(line_item_name)):
                ditem = QtWidgets.QTableWidgetItem()
                ditem.setText(str(order.getOrderDict()[line_item_name[i]]))
                ditem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.child.order_table_widget.setItem(idx, i, ditem)
            ditem = QtWidgets.QTableWidgetItem()
            ditem.setText(__TQC_VERSION__)
            ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.child.order_table_widget.setItem(idx, 1, ditem)

        self.child.ok_btn.clicked.connect(self.selectBtnOnClicked)
        self.child.exit_btn.clicked.connect(sys.exit)





