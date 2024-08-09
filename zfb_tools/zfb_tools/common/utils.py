import requests,json,hashlib,configparser,os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time,shutil,threading
import zipfile,subprocess,logging
from Crypto.Cipher import AES

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

root_path = os.path.join( os.getcwd(), r"../")

__SOFTERWARE_VERSION__ = "CMBT-V1.81"#"TCTA-V2.80"
__TQC_VERSION__ = "TQC-V3.7"
__TBA_VERSION__ = "TBA-V4.2"

def getAppVersion():
    return __SOFTERWARE_VERSION__

cwd_path = os.getcwd()
def getAppRootPath(init_path = None):
    if os.path.basename(cwd_path).__eq__("common"):
        root_path = os.path.join(cwd_path, r"../")
    else:
        root_path = cwd_path+"/"
    return  root_path

def fileMd5(file_name):
    if not os.path.exists(file_name):
        return "0"
    file_object = open(file_name, 'rb')

    file_content = file_object.read()
    file_object.close()
    file_md5 = hashlib.md5(file_content)
    return file_md5.hexdigest()

def cfgWrite(file_name, section, option,val):
    config = configparser.ConfigParser(strict=False)
    config.optionxform = str
    config.read(file_name)
    config.set(section, option, val)
    config.write(open(file_name, "w"))

def isImei(imei):
    try:
        imeiChar = list(imei)  # .toCharArray()
        resultInt = 0
        i = 0
        while i < len(imeiChar) - 1:
            a = int(imeiChar[i])
            i += 1
            temp = int(imeiChar[i]) * 2
            b = (temp - 9, temp)[temp < 10]  # temp if temp < 10 else temp - 9
            resultInt += a + b
            i += 1
        resultInt %= 10
        resultInt = (10 - resultInt, 0)[resultInt == 0]
        crc = int(imeiChar[14])
        return resultInt == crc
    except:
        return False

def getAuthInfo(authCfg, uid):
    try:
        headers={"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
                 "Accept-Encoding": "gzip, deflate","Content-Type": "application/x-www-form-urlencoded"}
        url = "https://visit.chinainfosafe.com/platform-admin/other/device/verification"
        data = "username=%s&password=%s&deviceUno=%s&pname=%s&cname=%s"%(authCfg["username"],authCfg["password"], uid,authCfg["pname"],authCfg["cname"])
        resp = requests.post(url,data.encode(),headers=headers,verify=False)
        content = resp.content.replace(b" ", b"")
        content = json.loads(content.decode())
        if "success".__eq__(content["msg"]):
            # 获取authorizationCode 字段
            auth = content["data"][0]["authorizationCode"]
            return auth
    except Exception as e:
        print(e)
        return None

def genHwVersion(project_ver, fw_ver):
    # 600RGLB10V1132600RGBFRD20G0251product
    if fw_ver is None:
        version = project_ver.replace("-", "").replace(".", "").replace("_","")[2:16]
    else:
        version = project_ver.replace("-", "").replace(".", "").replace("_", "")
        version = version[2:version.find(fw_ver)]
    batch_no = version + "W"+ time.strftime('%Y')[2:] + time.strftime('%W')
    return (version, batch_no)

def zipFile(src_folder, dst_path, del_src = True):
    if os.path.exists(dst_path):
        os.remove(dst_path)
    # print("src: ", src_folder)
    # print("dst: ", dst_path)
    fd = zipfile.ZipFile(dst_path, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            fd.write(os.path.join(root, file), os.path.join(root, file).replace(src_folder+"\\", ""))
    fd.close()
    if del_src:
        shutil.rmtree(src_folder)
    logging.info("ZIP file: %s SUCCESS"%(dst_path))

def runExe(exe_path, check_name):

    def _run(exe_path, check_name):

        subprocess.Popen(exe_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        cmd = "wmic process where name=\"%s\" get executablepath,processid"%(check_name)
        ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while True:
            for line in iter(ret.stdout.readline, b""):
                if check_name.encode() in line:
                    pid = int(line.decode().strip().replace(" ", "").split(check_name)[-1])
                    print("Get PID: %d" % (pid))
                    return

    threading.Thread(target=_run, args=(exe_path, check_name)).start()
    time.sleep(3)

def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')

def aesEncrypt(text, key="chinainfosafemes", iv = "1478523698529637"):
    mode = AES.MODE_CBC
    text = add_to_16(text)
    crypt = AES.new(key.encode("utf-8"), mode, iv.encode("utf-8"))
    return crypt.encrypt(text).hex()

def aesDecrypt(text, key="chinainfosafemes", iv = "1478523698529637"):
    mode = AES.MODE_CBC
    decrypt = AES.new(key.encode("utf-8"), mode, iv.encode("utf-8"))
    return decrypt.decrypt(bytes.fromhex(text)).decode().rstrip("\0")

# print(fileMd5(r"C:\Users\chutty\Downloads\mmpt_tool_lossSet_P3.zip"))
