from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject,Qt,QObject,QRegExp,pyqtSignal
from PyQt5.QtGui import QPixmap,QImage,QTransform,QPalette,QRegExpValidator
from PyQt5.QtWidgets import QMessageBox,QDialog,QHeaderView
from UI.ec_losset import Ui_ec_loss_dialog
import sys,os,logging,threading,datetime
from device.dc_device import DcDevice
from device.usb_device import UsbDevice
from manager.ec_slot import EcSlot
from device.ec_dut import EcDut

class CloseEventQDialog(QDialog):
    def closeEvent(self, event):
        logging.info("Close by user")
        sys.exit(-1)

class EcLossView(CloseEventQDialog, QObject):
    cal_loss_signal = pyqtSignal(dict)
    def getTimestamp(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def msgBox(self,info):
        qmsg = QMessageBox()
        # qmsg.setWindowIcon()
        qmsg.question(self,"警告",info,QMessageBox.Ok)

    def msgBoxError(self,info):
        qmsg = QMessageBox()
        qmsg.critical(self,"错误",info,QMessageBox.Ok)
        self.hide()

    def resInfoAppend(self, info):
        if info.startswith("----"):
            self.res_info_list.append(info)
        else:
            self.res_info_list.append("[%s] %s" % (self.getTimestamp(), info))
        if len(self.res_info_list) > 15:
                self.res_info_list = self.res_info_list[-15:]
        info = ""
        for txt in self.res_info_list:
            info += txt+"\r\n"
        self.child.info_label.setText(info)

    def processResHandle(self, info):
        self.resInfoAppend(info["msg"])
        if info["res"] :
            if info["is_completed"] :
                self.msgBox(info["msg"])
                # self.slot
                self.hide()
        else:
            self.msgBoxError(info["msg"])

    def fwCheck(self, fw_1):
        if not self.cfg.fw_version_name[:5].__eq__(fw_1[:5]):
            return False
        return True

    def waitDevPoweron(self):
        while True:
            try:
                self.start_event.clear()
                self.start_event.wait()
                port = self.port_list[0][0]
                dut = EcDut(port, update_authid=False)
                imei = dut.getImei()
                fw = dut.at_dev.fwVersion()
                dut.destory()
            except Exception as e:
                self.msgBox("请重试: %s" % (str(e)))
                continue
            if self.fwCheck(fw) is False:
                self.msgBox("请使用订单同平台(%s)金板测试"%(self.cfg.fw_version_name[:5]))
                continue
            else:
                return fw,imei

    def __process(self):
        loop_cnt = 0
        fw_1, imei_1 = self.waitDevPoweron()
        self.slot.start(self.port_list[0][0])
        self.cal_loss_signal.emit({"res": True, "msg": "使用第一块金板开始测试，请等待....", "loop_cnt": 1, "is_completed": False})
        res, msg = self.slot.waitComplete()
        if res:
            self.first_loss = self.slot.lossUpdate()
            self.cal_loss_signal.emit({"res": res, "msg": "使用第一块金板开始测试成功!\n请放入第二块金板确认", "loop_cnt": 1, "is_completed": False})
        else:
            self.msgBoxError("运行出错!"+msg)

        while True:
            _,imei_2 = self.waitDevPoweron()
            if not imei_1.__eq__(imei_2):
                break
            else:
                self.cal_loss_signal.emit(
                    {"res": res, "msg": "不能使用相同金板测试,请再放入不同金板确认", "loop_cnt": 1, "is_completed": False})

        self.slot.start(self.port_list[0][0])
        self.cal_loss_signal.emit(
            {"res": res, "msg": "使用第二块金板开始测试，请等待....", "loop_cnt": 1, "is_completed": False})
        res, msg = self.slot.waitComplete()
        if res:
            self.second_loss = self.slot.lossUpdate()
            if self.second_loss is None:
                self.msgBoxError("运行出错!未找到线损输出文件" )
            self.cal_loss_signal.emit({"res": res, "msg": "使用第二块金板测试成功，开始计算线损", "loop_cnt": 2, "is_completed": False})
        else:
            self.msgBoxError("运行出错!"+msg)

        diff_res = True
        for band in self.first_loss.keys():
            first_list = self.first_loss[band].split(",")
            second_list = self.second_loss[band].split(",")
            # print(first_list, second_list)
            for idx in range(len(first_list)):
                diff = float(second_list[idx]) - float(first_list[idx])
                if diff > 0.6 or diff < -0.6:
                    msg = "[Thoushold 0.6]%s freq:%s/%s val:%s/%s diff: %f "%(band,first_list[idx - 1],second_list[idx - 1], first_list[idx],second_list[idx], diff )
                    # print(msg)
                    self.cal_loss_signal.emit({"res": True, "msg": msg, "is_completed": False})
                    diff_res = False
        if diff_res is False:
            self.cal_loss_signal.emit({"res": False, "msg": "两次结果校验出错", "is_completed": True})
            return
        print("Get Imei from Dut:" , imei_1)
        self.slot.lossSave(self.first_loss, fw_1, self.cfg.station_num)
        self.slot.stop()
        self.cal_loss_signal.emit({"res": True, "msg": "线损更新完成, 请重启工具！", "is_completed": True})

    def portChangeNotitfy(self, port_list):
        if len(port_list) > 0:
            logging.info("port start -> %s" % (port_list[0][0]))
            self.port_list = port_list
            self.start_event.set()
        else:
            self.start_event.clear()

    def __init__(self,mes, cfg):
        QDialog.__init__(self)
        self.child = Ui_ec_loss_dialog()
        self.child.setupUi(self)
        self.mes = mes
        self.cfg = cfg

        self.port_list = None
        self.slot = EcSlot(EcSlot.PROCESS_CAB_LOSS, self.cfg)
        self.start_event = threading.Event()
        self.start_event.clear()

        self.first_loss = None
        self.second_loss = None
        self.res_info_list = []
        self.cal_loss_signal.connect(self.processResHandle)
        self.processs = threading.Thread(target= self.__process, args=())
        self.processs.start()











