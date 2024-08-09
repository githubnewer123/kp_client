from UI.product_main import Ui_ProductMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu,QAction
from PyQt5.QtCore import QObject,QTimer
import common.utils as Utils
import sys, logging,datetime
from mes.mes import Mes

from view.product_main_controller import ProductMainController
from view.product_ec_main_controller import ProductEcMainController
from device.com_port_manager import AtPortManager
from manager.ec_slot import EcSlot
from view.ec_loss_view import EcLossView
from view.mes_login_view import MesLoginView
from view.order_view import OrderView
from view.config_view import ConfigView
from view.app_update_view import AppUpdateView
from view.auto_update_view import AutoUpdateView
from manager.tool_config import ToolConfig
from manager.window_manager import WindowsManager
from burn_tool.Main_UI import Main_ui

from PyQt5.QtWidgets import QMessageBox


class CloseEventQMainWindow(QtWidgets.QMainWindow):

    def closeEvent(self, event):
        logging.info("Close by user")
        self.close()

class ProductMainView(Ui_ProductMainWindow, QObject):
    PRODUCT_RES_IDLE = 0x01
    PRODUCT_RES_BUSY  = 0x02
    PRODUCT_RES_SUCCESS = 0x03
    PRODUCT_RES_FAIL = 0x04

    def msgBox(self,info):
        qmsg = QMessageBox()
        qmsg.question(self.main_win,"警告",info,QMessageBox.Ok)

    def getTimestamp(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def setProductResLabel(self, status):
        if status == ProductMainView.PRODUCT_RES_BUSY:
            self.elapse_cnt = 0
            self.elapsed_time_label.setText("0")
            self.elapsed_timer.start(1000)
            color = ""
            text = "运行中"
        elif status == ProductMainView.PRODUCT_RES_SUCCESS:
            color = "background-color:green"
            text = "成功"
            self.elapsed_timer.stop()
            self.win_manager.winMin(self.win_manager.getMmptTitleName())
        elif status == ProductMainView.PRODUCT_RES_FAIL:
            color = "background-color:red"
            text = "失败"
            self.elapsed_timer.stop()
            self.win_manager.winMin(self.win_manager.getMmptTitleName())
        elif status == ProductMainView.PRODUCT_RES_IDLE:
            text = "等待"
            color = ""
        else:
            raise Exception("设置生成结果背景状态出错")
        self.res_bg_label.setStyleSheet(color)
        self.res_bg_label.setText(text)

    def resInfoAppend(self, info):
        if info.startswith("----"):
            self.res_info_list.append(info)
        else:
            self.res_info_list.append("[%s] %s" % (self.getTimestamp(), info))
        if len(self.res_info_list) > 64:
                self.res_info_list = self.res_info_list[-64:]
        info = ""
        for txt in self.res_info_list:
            info += txt+"\r\n"
        self.product_info_text.setText(info)
        cursor = self.product_info_text.textCursor()  # 设置游标
        pos = len(self.product_info_text.toPlainText())  # 获取文本尾部的位置
        cursor.setPosition(pos)  # 游标位置设置为尾部
        self.product_info_text.setTextCursor(cursor)  # 滚动到游标位置

    def portChageHandle(self, port_list):
        logging.info("port change: len port list -> %d"%(len(port_list)))
        if self.cab_loss_notify:
            self.cab_loss_notify.portChangeNotitfy(port_list)
            return
        if len(port_list) > 0:
            logging.info("port start -> %s" % (port_list[0][0]))
            self.setProductResLabel(ProductMainView.PRODUCT_RES_BUSY)
            if int(self.cfg.station_type) != 2:
                self.imei_edit_timer.stop()
                imei = self.imei_edit.text().strip()
                # if imei is None:
                #     imei = "869734053181990"
                if len(imei) > 15:
                    imei = imei[-15:]
                if Utils.isImei(imei):
                    self.resInfoAppend("-" * 54)
                    self.pruduct_ctrl.start(0, port_list[0][0], imei)
                    self.product_imei_lable.setText(imei)
                    # self.pruduct_ctrl.setSlotImei(0, imei)
                else:
                    self.resInfoAppend("IMEI输入格式错误")
                    self.setProductResLabel(ProductMainView.PRODUCT_RES_FAIL)
            else:
                self.pruduct_ctrl.start(0, port_list[0][0], "")
        else:
            self.pruduct_ctrl.deviceAbort(0)
            self.resInfoAppend("等待设备接入")
            self.product_imei_lable.setText("")
            self.imei_edit.clear()
            self.setProductResLabel(ProductMainView.PRODUCT_RES_IDLE)

    def pruductInfoUpdata(self):
        self.success_total_label.setText(str(self.cfg.success_cnt))
        self.false_total_label.setText(str(self.cfg.false_cnt))
        self.lte_false_label.setText(str(self.cfg.lte_false_cnt))
        self.gsm_false_label.setText(str(self.cfg.gsm_false_cnt))
        self.imei_false_label.setText(str(self.cfg.imei_false_cnt))
        self.adc_false_label.setText(str(self.cfg.adc_false_cnt))
        self.other_false_label.setText(str(self.cfg.other_false_cnt))
        self.mes_false_label.setText(str(self.cfg.mes_false_cnt))
        self.pruduct_ctrl.infoSave()

    def productResultHandle(self,res):
        msg = res
        logging.info("RES info: %s"%( res["info"]))
        self.resInfoAppend(res["info"])
        if msg["res"] and msg["is_complete"]:
            self.setProductResLabel(ProductMainView.PRODUCT_RES_SUCCESS)
            self.resInfoAppend("-" * 54)

        elif msg["res"] is False:
            self.setProductResLabel(ProductMainView.PRODUCT_RES_FAIL)

            self.resInfoAppend("-" * 54)
        self.pruductInfoUpdata()
        if self.cfg.factory_mes_enable:
            self.factory_mes_res_label.setText(
                "成功: %s   失败: %s" % (str(self.cfg.fac_mes_success_total), str(self.cfg.fac_mes_false_total)))

    def orderInfoInit(self):
        split_num = 20
        product_ver = []
        self.order_num_label.setText(self.order.order_id)
        for idx in range(0,len(self.order.project_version)//split_num):
            product_ver.append(self.order.project_version[idx*split_num:(idx+1)*split_num])
        product_ver.append(self.order.project_version[-(len(self.order.project_version)%split_num):])
        self.product_ver_label.setText("\r\n".join(product_ver))
        self.project_name_label.setText(self.order.project_name)
        self.product_count_label.setText(str(self.order.getProductTotal()))
        self.material_code_label.setText(self.order.material_id)
        self.erp_material_id_label.setText(self.order.erp_material_id)

    def stationInfoInit(self):
        self.station_type_label.setText(self.cfg.getStationInfo())
        self.station_flow_label.setText(self.cfg.getStationFlowInfo())
        self.dc_address_label.setText(self.cfg.dc_gpib_addr +"  通道:%s"%(str(self.cfg.dc_channle)))
        self.cmw_addr_label.setText("%s   slot:%s"%(self.cfg.cmw_ip_addr, str(self.cfg.cmw_slot)))

        self.station_num_label.setText(str(self.cfg.station_num))

        if int(self.cfg.station_type) == 0 or self.cfg.factory_mes_enable is False or self.cfg.line_num == "无":
            self.line_num_label.setVisible(False)
            self.linenum_txt_label.setVisible(False)
        else:
            self.line_num_label.setVisible(True)
            self.linenum_txt_label.setVisible(True)
            self.line_num_label.setText("TEST%s_功能测试"%(self.cfg.line_num))

    def elapsed_handle(self):
        self.elapse_cnt += 1
        self.elapsed_time_label.setText(str(self.elapse_cnt)+'秒')

    def appUpdateShow(self):
        app_update_view = AppUpdateView()
        app_update_view.show()
        status = app_update_view.exec()

        if status == 0:
            self.pruduct_ctrl.quit()
            self.main_win.close()

    def systemFaultHandle(self, info):
        self.msgBox(info["info"])
        self.main_win.close()

    def imeiEditFinished(self):
        # print(Utils.isImei(self.imei_edit.text()) , self.imei_edit_timer.isActive())
        if len(self.imei_edit.text().strip()) > 15:
            self.imei_edit.setText(self.imei_edit.text().strip()[-15:])

        if Utils.isImei(self.imei_edit.text()) and not self.imei_edit_timer.isActive():
            self.setProductResLabel(ProductMainView.PRODUCT_RES_IDLE)
            self.imei_edit_timer.start(20*1000)

    def imeiEditTimerHandle(self):
        self.imei_edit_timer.stop()
        self.imei_edit.clear()
        self.productResultHandle({"res":False, "is_complete":True, "info": "IMEI: 接收IMEI后等待设备接入超时"})
        # self.setProductResLabel(ProductMainView.PRODUCT_RES_FAIL)

    def clearProductInfo(self):
        #     clear UI
        self.pruduct_ctrl.clearInfo()
        self.pruductInfoUpdata()

    def clearProductInfoOnClicked(self):
        qmsg = QMessageBox()
        replay = qmsg.question(self.main_win, "警告", "确认清除历史生产信息？", QMessageBox.Yes|QMessageBox.No)
        if replay == QMessageBox.Yes:
            print("删除历史信息")
            self.clearProductInfo()
        else:
            print("取消删除")

    def createInfoRightMenu(self):
        self.gbox_menu = QMenu()
        self.clear_action = QAction("清除信息", self)
        self.gbox_menu.addAction(self.clear_action)
        self.clear_action.triggered.connect(self.clearProductInfoOnClicked)
        self.gbox_menu.popup(QCursor.pos())

    def __init__(self):
        super().__init__()
        app = QtWidgets.QApplication(sys.argv)
        self.main_win = CloseEventQMainWindow()
        super().setupUi(self.main_win)

        self.win_manager = WindowsManager()

        self.res_info_list = []
        self.product_info_text.setStyleSheet("background-color:white")
        self.product_info_text.ensureCursorVisible()

        self.cab_loss_notify = None

        self.auto_update = AutoUpdateView()
        self.auto_update.show()
        res = self.auto_update.exec()
        if res == 0:
            self.main_win.close()
            sys.exit(0)

        self.mes = Mes()
        self.cfg = ToolConfig()

        self.login_view = MesLoginView(self.mes, self.cfg)
        self.login_view.setWindowTitle(self.login_view.windowTitle() + "  " + Utils.getAppVersion())
        self.login_view.show()
        self.login_view.exec()

        self.order_view = OrderView(self.mes, self.cfg)
        self.order_view.setWindowTitle(self.order_view.windowTitle() + "  " + Utils.getAppVersion())
        self.order_view.show()
        self.order_view.exec()

        self.config_view = ConfigView(self.mes.getActiveOrder(), self.cfg)
        self.config_view.setWindowTitle( self.config_view.windowTitle()+"  "+Utils.getAppVersion() )
        self.config_view.show()
        self.config_view.exec()

        self.burn_view = Main_ui(self.mes, self.cfg)
        self.burn_view.setWindowTitle( self.burn_view.windowTitle()+"  "+Utils.getAppVersion() )
        self.burn_view.show()
        self.burn_view.exec()

        # self.setProductResLabel(ProductMainView.PRODUCT_RES_IDLE)
        # self.produce_res = True
        # self.elapse_cnt = 0
        # self.order = self.mes.getActiveOrder()
        #
        # self.orderInfoInit()
        # self.stationInfoInit()
        # self.pruduct_ctrl = ProductMainController(self.mes, self.cfg)  # 产品的配置
        #
        # if "EG" in self.mes.getActiveOrder().module_platform:
        #     if int(self.cfg.station_type) == 2:
        #         self.port_manager = AtPortManager("USB 串行设备")
        #     else:
        #         self.port_manager = AtPortManager("USB 串行设备", at_check_en= True)
        #     self.port_manager.device_detect_signal.connect(self.portChageHandle)
        #     loss_check_res,loss_check_info = EcSlot.checkLosssetEnabel(self.mes.getActiveOrder().fw_version_name)
        #
        #     if int(self.cfg.station_type) != 2 and loss_check_res is False:
        #         self.msgBox(loss_check_info+",请重新测试线损")
        #         while True:
        #             self.losset_view = EcLossView(self.mes, self.cfg)
        #             self.cab_loss_notify = self.losset_view
        #             self.losset_view.setWindowTitle(self.losset_view.windowTitle() + "  " + Utils.getAppVersion())
        #             self.losset_view.show()
        #             self.losset_view.exec()
        #             loss_check_res, loss_check_info = EcSlot.checkLosssetEnabel(
        #                 self.mes.getActiveOrder().fw_version_name)
        #             if loss_check_res:
        #                 sys.exit()
        #     self.cab_loss_notify = None
        #     self.pruduct_ctrl = ProductEcMainController(self.mes, self.cfg)
        # else:
        #     if int(self.cfg.station_type) == 2:
        #         self.port_manager = AtPortManager("ASR Serial Download Device")
        #     else:
        #         self.port_manager = AtPortManager()
        #     self.port_manager.device_detect_signal.connect(self.portChageHandle)
        #
        #     self.pruduct_ctrl = ProductMainController(self.mes, self.cfg)  # 产品的配置
        # self.pruductInfoUpdata()
        # self.resInfoAppend("等待设备接入")

        # self.main_win.setWindowTitle(self.main_win.windowTitle())

        # self.tool_version_label.setStyleSheet("background-color:red")
        # self.tool_version_label.setText(Utils.getAppVersion())

        # self.elapsed_timer = QTimer(self)
        # self.elapsed_timer.timeout.connect(self.elapsed_handle)
        #
        # if int(self.cfg.station_type) != 2:
        #     self.imei_edit_timer = QTimer()
        #     self.imei_edit_timer.timeout.connect(self.imeiEditTimerHandle)
        #
        #     # self.imei_edit.editingFinished.connect(self.imeiEditFinished)
        #     self.imei_edit.textChanged.connect(self.imeiEditFinished)
        # self.product_info_gbox.customContextMenuRequested.connect(self.createInfoRightMenu)
        # self.pruduct_ctrl.pruduct_result_signal.connect(self.productResultHandle)
        # self.pruduct_ctrl.system_fault_signal.connect(self.systemFaultHandle)
        # self.app_update_action.triggered.connect(self.appUpdateShow)
        #
        # # 设置固定窗口
        # self.main_win.setFixedSize(self.main_win.width(), self.main_win.height())
        # self.main_win.show()
        # app.exec_()
        # self.pruduct_ctrl.quit()
        # self.port_manager.stop()
        # sys.exit()
