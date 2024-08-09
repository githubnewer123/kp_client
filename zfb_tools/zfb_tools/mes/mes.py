import requests,json,logging,os
from mes.order import Order
import pymysql.cursors
import time,threading

# {"name": "xk_mes@zyxa", "password": "xk_mes"}
# MES_ADDRESS_OFFICIAL = "mes.chinainfosafe.com"
# MES_ADDRESS_TEST = "testmes.chinainfosafe.com"
# global MES_ADDRESS

class Mes():
    def __init__(self):
        # self.user_name = "xk_mes@zyxa"
        # self.password = "xk_mes"
        self.mes_address_test = "testmes.chinainfosafe.com"
        self.mes_address_official = "mes.chinainfosafe.com"
        self.token = None
        self.test_mode = False
        self.enable_mode = False
        self.orderlist = []
        self.active_order = None
        self.chipid_list = None
        self.chip_id_get_event =  threading.Event()
        self.retry_cnt = 3

    def getOrderInfo(self, orderid):
        if self.enable_mode:
            url = "http://120.76.176.138:6602/platform-admin/system/element/v2/getElementByOrderId"
        else:
            url = "http://%s/platform-admin/system/element/getElementByOrderId"%(self.mes_address_test if self.test_mode else self.mes_address_official)
        headers = {"Content-Type": "application/json;charset=UTF-8", "token": self.token}
        data = {"orderId": orderid}
        logging.info(str(data))
        data_json = json.dumps(data)
        response = requests.post(url, data=data_json, headers=headers, json=True, timeout=5)
        logging.info(response.content.decode())
        information = json.loads(response.content.decode())
        # print("获得订单信息",information)
        return information


    def setActiceOrder(self, order_id, db_update = True, scrip_update = True):
        for order in self.orderlist:
            if order.order_id == order_id:
                self.active_order = order
                logging.info("Active Order ID: %s"%(self.active_order.order_id))
                info = self.getOrderInfo(order_id)
                logging.info("%s %s"%(info["msg"], info['code']))
                if info["msg"].__eq__('success') and int(info['code']) == 0:
                    order.setOrderInfo(info["list"],db_update, scrip_update)
                    return
                else:
                    raise Exception("获取订单详细信息出错！\n msg:%s code:%d"%(info["msg"], info['code']))
        else:
            raise Exception("选择激活订单号错误: "+order_id)



    def getActiveOrder(self):
        if self.active_order is None:
            raise  Exception("当前没有激活的订单")
        return self.active_order

    def setTestMode(self, enable):
        self.test_mode = enable

    def setMESMode(self,enable):
        self.enable_mode = enable

    def login(self, use_name, passworld):
        self.user_name = use_name
        self.password = passworld
        if self.enable_mode:
            url = "http://120.76.176.138:6602/platform-admin/system/element/v2/login"
        else:
            url = "http://%s/platform-admin/system/element/login"%(self.mes_address_test if self.test_mode else self.mes_address_official)
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        data = {"userName": self.user_name, "password": self.password}
        data_json = json.dumps(data)
        response = requests.post(url, data=data_json, headers=headers, json=True)
        logging.info(str(response.content))
        information = json.loads(response.content.decode())
        logging.info(information["code"])
        if information["code"] == 0:
            print(url, self.user_name, self.password, information)
            self.token = information["token"]
        else:
            raise Exception("登录服务器出错！请检查用户名和密码\n 服务器返回 code: "+str(information["code"]))

    def getToken(self):
        return self.token

    def _dbGetChipId(self, imei):
        db = pymysql.connect(host='rm-wz965xa64b024m2bzyo.mysql.rds.aliyuncs.com',
                             port=3306,
                             user='cis_test',
                             password='Zyxatest123',
                             db='product_zyxames',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        cmd = "SELECT chip_id FROM zyxa_process_data where imei = '%s' and process_sequence = 2 and process_result = 1 group by create_time" % (
            imei)
        cursor.execute(cmd)
        rl = cursor.fetchall()
        db.close()
        if rl is None:
            self.chip_id_get_event.set()
            return
        self.chipid_list = []
        for id in rl:
            if id["chip_id"] is None:
                continue
            if id["chip_id"] not in self.chipid_list:
                self.chipid_list.append(id["chip_id"])
        self.chip_id_get_event.set()

    def waitChipIdGetDone(self, timeout = 1):
        self.chip_id_get_event.wait(timeout)
        self.chip_id_get_event.clear()

    def getChipidFromMes(self, imei):
        self.chipid_list = None
        self.chip_id_get_event.clear()
        threading.Thread(target=self._dbGetChipId, args=(imei,)).start()


    def orderParse(self, info):
        if info is None or info["msg"] != "success" or info["code"] != 0 :
            raise Exception("获取订单信息解析出错\n" + info)
        orders = info["page"]["records"]
        # print("orders:",orders)
        if len(orders) == 0:
            raise Exception("未获取到该账号下的订单信息，请联系供应商！\n")

        self.orderlist.clear()
        for item in orders:
            try:
                order = Order(item)
                # print(order.getOrderDict())
                self.orderlist.append(order)
            except Exception as e:
                print("错误信息：",e)
                logging.info(str(e))

    def getOrderList(self):
        if self.enable_mode:
            url = "http://120.76.176.138:6602/platform-admin/system/element/v2/getOrderList"
        else:
            url = "http://%s//platform-admin/system/element/getOrderList"%(self.mes_address_test if self.test_mode else self.mes_address_official)
        headers = {"Content-Type": "application/json;charset=UTF-8", "token": self.token}
        data = {"page": 1, "limit": 100}
        data_json = json.dumps(data)
        response = requests.post(url, data=data_json, headers=headers, json=True, timeout=5)
        information = json.loads(response.content.decode())
        # print("information",information,self.test_mode)
        logging.info(information)
        self.orderParse(information)
        # print("订单列表",self.orderlist)
        return self.orderlist

    def getProductOrderList(self):
        order_list = []
        for order in self.orderlist:
            if order.order_status is not None:
                # print("order:",order.order_status,order.order_id)
                if order.order_status == 2 or order.order_status == 3:
                    order_list.append(order)
            else:
                order_list.append(order)
        return order_list

    def getRepairOrderList(self):
        order_list = []
        for order in self.orderlist:
            if order.order_status is not None:
                if order.order_status == 6:
                    order_list.append(order)
        return order_list

    def postProductData(self, data):
        if self.enable_mode:
            url = "http://120.76.176.138:6602/platform-admin/system/element/v2/saveProduceData"
        else:
            url = "http://%s/platform-admin/system/element/saveProduceData"%(self.mes_address_test if self.test_mode else self.mes_address_official)
        print(self.test_mode, self.token)
        headers = {"Content-Type": "application/json;charset=UTF-8", "token": self.token}
        logging.info("post data: %s"%(str(data)))
        tool_data_json = json.dumps(data)
        logging.info(str(tool_data_json))
        response = requests.post(url, data=tool_data_json, headers=headers, json=True, timeout=5)
        information = json.loads(response.content.decode())
        logging.info(information)
        print(information)
        print(self.user_name,self.password)

        if information["code"] == 401 and self.retry_cnt > 0:
            self.login(self.user_name, self.password)
            self.postProductData(data)
            self.retry_cnt -= 1
        elif information["code"] != 0 or not information["msg"].__eq__("success"):
            raise Exception("Mes 上传生产数据出错!code: %d msg: %s"%(information["code"],information["msg"]))

        if len(information["data"]["failList"]) > 0:
            fail_reason = ""
            for item in information["data"]["failList"]:
                fail_reason += item["reason"]

            raise  Exception("Mes: 提交出错，reason: "+fail_reason)

    def postLogFile(self, file_path, chip_id):
        if self.enable_mode:
            url = "http://120.76.176.138:6602/platform-admin/system/element/v2/uploadFile"
        else:
            url = "http://%s/platform-admin/system/element/uploadFile"%(self.mes_address_test if self.test_mode else self.mes_address_official)
        files = {"file": open(file_path, 'rb')}
        data = {
            "deviceId": chip_id,
            "orderId": self.getActiveOrder().order_id,
            "processName": "校准文件",
        }
        headers = {
            "token": self.token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.1'
            # "Content-Type": "multipart/form-data"
        }
        try:
            logging.info("post log file size: %d url: %s\n data: %s"%(os.path.getsize(file_path),url, str(data)))
            response = requests.post(url, data=data, files=files, headers=headers, json=True, timeout=5)
        except Exception:
            raise  Exception("MES: 上传log文件请求出错")
        logging.info(response.content)
        logging.info(response.content.decode())
        information = json.loads(response.content.decode())
        logging.info(information)
        if information["code"] == 0 and information["msg"].__eq__("success"):
            self.retry_cnt = 3
            return information["url"]
        elif information["code"] == 401 and self.retry_cnt > 0:
            self.login(self.user_name, self.password)
            self.postLogFile(file_path, chip_id)
            self.retry_cnt -= 1
        elif information["code"] == 500:
            raise Exception("MES: 服务器返回出错: %s" % (information["msg"]))
        else:
            self.retry_cnt = 3
            raise Exception("MES: 上传log文件回复出错 code: %d"%(information["code"]))

    def checkmodle(self, orderid,type, processSequence, uniIdList):
        if self.enable_mode:
            url = "http://120.76.176.138:6602/platform-admin/system/element/v2/checkBySequence"
        else:
            url = "http://%s//platform-admin/system/element/checkBySequence"%(self.mes_address_test if self.test_mode else self.mes_address_official)
        headers = {"Content-Type": "application/json;charset=UTF-8", "token": self.token}
        data = {"orderId": orderid, "uniIdType": type, "processSequence": processSequence,"uniIdList": uniIdList}
        data_json = json.dumps(data)
        try:
            response = requests.post(url, data=data_json, headers=headers, json=True, timeout=5)
            information = json.loads(response.content.decode())
        except Exception:
            return False
        if information["code"] != 0:
            return False
        return information