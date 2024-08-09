# {'id': '9e3759b946f75fbbc46751e9d7f755c4', 'orderId': 'DD1632658237219', 'producerName': 'XK', 'num': 240, 'deliveryTs': '2021-09-26 00:00:00',
#  'projectName': 'ZX600', 'projectVersionName': 'ZX600_CH-EB13-V11.05_V2_debug', 'orderTypeName': '工程订单', 'bomId': '8dc6b1325490b17d199c88f1c10040d0',
#  'bomVersionName': 'CH-EB13-V11.05', 'bomVersionCode': 'BOMBB1631927343007', 'bomVersionDesc': None,
#  'downloadUrl': 'http://testmes.chinainfosafe.com/platform-admin/sys/oss/download/20210918/b1d08f2373d74fdeb166bb9300c31ed3.xlsx',
#  'orderConfig': '{"processTotalCount":3,"process": {"烧录":"",
#  "校准":{"set":{"write_sn": "disable","write_imei": "disable","cal": "disable","cal_adc": "disable","activation": "disable",'
#                 '"work_version": {"model": "4G+2G", "filechecknumber": 4}}},'
#                 '"测试":{"set":{"test_nst": "disable","test_adc": "disable","test_imei": "disable","test_sn": "disable","test_activation": "disable"}}}}',
#  'successNum': 0, 'failNum': 1}


# 'orderConfig': '{"processTotalCount":3,"process": {"烧录":"","校准":{"set":{"write_sn": "enable","write_imei": "enable","cal": "disable","cal_adc": "enable","activation": "enable","work_version": {"model": "4G+2G", "filechecknumber": 4}}},"测试":{"set":{"test_nst": "disable","test_adc": "enable","test_imei": "enable","test_sn": "enable","test_activation": "enable"}}}}'

import json,os,shutil
from mes.file_downloader import FileDownloader
import common.utils as Utils

