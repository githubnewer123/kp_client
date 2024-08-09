import os,shutil,subprocess,time,threading,logging
import common.utils as Utils
import zipfile,configparser,psutil,signal
from manager.window_manager import WindowsManager

class MmptSlot():

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

    @staticmethod
    def getProcess(process):
        info = ["LTE校准","GSM校准","LTE综测","GSM综测","RF测试全部"]
        return info[process]

    def cmwConfig(self):
        dst_cmw_cfg = Utils.getAppRootPath() + "MMPT\%s\MMPT_Tool\Exec\config\DevLossConfig.ini" % (str(self.slot_num))
        cfg_dst = configparser.ConfigParser(strict=False)
        cfg_dst.optionxform = str
        cfg_dst.read(dst_cmw_cfg)
        cfg_dst.set("DeviceSetting", "IPAddress", str(self.slot_config.cmw_ip_addr))
        cfg_dst.set("DeviceSetting", "Instrument slot", str(self.slot_config.cmw_slot))
        cfg_dst.set("DeviceSetting", "IPPort", str(self.slot_config.cmw_slot))
        cfg_dst.write(open(dst_cmw_cfg, "w"))


    def lossFileMerge(self,src_loss_file, dst_loss_file):
        # src_loss_file = r"XTC\CableLoss.ini"
        # dst_loss_file = r"DevLossConfig.ini"

        gsm_item_mapping = {"EGSM": "GSM900", "DCS": "DCS1800", "G850": "GSM850", "PCS": "PCS1900"}

        if "TR3B-RG-SE00" in self.slot_config.project_version:
            lte_item_mapping = {"LTE_B1": "B1", "LTE_B3": "B3", "LTE_B5": "B5","LTE_B7": "B7", "LTE_B8": "B8",
                                "LTE_B20": "B20","TDDLTE_B38": "B38","TDDLTE_B40": "B40", "TDDLTE_B41": "B41"}
        elif "TR3B-RG-SN00" in self.slot_config.project_version:
            lte_item_mapping = {"LTE_B2": "B2", "LTE_B4": "B4", "LTE_B5": "B5", "LTE_B7": "B7", "LTE_B8": "B8", "LTE_B12": "B12",
                                "LTE_B13": "B13","TDDLTE_B41": "B41"}
        elif "-SG-LE" in self.slot_config.project_version:
            lte_item_mapping = {"LTE_B1": "B1", "LTE_B3": "B3", "LTE_B5": "B5","LTE_B7": "B7", "LTE_B8": "B8",
                                "LTE_B20": "B20","LTE_B28": "B28"}
        else:
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

        # if cfg_src.has_section("LastModified"):
        #     if int(cfg_src["LastModified"]["DATE"]) - int(time.time()) > 7*24*60:
        #         raise Exception("线损文件过期，请使用金板重新生成")
        if "LTELossSetting" in cfg_dst.sections():
            cfg_dst.remove_section("LTELossSetting")
            cfg_dst.add_section("LTELossSetting")
        for band in gsm_item_mapping.keys():
            val = cfg_src["CABLELOSS_0"][band + "_UP"] + "," + cfg_src["CABLELOSS_0"][band + "_DL"] + ",0,0,0"
            cfg_dst.set("GSMLossSetting", gsm_item_mapping[band], val)

        for band in lte_item_mapping.keys():
            val = cfg_src["CABLELOSS_0"][band + "_UP"] + "," + cfg_src["CABLELOSS_0"][band + "_DL"] + ",0,0,0"
            cfg_dst.set("LTELossSetting", lte_item_mapping[band], val)
        cfg_dst.write(open(dst_loss_file, "w"))

    def mmpt_config(self):

        config = {"Lte_Cal": {"path": "", "enable":self.lte_cal}, "Gsm_Cal": {"path": "", "enable":self.gsm_cal},
                  "Lte_Nst": {"path": "", "enable":self.lte_nst}, "Gsm_Nst": {"path": "", "enable":self.gsm_nst},
                  "WB": {"path": "", "enable":True}}
        for item in config.keys():
            if config[item]["enable"] is False:
                continue
            path = Utils.getAppRootPath() + "MMPT/main/M_set/" + item
            for bin_file in os.listdir(path):
                if os.path.isfile(path + "/" + bin_file) and (bin_file.endswith(".tb") or bin_file.endswith(".txt")):
                    config[item]["path"] = path + "/" + bin_file
                    break
            else:
                raise Exception("MMPT_SLOT: 脚本文件 %s 未找到"%(item))

        Utils.cfgWrite(self.tool_cfg_path, "CommSetting", "bEnableTE1", str(1 if self.lte_cal is True else 0))
        Utils.cfgWrite(self.tool_cfg_path, "CommSetting", "bEnableTE2", str(1 if self.gsm_cal is True else 0))
        Utils.cfgWrite(self.tool_cfg_path, "CommSetting", "bEnableTE3", str(1 if self.lte_nst is True else 0))
        Utils.cfgWrite(self.tool_cfg_path, "CommSetting", "bEnableTE4", str(1 if self.gsm_nst is True else 0))

        Utils.cfgWrite(self.tool_cfg_path, "CommSetting", "TestEngineScript1", config["Lte_Cal"]["path"])
        Utils.cfgWrite(self.tool_cfg_path, "CommSetting", "TestEngineScript2", config["Gsm_Cal"]["path"])
        Utils.cfgWrite(self.tool_cfg_path, "CommSetting", "TestEngineScript3", config["Lte_Nst"]["path"])
        Utils.cfgWrite(self.tool_cfg_path, "CommSetting", "TestEngineScript4", config["Gsm_Nst"]["path"])

        if self.slot_config.project_version[5:].startswith("-SG-"):
            Utils.cfgWrite(self.tool_cfg_path, "CommSetting", "BOOTCMD", "0")

        shutil.copyfile(config["WB"]["path"], Utils.getAppRootPath() + "MMPT/" + str(self.slot_num) + "/MMPT_Tool/TestEngine/Tests-Dlls/"+os.path.basename(config["WB"]["path"]))

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

    def clearCalData(self):
        # 删除CalData信息
        if not os.path.exists(self.cal_data_path):
            os.mkdir(self.cal_data_path)
        else:
            files = os.listdir(self.cal_data_path)
            for file in files:
                if not file == "UiLog":
                    shutil.rmtree(self.cal_data_path + "/" + file)

    def checkLosssetToolVersion(self, version, check_version):
        if "LossSetCal" not in version:
            return False

        cur_version =  int(version.replace("LossSetCal-V", "").replace(".",""))
        if cur_version < check_version:
            return False
        return True

    def prepareMmptTool(self, slot_num):
        if not os.path.exists( "MMPT/log/%d"%(slot_num)):
            os.makedirs("MMPT/log/%d"%(slot_num))

        # 检查M_set DB_set文件存在
        m_set_path = os.path.join(Utils.getAppRootPath() + "MMPT/main/M_set")
        db_set_path = os.path.join(Utils.getAppRootPath() + "MMPT/main/DB_set")
        if not os.path.exists(m_set_path):
            logging.info(m_set_path)
            raise Exception("MMPT Tool: Folder missing: MMPT/main/M_set")

        if not os.path.exists(db_set_path):
            logging.info(db_set_path)
            raise Exception("MMPT Tool: Folder missing: MMPT/main/DB_set")

        # 检查MMPT tool工具上次解压完整
        if self.slot_config.mmpt_tool_update:
            zip_src = os.path.join(Utils.getAppRootPath(), "data/mmpt_tool.zip")
            zip_dst = os.path.join(Utils.getAppRootPath(), "MMPT/%s/MMPT_Tool"%(str(slot_num)))
            self.unzipMmptTool(zip_src, zip_dst)

        # copy DB_set到main工具下
        ue_db_path = os.path.join(Utils.getAppRootPath() + "MMPT/%d/MMPT_Tool/Exec/DB/UE_Commands.mdb"%(slot_num))
        nvm_db_path = os.path.join(Utils.getAppRootPath() + "MMPT/%d/MMPT_Tool/Exec/DB/NVM.mdb"%(slot_num))
        txt_db_path = os.path.join(Utils.getAppRootPath() + "MMPT/%d/MMPT_Tool/Exec/DB/MDB.txt" % (slot_num))

        # 找到服务器下载的DB文件
        print(self.slot_config.mmpt_version)
        if self.slot_config.mmpt_version.__eq__("MMPT-RF16.010-P3(CIS-CMW100)-V1.2"):
            if os.path.exists(ue_db_path):
                os.remove(ue_db_path)
            if os.path.exists(nvm_db_path):
                os.remove(nvm_db_path)

            for item in os.listdir(Utils.getAppRootPath() + "MMPT/main/DB_set/NVM"):
                if "_cp_NVM." in item:
                    shutil.copy(Utils.getAppRootPath() + "MMPT/main/DB_set/NVM/"+item, nvm_db_path)
            for item in os.listdir(Utils.getAppRootPath() + "MMPT/main/DB_set/UE"):
                if "_cp_UE_" in item:
                    shutil.copy(Utils.getAppRootPath() + "MMPT/main/DB_set/UE/" + item, ue_db_path)
        elif self.slot_config.__eq__("MMPT RF16.010 Release P7"):
            if os.path.exists(txt_db_path):
                os.remove(txt_db_path)
            for item in os.listdir(Utils.getAppRootPath() + "MMPT/main/DB_set/TXT"):
                if "cp_MDB.txt" in item:
                    shutil.copy(Utils.getAppRootPath() + "MMPT/main/DB_set/TXT/" + item, txt_db_path)
        else:
            raise Exception("MMPT 工具版本出错")

        # 配置tool上需要运行哪些校正和综测脚本
        self.mmpt_config()

        # 删除CalData信息
        self.clearCalData()

        # loss file merge
        src_loss = Utils.getAppRootPath()+"data/XTC/CableLoss.ini"
        dst_loss = Utils.getAppRootPath()+"MMPT\%s\MMPT_Tool\Exec\config\DevLossConfig.ini"%(str(slot_num))
        if not os.path.exists(src_loss):
            if not os.path.exists(Utils.getAppRootPath()+"data/XTC/"):
                os.makedirs(Utils.getAppRootPath()+"data/XTC/")
            raise Exception("MMPT: 线损文件不存在,请将该工位线损文件放置下面路径中:\r\n%s"%(src_loss))

        # print(time.time() - os.path.getmtime(src_loss))


        if int(time.time() - os.path.getmtime(src_loss)) > 14*24*60*60:
            print(time.time(), os.path.getmtime(src_loss))
            print(int(time.time() - os.path.getmtime(src_loss)))
            raise Exception("MMPT: 线损文件[%s]最后修改时间已过期， 请使用工具重新确认线损值" % (src_loss))

        cfg_src = configparser.ConfigParser()
        cfg_src.optionxform = str
        cfg_src.read(src_loss)

        if not cfg_src.has_section("StationInfo") or time.time() -  int(cfg_src["StationInfo"]["cal_time"]) > 14 * 24 * 60 *60:
            raise Exception("MMPT: 线损文件[%s]更新时间已过期， 请使用工具重新确认线损值" % (src_loss))

        if not cfg_src.has_section("Platform") or not cfg_src["Platform"]["version"][0:5].__eq__(self.slot_config.fw_version_name[0:5]) :
            raise Exception("MMPT: 线损文件[%s]和当前项目不匹配,请用 ZX%s 模组金板重新生成线损文件" % (src_loss, self.slot_config.fw_version_name[0:5]))
        print(cfg_src["Platform"]["version"], self.slot_config.fw_version_name)
        if "RGBF" in self.slot_config.fw_version_name:
            if not cfg_src["Platform"]["version"][5:8].__eq__(self.slot_config.fw_version_name[5:8]):
                raise Exception(
                    "MMPT: 线损文件[%s]和当前项目不匹配,请用 ZX%s 模组金板重新生成线损文件" % (src_loss, self.slot_config.fw_version_name[0:8]))

        if "SofterWareVersion" not in cfg_src["StationInfo"].keys() or self.checkLosssetToolVersion(cfg_src["StationInfo"]["SofterWareVersion"], 14) is False:
            raise Exception("MMPT: 线损文件[%s]版本错误， 请使用工具V1.4以上版本重新确认线损值" % (src_loss))

        self.lossFileMerge(src_loss,dst_loss)

        # CMW ip & slot config set
        self.cmwConfig()


    def __init__(self, slot_num, config, fault_signal = None):
        # if lte_cal is False and gsm_cal is False and lte_nst is False and gsm_nst is False:
        #     raise Exception("MmptSlot: LTE/GSM校准和综测至少要设置一项")
        self.slot_config = config
        self.fault_signal = fault_signal
        self.slot_num = slot_num
        self.lte_cal = self.slot_config.cal_lte
        self.lte_nst = self.slot_config.nst_lte
        self.gsm_cal = self.slot_config.cal_gsm
        self.gsm_nst = self.slot_config.nst_gsm
        if int(self.slot_config.station_type) == 0:
            self.lte_nst = False
            self.gsm_nst = False
        if int(self.slot_config.station_type) == 1:
            self.lte_cal = False
            self.gsm_cal = False
        self.process_step = [ {"enable":self.lte_cal, "check_name":"LteCal"},
                              {"enable": self.gsm_cal, "check_name": "GsmCal"},
                              {"enable": self.lte_nst, "check_name": "LteNst"},
                              {"enable": self.gsm_nst, "check_name": "GsmNst"}]

        self.pid = None
        self.error_code_handle = 0
        self.tool_cfg_path = Utils.getAppRootPath() + "MMPT\%d\MMPT_Tool\Exec\MMPT.ini" % (self.slot_num)
        self.exe_path = Utils.getAppRootPath() + "MMPT\%d\MMPT_Tool\Exec\MMPT.exe" % (self.slot_num)
        self.cal_data_path = Utils.getAppRootPath() + "MMPT\\" + str(self.slot_num) + "\MMPT_Tool\CalData"

        self.run_thread = None
        self.exit_event = threading.Event()
        self.start_event = threading.Event()
        self.dev_abort_event = threading.Event()
        self.notify = None
        self.mmpt_check_fname = "CIS_mmpt_Tool.cfg"

        self.is_active = False
        self.is_opened = False
        self.win_manage = WindowsManager()
        self.run_thread = threading.Thread(target=self.run_thread_handle, args=())
        self.run_thread.setDaemon(True)
        self.run_thread.start()


    def getLteCal(self):
        return self.lte_cal

    def getGsmCal(self):
        return self.gsm_cal

    def getLteNst(self):
        return self.lte_nst

    def getGsmNst(self):
        return self.gsm_nst

    def reset(self):
        shutil.rmtree(Utils.getAppRootPath() + "MMPT/" + str(self.slot_num))
        shutil.copytree(Utils.getAppRootPath() + "MMPT/main", Utils.getAppRootPath() + "MMPT/" + str(self.slot_num))
        self.mmpt_config()

    def kill(self):
        pid_dict = {}
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            pid_dict[pid] = p.name()
        for t in pid_dict.keys():
            if pid_dict[t] == "MMPT.exe":
                os.kill(t, signal.SIGABRT)
                self.error_code_handle = 0
        self.is_opened = False

    def restart(self):
        pid_dict = {}
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            pid_dict[pid] = p.name()
        for t in pid_dict.keys():
            if pid_dict[t] == "MMPT.exe":
                os.kill(t, signal.SIGABRT)
                self.error_code_handle = 0
        self.openMMPT()

    def __get_MMPT_pid(self):
        cmd = "wmic process where name=\"MMPT.exe\" get executablepath,processid"
        ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        cur_path = b"\\MMPT\\%d\\MMPT_Tool\\Exec\\MMPT.exe"%(self.slot_num)
        while True:
            for line in iter(ret.stdout.readline, b""):
                if cur_path in line:
                    self.pid = int(line.decode().strip().replace(" ","").split("MMPT.exe")[-1])
                    print("Get PID: %d"%( self.pid))
                    return

    def getMmptStatus(self, title):
        status = self.win_manage.getMmptStatus(title)
        if status is None:
            return None
        if "doing" in status:
            return MmptSlot.MMPT_STATUS_DOING
        elif "pass" in status:
            return MmptSlot.MMPT_STATUS_PASS
        elif "fail" in status:
            return MmptSlot.MMPT_STATUS_FAIL
        elif "ready" in status:
            return MmptSlot.MMPT_STATUS_READY
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
                return (MmptSlot.PROCESS_NG_ABORT, "%s :MMPT 运行时设备被拔出或重启,%d"%(item, int(time.time()-stime)))

            if time.time() - stime > timeout:
                self.is_active = False
                return (MmptSlot.PROCESS_NG_TIMEOUT, "%s: MMPT 等到返回结果超时 timeout: %d"%(item, timeout))


            status = self.getMmptStatus(title)

            if status == MmptSlot.MMPT_STATUS_READY:
                if click_run:
                    self.win_manage.clickButton(title, "Button", "RUN")
                time.sleep(10)
            elif status == MmptSlot.MMPT_STATUS_DOING:
                time.sleep(.5)
                continue
            elif status == MmptSlot.MMPT_STATUS_PASS:
                self.is_active = False
                return (MmptSlot.PROCESS_SUCCESS, "%s: MMPT 返回成功,%d"%(item, int(time.time()-stime)))
            elif status == MmptSlot.MMPT_STATUS_FAIL:
                self.is_active = False
                print("Get Error code handle: ", self.error_code_handle)
                error_code = self.win_manage.getErrorCode(self.error_code_handle)
                print("error code: ", error_code)
                if error_code == "":
                    error_code = "无"
                return (MmptSlot.PROCESS_NG_RF, "%s: MMPT 返回错误(%s),%d"%(item, error_code, int(time.time()-stime)))

            time.sleep(1)



    def fileCheck(self, res, check_name, timeout):
        stime = time.time()
        while True:
            if time.time() - stime > timeout:
                return None
            files = os.listdir(self.cal_data_path)
            for file in files:
                if file.split("_")[0] == check_name:
                    if res is False and file.split("_")[-1] == "Fail":
                        return os.path.join(self.cal_data_path, file)
            else:
                time.sleep(1)

    def FileGrab(self, timeout):
        check_name = self.process_step[self.cur_process]["check_name"]
        print("start Check Name: ", check_name)
        re_check = True
        self.is_active = True
        mmpt_res = False
        stime = time.time()
        while True:
            stime = time.time()
            # if self.dev_abort_event.isSet():
            #     self.is_active = False
            #     self.dev_abort_event.clear()
            #     return (MmptSlot.PROCESS_NG_ABORT, None)
            #
            # if time.time() - stime > timeout:
            #     self.is_active = False
            #     return (MmptSlot.PROCESS_NG_TIMEOUT, None)
            try:

                status = self.getMmptStatus()
                if status == MmptSlot.MMPT_STATUS_READY:
                    time.sleep(10)
                    continue
                elif status == MmptSlot.MMPT_STATUS_PASS or status == MmptSlot.MMPT_STATUS_FAIL:
                    for file in os.listdir(self.cal_data_path):
                        print(file)
                        if os.path.isdir(os.path.join(self.cal_data_path, file)) and "Cal" in file:
                            fpath = os.path.join(self.cal_data_path, file)
                            for f in os.listdir(fpath):
                                print(f, os.path.getsize(os.path.join(fpath, f)))

                logging.info("get Done cost: %d"%( int(time.time()-stime)))
                time.sleep(.5)
                logging.info("timesleep Done")
            except Exception as e:
                logging.info(str(e))
                logging.info("break")
                break

            # if status == MmptSlot.MMPT_STATUS_FAIL:
            #     return (MmptSlot.PROCESS_NG_RF, self.fileCheck(False,check_name, 4))
            # elif status == MmptSlot.MMPT_STATUS_PASS:
            #     return (MmptSlot.PROCESS_SUCCESS, None)
            # else:
            #     time.sleep(2)

    def initProcess(self):
        self.cur_process = 0
        while True:
            if self.process_step[self.cur_process]["enable"] is True:
                return

            self.cur_process = self.cur_process + 1
            if self.cur_process >= len(self.process_step):
                return False

    def openMMPT(self):
        logging.info("open MMPT Tool: %s"%(self.exe_path))
        cmd = self.exe_path
        subprocess.Popen(cmd)
        self.title = self.win_manage.getMmptTitleName(timeout=6)
        if self.title:
            self.__get_MMPT_pid()
            self.win_manage.winMin(self.title)
            self.error_code_handle = self.win_manage.getErrorCodeHandle(self.title)
            print("Error code handle: ", self.error_code_handle)
            self.win_manage.winActive(self.title)
        self.is_opened = True

    def nextProcess(self):
        while True:
            self.cur_process = self.cur_process + 1
            if self.cur_process >= len(self.process_step):
                return False

            if self.process_step[self.cur_process]["enable"] is True:
                return True

    def getTimeout(self, process):
        if process == self.PROCESS_LTE_CAL:
            return self.slot_config.mmpt_cal_lte_timeout
        elif process == self.PROCESS_GSM_CAL:
            return self.slot_config.mmpt_cal_gsm_timeout
        elif process == self.PROCESS_LTE_NST:
            return self.slot_config.mmpt_nst_lte_timeout
        elif process == self.PROCESS_GSM_NST:
            return self.slot_config.mmpt_nst_gsm_timeout

    def run_thread_handle(self):
        try:
            self.prepareMmptTool(self.slot_num)
            self.openMMPT()
            self.cur_process = 0

            self.clearCalData()
        except Exception as e:
            if self.fault_signal:
                self.fault_signal.emit({"info": str(e)})
            else:
                raise e

        # while True:
        #     if self.exit_event.isSet():
        #         self.exit_event.clear()
        #         break
        #
        #     if self.start_event.isSet():
        #         self.start_event.clear()
        #
        #         self.initProcess()
        #         self.clearCalData()
        #         while True:
        #             logging.info("[%d]start file check index:%d" % (self.slot_num, self.cur_process))
        #             stime = time.time()
        #             res,fpath = self.FileGrab(int(self.getTimeout(self.cur_process)))
        #             if self.notify is not None:
        #                 self.notify(self.slot_num, self.cur_process, res, fpath, int(time.time()-stime))
        #                 if res != MmptSlot.PROCESS_SUCCESS:
        #                     break
        #             if self.nextProcess() is False:
        #                 self.notify(self.slot_num, MmptSlot.PROCESS_COMPLETE, True, None, int(time.time()-stime))
        #                 break
        #             time.sleep(1)
        #
        #     time.sleep(.500)

    def setNotify(self, notify):
        self.notify = notify

    # 检测到有设备接入时调用
    def start(self):
        self.start_event.set()

    def exit(self):
        pass
        # self.exit_event.set()
        # self.run_thread.join(2)

    def stop(self):
        if self.is_active:
            self.cur_process = 0
            self.dev_abort_event.set()

    def isOpened(self):
        return self.is_opened

