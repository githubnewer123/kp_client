from device.at_device import  AtDevice
from device.dc_device import DcDevice
import common.utils as Utils
import time,logging,threading
from device.dut import Dut


class DutModem2(Dut):

    def __init__(self, com_port = None, update_authid = True):
        if com_port is None:
            port_list = AtDevice.getAtPortList("ASR Modem Device 2")
            if len(port_list) == 0:
                raise Exception("Auto get modem AT 2 device ERROR")
            com_port = port_list[0][0]
        Dut.__init__(self, com_port, update_authid=False, default_cmd = False)

    def checkTr3bHW(self):
        res, datas = self.at_dev.writeCmd("AT+TR3B_TEST\r\n", "+TR3B_TEST:")
        if res is False or "ERROR" in datas:
            self.at_dev.destory()
            raise Exception("TR3B test error: %s"%(datas))
        self.at_dev.destory()
        return datas


