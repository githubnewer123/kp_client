import configparser,sys,os,logging,datetime
import common.utils as Utils

class ToolConfig():
    def getBoolItem(self, key, info):
        return info[key].__eq__("1")

    def getLossSetLastModify(self):
        if "EG" in self.fw_version_name:
            src_loss = Utils.getAppRootPath() + "data/XTC/ec_CableLoss.ini"
        else:
            src_loss = Utils.getAppRootPath()+"data/XTC/CableLoss.ini"
        if not os.path.exists(src_loss):
            return "文件不存在"
        lm_time = os.path.getmtime(src_loss)
        return datetime.datetime.fromtimestamp(lm_time).strftime('%Y-%m-%d %H:%M:%S')

    def __init__(self):
        # default value
        self.cal_sn = False
        self.cal_imei = False
        self.cal_adc = False
        self.cal_auth = False
        self.cal_lte = False
        self.cal_gsm = False

        self.nst_sn = False
        self.nst_imei = False
        self.nst_lte = False
        self.nst_gsm = False
        self.nst_adc = False
        self.nst_auth = False

        self.test_adc_flag = None
        self.test_io = None

        self.mmpt_cal_lte_timeout = 120
        self.mmpt_cal_gsm_timeout = 40
        self.mmpt_nst_lte_timeout = 120
        self.mmpt_nst_gsm_timeout = 40

        self.adc_check_en = True
        self.cal_process = True

        self.cmw_ip_addr = "172.22.1.3"
        self.cmw_slot = 0

        self.dc_gpib_addr = "GPIB0::5::INSTR"
        self.dc_channle = 2

        self.station_type = "2"
        self.station_num = "1"
        self.order_id = "0"
        self.download_process = False
        self.process_total_count = 3

        self.check_post_res = True

        self.db_file_update = True
        self.scrip_file_update = True
        self.mmpt_tool_update = True

        self.nst_adc_dc_en = True
        self.nst_check_lte_flag = True
        self.nst_check_gsm_flag = True

        self.factory_mes_enable = False
        self.fac_mes_success_total = 0
        self.fac_mes_false_total = 0
        self.line_num = "无"
        self.fw_version_name = ""
        self.rf_tool_version = ""

        self.mmpt_version = None
        self.project_version = ''

        self.success_cnt = 0
        self.false_cnt = 0
        self.lte_false_cnt = 0
        self.gsm_false_cnt = 0
        self.adc_false_cnt = 0
        self.imei_false_cnt = 0
        self.mes_false_cnt = 0
        self.other_false_cnt = 0

        self.ui_station_items  = [1,4,8]
        self.ui_dc_gpib_items = [i for i in range(0, 11)]
        self.ui_dc_gpib_default = 0
        self.ui_dc_instr_items = [i for i in range(0, 11)]
        self.ui_dc_instr_default = 5
        self.ui_dc_ch = [1,2]
        self.ui_dc_ch_default = 2

        self.cfg_path = os.path.join( Utils.getAppRootPath(), "cfg.ini")

        self.cfg = configparser.ConfigParser(strict=False)
        self.cfg.optionxform = str
        self.cfg.clear()

        if not os.path.exists(self.cfg_path):
            self.configInit()
        else:
            # self.cfg.read(self.cfg_path)
            try:
                with open(self.cfg_path, 'r', encoding='UTF-8', errors='ignore') as fp:  # 替换'你的编码'为实际编码
                    self.cfg.read_file(fp)
                    self.configLoad()
            except Exception as e:
                self.configInit()

    def _syncToFile(self):
        self.cal_setting = {"CalLteEnable": self.cal_lte, "CalGsmEnable": self.cal_gsm,
                            "WriteImeiEnable": self.cal_imei,
                            "AdcCalEnable": self.cal_adc, "WriteSnEnable": self.cal_sn, "DeviceAuth": self.cal_auth}
        self.nst_setting = {"NstLteEnable": self.nst_lte, "NetGsmEnable": self.nst_gsm,
                            "CheckImeiEnable": self.nst_imei,
                            "AdcCheckEnable": self.nst_adc, "SnCheckEnable": self.nst_sn,
                            "DeviceAuthCheck": self.nst_auth}
        self.dc_setting = {"GPIB_Address": self.dc_gpib_addr, "Channel": self.dc_channle}
        self.cmw_setting = {"IPAddress": self.cmw_ip_addr, "slot": self.cmw_slot}
        self.station_setting = {"StationType": self.station_type, "StationNumber":self.station_num}
        self.mmpt_setting = {"MmptCalLteTimeout": self.mmpt_cal_lte_timeout,"MmptCalGsmTimeout": self.mmpt_cal_gsm_timeout,
                            "MmptNstLteTimeout": self.mmpt_nst_lte_timeout,"MmptNstGsmTimeout": self.mmpt_nst_gsm_timeout}
        self.factory_mes_setting = {"FactoryMesLineNumber": self.line_num,
                                    "FactoryMesPostSuccess": self.fac_mes_success_total, "FactoryMesPostFalse":self.fac_mes_false_total}
        self.order_dict = {"OrederID":self.order_id, "FirmwareVersion":self.fw_version_name,"RfToolVersion": self.rf_tool_version}
        self.product_info_dict = {"ProductSuccessTotal": self.success_cnt, "ProductFalseTotal": self.false_cnt,
                                  "ProductLteFalseTotal": self.lte_false_cnt,
                                  "ProductGsmFalseTotal": self.gsm_false_cnt,
                                  "ProductAdcFalseTotal": self.adc_false_cnt,
                                  "ProductImeiFalseTotal": self.imei_false_cnt,
                                  "ProductMesFalseTotal": self.mes_false_cnt,
                                  "ProductOtherFalseTotal": self.other_false_cnt}
        # self.bool_section_dict = {"CalSetting": self.cal_setting, "Te stSetting": self.nst_setting}
        self.bool_section_dict = {}
        self.str_section_dict = {"StationSetting": self.station_setting, "DcSourceSetting": self.dc_setting,
                                 "CMWSetting": self.cmw_setting, "OrderInfo":self.order_dict,"MmptSetting":self.mmpt_setting,
                                  "FactoryMesSetting": self.factory_mes_setting,"ProductInfo": self.product_info_dict}

        for section in self.bool_section_dict.keys():
            if not self.cfg.has_section(section):
                self.cfg.add_section(section)
            for option in self.bool_section_dict[section]:
                self.cfg.set(section, option, "1" if self.bool_section_dict[section][option] else "0")

        for section in self.str_section_dict.keys():
            if not self.cfg.has_section(section):
                self.cfg.add_section(section)
            for option in self.str_section_dict[section]:
                self.cfg.set(section, option, str(self.str_section_dict[section][option]))
        self.cfg.write(open(self.cfg_path, "w+"))


    # file -> self var
    def configLoad(self):
        # cal_sec = self.cfg["CalSetting"]
        # self.cal_sn = self.getBoolItem("WriteSnEnable", cal_sec)
        # self.cal_imei = self.getBoolItem("WriteImeiEnable", cal_sec)
        # self.cal_adc = self.getBoolItem("AdcCalEnable", cal_sec)
        # self.cal_auth = self.getBoolItem("DeviceAuth", cal_sec)
        # self.cal_lte = self.getBoolItem("CalLteEnable", cal_sec)
        # self.cal_gsm = self.getBoolItem("CalGsmEnable", cal_sec)

        # nst_sec = self.cfg["TestSetting"]
        # self.nst_sn = self.getBoolItem("SnCheckEnable", nst_sec)
        # self.nst_imei = self.getBoolItem("CheckImeiEnable", nst_sec)
        # self.nst_lte = self.getBoolItem("NstLteEnable", nst_sec)
        # self.nst_gsm = self.getBoolItem("NetGsmEnable", nst_sec)
        # self.nst_adc = self.getBoolItem("AdcCheckEnable", nst_sec)
        # self.nst_auth = self.getBoolItem("DeviceAuthCheck", nst_sec)
        try:

            self.dc_gpib_addr = self.cfg["DcSourceSetting"]["GPIB_Address"]
            self.dc_channle = self.cfg["DcSourceSetting"]["Channel"]

            self.cmw_ip_addr = self.cfg["CMWSetting"]["IPAddress"]
            self.cmw_slot = self.cfg["CMWSetting"]["slot"]

            self.station_type = self.cfg["StationSetting"]["StationType"]
            self.station_num = self.cfg["StationSetting"]["StationNumber"]

            self.order_id = self.cfg["OrderInfo"]["OrederID"]

            self.mmpt_cal_lte_timeout = self.cfg["MmptSetting"]["MmptCalLteTimeout"]
            self.mmpt_cal_gsm_timeout = self.cfg["MmptSetting"]["MmptCalGsmTimeout"]
            self.mmpt_nst_lte_timeout = self.cfg["MmptSetting"]["MmptNstLteTimeout"]
            self.mmpt_nst_gsm_timeout = self.cfg["MmptSetting"]["MmptNstGsmTimeout"]

            self.fac_mes_success_total = int(self.cfg["FactoryMesSetting"]["FactoryMesPostSuccess"])
            self.fac_mes_false_total = int(self.cfg["FactoryMesSetting"]["FactoryMesPostFalse"])
            self.line_num = str(self.cfg["FactoryMesSetting"]["FactoryMesLineNumber"])
        except Exception as e:
            logging.info(str(e))

        if self.cfg.has_section("ProductInfo"):
            try:
                self.success_cnt = int(self.cfg["ProductInfo"]["ProductSuccessTotal"])
                self.false_cnt = int(self.cfg["ProductInfo"]["ProductFalseTotal"])
                self.lte_false_cnt = int(self.cfg["ProductInfo"]["ProductLteFalseTotal"])
                self.gsm_false_cnt = int(self.cfg["ProductInfo"]["ProductGsmFalseTotal"])
                self.adc_false_cnt =int(self.cfg["ProductInfo"]["ProductAdcFalseTotal"])
                self.imei_false_cnt = int(self.cfg["ProductInfo"]["ProductImeiFalseTotal"])
                self.mes_false_cnt = int(self.cfg["ProductInfo"]["ProductMesFalseTotal"])
                self.other_false_cnt = int(self.cfg["ProductInfo"]["ProductOtherFalseTotal"])
            except Exception as e:
                logging.info(str(e))

    # self var defaule value -> file
    def configInit(self):
        self._syncToFile()

    def configOrderId(self, order_id):
        self.order_id = order_id
        self._syncToFile()

    # self var value -> file
    def configBoolWrite(self,cal_lte,cal_gsm, cal_imei,cal_adc,cal_auth,cal_sn,nst_lte,nst_gsm,nst_imei,nst_adc,nst_auth,nst_sn):

        self.cal_sn = cal_sn
        self.cal_imei = cal_imei
        self.cal_adc = cal_adc
        self.cal_auth = cal_auth
        self.cal_lte = cal_lte
        self.cal_gsm = cal_gsm

        self.nst_sn = nst_sn
        self.nst_imei = nst_imei
        self.nst_lte = nst_lte
        self.nst_gsm = nst_gsm
        self.nst_adc = nst_adc
        self.nst_auth = nst_auth

    def configNst(self, nst_lte_flag, nst_gsm_flag, adc_dc_en, test_adc_flag = None, test_io = False):
        self.nst_adc_dc_en = adc_dc_en
        self.test_adc_flag = test_adc_flag
        self.test_io = test_io
        self.nst_check_lte_flag = nst_lte_flag
        self.nst_check_gsm_flag = nst_gsm_flag


    def configFactoryMesResult(self, res):
        if res:
            self.fac_mes_success_total += 1
        else:
            self.fac_mes_false_total += 1
        self._syncToFile()

    def productInfoSave(self):
        self._syncToFile()

    def configFactoryMes(self):
        # self.line_num = line_num
        # self.fac_mes_success_total = str(success_total)
        # self.fac_mes_false_total = str(false_total)
        self._syncToFile()

    def configStrWrite(self, gpib_addr, channel, station_type, station_num, cmw_ip,cmw_slot):

        self.dc_gpib_addr = gpib_addr
        self.dc_channle = channel
        self.station_type = station_type
        self.station_num = station_num

        self.cmw_ip_addr = str(cmw_ip)
        self.cmw_slot = str(cmw_slot)

        self._syncToFile()

    def getStationInfo(self):
        type = int(self.station_type)
        if type == 0:
            return "校准工位"
        elif type == 1:
            return "测试工位"
        elif type == 2:
            return "烧录工位"
    def setOrderId(self, order_id):
        self.order_id = order_id

    def getStationFlowInfo(self):
        type = int(self.station_type)
        info = ""
        if type == 0:
            if self.cal_lte:
                info += "LTE校准"
            if self.cal_gsm:
                info += "/GSM校准"
            if self.cal_adc:
                info += "/ADC校准"
            if self.cal_imei:
                info += "/写IMEI"
            if self.cal_sn:
                info += "/写SN"
            if self.cal_auth:
                info += "/激活"
        if type == 1:
            if self.nst_lte:
                info += "LTE综测"
            if self.nst_gsm:
                info += "/GSM综测"
            if self.nst_adc:
                info += "/ADC测试"
            if self.nst_imei:
                info += "/检查IMEI"
            if self.nst_sn:
                info += "/检查SN"
            if self.nst_auth:
                info += "/检查激活"
            info = info + "/IO测试/功耗测试"

        if type == 2:
            info += "烧录固件"

        return info
