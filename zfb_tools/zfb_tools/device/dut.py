from device.at_device import  AtDevice
from device.dc_device import DcDevice
import common.utils as Utils
import time,logging,threading

authCfg = {"username":"ASR1603@zyxa", "password":"11447733", "pname":"XZX", "cname":"CIS_MODULE"}

def tryThreeTimes(func):
    def wrapper(*args, **kwargs):
        tryCnt = 3
        while tryCnt > 0:
            try:
                func(*args, **kwargs)
                break
            except Exception as e:
                tryCnt -= 1
                if tryCnt <= 0:
                    raise e
                time.sleep(1)

    return wrapper

def checkAdcEnable(func):
    def wrapper(*args, **kwargs):
        if args[0].dc_dev is None or args[0].dc_ch is None:
            raise Exception("Dut: 不支持ADC校准操作")
        func(*args, **kwargs)

    return wrapper

class Dut:
    def __init__(self, com_port, dc_address=None, dc_ch=None, update_authid = True, default_cmd=True):
        cnt = 3
        while True:
            try:
                self.at_dev = AtDevice(com_port)
                time.sleep(1)
                break
            except Exception as e:
                cnt -= 1
                if cnt <= 0:
                    raise Exception(str(e))

        self.dc_dev = None
        self.dc_address = dc_address
        self.dc_ch = dc_ch

        self.max_adc_cal_diff = 850
        self.max_adc_nst_diff = 850
        self.default_volt = 1.3
        self.delay_time = 0.02
        self.adc_cal_list = [1.80, 1.62, 1.44, 1.26, 1.08, 0.90, 0.72, 0.54, 0.36, 0.25]
        self.max_diff = 0

        self.adc_cal_check_list = [1.75, 1.36, 0.64, 0.4]
        self.adc_nst_list = [1.75, 1.53, 0.82, 0.4]
        if default_cmd:
            self.at_dev.ATE0()
            self.factoryMode()
        if update_authid:
            self.auth_id = self.at_dev.getAuthID(authCfg["cname"], authCfg["pname"])
            self.auth_code = None
            self.authAsync()
        else:
            self.auth_id = None
            self.auth_code = None
            # self.authAsync()

    # @checkAdcEnable
    def adcCal(self, rtpEn = True):
        #  ADC VOLT READ FROM ini file ?
        if len(self.adc_cal_list) < 10:
            raise Exception("ADC: ADC校准电压列表不满足最少10个")


        if self.dc_address is not None or self.dc_ch is not None:
            try:
                logging.info("Create DC Device")
                self.dc_dev = DcDevice(self.dc_address)
                self.dc_ch = int(self.dc_ch)
            except Exception as e:
                raise Exception("ADC: 打开电源出错,请检查电源地址和接线")

        if self.dc_dev is None:
            raise Exception("ADC: 未配置电源地址,不能进行ADC校正操作")

        self.factoryMode()
        self.at_dev.delAdc()
        if rtpEn:
            self.at_dev.delAdc("RTP")

        self.dc_dev.setMaxVolt(self.adc_cal_list[0])
        self.dc_dev.on(self.dc_ch)
        self.dc_dev.setVolt(self.default_volt, self.dc_ch)
        for _ in range(0,3):
            for index,volt in enumerate(self.adc_cal_list):
                # try three time:
                rval = self.dc_dev.setVolt(volt, self.dc_ch)
                # time.sleep(self.delay_time)
                self.at_dev.writeAdcCal(index, rval)
                if rtpEn:
                    self.at_dev.writeAdcCal(index, rval, type="RTP")

            # self.dc_dev.setVolt(self.default_volt, self.dc_ch)
            self.at_dev.writeAdcFlag()
            if rtpEn:
                self.at_dev.writeAdcFlag(type="RTP")
            try:
                vbat_diff,rtp_diff = self.adcCheck(self.adc_cal_check_list,rtpEn, dc_enable = True, max_diff=self.max_adc_cal_diff)
                # print("vbat diff: %f~%f rtp diff: %f~%f"%(vbat_diff[0],vbat_diff[-1],rtp_diff[0],rtp_diff[-1]))
                return vbat_diff,rtp_diff
            except Exception as e:
                continue
        else:
            raise Exception("ADC: ADC 校准出错, Max diff > %d"%(self.max_adc_cal_diff))

    def adcCheck(self,volt_list , rtpEn = True, dc_enable = False, max_diff = 15):
        if self.at_dev.checkAdcFlag() is False:
            raise Exception("ADC: vbat ADC校验标志未设置")

        if rtpEn is True and self.at_dev.checkAdcFlag("RTP") is False:
            raise Exception("ADC: RTP ADC校验标志未设置")

        if dc_enable is False:
            return None

        if self.dc_address is not None or self.dc_ch is not None:
            try:
                self.dc_dev = DcDevice(self.dc_address)
                self.dc_ch = int(self.dc_ch)
            except Exception as e:
                raise Exception("ADC: 打开电源出错,请检查电源地址和接线")

        if self.dc_dev is None:
            raise Exception("ADC: 未配置电源地址,不能进行ADC校正操作")

        vbat_diff = []
        rtp_diff = []

        if dc_enable:
            for volt in volt_list:
                rval = self.dc_dev.setVolt(volt, self.dc_ch)
                # time.sleep(self.delay_time)
                rvolt = 0
                rcnt = 5
                volts = []
                for _ in range(rcnt):
                    volts.append(self.at_dev.getAdc())
                    time.sleep(0.01)
                volts.sort()
                # print(volts)
                for v in volts[1:-1]:
                    rvolt += v
                rvolt = rvolt // (rcnt-2)
                diff = rvolt - int(rval * 1000)
                # print("Vbat Diff :",diff)
                vbat_diff.append(diff)
                if diff > max_diff or diff < -max_diff:
                    logging.info("ADC: Vbat check: %d get: %d diff: %d ERROR"%(volt*1000, rvolt, diff))
                    raise Exception("ADC: VBAT ADC检验差值超过阈值: %d 实际测试差值: %d"%(max_diff, diff))
                if rtpEn:
                    rvolt = 0
                    rcnt = 5
                    volts = []
                    for _ in range(rcnt):
                        volts.append(self.at_dev.getAdc("RTP"))
                        time.sleep(0.01)
                    volts.sort()
                    for v in volts[1:-1]:
                        rvolt += v
                    rvolt = rvolt // (rcnt-2)
                    diff = rvolt - int(rval * 1000)
                    rtp_diff.append(diff)
                    if diff > max_diff or diff < -max_diff:
                        logging.info("ADC: RTP check: %d get: %d diff: %d ERROR" % (volt * 1000, rvolt, diff))
                        raise Exception("ADC: RTP ADC检验差值超过阈值: %d 实际测试差值: %d"%(max_diff, diff))

            self.dc_dev.setVolt(self.default_volt, self.dc_ch)
            return [sorted(vbat_diff), sorted(rtp_diff)]

    @tryThreeTimes
    def auth(self):
        if self.auth_id is None:
            self.auth_id = self.at_dev.getAuthID(authCfg["cname"], authCfg["pname"])
        if self.auth_code is None:
            self.auth_code = Utils.getAuthInfo(authCfg, self.auth_id)
        if self.auth_code is None:
            raise Exception("AUTH: 设备激活出错，请检查电脑是否联网")
        self.at_dev.writeAuth(authCfg["cname"], authCfg["pname"],self.auth_code)
        self.at_dev.checkAuth(authCfg["cname"], authCfg["pname"])

    def setCmccBand(self):
        lte_band_h = 482
        lte_band_l = 132
        r_lte_band_h, r_lte_band_l = self.at_dev.getLteBand()
        if r_lte_band_h == lte_band_h and r_lte_band_l == lte_band_l:
            return ("%d-%d"%(r_lte_band_h,r_lte_band_l))

        self.at_dev.setLteBand(lte_band_h, lte_band_l)
        r_lte_band_h,r_lte_band_l = self.at_dev.getLteBand()
        if r_lte_band_h != lte_band_h or r_lte_band_l != lte_band_l:
            raise Exception("AT: set CMCC band ERROR")
        return ("%d-%d" % (r_lte_band_h, r_lte_band_l))

    def setTddOnlyBand(self):
        lte_band_h = 482
        lte_band_l = 0
        r_lte_band_h, r_lte_band_l = self.at_dev.getLteBand()
        if r_lte_band_h == lte_band_h and r_lte_band_l == lte_band_l:
            return ("%d-%d"%(r_lte_band_h,r_lte_band_l))

        self.at_dev.setLteBand(lte_band_h, lte_band_l)
        r_lte_band_h,r_lte_band_l = self.at_dev.getLteBand()
        if r_lte_band_h != lte_band_h or r_lte_band_l != lte_band_l:
            raise Exception("AT: set CMCC band ERROR")
        return ("%d-%d" % (r_lte_band_h, r_lte_band_l))

    def checkAllBand(self):
        lte_band_h = 482
        lte_band_l = 149
        r_lte_band_h, r_lte_band_l = self.at_dev.getLteBand()
        if r_lte_band_h != lte_band_h or r_lte_band_l != lte_band_l:
            raise Exception("AT: check all band ERROR")
        return ("%d-%d" % (r_lte_band_h, r_lte_band_l))

    def setBand(self, lte_band_h, lte_band_l):
        r_lte_band_h, r_lte_band_l = self.at_dev.getLteBand()
        if r_lte_band_h == lte_band_h and r_lte_band_l == lte_band_l:
            return ("%d-%d"%(r_lte_band_h,r_lte_band_l))

        self.at_dev.setLteBand(lte_band_h, lte_band_l)
        r_lte_band_h,r_lte_band_l = self.at_dev.getLteBand()
        if r_lte_band_h != lte_band_h or r_lte_band_l != lte_band_l:
            raise Exception("AT: set band(%d,%d) ERROR"%(lte_band_h, lte_band_l))
        return ("%d-%d" % (r_lte_band_h, r_lte_band_l))

    def customeConfigCheck(self, item, val):
        r_val = self.at_dev.getCustomerCfg(item)
        if r_val is None:
            return (False, "Get config error")

        if str(val).__eq__(str(r_val)):
            return (True, str(r_val))

        self.at_dev.setCustomerCfg(item,val)

        r_val = self.at_dev.getCustomerCfg(item)
        if r_val is None or not str(val).__eq__(str(r_val)):
            return (False, "Set config error: "+str(r_val))
        return (True, str(r_val))

    def customConfig(self, config):
        info = {}
        for item in config.keys():
            res,info[item] = self.customeConfigCheck(item, config[item])
            if res is False:
                return (False, info)
        return (True, info)

    def checkBand(self, lte_band_h, lte_band_l):
        r_lte_band_h, r_lte_band_l = self.at_dev.getLteBand()
        if r_lte_band_h != lte_band_h or r_lte_band_l != lte_band_l:
            raise Exception("AT: check band(%d,%d) ERROR" % (r_lte_band_h, r_lte_band_l))
        return ("%d-%d" % (r_lte_band_h, r_lte_band_l))

    def checkUartVolt(self, volt):
        rvolt = self.at_dev.getAtUartVolt()
        if rvolt != volt:
            self.at_dev.setAtUartVolt(volt)
            return self.at_dev.getAtUartVolt()
        return rvolt

    def authCodeGet(self):
        for i in range(3):
            try:
                self.auth_code = Utils.getAuthInfo(authCfg, self.auth_id)
                return
            except Exception as e:
                continue

    def authAsync(self):
        threading.Thread(target=self.authCodeGet, args=()).start()

    def writeImei(self, imei):
        if Utils.isImei(imei) is False:
            raise Exception("IMEI: IMEI 规则检查出错: "+imei)

        self.at_dev.writeImei(imei)
        rimei = self.at_dev.getImei()
        if not rimei.__eq__(imei):
            raise Exception("IMEI: 写入IMEI后检查出错")

    def checkImei(self, imei):
        rimei = self.at_dev.getImei()
        if not Utils.isImei(rimei) or not rimei.__eq__(imei):
            raise Exception("IMEI: 检查IMEI出错 QR: %s read imei:%s "%(imei, rimei))

    def checkLteCal(self):
        return self.at_dev.checkCalInfo("Lte")

    def checkGsmCal(self):
        return self.at_dev.checkCalInfo("Gsm")

    def checkAuth(self,cname,pname):
        return self.at_dev.checkAuth(cname,pname)

    def checkGPIO(self):
        return self.at_dev.checkGPIO()

    def getChipID(self):
        return self.at_dev.getChipID()

    def devReset(self):
        self.at_dev.reset()

    def checkFwVersion(self, version):
        r_ver = self.at_dev.fwVersion()
        if not r_ver.__eq__(version):
            raise Exception("Dut: 软件版本出错 mes version:%s read version:%s"%(version, r_ver))

    def checkHwVersion(self, project_version, fw_version = None):
        version, batch_no = Utils.genHwVersion(project_version, fw_version)
        try:
            resp = self.at_dev.readHwVersion()
            ver_read = resp.split("\"")[1]
            if not ver_read.__eq__(version):
                logging.info("read: %s gen: %s" % (ver_read, version))
                raise Exception("Dut： 对比硬件版本出错: "+str(ver_read))
            return ver_read
        except Exception as e:
            print(str(e))
            if "CODEC: " in str(e):
                print(hex(version), str(e))
                if hex(version) not in str(e):
                    raise Exception("Dut： 对比硬件版本出错: "+str(e))
            return version



    def getCCID(self):
        res,data = self.at_dev.writeCmd("AT*ICCID?", "*ICCID: ")
        print(res)
        if res and  data.startswith("\"") and data.endswith("\""):
            return data.replace("\"", '')
        raise Exception("CCID Error")

    def getCurSimIdx(self):
        res,data = self.at_dev.writeCmd("AT+SWITCHSIM?", "+SWITCHSIM: ")
        print(data)
        if res:
            return int(data)
        raise Exception("Get sim index Error")

    def setHwVersion(self, project_version, fw_version = None):
        version, batch_no = Utils.genHwVersion(project_version, fw_version)
        self.at_dev.writeHwVersion(version, batch_no)
        return batch_no

    def destory(self):
        self.at_dev.destory()
        if self.dc_dev:
            self.dc_dev.destory()

    def factoryMode(self):
        self.at_dev.factoryMode()

    def checkGPIOExt(self, check_info, platform = "RG"):
        gpio_check = GpioCheck(check_info, platform)
        data = ""
        res = True
        try:
            if gpio_check.gpio_check_en:
                res, data = self.at_dev.writeCmd("AT+FTEST=\"GPIO\",1,1", "+FTEST: ")
                res,data = gpio_check.checkIO(data)
            if gpio_check.check_sim1:
                data += "SIM1:"
                sim1_res = True
                if self.getCurSimIdx() != 0:
                    sim1_res,_ = self.at_dev.writeCmd("AT+SWITCHSIM=0")
                if sim1_res:
                    time.sleep(.010)
                    data += self.getCCID()
                else:
                    data += "ERROR"
                    res = False
            if gpio_check.check_sim2:
                data += " SIM2:"
                sim2_res = True
                if self.getCurSimIdx() != 1:
                    sim2_res,_= self.at_dev.writeCmd("AT+SWITCHSIM=1")
                if sim2_res:
                    time.sleep(.010)
                    data += self.getCCID()
                    self.at_dev.writeCmd("AT+SWITCHSIM=0")
                else:
                    data += "ERROR"
                    res = False
            return res,data
        except Exception as e:
            if gpio_check.check_sim2 or gpio_check.check_sim1:
                self.at_dev.writeCmd("AT+SWITCHSIM=0")
            return False,data + "," + str(e)

