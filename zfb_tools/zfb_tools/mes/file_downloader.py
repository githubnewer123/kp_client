import os,threading,logging
import common.utils as Utils
import requests,zipfile,time,shutil
from PyQt5.QtCore import QObject,pyqtSignal

class FileDownloader(QObject):
    DOWNLOAD_PRCESS_DOWNLOAD_STARTED  = 0x00
    DOWNLOAD_PRCESS_DOWNLOAD_COMPLETE = 0x01
    DOWNLOAD_PRCESS_DOWNLOAD_FALSE  = 0x02
    DOWNLOAD_PRCESS_IDLE   = 0x04
    DOWNLOAD_PRCESS_UNZIP = 0x05
    DOWNLOAD_PRCESS_UNZIP_COMPLETE = 0x06
    DOWNLOAD_PRCESS_UNZIP_FALSE = 0x07

    download_progresss_signal = pyqtSignal(int)

    def __init__(self, url, file_name, md5_code,unzip_path = None):
        super().__init__()
        self.save_path = os.path.join(Utils.getAppRootPath(), "data")
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        #
        self.download_url = url
        self.download_name = file_name
        self.md5_code = md5_code
        self.download_process = 0
        self.unzip_path = unzip_path
        self.save_path = os.path.join(self.save_path, self.download_name)

        self.download_status = FileDownloader.DOWNLOAD_PRCESS_IDLE

    def status(self):
        return self.download_status

    def downloadFile(self):
        with requests.get(self.download_url, stream=True) as fget:
            file_size = int(fget.headers["Content-Length"])
            self.download_progresss_signal.emit(0)
            chunk_size = 1024*512
            file_done = 0
            with open(self.save_path, "wb") as fw:
                for chunk in fget.iter_content(chunk_size):
                    fw.write(chunk)
                    file_done = file_done + chunk_size
                    percent = file_done*100 / file_size
                    if file_done <= file_size:
                        self.download_progresss_signal.emit(percent-1)
                    else:
                        self.download_progresss_signal.emit(99)

    def downloadThreadHandle(self):
        # try:
            # file exist  check MD5
            logging.info("开始下载: %s"%(self.save_path))
            if os.path.exists(self.save_path):
                print("Check MD5 file: ",Utils.fileMd5(self.save_path) , end='' )
            print(" MD5 mes: ", self.md5_code, end='')
            if os.path.exists(self.save_path) and self.md5_code.__eq__(Utils.fileMd5(self.save_path)):
                print("NO need download")
                self.download_status = FileDownloader.DOWNLOAD_PRCESS_DOWNLOAD_COMPLETE
                self.download_progresss_signal.emit(99)
            else:
                print("download start")
                self.download_status = FileDownloader.DOWNLOAD_PRCESS_DOWNLOAD_STARTED
                self.downloadFile()
                if not self.md5_code.__eq__(Utils.fileMd5(self.save_path)):
                    self.download_status = FileDownloader.DOWNLOAD_PRCESS_DOWNLOAD_FALSE
                    raise Exception("下载文件校验MD5出错！[%s]"%(self.save_path))
                self.download_status = FileDownloader.DOWNLOAD_PRCESS_DOWNLOAD_COMPLETE

            logging.info("文件:%s 下载完成" % (self.save_path))


            if self.unzip_path:
                if os.path.exists(self.unzip_path):
                    shutil.rmtree(self.unzip_path)
                else:
                    os.makedirs(self.unzip_path)

                self.download_status = FileDownloader.DOWNLOAD_PRCESS_UNZIP
                zip_file = zipfile.ZipFile(self.save_path)
                for file in zip_file.namelist():
                    zip_file.extract(file, self.unzip_path)
                zip_file.close()
                self.download_status = FileDownloader.DOWNLOAD_PRCESS_UNZIP_COMPLETE
                logging.info("文件:%s 解压完成"%(self.save_path))
            self.download_progresss_signal.emit(100)
        # except Exception as e:
        #     print(str(e))
        #     self.download_status = FileDownloader.DOWNLOAD_PRCESS_UNZIP_FALSE
        #     self.download_progresss_signal.emit(-1)

    def start(self):
        self.thread = threading.Thread(target=self.downloadThreadHandle, args=())
        self.thread.start()





