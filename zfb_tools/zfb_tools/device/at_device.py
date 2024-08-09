import time
import serial, threading
import serial.tools.list_ports

class AtDevice:
    # __open_port_list = []

    @staticmethod
    def getAtPortList(filter = "ASR Modem Device"):
        at_port_list = []
        for port in serial.tools.list_ports.comports():
            if filter in port[1]:
                at_port_list.append(port)
        return at_port_list.copy()

    @staticmethod
    def getAtPortListWithCheck(filter="ASR Modem Device"):
        at_port_list = []
        filt_port_list = []

        for port in serial.tools.list_ports.comports():
            if filter in port[1]:
                filt_port_list.append(port)
        if len(filt_port_list) <= 0:
            return filt_port_list

        filt_port_list.sort(key=lambda x: x[0])
        for port in filt_port_list[::-1]:
            try:
                dev = serial.Serial(port=port[0], timeout=.1)
                dev.write(b"AT\r\n")
                dat = dev.read(4)
                if b"OK" in dat or b"AT" in dat:
                    at_port_list.append(port)
                    dev.close()
                    break
                dev.close()
            except :
                pass
        return at_port_list.copy()

    @staticmethod
    def waitPortAvailable(port, timeout):
        stime = time.time()
        while True:
            if time.time() - stime > timeout:
                return False
            try:
                dev = serial.Serial(port=port)
                dev.close()
                return True
            except Exception:
                time.sleep(.500)

    def __init__(self, port, baudrate = 115200, read_timeout = 1, open_delay = 1):
        # if port in AtDevice.__open_port_list:
        #     raise Exception("AtDevice: 端口已经打开")

        self.port = port
        self.baudrate = baudrate
        self.read_timeout = 1
        if open_delay > 0:
            time.sleep(open_delay)

        self.dev = serial.Serial(port, baudrate,timeout=read_timeout)
        self.dev.isatty()
        # AtDevice.__open_port_list.append(port)

    def destory(self):
        if self.dev.isOpen():
            self.dev.close()
        # AtDevice.__open_port_list.remove(self.port)

    def ATE0(self):
        self.writeCmd(b"ATE0\r\n")

    def vbatAdcDel(self):
        self.writeCmd(b"AT*MRD_ADC=D\r\n")

    def waitData(self):
        stime = time.time()
        while True:
            if time.time() - stime > 10:
                raise Exception("AtCmd: wait data error")
            try:
                datas = self.dev.readline().strip().decode()
                print(datas)
            except Exception as e:
                raise Exception("CODEC: "+hex(datas))
            if len(datas) == 0:
                continue
            else:
                return datas

    def writeCmd(self, cmd, waitRes=None):
        if type(cmd) == str:
            cmd = cmd.encode()
        print("Send cmd:", cmd)
        self.dev.reset_input_buffer()
        self.dev.reset_output_buffer()
        res = self.dev.write(cmd + b"\r\n")
        if not res:
            raise Exception("AtDevice: write serial cmd error")
        res = ""
        while True:
            datas = self.waitData()
            if datas == None:
                continue
            if waitRes:
                if waitRes in datas:
                    res = datas.replace(waitRes, "")
                    datas = self.waitData()
                else:
                    continue
            if "OK" in datas:
                return (True, res)
            elif "ERROR" in datas or "error" in datas:
                return (False, res)
            else:
                res = res + datas +"\r\n"
                continue


    def writeData(self, cmd, sdata, dataFlag=">"):
        self.dev.reset_input_buffer()
        self.dev.reset_output_buffer()
        if type(cmd) == str:
            cmd = cmd.encode()
        self.dev.write(cmd + b"\r\n")

        while True:
            datas = self.dev.readline().strip().decode()
            if len(datas) == 0:
                continue

            if dataFlag in datas:
                self.dev.write(sdata)
                datas = self.waitData()
                if "OK" in datas:
                    return True
                elif "ERROR" in datas:
                    raise Exception("AtDevice: cmd response error")
            else:
                continue


    def readData(self, cmd):
        if type(cmd) == str:
            cmd = cmd.encode()
        self.dev.write(cmd + b"\r\n")
        res = None

        datas = ''
        while True:
            da = self.waitData()
            if da.__eq__("OK"):
                return (True, datas)
            elif da.__eq__("ERROR"):
                raise Exception("AtDevice: read data error")
            else:
                datas += da

    def getImei(self):
        cmd = b"AT*MRD_IMEI=R,0\r\n"
        res, data = self.writeCmd(cmd, waitRes="*MRD_IMEI")
        if res is False or data is None:
            raise Exception("AtDevice: 获取IMEI指令写入出错")
        items = data.split(",")
        if items is None or len(items) != 3:
            raise Exception("AtDevice: 从响应中获取IMEI出错")
        return items[-1]

    def checkGPIO(self):
        res, resp = self.writeCmd("AT+FTEST=\"GPIO\",1,1\r\n")
        if res is False or resp is None:
            raise Exception("GPIO: 测试GPIO出错,"+str(resp))

    def writeImei(self, imei):
        self.writeCmd("AT*MRD_IMEI=D,0\r\n")
        res,_ = self.writeCmd("AT*MRD_IMEI=W,0101,12NOV2010," + imei + ",0\r\n")
        if res is False:
            raise Exception("AtDevice: 写IMEI出错")

    def delAdc(self, type = ""):
        self.writeCmd("AT*MRD_%sADC=D\r\n"%(type))

    def factoryMode(self):
        self.writeCmd("AT*PROD=1\r\n")

    def writeAdcCal(self, index, volt, type = ""):
        cmd = "AT*MRD_%sADC=W,1000,08Jul2021,0,%d,%d\r\n" % (type, int(volt * 1000), index)
        self.writeCmd(cmd)

    def getAdc(self, type=""):
        cmd = "AT*MRD_%sADC=C\r\n" % (type)
        res, data = self.writeCmd(cmd, "*MRD_%sADC:" % (type))
        volt = int(data.split(":")[-1])
        return volt

    def checkAdcFlag(self, type=""):
        cmd = "AT*MRD_%sADC=R,1\r\n" % (type)
        res, data = self.writeCmd(cmd, "*MRD_%sADC:" % (type))
        # print(data)
        if res is True and data is not None:
            if "Missing" in data:
                return False
            val = int(data.split(":")[-1])
            if val == 1:
                return True
        return False

    def writeAdcFlag(self, type = ""):
        cmd = "AT*MRD_%sADC=W,1000,08Jul2021,1,1\r\n" % (type)
        self.writeCmd(cmd)

    def getChipID(self):
        res, resp = self.writeCmd("AT+AUTHID?\r\n" ,"+AUTHID: ")
        if res is True and resp is not None:
            return resp.strip()
        raise Exception("AUTHID: Get UID error")


    def getAuthID(self, cname, pname):
        res, resp = self.writeCmd("AT+AUTHID=\"%s\",\"%s\"\r\n" % (cname, pname), "+AUTHID: ")
        if res is False or resp is None:
            raise Exception("AUTHID: 设备激活出错")
        resps = resp.replace(" ", "").strip().split(",")
        if resps is None or len(resps) < 1:
            raise Exception("AUTHID: 设备激活出错")
        return resps[-1]

    def writeAuth(self, cname, pname, auth):
        res, _ = self.writeCmd("AT+AUTH=\"%s\",\"%s\",\"%s\"\r\n" % (cname, pname, auth))
        if res is False:
            raise Exception("AUTH: 设备激活出错")

    def setLteBand(self, lte_bandH, lte_bandL):
        res, _ = self.writeCmd("AT*BAND=5,0,0,%d,%d\r\n" % (lte_bandH, lte_bandL))
        if res is False:
            raise Exception("AT: Set Band ERROR")

    def getLteBand(self):
        res, data = self.writeCmd("AT*BAND?\r\n" , "*BAND:")
        if res is False:
            raise Exception("AT: Get Band ERROR")
        lte_bandH, lte_bandL = data.split(",")[3:5]
        return int(lte_bandH.strip()),int(lte_bandL.strip())

    def getCustomerCfg(self, config):
        res, data = self.writeCmd("AT+FCISCFG=%s\r\n"%(config), "+FCISCFG: ")
        if res is False:
            raise Exception("AT: Get CIS config error")
        if config in data:
            return data.split(":")[-1]
        raise Exception("AT: Get CIS config error")

    def setCustomerCfg(self, config,val):
        res, data = self.writeCmd("AT+FCISCFG=%s,%s\r\n"%(config, str(val)))
        if res is False:
            raise Exception("AT: Get CIS config error")

    def setAtUartVolt(self, volt):
        res, _ = self.writeCmd("AT+ZXUARTVOL=%d\r\n" % (volt))
        if res is False:
            raise Exception("AT: Set AT uart volt ERROR")

    def getAtUartVolt(self):
        res, data = self.writeCmd("AT+ZXUARTVOL?\r\n" , "+ZXUARTVOL:")
        if res is False or 'v' not in data.lower():
            raise Exception("AT: Get AT uart vole ERROR")
        return int(data.lower().replace("v",'').replace('.',''))

    def checkAuth(self, cname, pname):
        res, resp = self.writeCmd("AT+AUTH\r\n", "+AUTH: ")
        if res is False or resp is None:
            raise Exception("AUTH: 检查到设备未激活")
        res, rcname, rpname, _ = resp.split(',')
        if int(res) != 2 or not rcname.replace("\"","").__eq__(cname) or not rpname.replace("\"","").__eq__(pname):
            raise Exception("AUTH: 设备激活码检验错误")

    def checkCalInfo(self, type="Lte"):
        cmd = "AT*CalInfo=R,%sCal"%(type)
        res, resp = self.writeCmd(cmd, "*CALINFO: ")
        if res and resp is not None and "%sCal"%(type) in resp and "PASS" in resp:
            return resp
        raise Exception("%s: %s射频校准信息检查出错"%(type, type))

    def reset(self):
        self.writeCmd("AT+RESET\r\n")

    def fwVersion(self):
        cmd = "AT+FSWVER\r\n"
        res, resp = self.writeCmd(cmd)
        if res and resp is not None and "VER_SW: " in resp:
            version = resp.split("VER_SW: ")[-1].strip()
            return version
        raise Exception("AtDevice: 读取FW版本出错")

    def readHwVersion(self):
        cmd = "AT+FHWVER?\r\n"
        res, resp = self.writeCmd(cmd,"+FHWVER: ")
        if res and resp is not None:
            return resp
        raise Exception("AtDevice: 读取HW版本出错")

    def writeHwVersion(self, hw_version, batch_no):
        cmd = "AT+FHWVER=\"%s\",\"%s\"\r\n"%(hw_version, batch_no)
        res, resp = self.writeCmd(cmd)
        if res is False:
            raise Exception("写HW版本出错")
