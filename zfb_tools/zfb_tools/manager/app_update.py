import oss2,os,threading
from PyQt5.QtCore import QObject,pyqtSignal
import os,sys,json,zipfile,shutil

# import pythoncom
# from win32com.shell import shell
# from win32com.shell import shellcon

endpoint = "oss-cn-shenzhen.aliyuncs.com"
accesskey_id = "LTAI5t6PekmC9SQGST5r3Bv4"
accesskey_secrtet = "jl1FfvbhJhkyX5llOLKJg1tdbIhC9h"
bucket_name = "cisota"

class AppUpdate(QObject):
    download_progresss_signal = pyqtSignal(int)
    check_version_signal = pyqtSignal(dict)

    def createInk(self, file_path, ink_name, work_dirc):
        # 获取"启动"文件夹路径，关键是最后的参数CSIDL_STARTUP，这些参数可以在微软的官方文档中找到

        startup_path = shell.SHGetPathFromIDList(shell.SHGetSpecialFolderLocation(0, shellcon.CSIDL_STARTUP))

        # 获取"桌面"文件夹路径，将最后的参数换成CSIDL_DESKTOP即可

        desktop_path = shell.SHGetPathFromIDList(shell.SHGetSpecialFolderLocation(0, shellcon.CSIDL_DESKTOP)).decode()

        filename = file_path  # 要创建快捷方式的文件的完整路径

        lnkname = os.path.join(desktop_path , ink_name) # 将要在此路径创建快捷方式

        shortcut = pythoncom.CoCreateInstance(

            shell.CLSID_ShellLink, None,

            pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)

        shortcut.SetPath(filename)
        shortcut.SetWorkingDirectory(work_dirc)

        if os.path.splitext(lnkname)[-1] != '.lnk':
            lnkname += ".lnk"

        for file in os.listdir(desktop_path):
            if file.startswith("%s-V"%(self.name)) and file.endswith(".lnk"):
                os.remove(os.path.join(desktop_path, file))
        shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnkname, 0)


    def __init__(self, app_name):
        super().__init__()
        self.name = app_name
        self.bucket = None

    def downloadFile(self, file_name, local_path):
        if self.bucket is None:
            self.auth()

        self.bucket.get_object_to_file("%s/%s" % (self.name,file_name) , local_path)

    def download(self, version, local_path):
        def _download(version, local_path):
            def percentage(consumed_bytes, total_bytes):
                if total_bytes:
                    rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
                    self.download_progresss_signal.emit(rate)

            for obj in oss2.ObjectIterator(self.bucket, prefix=str("%s/%s-"%("CMPT",self.name))):
                if version in obj.key:
                    self.bucket.get_object_to_file("%s/"%("CMPT") + version, local_path + version,
                                                   progress_callback=percentage)
            zip_file_path = os.path.join(local_path, version)
            print("app压缩包保存路径:",zip_file_path)
            try:
                with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
                    print("app解压路径:", "./")
                    zip_file.extractall('./')  # 使用extractall解压所有文件到当前目录
            except Exception as e:
                print(f"解压过程中发生错误: {e}")
            # if os.path.isfile(zip_file_path):
            #     os.remove(zip_file_path)
            # else:
            #     print(f"{zip_file_path}文件不存在")

        threading.Thread(target=_download, args=(version, local_path)).start()


    def getFileMeta(self, file_name):
        meta = self.bucket.get_object_meta("%s/"%(self.name) + file_name)
        return meta

    def auth(self):
        self.auth = oss2.Auth(accesskey_id, accesskey_secrtet)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)

    def getFile(self, file_name):
        if self.bucket is None:
            self.auth()

        return self.bucket.get_object("%s/%s"%(self.name,file_name))

    def _checkVersion(self, cur_version):
        try:
            self.auth = oss2.Auth(accesskey_id, accesskey_secrtet)
            self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)
            self.version_list = []
            cur_version = int(cur_version.replace("%s-V"%(self.name), "").replace(".exe", "").replace(".",""))
            max_version_num = 0.0
            max_version_txt = ""
            for version in oss2.ObjectIterator(self.bucket, prefix=str("%s/%s-"%("CMPT", self.name))):
                print(version.key)
                self.version_list.append(version.key.replace("%s/"%("CMPT"), ""))
                # print(self.version_list)
            # key = "CMPT/CMBT-V1.80.zip"
            # self.bucket.delete_object("CMPT/CMBT-V1.80.zip")  # 删除特定的对象
            for version in self.version_list:
                ver_num = int(version.replace("%s-V"%(self.name),"").replace(".exe","").replace(".","").replace("zip","").replace("7z",""))
                if ver_num > max_version_num:
                    max_version_num = ver_num
                    max_version_txt = version

            print(cur_version, max_version_num)
            if cur_version >= max_version_num:
                self.check_version_signal.emit({"res":True,"version":None})
            else:
                self.check_version_signal.emit({"res":True,"version":max_version_txt})

        except Exception as e:
            self.check_version_signal.emit({"res":False,"info":str(e)})

    def checkVersion(self, cur_version):
        threading.Thread(target=self._checkVersion, args=(cur_version,)).start()

    def uploadFile(self, src_file, dir = None):
        self.auth = oss2.Auth(accesskey_id, accesskey_secrtet)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)
        def percentage(consumed_bytes, total_bytes):
            if total_bytes:
                sys.stdout.flush()
                rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
                print("%d percent done" % int(rate), end="")

        dst = os.path.basename(src_file)
        with open(src_file, 'rb') as fileobj:
            if dir:
                self.bucket.put_object(self.name + "/"+dir+"/" + dst, fileobj, progress_callback=percentage)
            else:
                self.bucket.put_object(self.name + "/"+dst, fileobj, progress_callback=percentage)

        for version in oss2.ObjectIterator(self.bucket, prefix=str("%s" % (self.name))):
            print(version.key)

if __name__ == "__main__":
    # lossset_cfg_path = "/home/cis/桌面/zfb_tools/BT/CMBT-V1.80.zip"
    lossset_cfg_path = "D:/NEW/zfb_tools/BT/CMBT-V1.80.zip"
    # imei = "862406064226059"
    # cal_data = "PASS_202203231517"
    # db_path = "722CGOHRD10G0396-DB-set.zip"
    # nst_path = "D:/NEW/zfb_tools/BT/%s.csv"%(imei)
    app_update = AppUpdate("CMPT")
    # app_update.downloadFile("LosssetDev.json", lossset_cfg_path)
    # with open(lossset_cfg_path, "r") as fd:
    #     info_file = json.loads(fd.read())
    # for item in info_file["Device"]:
    #     if "DB_PATH" not in item.keys():
    #         item["DB_PATH"] = db_path
    # for item in info_file["Device"]:
    #     if item["IMEI"].__eq__(imei):
    #         item["CAL_DATE"] = cal_data
    #         break
    # else:
    #     info_file["Device"].append({'IMEI': imei, 'CAL_DATE': cal_data})
    # with open(lossset_cfg_path, "w+") as fd:
    #     fd.write(json.dumps(info_file))
    app_update.uploadFile(lossset_cfg_path)
    # app_update.uploadFile(nst_path, "NstResult")

