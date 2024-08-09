#coding=utf-8
from ctypes import Structure
from ctypes import c_int, c_char_p, POINTER, c_byte
from ctypes import CDLL,cast
import sys
import os
from base64 import b64decode
from burn_tool.kp_zfb.adapter_utils import is_secure_chip_for_alipay

class KpLightKeyInfo(Structure):
    pass

KpLightKeyInfo._fields_ = [
    ('iType', c_int),#huk ,equals the huk when pull pass to interface
    ('iKeyLen', c_int),# chip id
    ('pKeyData', POINTER(c_byte)),# error msg
    ('pNext', POINTER(KpLightKeyInfo)),#next kp result,null if no more
]

class KpLightResult(Structure):
    pass

KpLightResult._fields_ = [
    ('pId', c_char_p),#huk ,equals the huk when pull pass to interface
    ('pCid', c_char_p),# chip id
    ('pDescribe', c_char_p),# error msg
    ('kr_data', c_char_p),# kr data
    ('pKeyInfoHead', POINTER(KpLightKeyInfo)),#kp data 
    ('pNext', POINTER(KpLightResult)),#next kp result,null if no more
]


class KpHSecResult(Structure):
    pass

KpHSecResult._fields_ = [
    ('pHuk', c_char_p),#huk ,equals the huk when pull pass to interface
    ('pCid', c_char_p),# chip id
    ('pDescribe', c_char_p),# error msg
    ('pKpData', POINTER(c_byte)),#kp data 
    ('iKpDataLen', c_int),#kp data len
    ('iIsValidKp', c_int),#if kp is validate ,if ==0m means it is a invaldate kp
    ('pNext', POINTER(KpHSecResult)),#next kp result,null if no more
]


class KpResponse(Structure):
    _fields_ = [
        ('iCode', c_int),#kp server response code, if !=0 means error ocurs
        ('pMessage', c_char_p),#server error message
        ('chipType', c_byte * 32),#server error message
        ('pResultHead', POINTER(KpHSecResult)),#pull result list
    ]

#init apis
PULL_CHIP_TYPE_HSEC = b"HSC32I1"
PULL_CHIP_TYPE_LIGHT = b"light"
PULL_CHIP_TYPE_WP_LX100 = b"WP_LX100"
PULL_CHIP_TYPE_DK_LX100 = b"DK_LX100"
HOST = b"http://30.198.69.35"  # 拉取地址
REPORT_PATH = b"/api/occ/kp/report"

def dumpHSecResult(pResult):
    datas = []
    while (pResult):#loop to read all kps
        if(pResult.contents.pDescribe):
            errorMsg = pResult.contents.pDescribe
        else:
            errorMsg = ""

        if(pResult.contents.iIsValidKp == 0):#check if kp data is valid
            print("error current not a valid kp\r\n")
        else:
            #write kp data to file
            kpDataType = c_byte * pResult.contents.iKpDataLen
            kpData = kpDataType()
            data_str = ""
            for i in range(0,pResult.contents.iKpDataLen):
                kpData[i] = pResult.contents.pKpData[i]#read kpdata to python value
                data_str += "%02X"%int.from_bytes((kpData[i]).to_bytes(1, 'little', signed=True), 'little', signed=False)
        
            datas.append({"cid":pResult.contents.pCid.decode("utf-8"),"huk":pResult.contents.pHuk.decode("utf-8"),"kr":data_str})
                    
        pResult = pResult.contents.pNext

    out = {"ret":0,"results":datas}
    print(out)

def dumpLightResult(pResult,huks):
    datas = []
    i = 0
    while (pResult):#loop to read all kps
        kr_data = b64decode(pResult.contents.kr_data)
        data_str = ""
        for j in range(0,len(kr_data)):
            data_str += "%02X"%kr_data[j]
        datas.append({"cid":pResult.contents.pCid.decode("utf-8"),"huk":huks[i].decode("utf-8"),"kr":data_str})
                 
        pResult = pResult.contents.pNext
        i += 1
    out = {"ret":0,"results":datas}
    print(out)


def print_ret(ret):
    result = {}
    result["ret"] = ret
    print(result)