def notyify(ports):
    for port in ports:
        logging.info(port[0])
from  device.gpio_check import GpioCheck
if __name__ == "__main__":
    check_info = {"GPIO_00_02":"enable","GPIO_01_03":"disable","GPIO_04_06":"disable","GPIO_05_07":"disable","GPIO_08_10":"disable","GPIO_09_11":"disable","GPIO_12_14":"enable","GPIO_13_15":"disable","GPIO_16_18":"disable","GPIO_17_19":"disable","GPIO_20_22":"enable","GPIO_21_23":"enable","GPIO_24_26":"enable","GPIO_32_34":"enable","GPIO_33_35":"enable","GPIO_36_124":"enable","GPIO_49_51":"enable","GPIO_50_52":"enable","GPIO_53_69":"enable","GPIO_54_70":"enable","GPIO_DIO9_121":"enable","GPIO_DIO10_122":"disable","GPIO_27_25":"enable","GPIO_28_31":"enable","SIM1":"enable","SIM2":"enable"}
    gpio_check = GpioCheck(check_info)
    dut = Dut("COM6")
    # res,data = dut.checkGPIOExt(check_info)
    # print(data)
    # data = "\"GPIO\",[0&2, 33&35,    24&26,50&52,77&121]"
    # res = gpio_check.checkIO(data)
    # print(res,data)
    # dut.setCmccBand()
    # dut.checkAllBand()

    print(dut.checkUartVolt(18))