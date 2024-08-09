# coding: utf-8
import sys,threading,logging
from base64 import b64decode
from PyQt5.QtCore import pyqtSignal, QObject
import os,time,datetime,serial
import serial.tools.list_ports
import crcmod
from ctypes import c_int, c_char_p, POINTER, c_byte
from ctypes import CDLL,cast
from burn_tool.kp_zfb.adapter_utils import is_secure_chip_for_alipay
from burn_tool.kp_zfb.demo_pull import print_ret,KpHSecResult,KpResponse,KpLightResult
import configparser,shutil
from burn_tool.PostProductData import Postdata

class Kp_send_com6(QObject):
    signal_send_freq_com6 = pyqtSignal(str) #定义一些发送的信号槽
    signal_send_pass_freq_com6 = pyqtSignal(str)
    signal_send_cos_fail_freq_com6 = pyqtSignal(str)
    signal_send_kr_fail_freq_com6 = pyqtSignal(str)
    signal_send_connect_com6 = pyqtSignal(str)
    signal_send_SuperText_com6 = pyqtSignal(str)
    signal_send_Progress_com6 = pyqtSignal(str)
    signal_send_pass_fail_com6 = pyqtSignal(str)
    signal_send_connect_messagebox_com6 = pyqtSignal(str)

    def __init__(self):
        super().__init__()  # 调用父类的 __init__() 方法

        self.Init()  # 初始化
        self.read_cmg()  # 阅读配置文件
        self.set_logger()  # 设置log文件

    def Init(self):
        self._stop_event = threading.Event()  # 用于停止线程的事件
        self.port = ""
        self.license = ""
        self.result = ""
        self.chip_id = None
        self.PULL_CHIP_TYPE_HSEC = b"HSC32I1"
        self.PULL_CHIP_TYPE_LIGHT = b"light"
        self.PULL_CHIP_TYPE_WP_LX100 = b"WP_LX100"
        self.PULL_CHIP_TYPE_DK_LX100 = b"DK_LX100"
        self.HOST = b"http://10.1.100.66:28080"  # 拉取地址
        self.REPORT_PATH = b"/api/occ/kp/report"

    def read_cmg(self):
        # 创建 ConfigParser 对象
        path = os.getcwd()
        config = configparser.ConfigParser()
        config_file = path + '/cfg/lisence_cfg.ini'
        # print(config_file)
        # if not os.path.exists(config_file):
        #     # 添加一个新的section
        #     config.add_section('settings')
        #     config.add_section('Database')
        #     # 在section下添加一些键值对
        #     config.set('settings', 'license', '')
        #     config.set('settings', 'pull_model', 'PAYMENT_ZX9660_SE')
        #     config.set('settings', 'chip_type', 'ZX9660')
        #     config.set('Database', 'log_file_size', "0")
        #     with open(config_file,"w") as f:
        #         config.write(f)
        try:
            # 读取配置文件
            config.read(config_file)
            self.license_name = config.get('settings', 'license')  # 获得配置文件的许可证名称
            self.pull_model = config.get('settings', 'pull_model')  # 获得产品类型
            self.chip_type = config.get('settings', 'chip_type')  # 获得芯片类型
        except Exception as e:
            print(e)


    def set_logger(self):
        # 配置日志基本设置
        self.logger_com6 = logging.getLogger(__name__)
        self.logger_com6.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
        # 检查文件夹是否已存在
        if not os.path.exists('./log'):
            # 不存在，则创建文件夹
            os.mkdir('./log')
        else:
            self.file_log_path = './log'
            # 获取文件夹大小（字节）到达500MB删除文件夹
            folder_size = self.get_folder_size(self.file_log_path)
            print(folder_size)
            self.my_function("文件夹大小为：{}".format(folder_size))
        # 创建一个文件处理器，将所有级别的日志记录到 'log' 文件中
        self.file_handler_com6 = logging.FileHandler(
            'log/kr_{}_com6.log'.format(datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')))
        self.file_handler_com6.setLevel(logging.DEBUG)
        self.file_handler_com6.setFormatter(formatter)
        self.logger_com6.addHandler(self.file_handler_com6)
        # 创建一个流处理器，将错误级别的日志消息输出到命令行
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.ERROR)
        stream_handler.setFormatter(formatter)
        self.logger_com6.addHandler(stream_handler)

    def stop(self):
        self._stop_event.set()  # 设置停止事件，使线程退出执行

    def Start_send(self,mes,cfg):
        self.mes = mes
        self.cfg = cfg
        try:
            print(self.port)
            self.dev = serial.Serial(port=self.port, baudrate=115200, timeout=0.005)  # 设置串口参数
            print(self.dev)
            verify = '43 44 a5 00 00 00 00'  # 0D 0A是\r\n
            verify = bytes.fromhex(verify)
            res_con = self.writeCmd(self.dev, verify)  # 发送

            if res_con:
                if res_con[0:12] == '5253a500000e':
                    self.my_function('串口已连接，通信正常')
                    self.signal_send_connect_com6.emit('{}'.format(self.port))
                    self.signal_send_SuperText_com6.emit('{} 串口已连接，通信正常'.format(self.get_cur_time()))
                    self.Data_dispose()  # 进入Kr烧入循环
                else:
                    self.my_function('串口未连接，通信异常')
                    self.signal_send_SuperText_com6.emit('{} 串口未连接，通信异常'.format(self.get_cur_time()))
                    self.signal_send_connect_messagebox_com6.emit("连接出错")  # mssagebox框提示
                    self.signal_send_connect_com6.emit("已关闭")
                    self.dev.close()
                    raise Exception("AtSelf.Dyevice: The serial port is not connected")
            else:
                self.signal_send_SuperText_com6.emit('{} 串口未连接，通信异常'.format(self.get_cur_time()))
                self.signal_send_connect_messagebox_com6.emit("连接出错")  #mssagebox框提示
                self.signal_send_connect_com6.emit("已关闭")
                self.dev.close()
                raise Exception("AtSelf.Dyevice: The serial port is not connected")
        except serial.SerialException as e:
            print("串口错误:", e)
            self.signal_send_connect_com6.emit("已关闭")
            self.signal_send_connect_messagebox_com6.emit(f"串口错误:{e}")
            self.dev.close()
        except Exception as e:
            self.logger_com6.exception('错误：{}'.format(e))
            sys.exit()###退出线程

    def Data_dispose(self):
        self.huk_end = 0
        self.total_times = 0
        self.pass_freq = 0
        self.fail_freq = 0
        self.kr_fail_freq = 0
        self.cos_fail_freq = 0
        while not self._stop_event.is_set():  # 检查停止事件是否被设置
            self.data_huk = self.readhuk() #读取huk或pass fail指令
            self.start = time.time()

            if self.data_huk:
                if self.data_huk[:12] == '5253b0000010':
                    self.kr_burn_in()
                elif self.data_huk == '5253b30a0000':
                    self.cos_fail_freq = self.cos_fail_freq + 1
                    self.fail_freq = self.kr_fail_freq + self.cos_fail_freq
                    self.burn_result = 'COM位6 COS烧入失败 次数{}'.format(self.cos_fail_freq)
                    self.signal_send_cos_fail_freq_com6.emit(str(self.cos_fail_freq))  # 发送失败拉取次数
                    self.signal_send_pass_fail_com6.emit('FAIL')  # pass fail判断
                    print(self.get_cur_time(), self.burn_result) #终端打印失败拉取次数
                    self.my_function(self.burn_result) #log打印失败拉取次数
                    self.signal_send_SuperText_com6.emit('{} COS烧入失败 次数{}'.format(self.get_cur_time(),self.cos_fail_freq)) #超级文本打印失败拉取次数
                    self.signal_send_freq_com6.emit(str(self.kr_fail_freq + self.cos_fail_freq + self.pass_freq))  # 文本显示总次数
                    self.my_function('烧入总次数{}'.format(str(self.kr_fail_freq + self.cos_fail_freq + self.pass_freq))) #log打印总拉取次数
                    print('-----'*40)
                    self.my_function('-----'*40)
                    self.signal_send_SuperText_com6.emit('-----'*40)
                    Postdata(self.mes, self.cfg, self.chip_id, self.burn_result,self.pass_freq,self.fail_freq)

                elif self.data_huk == '5253b30b0000':
                    self.kr_fail_freq = self.kr_fail_freq + 1
                    self.fail_freq = self.kr_fail_freq + self.cos_fail_freq
                    self.burn_result = 'COM位6 kr烧入失败 次数{}'.format(self.kr_fail_freq)
                    self.signal_send_kr_fail_freq_com6.emit(str(self.kr_fail_freq))  # 发送失败拉取次数
                    self.signal_send_pass_fail_com6.emit('FAIL')  # pass fail判断
                    print(self.get_cur_time(), self.burn_result) #终端打印失败拉取次数
                    self.my_function(self.burn_result) #log打印失败拉取次数
                    self.signal_send_SuperText_com6.emit('{} kr烧入失败 次数{}'.format(self.get_cur_time(),self.kr_fail_freq)) #超级文本打印失败拉取次数
                    self.signal_send_freq_com6.emit(str(self.cos_fail_freq + self.kr_fail_freq + self.pass_freq))  # 文本显示总次数
                    self.my_function('烧入总次数{}'.format(str(self.cos_fail_freq + self.kr_fail_freq + self.pass_freq))) #log打印总拉取次数
                    print('-----'*40)
                    self.my_function('-----'*40)
                    self.signal_send_SuperText_com6.emit('-----'*40)
                    Postdata(self.mes, self.cfg, self.chip_id, self.burn_result,self.pass_freq,self.fail_freq)

                elif self.data_huk == '5253b3000000':
                    self.pass_freq = self.pass_freq + 1  # 成功拉取次数
                    self.fail_freq = self.kr_fail_freq + self.cos_fail_freq
                    self.burn_result = 'COM位6 kr烧入成功 次数{}'.format(self.pass_freq)
                    self.signal_send_pass_freq_com6.emit(str(self.pass_freq))  # 发送成功拉取次数
                    self.signal_send_pass_fail_com6.emit('PASS')  # pass fail判断
                    print(self.get_cur_time(), self.burn_result) #终端打印失败拉取次数
                    self.my_function(self.burn_result) #log打印失败拉取次数
                    self.signal_send_SuperText_com6.emit('{} kr烧入成功 次数{}'.format(self.get_cur_time(),self.pass_freq)) #超级文本打印失败拉取次数
                    self.my_function('烧入总次数{}'.format(str(self.kr_fail_freq + self.cos_fail_freq + self.pass_freq))) #log打印总拉取次数
                    # self.signal_send_Progress_com6.emit(str(self.pass_freq))  # 进度条显示成功次数的进度
                    self.signal_send_freq_com6.emit(str(self.kr_fail_freq + self.cos_fail_freq + self.pass_freq))  # 文本显示总次数
                    print('-----'*40)
                    self.my_function('-----'*40)
                    self.signal_send_SuperText_com6.emit('-----'*40)
                    end = time.time()
                    self.end = (end - self.start)  # 收到b3的时间
                    print(self.get_cur_time(), '总花时：', self.huk_end + self.end)
                    self.my_function('总花时:{}'.format(self.huk_end + self.end))
                    self.signal_send_SuperText_com6.emit(
                        '{} 总花时：{}'.format(self.get_cur_time(), self.huk_end + self.end))
                    Postdata(self.mes, self.cfg, self.chip_id, self.burn_result,self.pass_freq,self.fail_freq)

                else:
                    self.my_function('{} No data was huk，Data anomalies！！'.format(self.get_cur_time()))
                    self.signal_send_SuperText_com6.emit('{} No data was huk，Data anomalies！！！'.format(self.get_cur_time()))
                    self.signal_send_connect_com6.emit("已关闭")
                    self.dev.close()
                    raise Exception("No data was huk，Data anomalies！！！") #抛出没有HUK的错误

            else:
                self.my_function('{} 停止读取数据'.format(self.get_cur_time()))
                self.signal_send_SuperText_com6.emit('{} 停止读取数据'.format(self.get_cur_time()))
                self.signal_send_connect_com6.emit("已关闭")
                self.dev.close()
                raise Exception("停止读取数据") #抛出没有数据的错误

            # self.total_times = self.fail_freq + self.pass_freq
            # self.signal_send_freq_com6.emit(str(self.total_times))  # 文本显示总次数
            # self.my_function('烧入总次数{}'.format(str(self.total_times))) #log打印总拉取次数
            # self.signal_send_SuperText_com6.emit('{} kr烧入 总次数{}'.format(self.get_cur_time(), self.total_times))  # 超级文本打印总次数

            # print('-----' * 40)
            # self.my_function('-----' * 40)
            # self.signal_send_SuperText_com6.emit('-----' * 40)

    def kr_burn_in(self):
        self.signal_send_SuperText_com6.emit(
            '开始拉取产品的许可证名称、产品型号、芯片类型分别为：{} {} {}'.format(self.license_name, self.pull_model,
                                                                               self.chip_type))
        kr = self.main_pull(self.pull_model, '1', self.chip_type, self.data_huk[12:], self.license_name)  # 拉取kr
        # kr = {'ret': 0, 'results': [{'cid': '73c5aaf8d9054b98915c869eaaba2792', 'huk': '3107111704534b3743542e3030233e23', 'kr': '496E44780300000004000100F4000000040020000000000080000000000D00103B00200000000000A0000000FFFFFFFF3E00100000000000C0000000FFFFFFFF5000240000000000D0000000FFFFFFFFE0AD344CAC6DCFE0C324CA9E4FC73AC3567EBA9F00000000000000000000000000000000000000000000000000000000306131366463386463623661343662303866313730666463623736373833303688C3A076DFC742E5FFC9ED14C95BC946E49BC9CBDC83D06B7B5D9757FFCFB33A310711191453413550432E3030637226B1030000F22216A38F3AFC261EB75A77CD5483D22A904D7AAD9D4380F637DB972D505719000000000000000000000000BD02B7D29CFF7DD1936E363F61230A8F8561A3F68758638A4F8AFAE5DE93EFCC25D73D58F18BD69345B8024E9A93A9E72B677EABAFC171795A42F1C5468285397B2273756363657373223A747275652C226465766963654365727469666963617465223A7B2263657274497373756572223A224F50454E415049222C22636F6D70616E79436F6465223A2232303231303033313737363231303336222C22646576696365496E666F726D6174696F6E223A7B22646576696365496D6569223A22646576696365496D6569222C226465766963654D6163223A226465766963654D6163222C22646576696365536E223A223061313664633864636236613436623038663137306664636237363738333036227D2C226578747261506172616D73223A7B226665617475726573223A5B225041594D454E54225D7D2C2270726F647563744D6F64656C223A225A5839363630222C2270726F6475637454797065223A225741544348222C227075626C69634B6579223A222D2D2D2D2D424547494E205055424C4943204B45592D2D2D2D2D5C6E4D466B77457759484B6F5A497A6A3043415159494B6F5A497A6A304441516344516741454A4B4745646C36545231676D3272517931736B566F5046452F37336E5C6E5A52686777397A4C49397253793137414847676E7130336D5754326F772B394D5451386F3550426534744C4E6D484A446B6E4C582F65537153773D3D5C6E2D2D2D2D2D454E44205055424C4943204B45592D2D2D2D2D5C6E222C2273656375726974794E65676F74696174696F6E223A2245434448222C227369676E223A225448557151564D4949502F507A6964526D4F424F732F77346C6A4638734C79324F62776F75774B634F376237337541544D2B724856645679355779585A564E6E6F64454E69444471326C4A546864482B73716E2B45537469314B4E2B326532416C484469386E68546C34436D6837707A4361376B6B2F7654722B65554931327A796D3878653274757259494B514A356C6834344F5A366F34665655674F477A714C764A3057334446583064613171415A752B5048623575754C4F664132617964746F665046647958782B774B304D494542644D475532765870664667725672536C6E35485378782F7052786C666A36757A4B5234564F492F566E4E6B35554B6635516D4D5943326636494338305179646B427767672F3376593051616642487A644B6B6C346258726139344232756573427655456671784968594C453351424F493678574D68414B76317458726D74516F4D78386A773D3D222C227369676E416C676F726974686D223A224241534536345F4F5645525F52534132303438222C22736E223A2232303234303330363031343132363031393834383437227D7D'}]}
        if isinstance(kr, dict):
            if kr['ret'] == 0:
                print(self.get_cur_time(), 'kr拉取完成')  ####判断kr
                self.my_function('kr拉取完成')
                self.signal_send_SuperText_com6.emit('{} kr拉取完成'.format(self.get_cur_time()))
                kr_data = kr["results"][0]['kr']  # kr数据解析
                # print('解析后kr：',kr_data)
                self.chip_id = kr["results"][0]['huk'] # chip_id

                Crc_str = self.crc16_kr(kr_data)
                print('crc:', Crc_str.hex())

                hex_kr = bytes.fromhex(kr_data)
                len_kr = len(hex_kr)
                print('解析后kr整数长度：',len_kr)
                lenkr = len_kr.to_bytes(2, byteorder='big')
                print(lenkr)

                cmd1 = '4344b10000'
                cmd1 = bytes.fromhex(cmd1)
                cmd2 = '4344b2'
                cmd2 = bytes.fromhex(cmd2)

                kr_send = cmd1 + lenkr + hex_kr  # 将字符串转换为字节字符串
                kr_send_crc = cmd2 + lenkr + Crc_str
                res_b1 = self.writeCmd(self.dev, kr_send)  # 发送kr
                if res_b1[:6] == "5253b1":
                    pass
                else:
                    self.my_function('发送lisence数据失败')
                    self.signal_send_SuperText_com6.emit(
                        '{} 发送lisence数据失败'.format(
                            self.get_cur_time()))
                res_b2 = self.writeCmd(self.dev, kr_send_crc)  # 发送kr总长和CRC
                if res_b2[:6] == "5253b2":
                    pass
                else:
                    self.my_function('发送crc校验失败')
                    self.signal_send_SuperText_com6.emit(
                        '{} 发送crc校验失败'.format(
                            self.get_cur_time()))

                huk_end = time.time()  # 收到huk的时间
                self.huk_end = (huk_end - self.start)
        else:
            print(self.get_cur_time(), '拉取失败,没有获取到kr，Data anomalies！！！,检查网络地址和配置的许可证')  ####判断kr
            self.my_function('拉取失败,没有获取到kr，Data anomalies！！！,检查网络地址和配置的许可证')
            self.signal_send_SuperText_com6.emit(
                '{} 拉取失败,没有获取到kr，Data anomalies！！！,检查网络地址和配置的许可证'.format(self.get_cur_time()))
            raise Exception("拉取失败,没有获取到kr，Data anomalies！！！,检查网络地址和配置的许可证")  # 抛出没有kr的错误

    def writeCmd(self, dev, cmd):
            if type(cmd) == str:
                cmd = cmd.encode()
            res = dev.write(cmd)
            if not res:
                raise Exception("AtSelf.Device: write serial cmd error")
            print('{}发送：{}\r\n{} 等待读取数据...'.format(self.get_cur_time(),cmd.hex(),self.get_cur_time()))
            self.my_function('发送:{}'.format(cmd.hex()))
            self.my_function('等待读取数据...')
            self.signal_send_SuperText_com6.emit('{} 发送：{} \r\n{} 等待读取数据...'.format(self.get_cur_time(), cmd.hex(),self.get_cur_time()))

            start_flag = False
            datas = b''
            hex_data = None
            # 假设我们设定的超时时间为2秒
            timeout = 2
            start_time = time.time()
            while not self._stop_event.is_set():
                # 检查是否超时
                if time.time() - start_time > timeout:
                    print("超时，未读取到任何数据")
                    break
                data = self.dev.read(1)  # 读取一个字节的数据
                if data:  # 如果数据不为空
                    if not start_flag:  # 如果还没有开始读取数据
                        start_flag = True  # 标记已开始读取数据
                        start_time = time.time()  # 重置开始时间
                    datas += data
                    hex_data = datas.hex()
                    # 处理读取到的数据
                else:  # 如果数据为空
                    if start_flag:  # 如果已经读取到数据
                        break  # 数据读取结束，跳出循环
            print(self.get_cur_time(), '收到:', hex_data)
            self.my_function('收到:{}'.format(hex_data))
            self.signal_send_SuperText_com6.emit('{} 收到:{}'.format(self.get_cur_time(),hex_data))
            return hex_data

    def readhuk(self):
        print(self.get_cur_time(), '等待读取huk或判断指令...')
        self.signal_send_SuperText_com6.emit('{} 等待读取huk或判断指令...'.format(self.get_cur_time()))
        self.my_function('等待读取huk或判断指令...')

        start_flag = False
        datas = b''
        huk_hex = None
        while not self._stop_event.is_set():  # 检查停止事件是否被设置
            # print(1)
            data = self.dev.read(1)  # 读取一个字节的数据
            if data:  # 如果数据不为空
                if not start_flag:  # 如果还没有开始读取数据
                    start_flag = True  # 标记已开始读取数据
                datas = datas + data
                huk_hex = datas.hex()
                # 处理读取到的数据
            else:  # 如果数据为空
                if start_flag:  # 如果已经读取到数据
                    break  # 数据读取结束，跳出循环
        print(self.get_cur_time(), '收到huk或判断指令:', huk_hex)
        self.signal_send_SuperText_com6.emit('{} 收到huk或判断指令:{}'.format(self.get_cur_time(), huk_hex))
        self.my_function('收到huk或判断指令:{}'.format(huk_hex))
        return huk_hex

    def my_function(self,info):
        self.logger_com6.debug(info)
        # self.logger.info(info)

    def test_pull(self, pull_model, pull_license, pull_count, chip_type, huks_in):
        api = CDLL('./libkp_client.so')
        api.csi_kp_pullup_offline.argtypes = [c_char_p, c_char_p, c_int, c_char_p, POINTER(c_char_p), c_char_p]
        api.csi_kp_pullup_offline.restype = POINTER(KpResponse)
        api.csi_kp_releaseResult.argtypes = [POINTER(KpResponse)]

        if (is_secure_chip_for_alipay(chip_type)):
            PULL_BATCH_PATH = b"/api/occ/kp/getKpInfo"
        elif (chip_type == self.PULL_CHIP_TYPE_LIGHT):
            PULL_BATCH_PATH = b"/api/occ/kp/pull"
        else:
            return -1
        url = self.HOST + PULL_BATCH_PATH
        if self.HOST != b"http://10.1.100.66:28080":
            self.signal_send_SuperText_com6.emit('网络超时，请检查网络地址')
        # init huks,huks size must equal to PULL_COUNT
        pullHuksArray = c_char_p * pull_count
        huks = pullHuksArray()
        for i in range(0, pull_count):
            huks[i] = huks_in[i]
        pres = api.csi_kp_pullup_offline(url, pull_model, pull_count, pull_license, huks, chip_type)  # pull kp
        print('pres', pres)
        if (pres):
            if (pres.contents.iCode != 0):
                print_ret("%d" % pres.contents.iCode)
                # print("pull error msg:%s code:%d"%(pres.contents.pMessage.decode(),pres.contents.iCode))
                api.csi_kp_releaseResult(pres)
                return -4
            if (is_secure_chip_for_alipay(chip_type)):
                pResult = cast(pres.contents.pResultHead, POINTER(KpHSecResult))
                pResult = self.dumpHSecResult(pResult)
                return pResult

            elif (chip_type == self.PULL_CHIP_TYPE_LIGHT):
                pResult = cast(pres.contents.pResultHead, POINTER(KpLightResult))
                pResult = self.dumpLightResult(pResult,huks)
                return pResult

            else:
                api.csi_kp_releaseResult(pres)
                return -2

            api.csi_kp_releaseResult(pres)
        else:
            print_ret(-400)
            return -3

        return 0

    def main_pull(self, pull_model, pull_count, chip_type, huk1, license_name):
        ret = 0
        # if(len(sys.argv) >= 2):
        #     if(sys.argv[1] == "pull"):
        #         if(len(sys.argv) < 6):
        #             print("invalid param")
        #             os._exit(1)
        license = b""
        # if(len(sys.A) >= 7):
        license = license_name.encode()
        huks = huk1.encode("utf-8").split(b"-")
        ret = self.test_pull(pull_model.encode("utf-8"), license, int(pull_count), chip_type.encode("utf-8"), huks)
        return ret

    def dumpHSecResult(self, pResult):
        datas = []
        while (pResult):  # loop to read all kps
            if (pResult.contents.pDescribe):
                errorMsg = pResult.contents.pDescribe
            else:
                errorMsg = ""

            if (pResult.contents.iIsValidKp == 0):  # check if kp data is valid
                print("error current not a valid kp\r\n")
            else:
                # write kp data to file
                kpDataType = c_byte * pResult.contents.iKpDataLen
                kpData = kpDataType()
                data_str = ""
                for i in range(0, pResult.contents.iKpDataLen):
                    kpData[i] = pResult.contents.pKpData[i]  # read kpdata to python value
                    data_str += "%02X" % int.from_bytes((kpData[i]).to_bytes(1, 'little', signed=True), 'little',
                                                        signed=False)

                datas.append(
                    {"cid": pResult.contents.pCid.decode("utf-8"), "huk": pResult.contents.pHuk.decode("utf-8"),
                     "kr": data_str})

            pResult = pResult.contents.pNext

        out = {"ret": 0, "results": datas}
        print(self.get_cur_time(),out)
        self.my_function('服务器拉取:{}'.format(out))
        self.signal_send_SuperText_com6.emit('服务器拉取:{}'.format(out))
        return out

    def dumpLightResult(self,pResult, huks):
        datas = []
        i = 0
        while (pResult):  # loop to read all kps
            kr_data = b64decode(pResult.contents.kr_data)
            data_str = ""
            for j in range(0, len(kr_data)):
                data_str += "%02X" % kr_data[j]
            datas.append({"cid": pResult.contents.pCid.decode("utf-8"), "huk": huks[i].decode("utf-8"), "kr": data_str})

            pResult = pResult.contents.pNext
            i += 1
        out = {"ret": 0, "results": datas}
        print(out)
        return out

    def get_cur_time(self):
        dt = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f]')
        return dt

    # def crc_kr(self, kr):
    #     crc16 = crcmod.mkCrcFun(0x11021, rev=False, initCrc=0x0000, xorOut=0x0000)
    #     kr = bytes.fromhex(kr)
    #     checksum = crc16(kr)
    #     checksum_hex = hex(checksum)  # 算出crc
    #
    #     Crc_kr = checksum_hex[2:]  # 去除前缀 '0x'
    #     Crc_kr = Crc_kr.zfill(len(Crc_kr) + len(Crc_kr) % 2)  # 使用 0 填充到偶数长度
    #     # 确保字符串只包含有效的十六进制字符（0-9，A-F，a-f）
    #     valid_chars = set('0123456789abcdefABCDEF')
    #     Crc_kr = ''.join(filter(lambda x: x in valid_chars, Crc_kr))
    #     Crc_kr = bytes.fromhex(Crc_kr)  ######
    #
    #     # print(Crc_kr)
    #     return Crc_kr

    def crc16_kr(self,kr):
        crc16 = crcmod.mkCrcFun(0x11021, rev=False, initCrc=0x0000, xorOut=0x0000)
        kr_bytes = bytes.fromhex(kr)
        checksum = crc16(kr_bytes)
        print(checksum)
        # 直接将整数转换为长度为 2 的字节串
        Crc_kr = checksum.to_bytes(2, byteorder='big')
        print(Crc_kr)
        return Crc_kr

    def get_folder_size(self,folder_path):
        total_size = 0
        # 遍历文件夹内的所有文件和子文件夹
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                # 获取文件路径
                file_path = os.path.join(dirpath, filename)
                # 累加文件大小
                total_size += os.path.getsize(file_path)
                # 如果文件大小达到指定大小，则删除文件
        try:
            if total_size >= 500000000:  # 500MB
                shutil.rmtree(folder_path)
                print("文件夹删除成功")
                self.my_function("文件夹删除成功")
                os.mkdir('./log')
        except Exception as e:
            print(f"文件夹删除失败: {e}")
            self.my_function("文件夹删除失败")
        return total_size

    def burn_result(self):
        return self.result