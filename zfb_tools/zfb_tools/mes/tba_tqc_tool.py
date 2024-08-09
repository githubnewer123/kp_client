import json
import os

import serial
import serial.tools.list_ports


class universalTool():
    def datetime_conversion(self,datetimedata):
        return datetimedata.strftime('%Y-%m-%d %H:%M:%S.%f')

    def write_setting(self, setname, writedata,filename):
        set_file = json.load(open(filename))
        set_file[setname] = writedata
        json.dump(set_file, open(filename, "w"))

    def read_setting(self, setname,filename):
        try:
            set_file = json.load(open(filename))
            res =set_file[str(setname)]
            return res
        except Exception:
            return False


    def check_setting(self):
        config_set = ["link_time_out",
                      "burn_time_out",
                        "burn_success_time_out",
                        "layout",
                        "calibration",
                        "path",
                    ]
        for i in config_set:
            if not self.read_setting(i):
                print(i)
                file = open("setting.json", "w")
                file.close()
                self.init_setting()
                return False
        return True

    def init_setting(self):
        set_file = {}
        set_file["link_time_out"] = "10"
        set_file["burn_time_out"] = "50"
        set_file["burn_success_time_out"] = "20"
        set_file["layout"] = "4*6"
        set_file["calibration"] = []
        set_file["path"] = "暂无"
        set_file["station"] = ""
        set_file["order_cache"] = ""
        set_file["fail_num"] = 0
        set_file["success_num"] = 0
        set_file["admin"] = ""
        set_file["password"] = ""
        json.dump(set_file, open("setting.json", "w"))

    def setting_check(self):
        if not os.path.isfile("setting.json"):
            self.init_setting()

class port():
    def __init__(self):
        self.port_dict = {"COM": "", "name": "", "location": "", "color": "", "label": "", "state": "",
                          "thread": ""}
        self.port_list = []

    def serial_List(self):
        port = list(serial.tools.list_ports.comports())
        for i in range(0, len(port)):
            state = str(port[i]).split(" ")
            states = ""
            for j in range(2, len(state) - 1):
                states = states + " " + state[j]
            if "ASR Serial Download Device" in str(port[i]):
                self.port_list.append({"text": str(port[i]).split(" ")[0], "name": states,
                                       "location": str(port[i].location).split(":")[0], "color": "yellow",})
        return self.port_list

    def port_Initialize(self):
        port_dict_copy = self.port_dict
        return port_dict_copy