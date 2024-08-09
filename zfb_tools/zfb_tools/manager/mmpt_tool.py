import os,shutil,subprocess,time,threading,logging
import common.utils as Utils
import zipfile,configparser,psutil,signal
from manager.window_manager import WindowsManager

class MmptTool():
    PROCESS_LTE_CAL = 0x00
    PROCESS_GSM_CAL = 0x01
    PROCESS_LTE_NST = 0x02
    PROCESS_GSM_NST = 0x03
    PROCESS_COMPLETE = 0x04

    PROCESS_NG_TIMEOUT = -0X01
    PROCESS_NG_ABORT = -0X02
    PROCESS_NG_RF = -0X03
    PROCESS_SUCCESS = 0x00

    MMPT_STATUS_DOING = 0x10
    MMPT_STATUS_PASS = 0x00
    MMPT_STATUS_FAIL = 0x11
    MMPT_STATUS_READY = 0x12

    def clearCalData(self):
        # 删除CalData信息
        if not os.path.exists(self.cal_data_path):
            os.makedirs(self.cal_data_path)
        else:
            files = os.listdir(self.cal_data_path)
            for file in files:
                if not file == "UiLog":
                    shutil.rmtree(self.cal_data_path + "/" + file)

    def configScripAllDisable(self):
        for idx in range(8):
            Utils.cfgWrite(self.tool_cfg_path, "CommSetting", "bEnableTE%d" % (idx + 1), str(0))

    def configRunScrip(self, index,enable = False, file_path = None):
        if not os.path.exists(file_path):
            raise Exception("配置的脚本文件不存在")

        Utils.cfgWrite(self.tool_cfg_path, "CommSetting", "bEnableTE%d"%(index+1), str(1 if enable else 0))
        if enable:
            Utils.cfgWrite(self.tool_cfg_path, "CommSetting", "TestEngineScript%d"%(index+1), file_path)

    def unzipMmptTool(self, src, dst):
        if not os.path.exists(src):
            raise Exception("MMTP_Tool.zip 文件不存在!请将改文件放置到 data目录下")

        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.makedirs(dst)

        zip_file = zipfile.ZipFile(src)
        check_path  = os.path.join(dst, self.mmpt_check_fname)
        if os.path.exists(dst) and os.path.exists(check_path):
            fd = open(check_path, "rb")
            f_list = fd.read().split(b"\r\n")
            fd.close()
            for file_name in zip_file.namelist():
                if file_name.encode() not in f_list:
                    shutil.rmtree(dst)
                    os.makedirs(dst)
                    break
            else:
                logging.info("MMPT 工具上次已经完整解压")
                return

        fd = open(check_path, "wb+")
        for file in zip_file.namelist():
            zip_file.extract(file, dst)
            fd.write(file.encode()+b"\r\n")
        zip_file.close()
        fd.close()

    def cmwConfig(self, cmw_ip_addr, cmw_slot):
        self.loss_cfg_parser.set("DeviceSetting", "IPAddress", str(cmw_ip_addr))
        self.loss_cfg_parser.set("DeviceSetting", "Instrument slot", str(cmw_slot))
        self.loss_cfg_parser.set("DeviceSetting", "IPPort", str(cmw_slot))
        self.loss_cfg_parser.write(open(self.losset_cfg_path, "w"))

    def __init__(self, root_path):
        # if lte_cal is False and gsm_cal is False and lte_nst is False and gsm_nst is False:
        #     raise Exception("MmptSlot: LTE/GSM校准和综测至少要设置一项")
        self.mmpt_check_fname = "CIS_mmpt_Tool.cfg"
        zip_src = os.path.join(Utils.getAppRootPath(), "data/mmpt_tool_lossSet.zip")
        self.unzipMmptTool(zip_src, root_path)
        self.error_code_handle = ""
        self.pid = None
        self.tool_cfg_path = os.path.join(root_path, "Exec\MMPT.ini")
        self.exe_path = os.path.join(root_path, "Exec\MMPT.exe")
        self.cal_data_path = os.path.join(root_path,"CalData")
        self.losset_cfg_path = os.path.join(root_path, "Exec\config\DevLossConfig.ini")
        self.is_active = False
        self.dev_abort_event = threading.Event()
        self.win_manage = WindowsManager()

        self.loss_cfg_parser = configparser.ConfigParser(strict=False)
        self.loss_cfg_parser.optionxform = str
        self.loss_cfg_parser.read(self.losset_cfg_path)

    def kill(self):
        # try:
        #     pid_dict = {}
        #     pids = psutil.pids()
        #     for pid in pids:
        #         p = psutil.Process(pid)
        #         pid_dict[pid] = p.name()
        #     for t in pid_dict.keys():
        #         if pid_dict[t] == "MMPT.exe":
        #             os.kill(t, signal.SIGABRT)
        # except Exception as e:
        #     print(str(e))
        self.win_manage.winClose(self.win_manage.getMmptTitleName())

    def restart(self):
        pid_dict = {}
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            pid_dict[pid] = p.name()
        for t in pid_dict.keys():
            if pid_dict[t] == "MMPT.exe":
                os.kill(t, signal.SIGABRT)
        self.openMMPT()

    def __get_MMPT_pid(self):
        cmd = "wmic process where name=\"MMPT.exe\" get executablepath,processid"
        ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        cur_path = b"MMPT_Tool\\Exec\\MMPT.exe"
        while True:
            for line in iter(ret.stdout.readline, b""):
                if cur_path in line:
                    self.pid = int(line.decode().strip().replace(" ","").split("MMPT.exe")[-1])
                    print("Get PID: %d"%( self.pid))
                    return
    def configFailContinue(self, enable):
        if enable is False:
            Utils.cfgWrite(self.tool_cfg_path, "CommSetting", "ScriptRunType" , "FailStop")
        else:
            Utils.cfgWrite(self.tool_cfg_path, "CommSetting", "ScriptRunType", "FailContinue")

    def openMMPT(self):
        logging.info("open MMPT Tool: %s" % (self.exe_path))
        cmd = self.exe_path
        subprocess.Popen(cmd)
        self.title = self.win_manage.getMmptTitleName(timeout=6)
        if self.title:
            self.__get_MMPT_pid()
            # self.win_manage.winMin(self.title)
            self.error_code_handle = self.win_manage.getErrorCodeHandle(self.title)
            print("Error code handle: ", self.error_code_handle)
            self.win_manage.winActive(self.title)
            # self.run()

    def setAutoTestEnable(self, enable):
        if enable:
            Utils.cfgWrite(self.tool_cfg_path, "BaseSetting", "bEnableAutoLoopTest", "1")
        else:
            Utils.cfgWrite(self.tool_cfg_path, "BaseSetting", "bEnableAutoLoopTest", "0")

    def winMin(self):
        self.win_manage.winMin(self.win_manage.getMmptTitleName(1))

    def run(self):
        self.win_manage.clickButton(self.win_manage.getMmptTitleName(1), "Button","Run")

    def isReady(self):
        status = self.win_manage.getMmptStatus(self.win_manage.getMmptTitleName(1))
        print(status)
        if status and "ready" in status:
            return True
        return False

    def isDoing(self):
        status = self.win_manage.getMmptStatus(self.win_manage.getMmptTitleName(1))
        print(status)
        if status and "doing" in status:
            return True
        return False

    def getResult(self):
        status = self.win_manage.getMmptStatus(self.win_manage.getMmptTitleName(1))
        print(status)
        if status and "pass" in status:
            return True
        return False

    def getMmptStatus(self, title):
        status = self.win_manage.getMmptStatus(title)
        if status is None:
            return None
        if "doing" in status:
            return MmptTool.MMPT_STATUS_DOING
        elif "pass" in status:
            return MmptTool.MMPT_STATUS_PASS
        elif "fail" in status:
            return MmptTool.MMPT_STATUS_FAIL
        elif "ready" in status:
            return MmptTool.MMPT_STATUS_READY
        return None

    def waitMmptDone(self, timeout = 60, click_run = False):
        stime = time.time()
        self.is_active = True
        self.clearCalData()
        self.dev_abort_event.clear()
        while True:
            title = self.win_manage.getMmptTitleName(2)
            if title and "lte" in title.lower():
                item = "LTE"
            elif title and "gsm" in title.lower():
                item = "GSM"
            else:
                item = "MMPT"
            if self.dev_abort_event.isSet():
                self.dev_abort_event.clear()
                self.is_active = False
                return (MmptTool.PROCESS_NG_ABORT, "%s :MMPT 运行时设备被拔出或重启,%d"%(item, int(time.time()-stime)))

            if time.time() - stime > timeout:
                self.is_active = False
                return (MmptTool.PROCESS_NG_TIMEOUT, "%s: MMPT 等到返回结果超时 timeout: %d"%(item, timeout))


            status = self.getMmptStatus(title)

            if status == MmptTool.MMPT_STATUS_READY:
                if click_run:
                    self.win_manage.clickButton(title, "Button", "RUN")
                time.sleep(10)
            elif status == MmptTool.MMPT_STATUS_DOING:
                time.sleep(.5)
                continue
            elif status == MmptTool.MMPT_STATUS_PASS:
                self.is_active = False
                return (MmptTool.PROCESS_SUCCESS, "%s: MMPT 返回成功,%d"%(item, int(time.time()-stime)))
            elif status == MmptTool.MMPT_STATUS_FAIL:
                self.is_active = False
                print("Get Error code handle: ", self.error_code_handle)
                error_code = self.win_manage.getErrorCode(self.error_code_handle)
                print("error code: ", error_code)
                if error_code == "":
                    error_code = "无"
                return (MmptTool.PROCESS_NG_RF, "%s: MMPT 返回错误(%s),%d"%(item, error_code, int(time.time()-stime)))

            time.sleep(1)

    def getStatus(self):
        return self.win_manage.getMmptStatus(self.win_manage.getMmptTitleName(1))

    def lossFileMerge(self, src_loss_file):
        # src_loss_file = r"./data/XTC\CableLoss.ini"
        dst_loss_file = self.losset_cfg_path

        gsm_item_mapping = {"EGSM": "GSM900", "DCS": "DCS1800", "G850": "GSM850", "PCS": "PCS1900"}
        lte_item_mapping = {"LTE_B1": "B1","LTE_B2": "B2", "LTE_B3": "B3", "LTE_B4": "B4","LTE_B5": "B5",
                            "LTE_B7": "B7","LTE_B8": "B8","LTE_B12": "B12","LTE_B13": "B13","LTE_B18": "B18",
                            "LTE_B19": "B19","LTE_B20": "B20","LTE_B26": "B26",
                            "LTE_B28": "B28", "TDDLTE_B34": "B34",
                            "TDDLTE_B38": "B38", "TDDLTE_B39": "B39", "TDDLTE_B40": "B40", "TDDLTE_B41": "B41"}

        cfg_dst = configparser.ConfigParser(strict=False)
        cfg_dst.optionxform = str
        cfg_dst.read(dst_loss_file)

        cfg_src = configparser.ConfigParser()
        cfg_src.optionxform = str
        cfg_src.read(src_loss_file)

        for band in gsm_item_mapping.keys():
            val = cfg_src["CABLELOSS_0"][band + "_UP"] + "," + cfg_src["CABLELOSS_0"][band + "_DL"] + ",0,0,0"
            cfg_dst.set("GSMLossSetting", gsm_item_mapping[band], val)

        for band in lte_item_mapping.keys():
            val = cfg_src["CABLELOSS_0"][band + "_UP"] + "," + cfg_src["CABLELOSS_0"][band + "_DL"] + ",0,0,0"
            cfg_dst.set("LTELossSetting", lte_item_mapping[band], val)
        cfg_dst.write(open(dst_loss_file, "w"))
        self.reloadLossset()

    def getLossset(self, band):

        val_list = self.loss_cfg_parser.get("LTELossSetting", "B%d" %band )
        val_list = val_list.split(",")
        return [float(val) for val in val_list[:3]]

    def configLosssetClear(self,val):
        init_val = "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,0,0,0"%(val,val,val,val,val,val)
        init_lte_band = [1,2,3,4,5,6,7,8,9,12,13,14,18,19,20,26,28,34,38,39,40,41]
        # init_gsm_band = ["GSM900", "DCS1800", "GSM850", "PCS1900"]

        for lte_band in init_lte_band:
            self.loss_cfg_parser.set("LTELossSetting", "B%d"%(lte_band), init_val)
        # for gsm_band in init_gsm_band:
        #     cfg_lossset.set("GSMLossSetting", gsm_band, init_val)

        self.loss_cfg_parser.write(open(self.losset_cfg_path, "w"))

    def configLossset(self, band ,val_dl,val_up):

        val = val_up + val_dl
        val += "0,0,0"

        self.loss_cfg_parser.set("LTELossSetting", "B%d" % (band), val)

        self.loss_cfg_parser.write(open(self.losset_cfg_path, "w"))

    def reloadLossset(self):

        self.loss_cfg_parser = configparser.ConfigParser(strict=False)
        self.loss_cfg_parser.optionxform = str
        self.loss_cfg_parser.read(self.losset_cfg_path)
