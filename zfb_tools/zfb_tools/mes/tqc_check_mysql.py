import pymysql.cursors
import json,time


class CisMesDb():
    def __init__(self, order_id):
        self.con= self.connect()
        self.cursor = self.con.cursor()
        self.order_id = order_id

    def connect(self):
        connection = pymysql.connect(host='rm-wz965xa64b024m2bzyo.mysql.rds.aliyuncs.com',
                                     port=3306,
                                     user='cis_test',
                                     password='Zyxatest123',
                                     db='product_zyxames',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        return connection

    def getChipidFromImei(self, imei,orderid):
        self.cursor.execute(
            "SELECT chip_id FROM zyxa_process_data where imei = '%s' and order_id = '%s' group by create_time"%(imei,orderid))
        rl = self.cursor.fetchall()
        if len(rl) > 0:
            for i in range(len(rl)):
                if rl[-i]["chip_id"] != None:
                    return rl[-i]["chip_id"]

    def getCalInfo(self, chip_id,orderid):
        self.cursor.execute(
            "SELECT * FROM zyxa_process_data where chip_id = '%s' and process_sequence = 2 and order_id = '%s' group by create_time" % (chip_id,orderid))
        rl = self.cursor.fetchall()
        return rl

    def getNstInfo(self, chip_id,orderid):
        self.cursor.execute(
            "SELECT * FROM zyxa_process_data where chip_id = '%s' and process_sequence = 3 and order_id = '%s' group by create_time"  % (chip_id,orderid))
        rl = self.cursor.fetchall()
        return rl

    def getDownloadInfo(self, chip_id,orderid):
        self.cursor.execute(
            "SELECT * FROM zyxa_process_data where chip_id = '%s' and process_sequence = 1 and order_id = '%s' group by create_time" % (chip_id,orderid))
        rl = self.cursor.fetchall()
        return rl

    def close(self):
        self.cursor.close()
        self.con.close()

class check_station():
    def check(self,orderid,imei):
        db = CisMesDb(orderid)
        stime = time.time()
        chip_id = db.getChipidFromImei(imei,orderid)
        download_info_list = db.getDownloadInfo(chip_id,orderid)
        cal_info_list = db.getCalInfo(chip_id,orderid)
        nst_info_list = db.getNstInfo(chip_id,orderid)
        process = []
        if len(download_info_list) > 0:
            info = download_info_list[-1]
            process.append([info["curr_station_number"],"无"])
        else:
            process.append(["无", "无"])
        if len(cal_info_list) > 0:
            info = cal_info_list[-1]
            process.append([info["curr_station_number"], process[-1][0]])
        else:
            process.append(["无", "无"])
        if len(nst_info_list) > 0:
            info = nst_info_list[-1]
            if process[-1][0] == "无" and process[-1][1] == "无":
                process.append([info["curr_station_number"], process[0][0]])
            else:
                process.append([info["curr_station_number"], process[-1][0]])
        else:
            process.append(["无", "无"])
        db.close()
        return process