def test_pull(pull_model,pull_license,pull_count,chip_type,huks_in):
    api = CDLL('./libkp_client.so')
    api.csi_kp_pullup_offline.argtypes = [c_char_p, c_char_p, c_int, c_char_p, POINTER(c_char_p),c_char_p]
    api.csi_kp_pullup_offline.restype = POINTER(KpResponse)
    api.csi_kp_releaseResult.argtypes = [POINTER(KpResponse)]

    if(is_secure_chip_for_alipay(chip_type)):
        PULL_BATCH_PATH = b"/api/occ/kp/getKpInfo"
    elif(chip_type == PULL_CHIP_TYPE_LIGHT):
        PULL_BATCH_PATH = b"/api/occ/kp/pull"
    else:
        return -1
    url = HOST + PULL_BATCH_PATH

    #init huks,huks size must equal to PULL_COUNT
    pullHuksArray = c_char_p * pull_count
    huks = pullHuksArray()
    for i in range(0,pull_count):
        huks[i] = huks_in[i]
    pres = api.csi_kp_pullup_offline(url, pull_model, pull_count, pull_license, huks,chip_type)#pull kp

    if(pres):
        if(pres.contents.iCode != 0):
            print_ret("%d"%pres.contents.iCode)
            # print("pull error msg:%s code:%d"%(pres.contents.pMessage.decode(),pres.contents.iCode))
            api.csi_kp_releaseResult(pres)
            return -4
        if(is_secure_chip_for_alipay(chip_type)):
            pResult = cast(pres.contents.pResultHead, POINTER(KpHSecResult))
            dumpHSecResult(pResult)
        elif(chip_type == PULL_CHIP_TYPE_LIGHT):
            pResult = cast(pres.contents.pResultHead, POINTER(KpLightResult))

            dumpLightResult(pResult,huks)
        else:
            api.csi_kp_releaseResult(pres)
            return -2

        api.csi_kp_releaseResult(pres)
    else:
        print_ret(-400)
        return -3

    return 0

def test_report(cids,is_success,chip_type):
    api = CDLL('./libkp_client.so')
    api.csi_kp_report_offline.argtypes = [c_char_p, POINTER(c_char_p), c_int, c_int, c_char_p]
    api.csi_kp_report_offline.restype = POINTER(KpResponse)
    api.csi_kp_releaseResult.argtypes = [POINTER(KpResponse)]

    url = HOST + REPORT_PATH

    cidsArray = c_char_p * len(cids)
    cid_result = {}
    cid_param = cidsArray()
    for i in range(0,len(cids)):
        cid_param[i] = cids[i]
        cid_result[cids[i].decode("utf-8")] = 1

    pres = api.csi_kp_report_offline(url, cid_param,len(cids),is_success,chip_type)#pull kp
    try:
        if(pres):
            if(is_secure_chip_for_alipay(chip_type)):
                pResult = cast(pres.contents.pResultHead, POINTER(KpHSecResult))
            elif(chip_type == PULL_CHIP_TYPE_LIGHT):
                pResult = cast(pres.contents.pResultHead, POINTER(KpLightResult))
            else:
                api.csi_kp_releaseResult(pres)
                return -1
            hasFail = 0
            while(pResult):
                if(pResult.contents.pDescribe):
                    reason = pResult.contents.pDescribe.decode()
                    cid_result[pResult.contents.pCid.decode("utf-8")] = 0
                    hasFail = 1
                else:
                    cid_result[pResult.contents.pCid.decode("utf-8")] = 1
                    reason = ""
                pResult = pResult.contents.pNext
            
            api.csi_kp_releaseResult(pres)
            if(hasFail):
                return -3
        else:
            for key in cid_result.keys():
                cid_result[key] = 0
            return -2
    finally:
        print(cid_result)

    return 0

def main():
    ret = 0
    if(len(sys.argv) >= 2):
        if(sys.argv[1] == "pull"):
            if(len(sys.argv) < 6):
                print("invalid param")
                os._exit(1)
            license = b""
            if(len(sys.argv) >= 7):
                license = sys.argv[6].encode()
            huks = sys.argv[5].encode("utf-8").split(b"-")
            ret = test_pull(sys.argv[2].encode("utf-8"),license,int(sys.argv[3]),sys.argv[4].encode("utf-8"),huks)
        elif(sys.argv[1] == "report"):
            if(len(sys.argv) < 5):
                print("invalid param")
                return False
            cids = sys.argv[2].encode("utf-8").split(b'-')
            ret = test_report(cids,int(sys.argv[3]),sys.argv[4].encode("utf-8"))
        else:
            print("invalid param")
            return False
    else:
        print("invalid param")
        return False
    return True

if __name__ == '__main__':
    try:
        print("Start_of_operation")
        main()
    finally:
        print("End_of_operation")
