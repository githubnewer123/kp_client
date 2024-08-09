from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject,Qt,QObject,QRegExp
from PyQt5.QtGui import QPixmap,QImage,QTransform,QPalette,QRegExpValidator
from PyQt5.QtWidgets import QMessageBox,QDialog,QHeaderView
from UI.UI_config_load import Ui_toolConfigDialog
import sys,os,logging
from device.dc_device import DcDevice
from device.usb_device import UsbDevice
from mes.order import Order
from manager.tool_config import ToolConfig
from mes.file_downloader import FileDownloader

class CloseEventQDialog(QDialog):
    def closeEvent(self, event):
        logging.info("Close by user")
        sys.exit(-1)

class ConfigView(CloseEventQDialog, QObject):

    def msgBox(self,info):
        qmsg = QMessageBox()
        # qmsg.setWindowIcon()
        qmsg.question(self,"警告",info,QMessageBox.Ok)

    def msgBoxError(self,info):
        qmsg = QMessageBox()
        qmsg.critical(self,"错误",info,QMessageBox.Ok)

    def comboxInit(self):

        self.child.mmpt_slot_total_cbox.addItems(["1","4","8"])
        self.child.mmpt_slot_total_cbox.setCurrentIndex(0)
        self.child.mmpt_slot_total_cbox.setEnabled(False)

        self.child.work_type_cbox.addItems([self.work_type_dict[name] for name in self.work_type_dict.keys()])

        checkbox_lists = [self.cal_checkbox_list, self.nst_checkbox_list]

        for checkbox_list in checkbox_lists:
            for key in checkbox_list.keys():
                # 先判断订单状态，订单是True 锁定选项
                if checkbox_list[key][0]:
                    key.setChecked(True)
                    if self.order.isProductOrder():
                        key.setEnabled(False)
                elif checkbox_list[key][1]:
                    # 判断用户上次配置 如果为TRUE  选中不锁定
                    key.setChecked(True)

        self.nstCheckBoxEnable(False)

        self.child.gpib_addr_cbox.addItems([str(i) for i in range(0,11)])
        self.child.instr_cbox.addItems([str(i) for i in range(0, 11)])
        addr = self.config.dc_gpib_addr
        if not addr.startswith("GPIB") or not addr.endswith("INSTR"):
            self.child.gpib_addr_cbox.setCurrentIndex(0)
            self.child.instr_cbox.setCurrentIndex(5)
        else:
            self.child.gpib_addr_cbox.setCurrentIndex(int(addr[4:addr.index("::")]))
            self.child.instr_cbox.setCurrentIndex(int(addr.split("::")[1]))

        self.child.dc_source_ch_cbox.addItems(["1", "2"])
        self.child.dc_source_ch_cbox.setCurrentIndex(int(self.config.dc_channle)-1)

        self.child.cmw_slot_cbox.addItems(["0", "1"])
        self.child.cmw_slot_cbox.setCurrentText(str(self.config.cmw_slot))

        self.child.station_num_cbox.addItems(["%02d"%(i) for i in range(1,100)])
        self.child.station_num_cbox.setCurrentText(str(self.config.station_num))

        if int(self.config.station_type) == 0:
            # 校准工位
            self.child.work_type_cbox.setCurrentIndex(0)
            self.child.work_type_cbox.setEnabled(False)
            self.child.station_num_cbox.setEnabled(False)
            self.child.cal_groupBox.setVisible(True)
            self.child.nst_groupBox.setVisible(False)
        elif int(self.config.station_type) == 1:
            # 测试工位
            self.child.work_type_cbox.setCurrentIndex(1)
            self.child.work_type_cbox.setEnabled(False)
            self.child.station_num_cbox.setEnabled(False)
            self.child.cal_groupBox.setVisible(False)
            self.child.nst_groupBox.setVisible(True)
        elif int(self.config.station_type) == 2:
            self.child.work_type_cbox.setCurrentIndex(2)
            self.child.work_type_cbox.setEnabled(False)
            self.child.station_num_cbox.setEnabled(False)
            self.child.cal_groupBox.setVisible(False)
            self.child.nst_groupBox.setVisible(False)
        else:
            self.child.work_type_cbox.setCurrentIndex(0)
            self.child.work_type_cbox.setEnabled(True)
            self.child.station_num_cbox.setEnabled(True)

        self.workTypeChangeEvent(self.child.work_type_cbox.currentIndex())
        self.child.line_num_cbox.addItem("无")
        self.child.line_num_cbox.addItems("%03d"%(i) for i in range(0,30))
        self.child.line_num_cbox.setCurrentText(self.config.line_num)

    def calCheckboxEnable(self, enable):
        for checkbox in self.cal_checkbox_list.keys():
            if enable is False or self.cal_checkbox_list[checkbox][0] is False or self.order.isProductOrder():
                checkbox.setEnabled(False)
            else:
                checkbox.setEnabled(enable)

    def nstCheckBoxEnable(self, enable):
        for checkbox in self.nst_checkbox_list.keys():
            if enable is False or self.nst_checkbox_list[checkbox][0] is False or self.order.isProductOrder():
                checkbox.setEnabled(False)
            else:
                checkbox.setEnabled(enable)

    def workTypeChangeEvent(self, index):
        # index = self.child.work_type_cbox.currentIndex()
        if self.cur_work_type == index:
            return
        self.cur_work_type = index
        if index == 0 or index == 1:
            self.setRfToolDownload()
        else:
            self.setBurnDownload()

        if index == 0:
        # 校准工位
            self.nstCheckBoxEnable(False)
            self.calCheckboxEnable(True)
            self.child.line_num_cbox.setVisible(False)
            self.child.line_num_label.setVisible(False)
            self.child.cal_groupBox.setVisible(True)
            self.child.nst_groupBox.setVisible(False)
        elif index == 1:
        # 测试工位
            self.child.cal_groupBox.setVisible(False)
            self.child.nst_groupBox.setVisible(True)
            self.nstCheckBoxEnable(True)
            self.calCheckboxEnable(False)
            if self.child.line_num_cbox.isEnabled():
                self.child.line_num_cbox.setVisible(True)
                self.child.line_num_label.setVisible(True)
        elif index == 2:
            self.child.cal_groupBox.setVisible(False)
            self.child.nst_groupBox.setVisible(False)
            self.calCheckboxEnable(False)
            self.nstCheckBoxEnable(False)

    def dcSourceTest(self):
        addr = "GPIB%s::%s::INSTR"%(self.child.gpib_addr_cbox.currentText(), self.child.instr_cbox.currentText())
        ch = int(self.child.dc_source_ch_cbox.currentText())
        try:
            DcDevice.GPIB_test(addr, ch)
            self.msgBox("电源已经成功打开,请将仪器显示界面切换到通道[%d]后,确认该通道的电压有在变化"%(ch))
        except Exception as e:
            self.msgBoxError("通过GPIB地址[%s] 通道[%d] 打开电源失败！\n请检查GPIB线正常连接到仪器,确认GPIB地址配置正确后重试"%(addr, ch))

    def okBtnClicked(self):
        # try:
            # if self.config.db_file_update is True and self.order.db_downloader and self.order.db_downloader.status() != FileDownloader.DOWNLOAD_PRCESS_UNZIP_COMPLETE:
            #     self.msgBox("MMPT 配置文件未下载完成，请稍候确认！\nDB文件未完成 ")
            #     return
            # if self.config.scrip_file_update is True and self.order.config_downloader and self.order.config_downloader.status() != FileDownloader.DOWNLOAD_PRCESS_UNZIP_COMPLETE:
            #     self.msgBox(
            #         "MMPT 配置文件未下载完成，请稍候确认！\n配置文件未完成")
            #     return
            #
            # if self.config.mmpt_tool_update is True and self.order.mmpt_downloader and self.order.mmpt_downloader.status() != FileDownloader.DOWNLOAD_PRCESS_UNZIP_COMPLETE:
            #     self.msgBox(
            #         "MMPT 配置工具未下载完成，请稍候确认！\n配置文件未完成")
            #     return

            # if self.child.work_type_cbox.currentIndex() != 2 and self.order.nst_adc_dc_en and self.adcDetected is False:
            #     self.msgBox("请插入中云提供的adc校准模块")
            #     return

            # if self.usb_dev:
            #     self.usb_dev.stopDeviceDetect()
            #     self.usb_dev.close()
            #
            # self.config.order_id = self.order.order_id
            # self.config.fw_version_name = self.order.fw_version_name
            # self.config.download_process = self.order.download_process
            # self.config.process_total_count = self.order.process_count
            # self.config.rf_tool_version = self.order.mmpt_version_name
            # self.config.project_version = self.order.project_version
            # self.config.configNst(self.order.rf_check_lte, self.order.rf_check_gsm, self.order.nst_adc_dc_en, self.order.test_adc_flag, self.order.test_io)
            # if self.child.line_num_cbox.currentText() == "无":
            #     self.config.factory_mes_enable = False
            #     self.config.line_num = "无"
            # else:
            #     self.config.factory_mes_enable = True
            #     self.config.line_num = self.child.line_num_cbox.currentText()
            #
            # self.config.configFactoryMes()
            # # configBoolWrite(cal_lte,cal_gsm, cal_imei,cal_adc,cal_auth,cal_sn,nst_lte,nst_gsm,nst_imei,nst_adc,nst_auth,nst_sn):
            # self.config.configBoolWrite(self.child.cal_lte_check.isChecked(), self.child.cal_gsm_check.isChecked(), self.child.cal_imei_check.isChecked(),
            #                             self.child.cal_adc_check.isChecked(),self.child.cal_auth_check.isChecked(), self.child.cal_sn_check.isChecked(),
            #                             self.child.nst_lte_check.isChecked(), self.child.nst_gsm_check.isChecked(), self.child.nst_imei_check.isChecked(),
            #                             self.child.nst_adc_check.isChecked(), self.child.nst_auth_check.isChecked(), self.child.nst_sn_check.isChecked())
            # # configStrWrite(self, gpib_addr, channel, station_type):
            # self.config.configStrWrite("GPIB%s::%s::INSTR"%(self.child.gpib_addr_cbox.currentText(),self.child.instr_cbox.currentText()),
            #                            self.child.dc_source_ch_cbox.currentText(), str(self.child.work_type_cbox.currentIndex()),self.child.station_num_cbox.currentText(),
            #                            self.child.cmw_ip_edit.text(), self.child.cmw_slot_cbox.currentText())
            # self.config.mmpt_version = self.order.mmpt_version_name

        # except Exception as e:
        #     self.msgBox(str(e))
        #     return
            self.hide()


    def dbDownloadUpdate(self, progress):
        self.child.download_1_progressbar.setValue(int(progress))
        if progress == 100:
            self.db_config_done = True
        elif progress == -1:
            self.msgBoxError("下载出错, 请退出确认")
            sys.exit(-1)
        if self.db_config_done and self.md_config_done and self.mmpt_config_done:
            self.child.OK_btn.setEnabled(True)

    def scriptDownloadUpdate(self, progress):
        self.child.download_2_progressbar.setValue(int(progress))
        if progress == 100:
            self.md_config_done = True
        elif progress == -1:
            self.msgBoxError("下载校准配置文件出错, 请退出确认")
            sys.exit(-1)
        if self.db_config_done and self.md_config_done and self.mmpt_config_done:
            self.child.OK_btn.setEnabled(True)

    def mmptDownloadUpdate(self, progress):
        self.child.download_3_progressbar.setValue(int(progress))
        if progress == 100:
            self.mmpt_config_done = True
        if self.db_config_done and self.md_config_done and self.mmpt_config_done:
            self.child.OK_btn.setEnabled(True)

    def fwDownloadUpdate(self, progress):
        self.child.download_2_progressbar.setValue(int(progress))
        if progress == 100:
            self.fw_config_done = True
        elif progress == -1:
            self.msgBoxError("下载固件出错, 请退出确认")
            sys.exit(-1)
        if self.aboot_config_done and self.fw_config_done:
            self.child.OK_btn.setEnabled(True)

    def cfgDownloadUpdate(self, progress):
        self.child.download_2_progressbar.setValue(int(progress))
        if progress == 100:
            self.fw_config_done = True
        elif progress == -1:
            self.msgBoxError("下载config出错, 请退出确认")
            sys.exit(-1)
        if self.aboot_config_done and self.fw_config_done:
            self.child.OK_btn.setEnabled(True)

    def abootDownloadUpdate(self, progress):
        self.child.download_1_progressbar.setValue(int(progress))
        if progress == 100:
            self.aboot_config_done = True
        elif progress == -1:
            self.msgBoxError("下载Aboot, 请退出确认")
            sys.exit(-1)
        if self.aboot_config_done and self.fw_config_done:
            self.child.OK_btn.setEnabled(True)


    def resetConfigClicked(self):
        self.child.station_num_cbox.setEnabled(True)
        self.child.work_type_cbox.setEnabled(True)
        self.child.line_num_cbox.setEnabled(True)
        self.config.fac_mes_success_total = 0
        self.config.fac_mes_false_total = 0

    def usbDeviceDetect(self, info):
        if info:
            self.adcDetected = True
            color = "background-color:green"
            text = "已连接"
            logging.debug('Set online status')

        else:
            self.adcDetected = False
            logging.debug('Set offline status')
            color = "background-color:red"
            text = "未连接"

        self.child.adc_detect_label.setStyleSheet(color)
        self.child.adc_detect_label.setText(text)

    def setRfToolDownload(self):
        # print(666666,self.config.db_file_update,self.order.db_downloader,self.config.scrip_file_update,self.order.config_downloader,self.config.mmpt_tool_update,self.order.mmpt_downloader)
        if self.config.db_file_update and self.order.db_downloader:
            self.child.dl_label_1.setText("DB下载: ")
            self.child.OK_btn.setEnabled(False)
            self.order.db_downloader.download_progresss_signal.connect(self.dbDownloadUpdate)
            self.order.db_downloader.start()
            self.db_config_done = False
        else:
            self.child.download_1_progressbar.setEnabled(False)

        if self.config.scrip_file_update is True and self.order.config_downloader:
            self.child.dl_label_2.setText("脚本下载: ")
            self.child.OK_btn.setEnabled(False)
            self.order.config_downloader.download_progresss_signal.connect(self.scriptDownloadUpdate)
            self.order.config_downloader.start()
            self.md_config_done = False
        else:
            self.child.download_2_progressbar.setEnabled(False)

        if self.config.mmpt_tool_update is True and self.order.mmpt_downloader:
            self.child.OK_btn.setEnabled(False)
            self.child.dl_label_3.setVisible(True)
            self.child.dl_label_3.setText("MMPT下载: ")
            self.child.download_3_progressbar.setVisible(True)
            self.order.mmpt_downloader.download_progresss_signal.connect(self.mmptDownloadUpdate)
            self.order.mmpt_downloader.start()
            self.mmpt_config_done = False
            pass
        else:
            self.child.download_3_progressbar.setEnabled(False)

    def setBurnDownload(self):
        self.child.dl_label_1.setText("固件下载: ")
        self.child.dl_label_2.setText("配置文件:")# ("工具下载: ")
        self.child.dl_label_1.setVisible(False) ###
        self.child.download_1_progressbar.setVisible(False) ###
        self.child.dl_label_3.setVisible(False)
        self.child.download_3_progressbar.setVisible(False)
        self.child.OK_btn.setEnabled(False)
        # self.order.aboot_downloader.download_progresss_signal.connect(self.abootDownloadUpdate)
        # self.order.fw_downloader.download_progresss_signal.connect(self.fwDownloadUpdate)
        self.order.config_downloader.download_progresss_signal.connect(self.cfgDownloadUpdate)
        # self.order.aboot_downloader.start()
        # self.order.fw_downloader.start()
        self.order.config_downloader.start()

    def __init__(self, order, config):
        QDialog.__init__(self)
        self.child = Ui_toolConfigDialog()
        self.child.setupUi(self)

        self.order = order
        self.config = config

        self.work_type = {}
        self.work_type_dict = {0:"校准工位",1:"测试工位", 2:"烧录工位"}
        self.cur_work_type = int(self.config.station_type)

        # self.cal_checkbox_list = {self.child.cal_lte_check:[self.order.cal_lte, self.config.cal_lte], self.child.cal_gsm_check:[self.order.cal_gsm, self.config.cal_gsm],
        #             self.child.cal_adc_check:[self.order.cal_adc,self.config.cal_adc],self.child.cal_imei_check:[self.order.cal_imei, self.config.cal_imei],
        #             self.child.cal_sn_check:[self.order.cal_sn,self.config.cal_sn],self.child.cal_auth_check:[self.order.cal_auth,self.config.cal_auth]}
        # self.nst_checkbox_list = {self.child.nst_lte_check: [self.order.nst_lte,self.config.nst_lte], self.child.nst_gsm_check: [self.order.nst_gsm,self.config.nst_gsm],
        #             self.child.nst_adc_check: [self.order.nst_adc,self.config.nst_adc], self.child.nst_imei_check: [self.order.nst_imei,self.config.nst_imei],
        #             self.child.nst_sn_check: [self.order.nst_sn,self.config.nst_sn], self.child.nst_auth_check: [self.order.nst_auth,self.config.nst_auth]}
        # self.comboxInit()
        # self.child.cmw_ip_edit.setText(self.config.cmw_ip_addr)
        # ip_addr_exp = QRegExp('^((2[0-4]\d|25[0-5]|[1-9]?\d|1\d{2})\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?):\d{1,5}$')
        # self.child.cmw_ip_edit.setValidator(QRegExpValidator(ip_addr_exp, self))
        # self.child.work_type_cbox.currentIndexChanged.connect(self.workTypeChangeEvent)


        # if self.order.nst_adc_dc_en and (self.child.cal_adc_check.isChecked() or self.child.nst_adc_check.isChecked()):
        #     self.adcDetected = False
        #     self.usb_dev = UsbDevice()
        #     self.usb_dev.device_detect_signal.connect(self.usbDeviceDetect)
        #     self.usb_dev.startDeviceDetect()
        # else:
        #     self.adcDetected = True
        #     self.usb_dev = None

        # self.child.dc_test_btn.clicked.connect(self.dcSourceTest)
        self.child.OK_btn.clicked.connect(self.okBtnClicked)
        # self.child.reset_btn.clicked.connect(self.resetConfigClicked)

        self.db_config_done = True
        self.md_config_done = True
        self.mmpt_config_done = True

        self.aboot_config_done = True
        self.fw_config_done = True

        if int(self.config.station_type) == 0 or int(self.config.station_type) == 1:
            self.setRfToolDownload()
        else:
            self.setBurnDownload()

        # if not self.child.line_num_cbox.currentText() == "无":
        #     self.child.line_num_cbox.setEnabled(False)
        #
        # if int(self.config.station_type) == 0:
        #     self.child.line_num_cbox.setVisible(False)
        #     self.child.line_num_label.setVisible(False)









