import os,threading,shutil,zipfile,logging
from ctypes import *
from common.utils import *
import os,sys

# os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
dll_path = getAppRootPath()+"./EMAT/0"
if dll_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + dll_path
    print(os.environ["PATH"])
class EcSlot:
    PROCESS_LTE_CAL = 0x00
    PROCESS_GSM_CAL = 0x01
    PROCESS_LTE_NST = 0x02
    PROCESS_GSM_NST = 0x03
    PROCESS_CAB_LOSS = 0x04
    PROCESS_COMPLETE = 0x05



    PROCESS_NG_TIMEOUT = -0X01
    PROCESS_NG_ABORT = -0X02
    PROCESS_NG_RF = -0X03
    PROCESS_SUCCESS = 0x00
    loss_cfg_path = os.path.join(getAppRootPath(), "data/XTC/ec_CableLoss.ini")
    @staticmethod
    def checkLosssetEnabel(fw_version_name):

        if not os.path.exists(EcSlot.loss_cfg_path):
            print(EcSlot.loss_cfg_path)
            return (False,"线损文件不存在")

        if int(time.time() - os.path.getmtime(EcSlot.loss_cfg_path)) > 14*24*60*60:
            return (False,"线损文件左后修改时间过期")

        cfg_src = configparser.ConfigParser(strict=False)
        cfg_src.optionxform = str
        cfg_src.read(EcSlot.loss_cfg_path)

        if not cfg_src.has_section("StationInfo") or time.time() -  int(cfg_src["StationInfo"]["cal_time"]) > 14 * 24 * 60 *60:
            return (False, "线损文件[%s]更新时间已过期"%(EcSlot.loss_cfg_path))
        print(cfg_src["Platform"]["version"][0:5],fw_version_name[0:5])
        if not cfg_src.has_section("Platform") or not cfg_src["Platform"]["version"][0:5].__eq__(fw_version_name[0:5]) :
            return (False, "线损文件[%s]和当前项目不匹配"%(EcSlot.loss_cfg_path))
        return (True,"")

    def unzipEmatTool(self, src, dst):
        if not os.path.exists(src):
            raise Exception("%s 文件不存在!请将改文件放置到 data目录下"%(src))

        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.makedirs(dst)

        zip_file = zipfile.ZipFile(src)
        check_path  = os.path.join(dst, self.emat_check_fname)
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
                logging.info("EMAT 工具上次已经完整解压")
                return

        fd = open(check_path, "wb+")
        for file in zip_file.namelist():
            zip_file.extract(file, dst)
            fd.write(file.encode()+b"\r\n")
        zip_file.close()
        fd.close()

    def prepTool(self):
        cal_Ecfg = os.path.normpath(os.path.join(getAppRootPath(), "./EMAT/main/EM_set/cal/EC618_#Calibration_NodeEditorConfigure.xml"))
        cal_RFcfg = os.path.normpath(
            os.path.join(getAppRootPath(), "./EMAT/main/EM_set/cal/EC618_#Calibration_RFTest.xml"))
        nst_Ecfg = os.path.normpath(
            os.path.join(getAppRootPath(), "./EMAT/main/EM_set/nst/EC618_#Nst_NodeEditorConfigure.xml"))
        nst_RFcfg = os.path.normpath(
            os.path.join(getAppRootPath(), "./EMAT/main/EM_set/nst/EC618_#Nst_RFTest.xml"))
        loss_Ecfg = os.path.normpath(
            os.path.join(getAppRootPath(), "./EMAT/main/EM_set/loss/EC618_#CabLossCalc_NodeEditorConfigure.xml"))
        loss_RFcfg = os.path.normpath(
            os.path.join(getAppRootPath(), "./EMAT/main/EM_set/loss/EC618_#CabLossCalc_RFTest.xml"))
        cfg_ini = os.path.normpath(
            os.path.join(getAppRootPath(), "./EMAT/main/EM_set/cfg/cis_config.ini"))

        self.unzipEmatTool(self.tool_zip_path, self.emat_root_path)
        if not os.path.exists(cfg_ini):
            raise Exception("Emat工具配置文件缺失")

        shutil.copyfile(cfg_ini,self.tool_ini)
        cfg = configparser.ConfigParser(strict=False)
        cfg.optionxform = str
        cfg.read(self.tool_ini)
        # unzip scrip
        if self.process_type == self.PROCESS_LTE_CAL:
            if not os.path.exists(cal_Ecfg) or not os.path.exists(cal_RFcfg):
                raise Exception("校准配置文件缺失")
            shutil.copyfile(cal_Ecfg, os.path.join(self.emat_root_path, "Config/EC618_#Calibration_NodeEditorConfigure.xml"))
            shutil.copyfile(cal_RFcfg, os.path.join(self.emat_root_path, "Data/RFTestConfiXml/EC618_#Calibration_RFTest.xml"))
            cfg["Machine"]["MachineType"] = "EC618_#Calibration"
        elif self.process_type == self.PROCESS_LTE_NST:
            if not os.path.exists(nst_Ecfg) or not os.path.exists(nst_RFcfg):
                raise Exception("综测配置文件缺失")
            shutil.copyfile(nst_Ecfg, os.path.join(self.emat_root_path, "Config/EC618_#Nst_NodeEditorConfigure.xml"))
            shutil.copyfile(nst_RFcfg, os.path.join(self.emat_root_path, "Data/RFTestConfiXml/EC618_#Nst_RFTest.xml"))
            cfg["Machine"]["MachineType"] = "EC618_#Nst"
        elif self.process_type == self.PROCESS_CAB_LOSS:
            if not os.path.exists(loss_Ecfg) or not os.path.exists(loss_RFcfg):
                raise Exception("综测配置文件缺失")
            shutil.copyfile(loss_Ecfg, os.path.join(self.emat_root_path, "Config/EC618_#CabLossCalc_NodeEditorConfigure.xml"))
            shutil.copyfile(loss_RFcfg, os.path.join(self.emat_root_path, "Data/RFTestConfiXml/EC618_#CabLossCalc_RFTest.xml"))
            cfg["Machine"]["MachineType"] = "EC618_#CabLossCalc"
        else:
            raise Exception("Process Type error")



        cfg["InstrumentInfo"]["InstrType"] = "CMW500"
        cfg["InstrumentInfo"]["InstrIP"] = self.cfg.cmw_ip_addr
        # cfg["InstrumentInfo"]["InstrRout"] = self.cfg.cmw_slot
        # cfg["InstrumentInfo"]["InstrPort"] = 'RF1COM'

        cfg["InstrumentInfo"]["InstrRout"] = '0' if self.cfg.cmw_slot.__eq__("0") else '1'
        cfg["InstrumentInfo"]["InstrPort"] = 'RF1COM' if self.cfg.cmw_slot.__eq__("0") else 'RF3COM'
        # loss merge
        if self.process_type != self.PROCESS_CAB_LOSS:
            loss_cfg = configparser.ConfigParser(strict=False)
            loss_cfg.optionxform = str
            loss_cfg.read(self.loss_cfg_path)
            print(loss_cfg["Loss"].keys())
            for band in loss_cfg["Loss"].keys():
                print(band, loss_cfg["Loss"][band])
                cfg["Loss"][band] = loss_cfg["Loss"][band]

        cfg.write(open(self.tool_ini, "w+"))

    def lossUpdate(self):
        # print(self.loss_res_path)
        if not os.path.exists(self.loss_res_path):
            return None

        with open(self.loss_res_path) as fd:
            loss_rec_lines = fd.readlines()
        band_info = {}
        for line in loss_rec_lines[1:]:
            band,freq,val = line.strip().replace(" ", "").split(',')
            print(band,freq,val)
            if "Band"+band not in band_info.keys():
                band_info["Band"+band] = ""
            if len(band_info["Band"+band]) > 0:
                band_info["Band" + band] +=","
            band_info["Band"+band] +="%s,%.1f"%(freq,float(val))
        print(band_info)
        return band_info

    def lossSave(self, loss_info, fw_version, station_num, ):
        src_loss_cfg_path = os.path.join(getAppRootPath(),"data/XTC/ec_CableLoss.ini")
        cfg = configparser.ConfigParser(strict=False)
        cfg.optionxform = str
        cfg.read(src_loss_cfg_path)

        if not cfg.has_section("Loss"):
            cfg.add_section("Loss")
        for band in loss_info.keys():
            cfg.set("Loss", band, loss_info[band])
        if not cfg.has_section("StationInfo"):
            cfg.add_section("StationInfo")
        if not cfg.has_section("Platform"):
            cfg.add_section("Platform")
        ctime = str(int(time.time()))
        cfg.set("StationInfo", "cal_time", ctime)
        cfg.set("StationInfo", "station_num", str(station_num))
        cfg.set("StationInfo", "SofterWareVersion", str(getAppVersion()))
        cfg.set("Platform", "version", fw_version)
        cfg.write(open(src_loss_cfg_path, "w+"))

    def __init__(self, process_type, cfg):
        self.cfg = cfg
        self.emat_check_fname = "CIS_EC_Tool.cfg"
        self.emat_root_path = os.path.normpath(os.path.join(getAppRootPath(), "./EMAT/0/"))
        if os.path.exists(self.emat_root_path):
            shutil.rmtree(self.emat_root_path)
        os.makedirs(self.emat_root_path)
        print(os.getcwd())
        self.threadId = 1
        self.init_path = getAppRootPath()

        self.process_type = process_type

        self.tool_zip_path = os.path.normpath(os.path.join(getAppRootPath(), "./data/emat_tool.zip"))
        self.scrip_path = os.path.normpath(os.path.join(getAppRootPath(), "./data/EM_set.zip"))

        self.iniPath = os.path.normpath(os.path.join(self.emat_root_path, "./Config/cis_config.ini")).encode('utf-8')
        if process_type == self.PROCESS_LTE_CAL:
            self.xmlPath = os.path.normpath(os.path.join(self.emat_root_path, "./Config/EC618_#Calibration_NodeEditorConfigure.xml")).encode('utf-8')
        elif process_type == self.PROCESS_LTE_NST:
            self.xmlPath = os.path.normpath(
                os.path.join(self.emat_root_path, "./Config/EC618_#Nst_NodeEditorConfigure.xml")).encode('utf-8')
        elif process_type == self.PROCESS_CAB_LOSS:
            self.xmlPath = os.path.normpath(
                os.path.join(self.emat_root_path, "./Config/EC618_#CabLossCalc_NodeEditorConfigure.xml")).encode('utf-8')
        self.tool_ini = os.path.normpath(
            os.path.join(self.emat_root_path, "./Config/cis_config.ini"))
        self.loss_res_path = os.path.normpath(
            os.path.join(self.emat_root_path, "./GoldMachineLoss_1.txt"))
        self.start_event = threading.Event()
        self.start_event.clear()
        self.done_event = threading.Event()
        self.done_event.clear()
        self.process_res = False
        self.err_msg = ''

        self.prepTool()

        self.dll_path = os.path.normpath(os.path.join(self.emat_root_path, "./TestServiceDlls/RfCalcTestAPI.dll"))
        print(self.dll_path)

        print(self.iniPath, self.xmlPath)
        # self.start()

    def _process(self, at_port):
        cfg = configparser.ConfigParser(strict=False)
        cfg.optionxform = str
        cfg.read(self.tool_ini)
        cfg["UartInfo"]["Port"] = at_port
        cfg.write(open(self.tool_ini, "w+"))
        os.chdir(getAppRootPath() + "./EMAT/0")
        hDll = CDLL(self.dll_path)
        # RFCalcNstStart function
        self.fun_RFCalcNstStart = hDll.RFCalcNstStart
        self.fun_RFCalcNstStart.argtypes = [c_int32, c_char_p, c_char_p, POINTER(c_int32), c_char_p]
        self.fun_RFCalcNstStart.restype = c_int32

        # RFCalcNstStop funciton
        self.fun_RFCalcNstStop = hDll.RFCalcNstStop
        self.fun_RFCalcNstStop.argtypes = [c_int32]
        self.fun_RFCalcNstStop.restype = None

        errId = c_int32(0)
        pErrId = pointer(errId)
        errMsg = create_string_buffer('a'.encode('utf-8'), 2000)
        errMsgAddr = addressof(errMsg)
        ret = c_int32(-1)

        try:
            print("start fun_RFCalcNstStart")
            ret = self.fun_RFCalcNstStart(self.threadId, self.iniPath, self.xmlPath, errId, errMsg)
            print(ret)
        except Exception as e:
            print("Exception: %s" % e)
            self.process_res, self.err_msg = False,str(e)
        os.chdir(self.init_path)
        self.process_res, self.err_msg = (True, "") if ret == 0 else (False,string_at(errMsgAddr).decode('utf-8'))
        print(self.process_res, self.err_msg)
        self.done_event.set()
        self.start_event.clear()


    def start(self, at_port):
        if self.start_event.isSet():
           return False
        self.start_event.set()
        self.done_event.clear()
        threading.Thread(target=self._process, args=(at_port, )).start()


    def stop(self):
        if not self.start_event.isSet():
            return True
        # self.fun_RFCalcNstStop(self.threadId)
        self.done_event.wait()
        self.start_event.clear()
        os.chdir(self.init_path)

    def getStatus(self):
        pass

    def waitComplete(self, timeout = 60):
        if self.done_event.wait(timeout) is None:
            self.stop()
            return (False, "等待结果超时")

        return (self.process_res, self.err_msg)