class Order():
    def getBoolItem(self, key, info):
        return info[key].__eq__("enable")

    def __init__(self, item):
        self.order_id = item["orderId"]
        self.material_id = item["materialCode"]
        self.erp_material_id = item["erpMaterialId"]
        self.project_name= item["projectName"]
        self.project_version = item["projectVersionName"]
        self.product_total = item["num"]
        self.download_url = item["downloadUrl"]
        self.order_type = item["orderTypeName"]
        if "status" in item.keys():
            self.order_status = item["status"]
        else:
            self.order_status = None
        self.info = item
        self.cal_gsm = False
        self.nst_gsm = False
        self.cal_lte = False
        self.nst_lte = False

        self.cal_enable = False
        self.nst_enable = False

        self.db_downloader = None
        self.config_downloader = None
        self.mmpt_downloader = None

        self.fw_downloader = None
        self.aboot_downloader = None
        self.test_adc_flag = None

        self.mmpt_version_name = None
        self.module_platform = self.project_version[:8]

        self.at_uart_volt = None

        self.test_custome_cfg = None
        self.cal_custome_cfg = None

        # config = json.loads(item["orderConfig"])
        # print("config:",config)
        # self.process_count = config["processTotalCount"]
        # self.download_process = config["process"]["proc_burn"].__eq__("enable")
        # if "proc_calibration" in config["process"].keys():
        #     self.cal_process = config["process"]["proc_calibration"]
        #     self.cal_sn = self.getBoolItem("write_sn", self.cal_process)
        #     self.cal_imei = self.getBoolItem("write_imei", self.cal_process)
        #     self.cal_adc = self.getBoolItem("cal_adc", self.cal_process)
        #     self.cal_auth = self.getBoolItem("activation", self.cal_process)
        #     self.cal_enable = self.getBoolItem("cal", self.cal_process)
        #
        #     if "custome_config" in self.cal_process.keys():
        #         self.cal_custome_cfg = self.cal_process["custome_config"]
        # else:
        #     self.cal_process = None
        #     self.cal_sn = False
        #     self.cal_imei = False
        #     self.cal_adc = False
        #     self.cal_auth = False
        #     self.cal_enable = False
        #
        # self.nst_process = None
        # self.gpio_mask = None
        # if "proc_test" in config["process"].keys():
        #     self.nst_process = config["process"]["proc_test"]
        #
        #     self.nst_sn = self.getBoolItem("test_sn", self.nst_process)
        #     self.nst_imei = self.getBoolItem("test_imei", self.nst_process)
        #     self.rf_check = self.getBoolItem("test_cal", self.nst_process)
        #     self.nst_enable = self.getBoolItem("test_nst", self.nst_process)
        #     self.nst_auth = self.getBoolItem("test_activation", self.nst_process)
        #
        #     if "custome_config" in self.nst_process.keys():
        #         self.test_custome_cfg = self.nst_process["custome_config"]
        #
        #     if "at_uart_volt" in self.nst_process.keys():
        #         self.at_uart_volt = self.nst_process["at_uart_volt"]
        #     if "test_adc_flag" not in self.nst_process:
        #         # 增加test_adc_flag字段之前的订单使用test_io判断是否要用电源做ADC测试， 否则只检查ADC flag
        #         self.nst_adc = self.getBoolItem("test_adc", self.nst_process)
        #         self.nst_adc_dc_en = self.getBoolItem("test_io", self.nst_process)
        #     else:
        #         self.nst_adc_dc_en = self.getBoolItem("test_adc", self.nst_process)
        #         self.test_io = self.getBoolItem("test_io", self.nst_process)
        #         if self.test_io and "gpio_test" in config["process"].keys():
        #             self.gpio_mask = config["process"]["gpio_test"]
        #         self.test_adc_flag = self.getBoolItem("test_adc_flag", self.nst_process)
        #         if self.nst_adc_dc_en is False and self.test_adc_flag is False:
        #             self.nst_adc = False
        #         else:
        #             self.nst_adc = True
        # self.fw_version_name = None
        # rc_cal_mode = config["mode"]
        #
        # self.rf_check_lte = False
        # self.rf_check_gsm = False
        # if self.rf_check:
        #     if rc_cal_mode["LTE"].__eq__("enable"):
        #         self.rf_check_lte = True
        #     if rc_cal_mode["GSM"].__eq__("enable"):
        #         self.rf_check_gsm = True
        #
        # if self.cal_enable:
        #     if rc_cal_mode["LTE"].__eq__("enable") :
        #         self.cal_lte = True
        #     if rc_cal_mode["GSM"].__eq__("enable"):
        #         self.cal_gsm = True
        #
        # if self.nst_enable:
        #     if rc_cal_mode["LTE"].__eq__("enable"):
        #         self.nst_lte = True
        #         self.rf_check_lte = True
        #     if rc_cal_mode["GSM"].__eq__("enable"):
        #         self.nst_gsm = True

    def getOrderDict(self):
        return self.info

    def isProductOrder(self):
        return self.order_type.__eq__("生产订单")

    def getProductTotal(self):
        return format(self.product_total, ",")

    def setOrderInfo(self, info, db_update = True, scrip_update = True):
        if info is None:
            raise Exception("设置的订单详细信息出错")
        for ele in info:
            # print(ele["elementEntity"])
            if "EG" in self.module_platform:
                if ele["elementEntity"]["zyxaElementCategoryEntity"]["category"] == "校准配置文件" and scrip_update:
                    unzip_path = os.path.join(Utils.getAppRootPath(), "EMAT\main\EM_set")
                    self.scrip_version = ele["versionName"]
                    self.config_downloader = FileDownloader(url=ele["downloadUrl"], file_name="EM_set.zip", md5_code=ele["hash"],unzip_path=unzip_path)
                elif ele["elementEntity"]["zyxaElementCategoryEntity"]["category"] == "固件":
                    # unzip_path = os.path.join(Utils.getAppRootPath(), "MMPT\main\M_set")
                    self.fw_version_name = ele["versionName"]
                    print(self.order_id ,self.fw_version_name)
                    # self.fw_downloader = FileDownloader(url=ele["downloadUrl"], file_name="fw.zip", md5_code=ele["hash"],unzip_path=None)
                elif ele["elementEntity"]["zyxaElementCategoryEntity"]["category"] == "MMPT":
                    # unzip_path = os.path.join(Utils.getAppRootPath(), "MMPT\main\M_set")
                    self.mmpt_version_name = ele["versionName"]
                    self.mmpt_downloader = FileDownloader(url=ele["downloadUrl"], file_name="emat_tool.zip", md5_code=ele["hash"],unzip_path=None)
                elif ele["elementEntity"]["zyxaElementCategoryEntity"]["category"] == "芯片生产配置文件" and scrip_update:
                    print("芯片生产配置文件。。。。。")
                    unzip_path = os.path.join(Utils.getAppRootPath(), "cfg")
                    self.scrip_version = ele["versionName"]
                    self.config_downloader = FileDownloader(url=ele["downloadUrl"], file_name="lisence_cfg.zip",md5_code=ele["hash"], unzip_path=unzip_path)
            else:
                if ele["elementEntity"]["zyxaElementCategoryEntity"]["category"] == "校准DB文件" and db_update:
                    print("校准DB文件。。。。。")
                    unzip_path = os.path.join(Utils.getAppRootPath(), "MMPT\main\DB_set")
                    self.db_downloader = FileDownloader(url=ele["downloadUrl"], file_name="DB_set.zip", md5_code=ele["hash"],unzip_path=unzip_path)

                elif ele["elementEntity"]["zyxaElementCategoryEntity"]["category"] == "校准配置文件" and scrip_update:
                    print("校准配置文件。。。。。")
                    unzip_path = os.path.join(Utils.getAppRootPath(), "MMPT\main\M_set")
                    self.scrip_version = ele["versionName"]
                    self.config_downloader = FileDownloader(url=ele["downloadUrl"], file_name="M_set.zip", md5_code=ele["hash"],unzip_path=unzip_path)
                elif ele["elementEntity"]["zyxaElementCategoryEntity"]["category"] == "固件":
                    # unzip_path = os.path.join(Utils.getAppRootPath(), "MMPT\main\M_set")
                    print("固件。。。。。")
                    self.fw_version_name = ele["versionName"]
                    self.fw_downloader = FileDownloader(url=ele["downloadUrl"], file_name="fw.zip", md5_code=ele["hash"],unzip_path=None)
                elif ele["elementEntity"]["zyxaElementCategoryEntity"]["category"] == "Aboot":
                    print("Aboot。。。。。")
                    unzip_path = os.path.join(Utils.getAppRootPath(), "aboot")
                    # if os.path.exists(unzip_path):
                    #     shutil.rmtree(unzip_path)
                    if not os.path.exists(unzip_path):
                        os.mkdir(os.path.join(Utils.getAppRootPath(), "aboot"))
                    self.aboot_downloader = FileDownloader(url=ele["downloadUrl"], file_name="aboot.zip", md5_code=ele["hash"],unzip_path=unzip_path)
                elif ele["elementEntity"]["zyxaElementCategoryEntity"]["category"] == "MMPT":
                    # unzip_path = os.path.join(Utils.getAppRootPath(), "MMPT\main\M_set")
                    print("MMPT。。。。。")
                    self.mmpt_version_name = ele["versionName"]
                    self.mmpt_downloader = FileDownloader(url=ele["downloadUrl"], file_name="mmpt_tool.zip", md5_code=ele["hash"],unzip_path=None)
                elif ele["elementEntity"]["zyxaElementCategoryEntity"]["category"] == "芯片生产配置文件" and scrip_update:
                    print("芯片生产配置文件。。。。。")
                    unzip_path = os.path.join(Utils.getAppRootPath(), "cfg")
                    self.scrip_version = ele["versionName"]
                    self.config_downloader = FileDownloader(url=ele["downloadUrl"], file_name="lisence_cfg.zip",md5_code=ele["hash"], unzip_path=unzip_path)