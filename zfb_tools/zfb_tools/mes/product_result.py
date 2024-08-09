import time,datetime
from manager.mmpt_slot import MmptSlot
from manager.tool_config import ToolConfig
import random
import common.utils as Utils
from mes.mes import Mes

class ProductResult():

    def getPlatformVersion(self):
        return self.config.fw_version_name[3:5]

    def __init__(self, config):
        self.cal_sn = "未测试"
        self.cal_imei = "未测试"
        self.cal_adc = "未测试"
        self.cal_auth = "未测试"
        self.cal_lte = ""
        self.cal_gsm = ""

        self.nst_sn = "未测试"
        self.nst_imei = "未测试"
        self.nst_lte = ""
        self.nst_rf_res = {}
        self.nst_gsm = ""
        self.nst_adc = "未测试"
        self.nst_auth = "未测试"
        self.nst_io = "未测试"
        self.fw_version = ""

        self.band_info = ''

        self.commitid = random.randint(0,99999999999)

        self.startTs = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.endTs = ""
        self.order_id = ""
        self.station_type = ""
        self.sn = ""
        self.imei = ""
        self.chip_id = ""
        self.config = config
        self.start_times = time.time()
        self.log_url = ""
        self.last_mmpt_info = ""

        self.scrip_version = ""
        self.at_uart_volt = 18

        self.custome_info = None
        self.custome_config = None
        self.successCount = ""
        self.failCount = ""
        self.lisence_available_count = ""

    def getFalseInfo(self,res):
        if res == MmptSlot.PROCESS_NG_RF:
            return "MMPT返回失败"
        elif res == MmptSlot.PROCESS_NG_ABORT:
            return "设备拔出"
        elif res == MmptSlot.PROCESS_NG_TIMEOUT:
            return "MMPT返回超时"

    def setMmptRes(self, process, res, info):
        txt = ""
        if res == MmptSlot.PROCESS_SUCCESS:
            txt = "成功,%s"%(info)
        else:
            txt = "失败,%s,%s"%(self.getFalseInfo(res),info)

        if process == MmptSlot.PROCESS_LTE_CAL:
            self.cal_lte = "LTE: 校准" + txt
            # self.cal_lte = "LTE: 校准成功,%d"%(info) if res == MmptSlot.PROCESS_SUCCESS else "LTE: 校准失败,%s"%(self.getFalseInfo(res))
            self.last_mmpt_info = self.cal_lte
        elif process == MmptSlot.PROCESS_GSM_CAL:
            self.cal_gsm = "GSM: 校准"  + txt
            # 成功,%d"%(info) if res == MmptSlot.PROCESS_SUCCESS else "GSM: 校准失败,%s"%(self.getFalseInfo(res))
            self.last_mmpt_info = self.cal_gsm
        elif process == MmptSlot.PROCESS_LTE_NST:
            self.nst_lte = "LTE: 综测"  + txt
            # 成功,%d"%(info) if res == MmptSlot.PROCESS_SUCCESS else "LTE: 综测失败,%s"%(self.getFalseInfo(res))
            self.last_mmpt_info = self.nst_lte
        elif process == MmptSlot.PROCESS_GSM_NST:
            self.nst_gsm = "GSM: 综测"  + txt
            # 成功,%d"%(info) if res == MmptSlot.PROCESS_SUCCESS else "GSM: 综测失败,%s"%(self.getFalseInfo(res))
            self.last_mmpt_info = self.nst_gsm

    def getUpdateData(self):
        return {
            "commitid": str(self.commitid),
            "count": self.lisence_available_count,#1,
            "successCount": self.successCount,
            "failCount": self.failCount,
            "orderId": self.config.order_id,#"DD1715408407424",
            "startTs": self.startTs,
            "endTs": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "prodectId": "",
            "processTotalCount": self.config.process_total_count,
            "processName": "校准",
            "processSequence": 2,
            "stationNumber":self.config.station_num,
            "processList": [{
                "processFlag": 0,
                "processTestInfo": {},
                "realEst": int(time.time() - self.start_times+5),
                "est": int(time.time() - self.start_times),
                "logZip": self.log_url,
                "processResult": 0,
                "remark": "",
                "sn": "",
                "imei": self.imei,
                "mac": "",
                "chipId": str(self.chip_id) if self.chip_id is not None else "",
                # "lisence_available_count": 25#self.lisence_available_count

            }]
        }

    def getNstUpdate(self , res = True, false_info = ""):
        update_nst_data = {
            "tool_version": Utils.getAppVersion(),
            "test_lte":self.nst_lte,
            "test_rf_result": self.nst_rf_res,
            "script_version": self.scrip_version,
            "test_gsm": self.nst_gsm,
            "test_adc": self.nst_adc,
            "test_imei": self.nst_imei,
            "test_sn": self.nst_sn,
            "test_activation": self.nst_auth,
            "lossSetLastModify": self.config.getLossSetLastModify(),
            "band_info": self.band_info,
            "test_io": self.nst_io,
            "fw_version":self.fw_version,
            "at_uart_volt": self.at_uart_volt,
            "rf_tool_version": self.config.rf_tool_version
        }
        if self.custome_info:
            update_nst_data["custome_info"] = self.custome_info

        if self.custome_config:
            update_nst_data["custome_config"] = self.custome_config

        info = self.getUpdateData()
        if self.config.line_num != "无":
            info["stationNumber"] = "TEST%s_功能测试_"%(self.config.line_num) + str(self.config.station_num)
        info["processList"][0]["processTestInfo"] = str(update_nst_data).replace("'","\"")
        info["processSequence"] = 0
        if self.config.download_process and not self.getPlatformVersion().__eq__('EG'):
            info["processSequence"] += 1
        if self.config.cal_process:
            info["processSequence"] += 1
        info["processSequence"] += 1
        info["processName"] = "测试"
        if res:
            info["processList"][0]["processResult"] = 1
            info["processList"][0]["processFlag"] = 1
        else:
            info["processList"][0]["processResult"] = 0
            info["processList"][0]["processFlag"] = 1
            info["processList"][0]["remark"] = false_info

        return info

    def getDownloadUpdate(self , res = True, false_info = ""):
        update_download_data = {
            "tool_version": Utils.getAppVersion(),
        }
        info = self.getUpdateData()
        info["processList"][0]["processTestInfo"] = str(update_download_data).replace("'","\"")
        info["processSequence"] = 1
        info["processName"] = "烧录"
        if res:
            info["processList"][0]["processResult"] = 1
            info["processList"][0]["processFlag"] = 1
        else:
            info["processList"][0]["processResult"] = 0
            info["processList"][0]["processFlag"] = 1
            info["processList"][0]["remark"] = false_info

        return info

    def getCalUpdate(self, res = True, false_info = ""):
        update_cal_data = {
            "tool_version": Utils.getAppVersion(),
            "write_sn": self.cal_sn,
            "write_imei": self.cal_imei,
            "cal_lte": self.cal_lte,
            "cal_gsm": self.cal_gsm,
            "script_version": self.scrip_version,
            "adc": self.cal_adc,
            "activation": self.cal_auth,
            "lossSetLastModify": self.config.getLossSetLastModify(),
            "rf_tool_version": self.config.rf_tool_version
        }
        if self.custome_info:
            update_cal_data["custome_info"] = self.custome_info
        if self.custome_config:
            update_cal_data["custome_config"] = self.custome_config
        info = self.getUpdateData()
        info["processList"][0]["processTestInfo"] = str(update_cal_data).replace("'","\"")
        info["processSequence"] = 2 if self.config.download_process and not self.getPlatformVersion().__eq__('EG') else 1
        info["processName"] = "校准"
        if res:
            info["processList"][0]["processResult"] = 1
            info["processList"][0]["processFlag"] = 2
        else:
            info["processList"][0]["processResult"] = 0
            info["processList"][0]["processFlag"] = 1
            info["processList"][0]["remark"] = false_info
        return info
