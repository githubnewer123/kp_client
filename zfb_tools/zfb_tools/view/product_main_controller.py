
from PyQt5.QtCore import QObject,pyqtSignal
from device.dut import Dut
from queue import Queue
import threading,logging
from manager.mmpt_slot import MmptSlot
import shutil,os,time,datetime,json
import common.utils as Utils
from mes.product_result import  ProductResult
from mes.factory_mes import FactoryMes
from manager.nst_parser import NstFileParser
from device.at_device import AtDevice
from device.fw_downloader import  FwDownloader
from device.dut_modem2 import DutModem2

def checkSlotIndex(func):
    def wrapper(*args, **kwargs):
        if args[1] >  args[0].active_slot_total:
            logging.info("index :%d  total:%d"%(args[1], args[0].total_slot))
            raise Exception("操作的MMPT工具编号错误")

        func(*args, **kwargs)

    return wrapper

AUTH_CFG = {"username": "ASR1603@zyxa", "password": "11447733", "pname": "XZX", "cname": "CIS_MODULE"}
class ProductMainController(QObject):
    TYPE_CAL  = 0x01
    TYPE_NST = 0x02
    TYPE_CAL_NST = 0x03

    pruduct_result_signal = pyqtSignal(dict)
    system_fault_signal = pyqtSignal(dict)

    def startBurnFw(self):
        if self.fw_downloader:
            self.fw_downloader.stop()
        self.fw_downloader = FwDownloader()
        self.fw_downloader.download_process_signal.connect(self.downloadUpdate)
        self.fw_downloader.start()

    def reportProductData(self, product_res, res, false_info):
        if int(self.config.station_type) == 0:
            self.mes.postProductData(product_res.getCalUpdate(res, false_info))
        elif int(self.config.station_type) == 1:
            self.mes.postProductData(product_res.getNstUpdate(res, false_info))
        elif int(self.config.station_type) == 2:
            self.mes.postProductData(product_res.getDownloadUpdate(res, false_info))

    @checkSlotIndex
    def setSlotImei(self, slot_index, imei):
        self.imei[slot_index] = imei

    @checkSlotIndex
    def start(self, slot_index, at_port, imei):
        self.setSlotImei(slot_index, imei)
        process = {"slot_index" : slot_index, "at_port":at_port,"imei":imei}
        self.queue.put(process)

    @checkSlotIndex
    def stop(self, slot_index):
        self.slot_index = slot_index
        self.mmpt_slot[slot_index].stop()

    @checkSlotIndex
    def deviceAbort(self, slot_index):
        if int(self.config.station_type) == 2:
            self.startBurnFw()
            return
        if self.mmpt_slot[slot_index]:
            self.mmpt_slot[slot_index].stop()

    def signalEmit(self, info,res = True, is_complete=False):
        self.pruduct_result_signal.emit({"res":res, "info": info, "is_complete":is_complete})

    def rfResultInfoEmit(self, file_path):
        info = ""
        mes_info = {}
        is_gsm = "gsm" in os.path.basename(file_path).lower()
        try:
            nst_parser = NstFileParser(file_path, is_gsm)
            for band in nst_parser.getBandList():
                res = nst_parser.getTestResult(band)
                if res and len(res) > 0:
                    if is_gsm:
                        info += ("%s=%s" % (band, str(res))).replace(" ", "")+" "
                        mes_info["%s"%band] = str(res)
                    else:
                        info += "B%d=%sdBm "%(band, str(res))
                        mes_info["B%s" % band] = str(res)
        except Exception as e:
            print("NstFileParser: "+str(e))

        if len(info) > 0:
            self.signalEmit(info)
        return mes_info

    def getLteCalDac(self, fpath):
        if not os.path.exists(fpath):
            return "DAC 获取失败,校准Log文件不存在"

        with open(fpath, "r") as fd:
            for line in fd.readlines():
                if "Temperature and volt indication=," in line:
                    return "Lte DAC:" + str(line.split("=,")[-1].split(',')[0])
            else:
                return "校准Log文件不存在DAC值"

    def copyCalLog(self,slot_index, folder, imei, res, product_res):
        # save in local IMEI folder
        if not os.path.exists(folder):
            return
        log_path = self.getLogPath(slot_index)
        imei_path = os.path.join(log_path, imei)
        dst_path = os.path.join(imei_path, os.path.basename(folder))
        if not os.path.exists(log_path):
            os.mkdir((log_path))
        if not os.path.exists(imei_path):
            # shutil.rmtree(os.path.join(log_path, imei))
            os.mkdir(imei_path)
        if os.path.exists(dst_path):
            shutil.rmtree(dst_path)
        logging.info("save log：%s -> %s"%(folder, imei))
        shutil.copytree(folder, dst_path)

        # save upload log  MMPT/log/%d/UPLOAD_IMEI
        upload_path = os.path.join(log_path, "UPLOAD_" + imei)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        if int(self.config.station_type) == 0:
            for file in os.listdir(folder):
                if "Calibration" in file and file.endswith("txt"):
                    if "Fail" in os.path.basename(folder) and "Failed" not in file:
                        continue
                    if "lte" in file.lower():
                        product_res.cal_lte = self.getLteCalDac(os.path.join(folder, file))
                    shutil.copy(os.path.join(folder, file), upload_path)
                    logging.info("copy %s -> %s"%(os.path.join(folder, file), upload_path))
                if file.__eq__("GPIB.txt") and "Fail" in os.path.basename(folder):
                    shutil.copy(os.path.join(folder, "GPIB.txt"), upload_path + "/cal_GPIB_Failed.txt")
                    logging.info("copy %s -> %s" % (os.path.join(folder, "GPIB.txt"), upload_path + "/cal_GPIB_Failed.txt"))
        else:
            for file in os.listdir(folder):
                if file.endswith(".csv"):
                    shutil.copy(os.path.join(folder, file), upload_path)
                    logging.info("copy %s -> %s" % (os.path.join(folder, file), upload_path))
                    product_res.nst_rf_res.update(self.rfResultInfoEmit(os.path.join(folder, file)))
                if file.__eq__("GPIB.txt") and "Fail" in os.path.basename(folder):
                    shutil.copy(os.path.join(folder, "GPIB.txt"), upload_path + "/nst_GPIB_Failed.txt")
                    logging.info("copy %s -> %s" % (os.path.join(folder, "GPIB.txt"), upload_path + "/nst_GPIB_Failed.txt"))

        shutil.rmtree(folder)
    def isDcEnable(self):
        if (type == 0 and self.config.cal_adc is False) or (type == 1 and self.config.nst_adc is False):
            return

    def updateFalseTotal(self, info):
        try:
            tag = info.split(":")[0]
            if tag.upper().__eq__("LTE"):
                self.config.lte_false_cnt += 1
            elif tag.upper().__eq__("GSM"):
                self.config.gsm_false_cnt += 1
            elif tag.upper().__eq__("ADC"):
                self.config.adc_false_cnt += 1
            elif tag.upper().__eq__("IMEI"):
                self.config.imei_false_cnt += 1
            else:
                self.config.other_false_cnt += 1
        except Exception:
            self.config.other_false_cnt += 1

    def uploadLogFolder(self, imei, chip_id, slot_index):
        src = "%sMMPT/log/%d/UPLOAD_%s"%(Utils.getAppRootPath(), slot_index, imei)
        if int(self.config.station_type) == 0:
            tag = "cal"
        else:
            tag = "nst"
        dst = "%sMMPT/log/%d/%s_%s_%s_PASS.zip" % (
            Utils.getAppRootPath(), slot_index, tag, imei, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        for file in os.listdir(src):
            if "Failed" in file:
                dst = "%sMMPT/log/%d/%s_%s_%s_FAIL.zip" % (
                Utils.getAppRootPath(), slot_index, tag,imei, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
                break

        Utils.zipFile(src, dst, del_src=False)
        zip_url = self.mes.postLogFile(dst, chip_id)
        logging.info("Post log file success: %s"%(zip_url))
        os.remove(dst)
        shutil.rmtree(src)
        return zip_url

    def getChipId(self, port):
        chip_id = ""
        try:
            # try get chipid
            dut = Dut(port)
            chip_id = dut.getChipID()
            dut.destory()
            return chip_id
        except Exception as err:
            logging.info(str(err))
        return ""

    def downloadUpdate(self, info):
        if info["status"] == FwDownloader.DOWNLOAD_STATUS_PROCESS and "process" in info.keys():
            if info["process"]%20 == 0:
                self.signalEmit("下载进度 %d%%"%(info["process"]))

    def stepProcess(self, info, product_res, func, val = "", *args, **kwargs):
        result = "%s 失败"%(info)
        stime = time.time()
        if len(val) > 0:
            self.signalEmit(info +"开始 :%s"%(val))
        else:
            self.signalEmit(info + "开始")

        func(*args,**kwargs)

        if len(val) > 0:
            self.signalEmit(info + "完成: %s,%d" % (val, int(time.time() - stime)))
            result = info + "成功: %s,%d" % (val, int(time.time() - stime))
        else:
            result = info + "成功,%d"%(int(time.time()-stime))
            self.signalEmit(info + "完成,%d" % (int(time.time() - stime)))
        return result

    def bandCheck(self, product_res, dut):
        if "TR3B" in self.mes.getActiveOrder().project_version:
            if "TR3B-RG-SE00" in self.mes.getActiveOrder().project_version:
                # 欧版：AT * BAND = 5, 0, 0, 416, 524501
                product_res.band_info = dut.setBand(416, 524501)
            elif "TR3B-RG-SN00" in self.mes.getActiveOrder().project_version:
                # 美版：AT * BAND = 5,0,0,256,6234
                product_res.band_info = dut.setBand(384, 6234)
            elif "TR3B-RG-SU00" in self.mes.getActiveOrder().project_version:
                # 美版：AT * BAND = 5, 0, 0, 482, 530655
                product_res.band_info = dut.setBand(482, 530655)
            else:
                # 国内版本不需要
                pass
        else:
            if self.mes.getActiveOrder().at_uart_volt is not None:
                product_res.at_uart_volt = dut.checkUartVolt(self.mes.getActiveOrder().at_uart_volt)

            if "RG-CB" in self.mes.getActiveOrder().project_version or \
                    "RG-SB" in self.mes.getActiveOrder().project_version or \
                    "RG-LB" in self.mes.getActiveOrder().project_version \
                    or "SG-LB" in self.mes.getActiveOrder().project_version:
                product_res.band_info = dut.setCmccBand()
            elif "RG-CT" in self.mes.getActiveOrder().project_version or \
                    "RG-ST" in self.mes.getActiveOrder().project_version or \
                    "SG-LT" in self.mes.getActiveOrder().project_version or \
                    "RG-LT" in self.mes.getActiveOrder().project_version:
                product_res.band_info = dut.setTddOnlyBand()
            elif "RG-CA" in self.mes.getActiveOrder().project_version or \
                    "RG-SA" in self.mes.getActiveOrder().project_version or \
                    "RG-LA" in self.mes.getActiveOrder().project_version \
                    or "SG-LA" in self.mes.getActiveOrder().project_version:
                product_res.band_info = dut.checkAllBand()
            elif "SG-CS" in self.mes.getActiveOrder().project_version or \
                    "SG-LS" in self.mes.getActiveOrder().project_version:
                product_res.band_info = dut.setBand(0, 134742229)
            elif "RG-LE" in self.mes.getActiveOrder().project_version or \
                    "SG-LE" in self.mes.getActiveOrder().project_version:
                product_res.band_info = dut.setBand(0, 134742213)
            elif "RG-LJ" in self.mes.getActiveOrder().project_version or \
                    "SG-LJ" in self.mes.getActiveOrder().project_version:
                product_res.band_info = dut.setBand(0, 168165509)
            elif "RG-SS" in self.mes.getActiveOrder().project_version or \
                "SG-SS" in self.mes.getActiveOrder().project_version:
                product_res.band_info = dut.setBand(384, 213)

    def __productThread(self):
        cal_lte = self.config.cal_lte
        cal_gsm = self.config.cal_gsm
        nst_lte = self.config.nst_lte
        nst_gsm = self.config.nst_gsm
        event_timeout = 0
        factory_post_res = True
        if int(self.config.station_type) == 0:
            nst_lte = False
            nst_gsm = False
            if cal_lte:
                event_timeout += int(self.config.mmpt_cal_lte_timeout)
            if cal_gsm:
                event_timeout += int(self.config.mmpt_cal_gsm_timeout)
        elif int(self.config.station_type) == 1:
            cal_lte = False
            cal_gsm = False
            if nst_lte:
                event_timeout += int(self.config.mmpt_nst_lte_timeout)
            if nst_gsm:
                event_timeout += int(self.config.mmpt_nst_gsm_timeout)
        elif int(self.config.station_type) == 2:
            nst_lte = False
            nst_gsm = False
            cal_lte = False
            cal_gsm = False
            fw_path = os.path.join(Utils.getAppRootPath(), "data/fw.zip")
            aboot_path = os.path.join(Utils.getAppRootPath(), "aboot")
            if not os.path.exists(fw_path) or not os.path.exists(aboot_path):
                self.system_fault_signal.emit({"info": "需要下载的固件文件不存在！请重启工具"})
            try:
                shutil.copyfile(fw_path, os.path.join(aboot_path, "fw.zip"))
                self.startBurnFw()
            except Exception as e:
                self.system_fault_signal.emit({"info": str(e)})

        if cal_lte or nst_lte or cal_gsm or nst_gsm:
            for idx in range(0, self.slot_total):
                try:
                    mslot = MmptSlot(idx, self.config, self.system_fault_signal)
                    self.mmpt_slot[idx] = mslot
                except Exception as e:
                    self.system_fault_signal.emit({"info":str(e)})
        if self.config.factory_mes_enable:
            factory_mes = FactoryMes(self.config)

        while True:
            # print("ADC校准: %s ADC测试: %s  ADC电压测试: %s ADC flag检查: %s IO检查: %s"%
            #       (str(self.config.cal_adc), str(self.config.nst_adc), str(self.config.nst_adc_dc_en), str(self.config.test_adc_flag), str(self.config.test_io)))
            process = self.queue.get()
            logging.info(process)
            # process = {"slot_index" : slot_index, "at_port":at_port,"imei":imei}
            slot_index = process["slot_index"]
            at_port = process["at_port"]
            imei = process["imei"]
            dut = None
            product_res = ProductResult(self.config)
            product_res.imei = imei
            process_res = False
            mmpt_res = MmptSlot.PROCESS_SUCCESS
            false_info = ""
            product_res.scrip_version = self.mes.getActiveOrder().scrip_version

            mmpt_log_path = os.path.join(
                os.path.join(Utils.getAppRootPath(), "MMPT/log/%d/UPLOAD_%s" % (slot_index, imei)))
            if os.path.exists(mmpt_log_path):
                shutil.rmtree(mmpt_log_path)
            try:
                type = int(self.config.station_type)
                if (type == 0 and self.config.cal_imei) or (type == 1 and self.config.nst_imei):
                    if self.config.check_imei_uniq:
                        self.mes.getChipidFromMes(imei)
                if cal_lte or nst_lte or cal_gsm or nst_gsm:
                    self.signalEmit("等待MMPT TOOL返回结果 IMEI: %s"%(imei))
                    mmpt_res, info = self.mmpt_slot[slot_index].waitMmptDone(event_timeout)

                    if mmpt_res != MmptSlot.PROCESS_NG_ABORT:
                        AtDevice.waitPortAvailable(at_port, 3)

                    if mmpt_res != MmptSlot.PROCESS_SUCCESS:
                        logging.info("MMPT res is False! kill mmpt, raise: %s"%(product_res.last_mmpt_info))
                        self.mmpt_slot[slot_index].kill()
                        raise Exception(info)
                    else:
                        self.signalEmit(info)

                if type == 2:
                    self.signalEmit("等待烧录完成")
                    process_res = False
                    res,chip_id, false_info = self.fw_downloader.waitFinish(120)
                    product_res.chip_id = chip_id
                    if res is False:
                        raise Exception(false_info)
                else:
                    dut = Dut(at_port, self.config.dc_gpib_addr, self.config.dc_channle)
                    product_res.chip_id = dut.getChipID()

                    if type == 0:
                        if self.config.cal_adc:
                            stime = time.time()
                            self.signalEmit("ADC 校准开始")
                            vbat_diff, rtp_diff = dut.adcCal(rtpEn=True)
                            self.signalEmit("ADC 校准完成 vbat: %.2f~%.2f rtp: %.2f~%.2f, %d" % (
                            vbat_diff[0], vbat_diff[-1], rtp_diff[0], rtp_diff[-1], int(time.time() - stime)))
                            product_res.cal_adc = "ADC 校准成功! vbat: %.2f~%.2f rtp: %.2f~%.2f, %d" % (
                            vbat_diff[0], vbat_diff[-1], rtp_diff[0], rtp_diff[-1], int(time.time() - stime))
                        if self.config.cal_imei:
                            if Utils.isImei(imei) is False:
                                raise Exception("IMEI规则检查错误！")
                            if self.config.check_imei_uniq:
                                self.mes.waitChipIdGetDone(2)
                                if self.mes.chipid_list:
                                    if len(self.mes.chipid_list) == 1 and product_res.chip_id not in self.mes.chipid_list:
                                        raise Exception("IMEI: 该IMEI已经被其它模组占用")
                                    if len(self.mes.chipid_list) > 1 :
                                        raise Exception("IMEI: 重复多次写入IMEI")
                            product_res.cal_imei = self.stepProcess("IMEI 写入", product_res, dut.writeImei, imei, imei)
                        if self.mes.getActiveOrder().cal_custome_cfg is not None:
                            res, product_res.custome_config = dut.customConfig(
                                self.mes.getActiveOrder().cal_custome_cfg)
                            if res is False:
                                raise Exception("CIS config 出错:" + str(product_res.custome_config))
                        if self.config.cal_sn:
                            stime = time.time()
                            self.signalEmit("SN 写入开始")
                            product_res.cal_sn = "SN 写入开始"
                            batch_no = dut.setHwVersion(self.mes.getActiveOrder().project_version, self.mes.getActiveOrder().fw_version_name)
                            product_res.sn = str(batch_no)
                            self.signalEmit("写入硬件版本完成: "+str(batch_no)+",%d"%(int(time.time()-stime)))
                            product_res.cal_sn = "写入硬件版本完成: "+str(batch_no)+",%d"%(int(time.time()-stime))
                        if self.config.cal_auth:
                            product_res.cal_auth = self.stepProcess("设备授权激活", product_res, dut.auth)


                        self.bandCheck(product_res, dut)

                    if type == 1 :
                        dut.checkFwVersion(self.mes.getActiveOrder().fw_version_name)
                        product_res.fw_version = self.mes.getActiveOrder().fw_version_name
                        self.signalEmit("检查软件版本完成: %s" % (self.mes.getActiveOrder().fw_version_name))

                        if self.mes.getActiveOrder().test_custome_cfg is not None:
                            res,product_res.custome_config = dut.customConfig(self.mes.getActiveOrder().test_custome_cfg)
                            if res is False:
                                raise Exception("CIS config 出错:"+str(product_res.custome_config))

                        self.bandCheck(product_res, dut)

                        if self.config.nst_check_lte_flag:
                            product_res.nst_lte = self.stepProcess("LTE校准Flag检测", product_res, dut.checkLteCal)
                        if self.config.nst_check_gsm_flag:
                            product_res.nst_gsm = self.stepProcess("GSM校准Flag检测", product_res, dut.checkGsmCal)
                        if self.config.test_io:
                            if self.mes.getActiveOrder().gpio_mask is None:
                                product_res.nst_io = self.stepProcess("IO检测", product_res, dut.checkGPIO)
                            else:
                                stime = time.time()
                                self.signalEmit("GPIO测试开始")
                                res,data = dut.checkGPIOExt(self.mes.getActiveOrder().gpio_mask, "800RG" if "800-RG" in self.mes.getActiveOrder().project_version else "CG")
                                product_res.nst_io = data
                                self.signalEmit(
                                    "GPIO测试完成: " + product_res.nst_io + ",%d" % (int(time.time() - stime)))
                                if res is False:
                                    raise Exception("IO测试: 错误,%s"%(data))
                        else:
                            product_res.nst_io = "IO测试: 未配置"

                        if self.config.nst_adc:
                            stime = time.time()
                            product_res.nst_adc = "ADC 测试Flag失败"
                            self.signalEmit("ADC 测试开始")

                            if self.config.nst_adc_dc_en:
                                vbat_diff, rtp_diff = dut.adcCheck(dut.adc_nst_list,rtpEn=True,dc_enable=True, max_diff=dut.max_adc_nst_diff)
                                adc_res = "ADC 测试成功! vbat: %.2f~%.2f rtp: %.2f~%.2f, %d"%(vbat_diff[0],vbat_diff[-1],rtp_diff[0],rtp_diff[-1], int(time.time()-stime))
                            elif self.config.test_adc_flag:
                                dut.adcCheck(None, rtpEn=True, dc_enable=False, max_diff=dut.max_adc_nst_diff)
                                adc_res = "ADC 测试Flag成功! "
                            self.signalEmit(adc_res)
                            product_res.nst_adc = adc_res
                        if self.config.nst_imei:
                            product_res.nst_imei = self.stepProcess("IMEI检查", product_res, dut.checkImei, imei, imei)
                            if self.config.check_imei_uniq:
                                self.mes.waitChipIdGetDone(2)
                                if self.mes.chipid_list:
                                    if len(self.mes.chipid_list) == 1 and product_res.chip_id not in self.mes.chipid_list:
                                        raise Exception("IMEI: 该IMEI已经被其它模组占用")
                                    if len(self.mes.chipid_list) > 1 :
                                        raise Exception("IMEI: 重复多次使用该IMEI")

                        if self.config.nst_sn:
                            stime = time.time()
                            self.signalEmit("SN 检查开始")
                            product_res.nst_sn = "SN 检查开始"
                            # print("order fw version: ", self.mes.getActiveOrder().fw_version_name)
                            batch_no = dut.checkHwVersion(self.mes.getActiveOrder().project_version)
                            product_res.nst_sn = str(batch_no)
                            self.signalEmit("检查硬件版本完成: %s,%d"%(str(batch_no),int(time.time()-stime)))
                        if self.config.nst_auth:
                            self.signalEmit("设备激活状态检测开始")
                            product_res.nst_auth = "设备激活状态检测失败"
                            dut.checkAuth(AUTH_CFG["cname"], AUTH_CFG["pname"])
                            self.signalEmit("设备激活状态检测完成")
                            product_res.nst_auth = "设备激活状态检测完成"
                            # product_res.nst_auth = self.stepProcess("设备激活状态检测", product_res, dut.checkAuth,AUTH_CFG["cname"], AUTH_CFG["pname"])
                        if "TR3B" in self.mes.getActiveOrder().project_version:
                            product_res.custome_info = DutModem2().checkTr3bHW()
                            self.signalEmit("TR3B check GPS&BT success")
                    dut.destory()
                self.signalEmit("所有项目全部完成")
                process_res = True
            except Exception as e:
                self.config.false_cnt += 1
                process_res = False
                false_info = str(e)
                self.signalEmit(false_info)
                if dut:
                    if len(product_res.chip_id) <= 0:
                        try:
                            product_res.chip_id = dut.getChipID()
                        except Exception:
                            product_res.chip_id = ''
                    dut.destory()
                if mmpt_res != MmptSlot.PROCESS_SUCCESS:
                    if mmpt_res != MmptSlot.PROCESS_NG_ABORT:
                        try:
                            product_res.chip_id = self.getChipId(at_port)
                        except Exception:
                            product_res.chip_id = ''
                    stime = time.time()
                    self.signalEmit("重新启动MMPT TOOL")
                    self.mmpt_slot[slot_index].openMMPT()
                    self.signalEmit("重新启动MMPT TOOL 完成,%d" % (int(time.time() - stime)))


                self.updateFalseTotal(false_info)
            try:
                if self.mmpt_slot[slot_index]:
                    for folder in os.listdir(self.mmpt_slot[slot_index].cal_data_path):
                        log_path = os.path.join(self.mmpt_slot[slot_index].cal_data_path, folder)
                        if os.path.isdir(log_path) and ("lte" in folder.lower() or "gsm" in folder.lower()):
                            self.copyCalLog(slot_index, log_path, imei, mmpt_res == MmptSlot.PROCESS_SUCCESS, product_res)

                if os.path.exists(mmpt_log_path):
                    product_res.log_url = self.uploadLogFolder(imei, product_res.chip_id, slot_index)

                if self.config.factory_mes_enable:
                    factory_post_res = factory_mes.postData(imei, process_res, false_info)

                if factory_post_res is False:
                    self.reportProductData(product_res, False, "工厂MES系统提交出错")
                    factory_post_res = True
                    raise Exception("MES: 工厂MES系统提交出错")

                self.reportProductData(product_res, process_res, false_info)
                if process_res:
                    self.config.success_cnt += 1
                self.signalEmit("mes 提交完成", res=process_res, is_complete=True)
            except Exception as e:
                self.config.mes_false_cnt += 1
                err_info = str(e)
                if self.config.check_post_res:
                    self.signalEmit(err_info, res=False, is_complete=True)
                else:
                    self.signalEmit(err_info, res=process_res, is_complete=True)
            while not self.queue.empty():
                self.queue.get()

    def waitRfRes(self, slot_index):
        stop_event = threading.Event()
        # self.slot_num, MmptSlot.PROCESS_COMPLETE, True, None, self.notify_param
        def _notify(slot_num, process, res, info, param):
            if res is False:
                raise Exception("MMPT执行 %d 出错"%(process),+info)
            if process == MmptSlot.PROCESS_COMPLETE:
                stop_event.set()
        self.mmpt_slot[slot_index].setNotify(_notify, stop_event)
        self.mmpt_slot[slot_index].start()
        if stop_event.wait(timeout=250) is False:
            raise Exception("等待RF执行完成超时")

    def getLogPath(self, slot_index):
        return os.path.join(Utils.getAppRootPath(), "MMPT/log/%d/" % (slot_index))

    def quit(self):
        for slot in self.mmpt_slot:
            if slot:
                slot.exit()
                slot.kill()
        if self.fw_downloader:
            self.fw_downloader.stop()


    def infoSave(self):
        self.config._syncToFile()

    def clearInfo(self):
        self.config.success_cnt = 0
        self.config.false_cnt = 0
        self.config.lte_false_cnt = 0
        self.config.gsm_false_cnt = 0
        self.config.adc_false_cnt = 0
        self.config.imei_false_cnt = 0
        self.config.mes_false_cnt = 0
        self.config.other_false_cnt = 0
        self.infoSave()

    def __init__(self, mes, config):
        super().__init__()
        self.config = config
        self.slot_total = 1
        self.active_slot_total = 1
        self.err_event = threading.Event()
        self.fw_downloader = None
        self.mes = mes

        self.queue = Queue(5)

        self.mmpt_slot = [None] * self.slot_total
        self.imei =[0] * self.slot_total

        self.auth_code = None

        self.produce_thread = threading.Thread(target=self.__productThread, args=())
        self.produce_thread.setDaemon(True)
        self.produce_thread.start()






