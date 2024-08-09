from UI.ui_lossset_window import Ui_LosssetMainWindow
import common.utils as Utils
import sys,cgitb,logging,os,datetime,configparser,json,zipfile

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject,pyqtSignal
import common.utils as Utils
import sys,cgitb,logging,datetime,threading,time,shutil
from manager.nst_parser import NstFileParser

from manager.mmpt_tool import MmptTool
from manager.window_manager import WindowsManager
from device.at_device import AtDevice
from device.dut import Dut

from PyQt5.QtWidgets import QMessageBox,QDialog,QHeaderView
from manager.tool_config import ToolConfig
from manager.app_update import AppUpdate
from view.auto_update_view import AutoUpdateView

class LosssetCalControl(QObject):
    info_update_signal = pyqtSignal(dict)

    def __init__(self,config):
        super().__init__()
        self.config = config
        self.init_val = None
        self.start_event = threading.Event()

        self.isBusy = False

    def start(self, imei, init_val, throushold, slot, is_check_step, db_path, platform_version, script_name, band_list = None):
        if self.isBusy:
            raise Exception("执行中")
        self.imei = imei
        self.is_check = is_check_step
        self.init_val = init_val
        self.throushold = throushold
        self.slot = slot
        self.band_list = band_list
        self.produce_thread = threading.Thread(target=self.__losssetThread, args=(db_path,platform_version, script_name))
        self.produce_thread.setDaemon(True)
        self.produce_thread.start()

    def updateCheckFile(self, file_path):
        md5_path = os.path.join(file_path.replace(os.path.basename(file_path), ""), "__check")
        md5 = Utils.fileMd5(file_path)
        with open(md5_path, "w+") as fd:
            fd.write(md5)

    def _checkLossset(self, src_path, platform_version):
        # dst_loss_file = r"DevLossConfig.ini"
        src_loss_file = r"data\XTC\CableLoss.ini"

        gsm_item_mapping = {"EGSM": "GSM900", "DCS": "DCS1800", "G850": "GSM850", "PCS": "PCS1900"}

        lte_item_mapping = {1: "LTE_B1", 2: "LTE_B2",3: "LTE_B3",4: "LTE_B4", 5: "LTE_B5", 7: "LTE_B7", 8: "LTE_B8", 12: "LTE_B12",
                            13: "LTE_B13", 18: "LTE_B18",19: "LTE_B19",
                            20: "LTE_B20",26: "LTE_B26",28:"LTE_B28",34: "TDDLTE_B34",38: "TDDLTE_B38", 39: "TDDLTE_B39",
                            40: "TDDLTE_B40", 41: "TDDLTE_B41"}

        save_path = os.path.join(Utils.getAppRootPath(), src_loss_file)
        cfg_dst = configparser.ConfigParser(strict=False)
        cfg_dst.optionxform = str
        cfg_dst.read(save_path)

        if self.band_list:
            band_check_list = self.band_list
        else:
            band_check_list = None

        src_parser = NstFileParser(src_path, band_list=band_check_list)
        dst_lossset_path = os.path.join(Utils.getAppRootPath(), "data/lossset/%s.csv"%(self.imei))

        dst_parser = NstFileParser(dst_lossset_path, band_list=band_check_list)
        isUpdate = False
        pre_val = ""

        for band in dst_parser.getBandList():
            src_val = src_parser.getTestResult(band)
            dst_val = dst_parser.getTestResult(band)

            if band == 34:
                val = [round(dst_val[0]-src_val[0], 2) for _ in range(3)]
            else:
                if len(src_val) < 3:
                    self.info_update_signal.emit({"res": None, "info":"测试信息不完整，重新开始"})
                    return True
                val = [round(dst_val[i] - src_val[i], 2) for i in range(3)]
            cur_val = self.mmpt.getLossset(band)
            set_val_UP = ""
            set_val_DL = ""
            for idx in range(3):
                if val[idx] > self.throushold or val[idx] < -self.throushold:
                    set_val = round(cur_val[idx] +val[idx], 2)
                    if set_val <= 0:
                        set_val = self.throushold
                    else:
                        isUpdate = True
                    set_val_UP += str(set_val)
                    set_val_DL += str(round(set_val + (0.1 if band < 33 else 0), 2))
                else:
                    set_val_UP += (str(cur_val[idx]))
                    set_val_DL += (str(round(cur_val[idx] + (0.1 if band < 33 else 0),2)))
                set_val_UP += ","
                set_val_DL += ","
                pre_val = str(cur_val[idx])
            # print("是否为检查阶段？ is_check : %s isUpdate: %s"%(str(self.is_check), str(isUpdate)))
            if self.is_check is True:
                if isUpdate is False:
                    ctime = str(int(time.time()))
                    self.updateCheckFile(save_path)
                    cfg_dst.set("StationInfo", "cal_time", ctime)
                    cfg_dst.set("StationInfo", "station_num", str(self.config.station_num))
                    cfg_dst.set("StationInfo", "SofterWareVersion", str(Utils.getAppVersion()))
                    cfg_dst.set("Platform", "version", str(platform_version))
                    cfg_dst.write(open(save_path, "w"))
                else:
                    self.info_update_signal.emit({"res": None, "info": "B%d_UP set: %s-%s" % ((band), set_val_UP[:-1],pre_val)})
                    self.info_update_signal.emit({"res": None, "info": "B%d_DL set: %s-%s" % ((band), set_val_DL[:-1],pre_val)})
                return isUpdate


            if isUpdate:
                cfg_dst.set("CABLELOSS_0", lte_item_mapping[band] + "_DL", set_val_DL[:-1])
                cfg_dst.set("CABLELOSS_0", lte_item_mapping[band] + "_UP", set_val_UP[:-1])

                print("[update]B%d_UP set:" % (band), cfg_dst["CABLELOSS_0"][lte_item_mapping[band] + "_UP"])
                print("[update]B%d_DL set:" % (band), cfg_dst["CABLELOSS_0"][lte_item_mapping[band] + "_DL"])

                if band == 3:
                    cfg_dst.set("CABLELOSS_0", "DCS_DL", set_val_DL[:-1])
                    cfg_dst.set("CABLELOSS_0", "DCS_UP", set_val_UP[:-1])

                if band == 8:
                    cfg_dst.set("CABLELOSS_0", "EGSM_DL", set_val_DL[:-1])
                    cfg_dst.set("CABLELOSS_0", "EGSM_UP", set_val_UP[:-1])
                if not cfg_dst.has_section("StationInfo"):
                    cfg_dst.add_section("StationInfo")

                if not cfg_dst.has_section("Platform"):
                    cfg_dst.add_section("Platform")

                # cfg_dst.set("StationInfo", "cal_time", ctime)
                cfg_dst.write(open(save_path, "w"))
                self.info_update_signal.emit({"res":None, "info":"B%d_UP set: %s" % ((band), set_val_UP[:-1])})
            self.mmpt.configLossset(band, set_val_DL,set_val_UP)


        return False

    def updateLossset(self, dir, platform_version):
        res = True
        print("List --> ",os.path.join(self.mmpt.cal_data_path, dir))
        for file in os.listdir(os.path.join(self.mmpt.cal_data_path, dir)):
            print(file)
            if "ltenstresult" in file.lower() and file.endswith(".csv"):
                file_src_path = os.path.join(os.path.join(self.mmpt.cal_data_path, dir), file)
                print(file_src_path)
                res = self._checkLossset(file_src_path, platform_version)
                log_path = os.path.join(Utils.getAppRootPath(), "MMPT\log\lossset")
                shutil.copytree(os.path.join(self.mmpt.cal_data_path, dir), log_path+"\%s"%(dir))
                shutil.rmtree(os.path.join(self.mmpt.cal_data_path, dir))
                return res
        return res

    def __losssetThread(self, db_path,  platform_version, scrip_name):
        self.isBusy = True
        scrip_path = os.path.join(Utils.getAppRootPath(), "data/lossset/%s"%(scrip_name))
        if os.path.exists(scrip_path):
            os.remove(scrip_path)
        AppUpdate("LossSetCal").downloadFile("NstResult/%s"%(scrip_name), scrip_path)

        log_path = os.path.join(Utils.getAppRootPath(), "MMPT\log\lossset")
        self.mmpt = MmptTool(os.path.join(Utils.getAppRootPath(), "MMPT/0/MMPT_Tool/"))
        self.mmpt.clearCalData()
        self.mmpt.configScripAllDisable()
        self.mmpt.configRunScrip(0, True, file_path=scrip_path)
        self.mmpt.configFailContinue(True)
        self.mmpt.setAutoTestEnable(True)

        index = 1
        isMmptDone = True
        re_check = True

        if not os.path.exists(log_path):
            os.makedirs(log_path)
        try:
            if self.init_val:
                self.mmpt.configLosssetClear(self.init_val)

            unzip_path = os.path.join(Utils.getAppRootPath(), "data/lossset/DB")
            if os.path.exists(unzip_path):
                shutil.rmtree(unzip_path)
                os.makedirs(unzip_path)
            zip_file = zipfile.ZipFile(os.path.join(Utils.getAppRootPath(), "data/lossset/%s" % (db_path)))
            for file in zip_file.namelist():
                zip_file.extract(file, unzip_path)
            zip_file.close()
            ue_db_path = os.path.join(Utils.getAppRootPath() + "MMPT/0/MMPT_Tool/Exec/DB/UE_Commands.mdb")
            nvm_db_path = os.path.join(Utils.getAppRootPath() + "MMPT/0/MMPT_Tool/Exec/DB/NVM.mdb")
            txt_db_path = os.path.join(Utils.getAppRootPath() + "MMPT/0/MMPT_Tool/Exec/DB/MDB.txt")

            # 找到服务器下载的DB文件
            if platform_version[3:5].__eq__("CG") or platform_version[3:5].__eq__("CH"):
                if os.path.exists(ue_db_path):
                    os.remove(ue_db_path)
                if os.path.exists(nvm_db_path):
                    os.remove(nvm_db_path)
                for item in os.listdir(Utils.getAppRootPath() + "data/lossset/DB/NVM"):
                    if "_cp_NVM." in item:
                        shutil.copy(Utils.getAppRootPath() + "data/lossset/DB/NVM/" + item, nvm_db_path)
                for item in os.listdir(Utils.getAppRootPath() + "data/lossset/DB/UE"):
                    if "_cp_UE_" in item:
                        shutil.copy(Utils.getAppRootPath() + "data/lossset/DB/UE/" + item, ue_db_path)
            else:
                if os.path.exists(txt_db_path):
                    os.remove(txt_db_path)
                for item in os.listdir(Utils.getAppRootPath() + "data/lossset/DB/TXT"):
                    if "_cp_MDB." in item:
                        shutil.copy(Utils.getAppRootPath() + "data/lossset/DB/TXT/" + item, txt_db_path)
            self.mmpt.cmwConfig("172.22.1.3", self.slot)
            timeout = 60

            print("self.is_check?", self.is_check)
            if self.is_check:
                self.mmpt.lossFileMerge(os.path.join(Utils.getAppRootPath(), r"data\XTC\CableLoss.ini"))
            self.mmpt.openMMPT()
            while True:
                self.info_update_signal.emit({"res":None, "info":"打开工具,开始第%d次测试"%(index)})

                isMmptDone = False
                time.sleep(5)

                # while True:
                #     print("开始等待工具ready")
                #     status = self.mmpt.getStatus()
                #     if "doing" not in status:
                #         self.mmpt.run()
                #         time.sleep(3)
                #     else:
                #         break

                print("开始等待工具返回结果")
                stime = time.time()
                while True:
                    if time.time() - stime > timeout:
                        # self.mmpt.kill()
                        self.info_update_signal.emit({"res": False, "info": "等待MMPT返回超时"})
                        self.isBusy = False
                        self.mmpt.kill()
                        return
                    self.mmpt.waitMmptDone(120)
                    files = os.listdir(self.mmpt.cal_data_path)
                    for dir in files:
                        print(dir)
                        if "nst" in dir.split("_")[0].lower():
                            # self.mmpt.kill()
                            self.info_update_signal.emit({"res": None, "info": "测试完成，开始计算线损值[%s]" % (dir)})
                            res = self.updateLossset(dir, platform_version)
                            if res is False:
                                self.info_update_signal.emit({"res": True, "info": "mmpt tool工具配置完成"})
                                self.isBusy = False
                                self.mmpt.kill()
                                return
                            elif self.is_check is True:
                                self.info_update_signal.emit({"res": False, "info": "两个金板计算线损偏差过大，请重启确认!"})
                                self.isBusy = False
                                self.mmpt.kill()
                                return
                            # 重启设备
                            if len(AtDevice.getAtPortList())  > 0:
                                dut = Dut(AtDevice.getAtPortList()[0][0])
                                self.info_update_signal.emit({"res": None, "info": "重启设备完成"})
                                try:
                                    dut.devReset()
                                except Exception as e:
                                    print(str(e))
                                dut.destory()
                            isMmptDone = True
                            break
                    else:
                        time.sleep(2)
                        continue
                    if isMmptDone:
                        isMmptDone = False
                        index += 1
                        break
        except Exception as e:
            self.info_update_signal.emit({"res":False, "info":str(e)})


