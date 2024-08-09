from device.at_device import  AtDevice
from device.dc_device import DcDevice
import common.utils as Utils
import time,logging,threading
from device.dut import Dut


class EcDut(Dut):
    def __init__(self, com_port, update_authid = True):
        Dut.__init__(self, com_port, update_authid=update_authid)

    def writeImei(self, imei):
        if Utils.isImei(imei) is False:
            raise Exception("IMEI: IMEI 规则检查出错: " + imei)

        res, _ = self.at_dev.writeCmd("AT+ECCGSN=\"IMEI\",\"%s\"\r\n"%(imei))
        if res is False:
            raise Exception("AtDevice: 写IMEI出错")
        self.checkImei(imei)

    def checkImei(self, imei):
        rimei = self.getImei()
        if not Utils.isImei(rimei) or not rimei.__eq__(imei):
            raise Exception("IMEI: 检查IMEI出错 QR: %s read imei:%s " % (imei, rimei))

    def getImei(self):
        cmd = b"AT+CGSN=1\r\n"
        res, data = self.at_dev.writeCmd(cmd, waitRes="+CGSN: ")
        if res is False or data is None:
            raise Exception("AtDevice: 获取IMEI指令写入出错")
        rimei = data.replace("\"", "")
        return rimei

    def factoryMode(self):
        cmd = b"AT+FPROD=1\r\n"
        res, _ = self.at_dev.writeCmd(cmd)
        if res is False:
            raise Exception("AtDevice: 进入工厂模式出错")

    def checkLteCal(self):
        cmd = b"AT+ECNPICFG?\r\n"
        res, data = self.at_dev.writeCmd(cmd, waitRes="+ECNPICFG: ")
        if res is False or data is None:
            raise Exception("AtDevice: 获取IMEI指令写入出错")
        data = data.replace(" ", "")
        if "\"rfCaliDone\":1" not in data:
            raise Exception("校准信息缺失")
        if "\"rfNSTDone\":1" not in data:
            raise Exception("综测信息缺失")

    def checkRndisEnumEnable(self):
        cmd = b"AT+ECPCFG?\r\n"
        res, data = self.at_dev.writeCmd(cmd, waitRes="+ECPCFG: ")
        if res is False or data is None:
            raise Exception("AtDevice: 获取ECPCFG指令出错")
        data = data.replace(" ", "")
        if "\"usbCtrl\":0" not in data:
            cmd = b"AT+ECPCFG=\"usbCtrl\",0\r\n"
            res, data = self.at_dev.writeCmd(cmd)
            cmd = b"AT+ECPCFG?\r\n"
            res, data = self.at_dev.writeCmd(cmd, waitRes="+ECPCFG: ")
            if res is False or data is None:
                raise Exception("AtDevice: 获取ECPCFG指令出错")
            data = data.replace(" ", "")
            if "\"usbCtrl\":0" not in data:
                raise Exception("AtDevice: 配置RNDIS enable出错")

if __name__ == "__main__":
    ec_dut = EcDut("COM90", update_authid=False)
    # ec_dut.writeImei("869734053181990")
    # ec_dut.checkLteCal()
    print(ec_dut.checkRndisEnumEnable())
    ec_dut.destory()