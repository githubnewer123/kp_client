import json

class GpioCheck:
    def __init__(self, cfg, platform = "RG"):
        self.gpio_check_en = False
        self.check_list_600_CG = {"GPIO_00_02":{"enable":False, "check_val":"0&2","desc":"GPIO0-2"},
                           "GPIO_01_03": {"enable": False, "check_val": "1&3", "desc": "GPIO1-3"},
                           "GPIO_04_06": {"enable": False, "check_val": "4&6", "desc": "GPIO4-6"},
                           "GPIO_05_07": {"enable": False, "check_val": "5&7", "desc": "GPIO5-7"},
                           "GPIO_08_10": {"enable": False, "check_val": "8&10", "desc": "GPIO8-10"},
                           "GPIO_09_11": {"enable": False, "check_val": "9&11", "desc": "GPIO9-11"},
                           "GPIO_12_14": {"enable": False, "check_val": "12&14", "desc": "GPIO12-14"},
                           "GPIO_13_15": {"enable": False, "check_val": "13&15", "desc": "GPIO13-15"},
                           "GPIO_16_18": {"enable": False, "check_val": "16&18", "desc": "GPIO16-18"},
                           "GPIO_17_19": {"enable": False, "check_val": "17&19", "desc": "GPIO17-19"},
                           "GPIO_20_22": {"enable": False, "check_val": "20&22", "desc": "GPIO20-22"},
                           "GPIO_21_23": {"enable": False, "check_val": "21&23", "desc": "GPIO21-23"},
                           "GPIO_24_26": {"enable": False, "check_val": "24&26", "desc": "GPIO24-26"},
                           "GPIO_32_34": {"enable": False, "check_val": "32&34", "desc": "GPIO32-34"},
                           "GPIO_33_35": {"enable": False, "check_val": "33&35", "desc": "GPIO33-35"},
                           "GPIO_36_124": {"enable": False, "check_val": "36&124", "desc": "GPIO36-124"},
                           "GPIO_49_51": {"enable": False, "check_val": "49&51", "desc": "GPIO49-51"},
                           "GPIO_50_52": {"enable": False, "check_val": "50&52", "desc": "GPIO50-52"},
                           "GPIO_53_69": {"enable": False, "check_val": "53&69", "desc": "GPIO53-69"},
                           "GPIO_54_70": {"enable": False, "check_val": "54&70", "desc": "GPIO54-70"},
                           "GPIO_DIO9_121": {"enable": False, "check_val": "77&121", "desc": "GPIO77-121"},
                           "GPIO_DIO10_122": {"enable": False, "check_val": "78&122", "desc": "GPIO78-122"},
                           "GPIO_27_25": {"enable": False, "check_val": "27&25", "desc": "GPIO27-25"},
                           "GPIO_28_31": {"enable": False, "check_val": "28&31", "desc": "GPIO28-31"},
                           "GPIO_126": {"enable": False, "check_val": "126", "desc": "GPIO126"}
                        }
        self.check_list_600_RG = {"GPIO_00_02": {"enable": False, "check_val": "71&2", "desc": "GPIO71-2"},
                           "GPIO_01_03": {"enable": False, "check_val": "72&3", "desc": "GPIO72-3"},
                           "GPIO_04_06": {"enable": False, "check_val": "4&6", "desc": "GPIO4-6"},
                           "GPIO_05_07": {"enable": False, "check_val": "5&7", "desc": "GPIO5-7"},
                           "GPIO_08_10": {"enable": False, "check_val": "8&10", "desc": "GPIO8-10"},
                           "GPIO_09_11": {"enable": False, "check_val": "9&11", "desc": "GPIO9-11"},
                           "GPIO_12_14": {"enable": False, "check_val": "12&14", "desc": "GPIO12-14"},
                           "GPIO_13_15": {"enable": False, "check_val": "13&15", "desc": "GPIO13-15"},
                           "GPIO_16_18": {"enable": False, "check_val": "16&18", "desc": "GPIO16-18"},
                           "GPIO_17_19": {"enable": False, "check_val": "17&19", "desc": "GPIO17-19"},
                           "GPIO_20_22": {"enable": False, "check_val": "20&22", "desc": "GPIO20-22"},
                           "GPIO_21_23": {"enable": False, "check_val": "21&23", "desc": "GPIO21-23"},
                           "GPIO_24_26": {"enable": False, "check_val": "24&26", "desc": "GPIO24-26"},
                           "GPIO_32_34": {"enable": False, "check_val": "32&34", "desc": "GPIO32-34"},
                           "GPIO_33_35": {"enable": False, "check_val": "33&35", "desc": "GPIO33-35"},
                           "GPIO_36_124": {"enable": False, "check_val": "36&124", "desc": "GPIO36-124"},
                           "GPIO_49_51": {"enable": False, "check_val": "49&51", "desc": "GPIO49-51"},
                           "GPIO_50_52": {"enable": False, "check_val": "50&52", "desc": "GPIO50-52"},
                           "GPIO_53_69": {"enable": False, "check_val": "53&69", "desc": "GPIO53-69"},
                           "GPIO_54_70": {"enable": False, "check_val": "54&70", "desc": "GPIO54-70"},
                           "GPIO_DIO9_121": {"enable": False, "check_val": "77&121", "desc": "GPIO77-121"},
                           "GPIO_DIO10_122": {"enable": False, "check_val": "78&122", "desc": "GPIO78-122"},
                           "GPIO_27_25": {"enable": False, "check_val": "27&25", "desc": "GPIO27-25"},
                           "GPIO_28_31": {"enable": False, "check_val": "28&31", "desc": "GPIO28-31"},
                           "GPIO_126": {"enable": False, "check_val": "126", "desc": "GPIO126"}
                        }
        self.check_list_800_RG = {"GPIO_00_71": {"enable": False, "check_val": "0&71", "desc": "GPIO0-71"},
                              "GPIO_01_72": {"enable": False, "check_val": "1&72", "desc": "GPIO1-72"},
                              "GPIO_02_03": {"enable": False, "check_val": "2&3", "desc": "GPIO2-3"},
                              "GPIO_04_06": {"enable": False, "check_val": "4&6", "desc": "GPIO4-6"},
                              "GPIO_05_07": {"enable": False, "check_val": "5&7", "desc": "GPIO5-7"},
                              "GPIO_08_10": {"enable": False, "check_val": "8&10", "desc": "GPIO8-10"},
                              "GPIO_09_11": {"enable": False, "check_val": "9&11", "desc": "GPIO9-11"},
                              "GPIO_16_18": {"enable": False, "check_val": "16&18", "desc": "GPIO16-18"},
                              "GPIO_17_19": {"enable": False, "check_val": "17&19", "desc": "GPIO17-19"},
                              "GPIO_20_22": {"enable": False, "check_val": "20&22", "desc": "GPIO20-22"},
                              "GPIO_21_23": {"enable": False, "check_val": "21&23", "desc": "GPIO21-23"},
                              "GPIO_24_26": {"enable": False, "check_val": "24&26", "desc": "GPIO24-26"},
                              "GPIO_32_34": {"enable": False, "check_val": "32&34", "desc": "GPIO32-34"},
                              "GPIO_33_31": {"enable": False, "check_val": "33&31", "desc": "GPIO33-31"},
                              "GPIO_36_124": {"enable": False, "check_val": "36&124", "desc": "GPIO36-124"},
                              "GPIO_49_51": {"enable": False, "check_val": "49&51", "desc": "GPIO49-51"},
                              "GPIO_50_52": {"enable": False, "check_val": "50&52", "desc": "GPIO50-52"},
                              "GPIO_53_69": {"enable": False, "check_val": "53&69", "desc": "GPIO53-69"},
                              "GPIO_54_77": {"enable": False, "check_val": "54&77", "desc": "GPIO54-77"},
                              "GPIO_73_74": {"enable": False, "check_val": "73&74", "desc": "GPIO73-74"},
                              "GPIO_27_25": {"enable": False, "check_val": "27&25", "desc": "GPIO27-25"},
                              "GPIO_77_78": {"enable": False, "check_val": "77&78", "desc": "GPIO77-78"},
                              "GPIO_126": {"enable": False, "check_val": "126", "desc": "GPIO126"}
                              }
        self.check_list_800_EG = {"GPIO_01_10": {"enable": False, "check_val": "1&10", "desc": "GPIO01-10"},
                                  "GPIO_03_7": {"enable": False, "check_val": "3&7", "desc": "GPIO3-7"},
                                  "GPIO_04_27": {"enable": False, "check_val":  "4&27", "desc": "GPIO4-27"},
                                  "GPIO_05_17": {"enable": False, "check_val": "5&17", "desc": "GPIO5-17"},
                                  "GPIO_06_12": {"enable": False, "check_val": "6&12", "desc": "GPIO6-12"},
                                  "GPIO_08_22": {"enable": False, "check_val": "8&22", "desc": "GPIO8-22"},
                                  "GPIO_10_16": {"enable": False, "check_val": "10&16", "desc": "GPIO10-16"},
                                  "GPIO_11_24": {"enable": False, "check_val": "11&24", "desc": "GPIO11-24"},
                                  "GPIO_26_28": {"enable": False, "check_val": "26&28", "desc": "GPIO26-28"},
                                  "GPIO_29_32": {"enable": False, "check_val": "29&32", "desc": "GPIO29-32"},
                                  "GPIO_30_31": {"enable": False, "check_val": "30&31", "desc": "GPIO30-31"},
                                  "GPIO_18_SWCLK1": {"enable": False, "check_val": "18&SWCLK1", "desc": "GPIO18-SWCLK1"},
                                  "GPIO_19_SWDIO1": {"enable": False, "check_val": "19&SWDIO1",
                                                     "desc": "GPIO19_SWDIO1"},
                                  "GPIO_9_WAKEUP2": {"enable": False, "check_val": "9&WU2",
                                                     "desc": "GPIO9-WAKEUP2"},
                                  "GPIO_13_WAKEUP0": {"enable": False, "check_val": "13&Wu0",
                                                     "desc": "GPIO13-WAKEUP0"}

                                  }
        self.check_list_600_EG = {"GPIO_01_22": {"enable": False, "check_val": "1&22", "desc": "GPIO1-22"},
                                  "GPIO_02_04": {"enable": False, "check_val": "2&4", "desc": "GPIO2-4"},
                                  "GPIO_03_07": {"enable": False, "check_val": "3&7", "desc": "GPIO3-7"},
                                  "GPIO_05_16": {"enable": False, "check_val": "5&16", "desc": "GPIO5-16"},
                                  "GPIO_18_19": {"enable": False, "check_val": "18&19", "desc": "GPIO18-19"},
                                  "GPIO_26_SWCLK1": {"enable": False, "check_val": "26&SWCLK1", "desc": "GPIO26-SWCLK1"},
                                  "GPIO_06_SWDIO1": {"enable": False, "check_val": "6&SWDIO1", "desc": "GPIO6-SWDIO1"}
                                  }
        self.check_list_800_SG = {"GPIO_12_15": {"enable": False, "check_val": "12&15", "desc": "GPIO12-15"},
                                  "GPIO_13_14": {"enable": False, "check_val": "13&14", "desc": "GPIO13-14"},
                                  "GPIO_73_74": {"enable": False, "check_val": "73&74", "desc": "GPIO73-74"},
                                  "GPIO_53_69": {"enable": False, "check_val": "53&69", "desc": "GPIO53-69"},
                                  "GPIO_05_34": {"enable": False, "check_val": "5&34", "desc": "GPIO5-34"},
                                  "GPIO_33_55": {"enable": False, "check_val": "33&55", "desc": "GPIO33-55"},
                                  "GPIO_10_37": {"enable": False, "check_val": "10&37", "desc": "GPIO10-37"},
                                  "GPIO_50_52": {"enable": False, "check_val": "50&52", "desc": "GPIO50-52"},
                                  "GPIO_49_51": {"enable": False, "check_val": "49&51", "desc": "GPIO49-51"},
                                  "GPIO_06_11": {"enable": False, "check_val": "6&11", "desc": "GPIO6-11"},
                                  "GPIO_04_70": {"enable": False, "check_val": "4&70", "desc": "GPIO30-31"},
                                  "GPIO_35_36": {"enable": False, "check_val": "35&36","desc": "GPIO35-36"},
                                  "GPIO_54_56": {"enable": False, "check_val": "54&56","desc": "GPIO54_56"},
                                  "GPIO_00_01": {"enable": False, "check_val": "0&1",  "desc": "GPIO0-1"},
                                  "GPIO_56_57": {"enable": False, "check_val": "56&57","desc": "GPIO54_56"},
                                  "GPIO_05_07": {"enable": False, "check_val": "5&7", "desc": "GPIO5_7"},
                                  "GPIO_02_03": {"enable": False, "check_val": "2&3", "desc": "GPIO2_3"}

                                  }

        self.check_list_600_SG = {"GPIO_37_56": {"enable": False, "check_val": "37&37", "desc": "GPIO37-56"},
                                  "GPIO_35_55": {"enable": False, "check_val": "35&55", "desc": "GPIO35-55"},
                                  "GPIO_02_05": {"enable": False, "check_val": "2&5", "desc": "GPIO2-5"},
                                  "GPIO_00_03": {"enable": False, "check_val": "0&3", "desc": "GPIO0-3"},
                                  "GPIO_01_74": {"enable": False, "check_val": "1&74", "desc": "GPIO1-74"},
                                  "GPIO_07_08": {"enable": False, "check_val": "7&8", "desc": "GPIO7-8"},
                                  "GPIO_49_73": {"enable": False, "check_val": "49&73", "desc": "GPIO49-73"},
                                  "GPIO_09_50": {"enable": False, "check_val": "9&50", "desc": "GPIO9-50"},
                                  "GPIO_13_14": {"enable": False, "check_val": "13&14", "desc": "GPIO13-14"},
                                  "GPIO_12_15": {"enable": False, "check_val": "12&15", "desc": "GPI12-15"},
                                  "GPIO_04_70": {"enable": False, "check_val": "4&70", "desc": "GPIO30-31"},
                                  "GPIO_36_57": {"enable": False, "check_val": "36&57", "desc": "GPIO36-57"},
                                  "GPIO_06_11": {"enable": False, "check_val": "6&11", "desc": "GPIO6_11"},
                                  "GPIO_54_69": {"enable": False, "check_val": "54&69", "desc": "GPIO54-69"},
                                  }
        # if platform.__eq__("RG"):
        #     self.check_list = self.check_list_RG
        # elif platform.__eq__("CG"):
        #     self.check_list = self.check_list_CG
        # else:
        #     raise Exception("Unsupport GPIO check platform")

        if platform.__eq__("800RG"):
            self.check_list = self.check_list_800_RG
        elif platform.__eq__("800EG"):
            self.check_list = self.check_list_800_EG
        elif platform.__eq__("600EG"):
            self.check_list = self.check_list_600_EG
        elif platform.__eq__("600RG"):
            self.check_list = self.check_list_600_RG
        elif platform.__eq__("800SG"):
            self.check_list = self.check_list_800_SG
        elif platform.__eq__("600SG"):
            self.check_list = self.check_list_600_SG
        else:
            self.check_list = self.check_list_600_CG
        for key in cfg.keys():
            if key not in self.check_list.keys():
                continue
                # raise  Exception("IO测试: IO测试项目(%s)工具不支持"%(key))
            if cfg[key].__eq__("enable"):
                self.gpio_check_en = True
                self.check_list[key]["enable"] = True
        self.check_sim1 = True if cfg["SIM1"].__eq__("enable") else False
        self.check_sim2 = True if cfg["SIM2"].__eq__("enable") else False

    def _getKeyFromVal(self, val):
        for key in self.check_list.keys():
            if self.check_list[key]["check_val"].__eq__(val):
                return key
        for key in self.check_list_600_CG.keys():
            if self.check_list_600_CG[key]["check_val"].__eq__(val):
                return key
        for key in self.check_list_600_RG.keys():
            if self.check_list_600_RG[key]["check_val"].__eq__(val):
                return key
        for key in self.check_list_800_RG.keys():
            if self.check_list_800_RG[key]["check_val"].__eq__(val):
                return key
        for key in self.check_list_800_EG.keys():
            if self.check_list_800_EG[key]["check_val"].__eq__(val):
                return key
        for key in self.check_list_600_EG.keys():
            if self.check_list_600_EG[key]["check_val"].__eq__(val):
                return key
        for key in self.check_list_800_SG.keys():
            if self.check_list_800_SG[key]["check_val"].__eq__(val):
                return key
        for key in self.check_list_600_SG.keys():
            if self.check_list_600_SG[key]["check_val"].__eq__(val):
                return key
        raise Exception("IO测试: 未找到设备错误项-%s"%(val))

    def checkIO(self, res):
        io_res = True
        if "\"GPIO\",[" not in res:
            raise Exception("GPIO测试结果错误")
        if "[]" in res:
            return True,"无异常"
        result = res.replace("\"GPIO\",[", "").replace("]", "")
        if len(result) == 0:
            return True,"无异常"
        if "," in result:
            false_items = result.split(",")
        else:
            false_items = [result]
        resp = ''
        for val in false_items:
            val = val.replace(" ", "")
            key = self._getKeyFromVal(val)
            resp += self.check_list[key]["desc"] + " "
            if self.check_list[key]["enable"] == True:
                io_res = False
        if resp != '':
            return io_res,resp
            # raise Exception("IO测试: %s 测试出错"%(resp))
        return io_res,"无异常"

if __name__ == "__main__":

    cfg = {"template":"LTE","processTotalCount":3,"process":{"proc_burn":"enable","proc_calibration":{"write_sn":"enable","write_imei":"enable","cal":"enable","cal_adc":"disable","activation":"enable"},"proc_test":{"test_io":"enable","test_nst":"enable","test_power":"enable","test_adc":"disable","test_imei":"enable","test_sn":"enable","test_activation":"enable","test_cal":"enable","test_adc_flag":"disable"},"gpio_test":{"GPIO_01_10": "enable","GPIO_03_7": "enable",  "GPIO_04_27": "enable", "GPIO_05_17": "enable", "GPIO_06_12": "enable", "GPIO_08_22": "enable", "GPIO_10_16": "enable","GPIO_11_24": "enable", "GPIO_26_28": "enable", "GPIO_29_32": "enable", "GPIO_30_31": "enable", "GPIO_18_SWCLK1": "enable", "GPIO_19_SWDIO1": "enable","GPIO_9_WAKEUP2": "enable", "GPIO_13_WAKEUP0": "enable","SIM1":"disable","SIM2":"disable"}},"mode":{"LTE":"enable","GSM":"disable"}}

    checker = GpioCheck(cfg["process"]["gpio_test"], "600EG")