class CloseEventQMainWindow(QtWidgets.QMainWindow):

    def closeEvent(self, event):
        logging.info("Close by user")
        self.close()

class ProductMainView(Ui_LosssetMainWindow, QObject):

    def msgBox(self,info):
        qmsg = QMessageBox()
        qmsg.question(self.main_win,"警告",info,QMessageBox.Ok)

    def getTimestamp(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    def resInfoAppend(self, info):

        if info.startswith("----"):
            self.res_info_list.append(info)
        else:
            self.res_info_list.append("[%s] %s" % (self.getTimestamp(), info))
        if len(self.res_info_list) > 15:
                self.res_info_list = self.res_info_list[-15:]
        info = ""
        for txt in self.res_info_list:
            info += txt+"\r\n"
        self.info_label.setText(info)

    def losssetCfgStart(self):
        port_list = AtDevice.getAtPortList()
        script_name = "LTE_B1B3B5B8B34B38B39B40B41_GoldenBoard.tb"
        band_list = None
        self.tool_name = "mmpt_tool_lossSet.zip"
        if len(port_list) <= 0:
            self.msgBox("请先接入设备后开始")
            return
        # if not self.mmpt_dwn_done_event.isSet():
        #     self.msgBox("请等待MMPT工具下载完成")
        #     return
        try:
            if len(self.imei_edit.text()) <= 0 or not Utils.isImei(self.imei_edit.text()):
                raise Exception("请先输入IMEI/检查IMEI格式是否正确")
            imei = self.imei_edit.text().strip()
            for dev in self.device_list:
                if imei in dev["IMEI"]:
                    print(dev)
                    cal_date = dev["CAL_DATE"]
                    db_path = dev["DB_PATH"]
                    if "TB_SCRIPT" in dev.keys():
                        script_name = dev["TB_SCRIPT"]
                    if "BAND_LIST" in dev.keys():
                        band_list = dev["BAND_LIST"]
                        print(band_list)

                    if "tool_name" in dev.keys():
                        self.tool_name = dev["tool_name"]
                    break
            else:
                raise Exception("该金板信息未上传服务器")

            if self.is_check_step is False:
                self.imei_1st = imei
            else:
                if self.imei_1st.__eq__(imei):
                    # pass
                    raise Exception("不能使用相同金板进行检查，请更换金板确认")

            for file in os.listdir(os.path.join(Utils.getAppRootPath(), "data/lossset")):
                if imei in file:
                    os.remove(os.path.join(os.path.join(Utils.getAppRootPath(), "data/lossset"), file))
                    break

            self.app_update.downloadFile("DbSet/%s" % (db_path),
                                         os.path.join(Utils.getAppRootPath(), "data/lossset/%s" % (db_path)))
            self.app_update.downloadFile("NstResult/%s.csv"%(imei), os.path.join(Utils.getAppRootPath(), "data/lossset/%s.csv"%(imei)))
            if not os.path.exists(os.path.join(Utils.getAppRootPath(), "data/lossset/%s" % (db_path))):
                raise Exception("下载DB文件失败!")

            print("Open port: ", port_list[0][0])
            dut = Dut(port_list[0][0])
            # dut.checkImei(self.imei)
            cal_info = dut.checkLteCal()
            self.platform_version = dut.at_dev.fwVersion()
            dut.destory()

            if cal_date not in cal_info:
                raise Exception("请确认该精板校准信息是否被擦除！！")

            print("信息检查完成")
            self.lossset_throushold = round(float(self.throushold_cbox.currentText()),2)
            if self.init_val_cbox.currentText() == "无" or self.is_check_step:
                self.init_val = None
                print("!!!!!!!!! 使用配置线损测试")
            else:
                self.init_val = round(float(self.init_val_cbox.currentText()),2)
                print("!!!!!!!!! 使用配置线损测试: %f"%(self.init_val))

            self.result_label.setStyleSheet("background-color:yellow")
            self.result_label.setText("开始")

            for tool_item in self.tool_data["tool_list"]:
                if tool_item["tool_name"].__eq__(self.tool_name):
                    tool_md5 = tool_item["MD5"]
                    break
            else:
                raise Exception("工具版本信息未找到！！")

            if os.path.exists(self.mmpt_zip_path) and tool_md5.__eq__(Utils.fileMd5(self.mmpt_zip_path)):
                self.mmpt_dwn_done_event.set()
            else:
                threading.Thread(target=self.downloadMmptTask, args=(tool_md5,)).start()
                print("!!!!!!!!! : 等待MMPT工具下载完成")

            self.mmpt_dwn_done_event.wait(60)

            self.init_val_cbox.setEnabled(False)
            self.throushold_cbox.setEnabled(False)
            self.start_btn.setEnabled(False)
            self.slot_cbox.setEnabled(False)
            self.lossset_cal.start(imei, self.init_val, self.lossset_throushold,
                                   self.slot_cbox.currentText(), self.is_check_step, db_path, self.platform_version, script_name, band_list)
        except Exception as e:
            self.msgBox(str(e))

    def cboxInit(self):
        init_list = ["无"]
        for i in range(20):
            init_list.append(str(round((0.4 + 0.2*i), 2)))
        self.init_val_cbox.addItems(init_list)
        throus_list = []
        for i in range(20):
            throus_list.append(str(round((0.1 + 0.1*i), 2)))
        self.throushold_cbox.addItems(throus_list)

        self.init_val_cbox.setCurrentText("0.4")
        self.throushold_cbox.setCurrentText("0.5")

        self.slot_cbox.addItems(["0", "1"])
        self.slot_cbox.setCurrentText(str(self.config.cmw_slot))

    def infoUpdate(self, info):
        print(info)
        if info["res"] is not None:
            self.init_val_cbox.setEnabled(True)
            self.throushold_cbox.setEnabled(True)
            self.start_btn.setEnabled(True)
            self.slot_cbox.setEnabled(True)

        self.resInfoAppend(info["info"])
        if info["res"] is True:
            if self.is_check_step is False:
                self.is_check_step = True
                self.result_label.setText("更换金板")
                self.resInfoAppend("请放入另外一个金板检查线损结果")
                self.slot_cbox.setEnabled(False)
                self.throushold_cbox.setEnabled(False)
                self.init_val_cbox.setEnabled(False)
                self.imei_edit.clear()
                self.imei_edit.setFocus()
            else:
                self.is_check_step = False
                self.result_label.setStyleSheet("background-color:green")
                self.result_label.setText("成功")
        elif info["res"] is False:
            self.is_check_step = False
            self.result_label.setStyleSheet("background-color:red")
            self.result_label.setText("失败")
    def downloadMmptTask(self, file_md5):
        print("开始下载MMPT文件: %s[%s]"%(self.tool_name, file_md5))
        AppUpdate("LossSetCal").downloadFile(self.tool_name, self.mmpt_zip_path)
        if file_md5.__eq__(Utils.fileMd5(self.mmpt_zip_path)):
            print("下载MMPT文件完成!")
            self.mmpt_dwn_done_event.set()
        else:
            self.msgBox("下载MMPT工具出错，请重启工具")
            self.main_win.close()

    def __init__(self):
        super().__init__()
        app = QtWidgets.QApplication(sys.argv)
        self.main_win = CloseEventQMainWindow()
        super().setupUi(self.main_win)

        if not os.path.exists(os.path.join(Utils.getAppRootPath(), "data/lossset")):
            os.makedirs("data/lossset")

        self.mmpt_zip_path = os.path.join(Utils.getAppRootPath(), "data/mmpt_tool_lossSet.zip")
        self.imei_1st = None
        self.is_check_step = False
        self.platform_version = ""

        self.auto_update_view = AutoUpdateView("LossSetCal")
        self.auto_update_view.show()
        res = self.auto_update_view.exec()
        if res == 0:
            self.main_win.close()
            sys.exit(0)

        self.main_win.setWindowTitle(self.main_win.windowTitle()+"--"+Utils.getAppVersion())
        self.config = ToolConfig()

        self.res_info_list = []
        self.info_label.setText("请输入精板IMEI后和选择线损初始值和阈值后点击开始")

        self.cboxInit()
        self.lossset_cal = LosssetCalControl(self.config)

        # self.imei_edit.setText("869734053165894")

        self.app_update = AppUpdate("LossSetCal")
        data = json.loads(self.app_update.getFile("LosssetDev.json").read())
        self.device_list = data["Device"]

        self.mmpt_dwn_done_event = threading.Event()
        self.mmpt_dwn_done_event.clear()

        self.tool_data = json.loads(self.app_update.getFile("mmpt_tool.json").read())
            # if "tool_md5" not in data.keys() or not data["tool_md5"].__eq__(tfile_md5):
            #     # download mmpt tool zip
            #     threading.Thread(target=self.downloadMmptTask, args=()).start()

        self.cur_port = None

        self.start_btn.clicked.connect(self.losssetCfgStart)
        self.lossset_cal.info_update_signal.connect(self.infoUpdate)

        # 设置固定窗口
        self.main_win.setFixedSize(self.main_win.width(), self.main_win.height())
        self.main_win.show()
        app.exec_()
        sys.exit()



if __name__ == "__main__":
    cgitb.enable(format='text')
    # log_path = "MMPT\\log\\app"
    # if not os.path.exists(log_path):
    #     os.makedirs(log_path)
    # file_list = os.listdir(log_path)
    # if len(file_list) > 100:
    #     file_list.sort()
    #     for file in file_list[0:-100]:
    #         os.remove(os.path.join(log_path, file))

    logging.basicConfig(level=logging.INFO,
                        # filename="MMPT\\log\\app\\%s.log"%(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')),
                        format="%(asctime)s %(name)s %(levelname)s %(message)s",
                        datefmt='%Y-%m-%d  %H:%M:%S %a')
    ProductMainView()