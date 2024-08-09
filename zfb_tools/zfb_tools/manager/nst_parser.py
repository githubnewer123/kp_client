import os,sys,csv

TEST_ITEM_IDX = 0
BAND_IDX = 1
CHANNEL_NO_IDX = 2
UL_BANDWITH_IDX = 3
RB_NUM_IDX = 4
TEST_RESULT_IDX = 7
LOW_LIMIT_IDX = 8
UP_LIMIT_IDX = 9

GSM_TEST_ITEM_IDX = 0
GSM_TEST_BAND_IDX = 1
GSM_TEST_CHANNEL_IDX = 3
GSM_TEST_RESULT_IDX = 7
band_list_default = [1, 3, 5, 8, 34, 38, 39, 40, 41]
gsm_band_list = ["EGSM", "GSM1800"]

class NstFileParser():

    def getBandList(self):
        if self.is_gsm:
            return gsm_band_list
        else:
            return self.band_list

    def getTestResult(self, band):
        try:
            if not self.is_gsm:
                return self.parser[band]
            else:
                if type(band) != str or band not in gsm_band_list:
                    return None
                return self.parser[band]
        except Exception as e:
            print(e)
            return None


    def _maxPowerInit(self):
        if self.is_gsm:
            for line in self.reader:
                if "ArgBustPower".__eq__(line[GSM_TEST_ITEM_IDX]):
                    self.parser[line[1]].append(float(line[GSM_TEST_RESULT_IDX]))
        else:
            for line in self.reader:
                if "Max Power".__eq__(line[TEST_ITEM_IDX]):
                    self.parser[int(line[1])].append(float(line[TEST_RESULT_IDX].replace("dBm", "")))

        # print(self.parser)

    def __init__(self, file_path, isGsm = False, band_list = None):
        if not file_path.endswith("csv"):
            raise Exception("综测分析不支持该文件格式")

        if not os.path.exists(file_path):
            raise Exception("综测分析文件不存在")

        self.file_path = file_path
        self.is_gsm = isGsm
        self.reader = csv.reader(open(self.file_path, "r"))
        self.parser = {}
        self.band_list = band_list
        if self.band_list is None:
            self.band_list = band_list_default
        if self.is_gsm:
            for band in gsm_band_list:
                self.parser[band] = []
        for band in self.band_list:
            self.parser[band] = []

        self._maxPowerInit()


class NstParser():
    def __init__(self, path_list):
        if len(path_list) <= 0:
            raise Exception("请正确选择需要分析的文件")

        self.paser_list = []
        for path in path_list:
            self.paser_list.append(NstFileParser(path))

    def getMaxpower(self, band):
        size = len(self.paser_list)
        power_list = [parser.getTestResult(band) for parser in self.paser_list]
        dl_val = 0.0
        mid_val = 0.0
        hi_val = 0.0
        for power in power_list:
            if len(power) == 1:
                dl_val += power[0]
                mid_val += power[0]
                hi_val += power[0]
            else:
                dl_val += power[0]
                mid_val += power[1]
                hi_val += power[2]
        return [round(dl_val/size, 2),round(mid_val/size, 2),round(hi_val/size, 2)]



if __name__ == "__main__":
    file_path1 = r"D:\tencent\WeChat Files\rx-2012\FileStorage\File\2021-10\CG5894_1.csv"
    file_path2 = r"D:\tencent\WeChat Files\rx-2012\FileStorage\File\2021-10\CG5894_2.csv"
    file_path3 = r"D:\tencent\WeChat Files\rx-2012\FileStorage\File\2021-10\CG5894_3.csv"
    nst_parser = NstParser([file_path1, file_path2, file_path3])
    print(nst_parser.getMaxpower(3))
    print(nst_parser.getMaxpower(34))
    print(nst_parser.getMaxpower(40))




