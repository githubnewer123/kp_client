import pyvisa as visa
import  time,logging,struct
import pyvisa.constants as constants
# from device.usb_device import UsbDevice #手动注释

class DcDevice:
    __addr_list = []
    __instance_list = []

    @staticmethod
    def GPIB_test(address, ch):
        "DcSource.GPIB_TEST([GPIB_number, instrt_num, ch])"
        # self.pb.configure(text=str(number+1)+"号GPIB地址测试开始")
        # GPIB_data_number = self.GPIB_get()[number]
        # if len(gpib_num) != 3:
        #     return False
        # address = "GPIB" + str(gpib_num[0]) + "::" + str(gpib_num[1]) + "::INSTR"
        voltage = 1.8

        powerDev = DcDevice(address)
        powerDev.on(ch)
        for i in range(5):
            time.sleep(0.5)
            powerDev.setVolt(float(voltage) - 0.1 * i, ch)
        powerDev.setVolt(float(voltage), ch)

        # self.pb.configure(text=str(number+1)+"号GPIB地址测试成功")
    def getAdcVal(self):
        ret, data = self.usb_dev.write(b"\xF0\x30\x00\x00\x00")
        val = 0
        if ret == 97:
            val = struct.unpack('<h', data[0:2])[0]
        return round(val/1000, 3)

    def adcDevReboot(self):
        ret, data = self.usb_dev.write(b"\xF0\x31\x00\x00\x00", timeout=1)
        # print("Adc reboot: ",ret, data)
        return True if ret == 97 else False


    def __init__(self, address,max_volt = 1.8):
        self.max_volt = max_volt
        self.usb_dev = None
        self.usb_dev = UsbDevice()
        dev_list = self.usb_dev.getDeviceList()
        if len(dev_list) == 0:
            raise Exception("ADC校准模块断开连接")
        self.usb_dev.open(dev_list[0])

        if address in DcDevice.__addr_list:
            self.gpib_inst = DcDevice.__instance_list[DcDevice.__addr_list.index(address)]
            return None

        rm = visa.ResourceManager()  # 获取visa资源，将python的visa和系统visa关联起来
        self.gpib_inst = rm.open_resource(address, open_timeout=5)  # 打开GPIB地址连接
        logging.info(self.gpib_inst.query('*IDN?'))  # 查询仪器型号
        DcDevice.__addr_list.append(address)
        DcDevice.__instance_list.append(self.gpib_inst)

    def destory(self):
        if self.usb_dev:
            self.adcDevReboot()
            self.usb_dev.close()

    def on(self, ch=1):
        self.gpib_inst.write("OUTP%d ON" % (ch))  # 打开供电开关

    def off(self, ch=1):
        self.gpib_inst.write("OUTP%d OFF" % (ch))  # 关闭供电开关

    def setMaxVolt(self, volt):
        self.max_volt = volt

    def setVolt(self, volt,ch=1):
        cnt = 3
        if volt > self.max_volt:
            raise Exception("ADC: 电源电压设置过高 最大电压: %f 设置电压: %f"%(self.max_volt, volt))
        while cnt > 0:
            try:
                self.gpib_inst.write("VOLT"+str(ch)+" %f" % (volt))
                ret = self.gpib_inst.query("VOLT" + str(ch) + "?")

                if float(ret) - volt < 0.5 and float(ret) - volt > -0.5:
                    time.sleep(0.02)
                    if self.usb_dev is not None:
                        val = self.getAdcVal()
                        if (val - volt) > 0.100 or (val - volt) < -0.100:
                            logging.info("Set val: %d read val: %d"%(volt*1000,val))
                            raise Exception("ADC: Error")
                        # print("Set val: %d read val: %d"%(volt*1000,val))
                        return val
                    else:
                        return volt
            except Exception as e:
                time.sleep(.200)
                logging.info(str(e))
                cnt -= 1
        else:
            raise Exception("ADC: 设置电压偏差超过100mv")


    def getVolt(self,ch=1):
        ret = self.gpib_inst.query("VOLT"+str(ch)+"?")
        return float(ret)

