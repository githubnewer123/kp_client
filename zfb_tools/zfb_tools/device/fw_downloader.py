import subprocess,threading,os,psutil,signal
from PyQt5.QtCore import QObject,pyqtSignal
import common.utils as Utils

class FwDownloader(QObject):

    DOWNLOAD_STATUS_START = 0X0001
    DOWNLOAD_STATUS_PROCESS = 0X0002
    DOWNLOAD_STATUS_STOP = 0X0003
    DOWNLOAD_STATUS_SUCCESS = 0X0004
    DOWNLOAD_STATUS_FALSE = 0X0005


    download_process_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.cur_status = None
        self.downloader_pid = None
        self.stop_event = threading.Event()
        self.burn_done_event = threading.Event()
        self.stop_event.clear()
        self.chip_id = ""
        self.pre_process = 0

    def __get_downloader_pid(self):
        cmd = "wmic process where name=\"adownload.exe\" get executablepath,processid"
        ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        cur_path = b"adownload.exe"
        while True:
            for line in iter(ret.stdout.readline, b""):
                if cur_path in line:
                    pid = int(line.decode().strip().replace(" ","").split("adownload.exe")[-1])
                    print("Get PID: %d"%(pid))
                    return pid
            else:
                return None

    def __downloadThread(self):
        cmd = "adownload.exe -q -u -s 3686400 -a fw.zip"
        print(cmd)

        ret = subprocess.Popen(cmd, shell=True,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               cwd=os.path.join(Utils.getAppRootPath(), "aboot"))


        self.downloader_pid = self.__get_downloader_pid()

        chip_id_list = []
        pre_process = 0
        self.pre_process = 0
        for line in iter(ret.stdout.readline, b""):
            print(line)
            if b"[INFO: EFuse     ]" in line:
                # print(line)
                if b"lotid" in line:
                    chip_id_list = line.decode().strip().split(":")[-1].split(" ")
                elif b"X_location" in line:
                    chip_id_list += [x.split(":")[-1].replace(" ","") for x in line.decode().strip().split(",")]
                    for id in chip_id_list:
                        if id != "":
                            self.chip_id += ("0"*(3-len(id)) + id)
                    self.cur_status = self.DOWNLOAD_STATUS_START
                    self.download_process_signal.emit({"status":self.DOWNLOAD_STATUS_START, "chipId":self.chip_id})

            if b"\"progress\" :" in line:
                process = int(line.decode().strip().replace("\"progress\" :", "").replace(",", ""))
                if process != self.pre_process and process >= self.pre_process:
                    self.pre_process = process
                    self.download_process_signal.emit({"status": self.DOWNLOAD_STATUS_PROCESS, "chipId": self.chip_id, "process":process})
                if process == 100:
                    self.burn_done_event.set()
            if b"aboot download engine stopped successfully" in line:
                if self.burn_done_event.isSet():
                    print("set status: self.DOWNLOAD_STATUS_SUCCESS")
                    self.cur_status = self.DOWNLOAD_STATUS_SUCCESS
                    self.download_process_signal.emit(
                        {"status": self.DOWNLOAD_STATUS_SUCCESS, "chipId": self.chip_id})
                else:
                    print("set status: self.DOWNLOAD_STATUS_FALSE")
                    self.cur_status = self.DOWNLOAD_STATUS_FALSE
                    self.download_process_signal.emit(
                        {"status": self.DOWNLOAD_STATUS_FALSE, "chipId": self.chip_id})
                break
        # self.cur_status = self.DOWNLOAD_STATUS_STOP
        self.pre_process = 0
        self.download_process_signal.emit(
            {"status": self.DOWNLOAD_STATUS_STOP, "chipId": self.chip_id})
        self.stop_event.set()



    def start(self):
        threading.Thread(target=self.__downloadThread, args=()).start()

    def getCurrentStatus(self):
        return self.cur_status

    def stop(self):
        if self.downloader_pid:
            try:
                pid_dict = {}
                pids = psutil.pids()
                for pid in pids:
                    p = psutil.Process(pid)
                    pid_dict[pid] = p.name()
                for t in pid_dict.keys():
                    if pid_dict[t] == "adownload.exe":
                        os.kill(t, signal.SIGABRT)
                        self.downloader_pid = None
                        return
            except Exception as e:
                print(str(e))

    def waitFinish(self, timeout):
        if self.stop_event.wait(timeout) is False:
            return (False,self.chip_id,"烧录固件超时")
        self.stop_event.clear()
        if self.chip_id == "" or len(self.chip_id) != 27:
            return (False,self.chip_id,"烧录固件获取CHIP ID出错")
        if self.cur_status != self.DOWNLOAD_STATUS_SUCCESS:
            return (False,self.chip_id,"烧录固件未完成")

        return (True,self.chip_id,"")

if __name__ == "__main__":
    fw_download = FwDownloader()
    fw_path = os.path.join(Utils.getAppRootPath(), "../aboot/bin/fw.zip")
    fw_download.start(fw_path)
