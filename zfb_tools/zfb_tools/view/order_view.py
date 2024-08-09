from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject,Qt,QObject,pyqtSignal,QSize
from PyQt5.QtGui import QPixmap,QImage,QTransform,QPalette
from PyQt5.QtWidgets import QMessageBox,QDialog,QHeaderView
from UI.order import Ui_OrderDialog
import sys

class CloseEventQDialog(QDialog):
    def closeEvent(self, event):
        sys.exit(-1)

class OrderView(CloseEventQDialog, QObject):

    def questionMsgBox(self, info):
        res = QMessageBox.question(self, "注意", info, QMessageBox.Yes | QMessageBox.No)
        return True if (QMessageBox.Yes == res) else False

    def msgBox(self,info):
        qmsg = QMessageBox()
        qmsg.question(self,"警告",info,QMessageBox.Ok)

    def selectBtnOnClicked(self):
        items = self.child.order_table_widget.selectedItems()
        # if items[1].text() == "DD1712720018353":
        if len(items) == 0:
            self.msgBox("请选择一个生产订单后再确认")
            return

        order = self.orders[items[1].row()]
        info = "请确认是否开始以下新的订单？\r\nMES工单: %s\r\n项目名称: %s\r\n产品编码: %s\r\n" \
               "产品版本: %s\r\n项目版本: %s\r\n生产数量: %s" % \
               (order.order_id, order.project_name, order.erp_material_id, order.material_id, order.project_version,
                order.getProductTotal())
        try:
            # print(self.orders[items[1].row()].getOrderDict()["orderId"])
            # print(99999999,self.config.order_id,order.order_id)
            if self.config.order_id != "0" and not self.config.order_id.__eq__(order.order_id):
                if self.questionMsgBox(info) is False:
                    return

            self.config.db_file_update = self.child.db_update_cbox.isChecked()
            self.config.scrip_file_update = self.child.scrip_update_cbox.isChecked()
            self.config.mmpt_tool_update = self.child.mmpt_update_cbox.isChecked()
            self.config.check_post_res = self.child.check_post_cbox.isChecked()
            # self.config.cal_process = order.cal_process
            self.config.check_imei_uniq = self.child.imei_uniq_cbox.isChecked()
            self.config.configOrderId(order.order_id)
            self.mes.setActiceOrder(items[1].text(), self.config.db_file_update, self.config.scrip_file_update)
            self.hide()
        except Exception as e:
            self.msgBox(str(e))

    def getOrderById(self, id):
        for order in self.orders:
            if id.__eq__(order.order_id):
                return order

    def widgetOnClicked(self):
        items = self.child.order_table_widget.selectedItems()
        order = self.getOrderById(items[1].text())
        if order.isProductOrder():
            self.child.scrip_update_cbox.setChecked(True)
            self.child.scrip_update_cbox.setEnabled(False)
            self.child.db_update_cbox.setChecked(True)
            self.child.db_update_cbox.setEnabled(False)
            self.child.check_post_cbox.setChecked(True)
            self.child.check_post_cbox.setEnabled(False)
            self.child.mmpt_update_cbox.setEnabled(False)
            self.child.mmpt_update_cbox.setChecked(True)
        else:
            self.child.scrip_update_cbox.setChecked(True)
            self.child.scrip_update_cbox.setEnabled(True)
            self.child.db_update_cbox.setChecked(True)
            self.child.db_update_cbox.setEnabled(True)
            self.child.check_post_cbox.setChecked(True)
            self.child.check_post_cbox.setEnabled(True)
            self.child.mmpt_update_cbox.setEnabled(True)
            self.child.mmpt_update_cbox.setChecked(True)

    def repairCboxStateChange(self):
        self.child.order_table_widget.clear()
        self.column_item_name = ["项目名称", "订单号", "物料编码", "订单版本", "生产数量"]
        self.line_item_name = ["projectName", "orderId", "materialCode", "projectVersionName", "num"]

        if self.child.repair_cbox.isChecked():
            self.orders = self.mes.getRepairOrderList()
        else:
            self.orders = self.mes.getProductOrderList()

        # self.child.order_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.child.order_table_widget.setColumnCount(len(self.column_item_name))
        self.child.order_table_widget.setRowCount(len(self.orders))
        self.child.order_table_widget.setColumnWidth(0, 80)
        self.child.order_table_widget.setColumnWidth(1, 150)
        self.child.order_table_widget.setColumnWidth(2, 130)
        self.child.order_table_widget.setColumnWidth(3, 420)
        self.child.order_table_widget.setColumnWidth(4, 90)
        self.child.order_table_widget.setHorizontalHeaderLabels(self.column_item_name)
        self.child.order_table_widget.setVerticalHeaderLabels([str(i + 1) for i in range(len(self.orders))])

        for idx, order in enumerate(self.orders):
            for i in range(len(self.line_item_name)):
                ditem = QtWidgets.QTableWidgetItem()
                # print("6666666666666666",str(order.getOrderDict()[self.line_item_name[i]]))
                ditem.setText(str(order.getOrderDict()[self.line_item_name[i]]))
                ditem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.child.order_table_widget.setItem(idx, i, ditem)


    def __init__(self, mes, config):
        QDialog.__init__(self)
        self.child = Ui_OrderDialog()
        self.child.setupUi(self)
        self.config = config

        try:
            self.mes = mes
            self.mes.getOrderList()
            self.repairCboxStateChange()

            self.child.ok_btn.clicked.connect(self.selectBtnOnClicked)
            self.child.exit_btn.clicked.connect(sys.exit)
            self.child.repair_cbox.stateChanged.connect(self.repairCboxStateChange)
            self.child.order_table_widget.clicked.connect(self.widgetOnClicked)
        except Exception as e:
            self.msgBox(str(e))
            sys.exit(-1)





