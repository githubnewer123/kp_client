import requests,json,logging
from manager.tool_config import ToolConfig
from lxml import etree
# {"name": "xk_mes@zyxa", "password": "xk_mes"}
# MES_ADDRESS_OFFICIAL = "mes.chinainfosafe.com"
# MES_ADDRESS_TEST = "testmes.chinainfosafe.com"
# global MES_ADDRESS

class FactoryMes():
    def __init__(self, config):
        self.mes_address = "http://192.168.1.239:808/MesInterFace.asmx/CollectPcbaPackInfo"
        self.config = config


    def postData(self, imei, result, false_info = ""):
        if int(self.config.station_type) == 0 or self.config.line_num == "无":
            return True

        data = {
            "iSN": imei,
            "iResCode": "TEST%s_功能测试"%(self.config.line_num),
            "iOperator": "TEST01",
            "iResult":"",
            "iErrCode":false_info,
            "iTSMemo":"1",
            "iFBatch":"1",
            "iFLine":"TEST01",
            "iCount":"1"

        }
        try:
            if result:
                data["iResult"] = "合格"
            else:
                data["iResult"] = "NG"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.1',
                "Content-Type": "application/x-www-form-urlencoded"
            }
            print(data)
            response = requests.post(self.mes_address, data=data,headers=headers, timeout=5)
            print(response.content.decode())
            res = response.content.decode().split("<string xmlns=\"http://localhost/\">")[-1].replace("</string>","")
            if res.lower().__eq__("ok"):
                self.config.configFactoryMesResult(True)
                return True
            self.config.configFactoryMesResult(False)
            return False
        except Exception as e:
            self.config.configFactoryMesResult(False)
            logging.error(str(e))
            # raise Exception("MES: 上传Factory Mes请求出错")
            return False

if __name__ == "__main__":
    fac_mes = FactoryMes(ToolConfig())
    fac_mes.postData("869734052240938", True, "SUCCESS")