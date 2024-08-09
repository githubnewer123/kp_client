# import pywinusb.hid as hid
import time
from queue import Queue,Empty
import threading
import logging,struct
from PyQt5.QtCore import QObject,pyqtSignal
    # self._recv_que.append(bytes(data))

CMD_OK = 0x9000
CMD_DAT = 0x61
CMD_RESP = 0x62
SW_CLA_NOT_SUPPORTED = 0x6E00
SW_INS_NOT_SUPPORTED    =    0x6D00
SW_INCORRECT_P1_P2      =    0x6B00
SW_INCORRECT_LENGTH     =    0x6700
SW_INCORRECT_DATA       =    0x6A80

RESP_DIRC = 0x00
RESP_PIN = 0x01
RESP_POLING = 0x02
RESP_NONE = 0x03


class UsbDevice(QObject):
    target_vendor_id = 0x4943
    usage_page = 0xffa0
    usage_id = 0x04

    device_detect_signal = pyqtSignal(object)

    def queClear(self):
        while not self._resp_que.empty():
            self._resp_que.get()
    # 检测USB 插入状态线程
    def deviceDetectThread(self):
        need_update_ui = True
        while True:
            if self.stop_detect_event.isSet():
                self.stop_detect_event.clear()
                break

            all_devices = hid.HidDeviceFilter(vendor_id=self.target_vendor_id).get_devices()
            # out_usage = hid.get_full_usage_id(self.usage_page, self.usage_id)
            # 未找到设备
            if len(all_devices) == 0:
                # 更新UI
                if self._device:
                    self._device.close()
                    self._device = None
                    logging.debug("Signal emit None")
                    if self.device_detect_signal:
                        self.device_detect_signal.emit(None)
                    self.queClear()
                    need_update_ui = True
            else:
                try:
                    if len(all_devices) > 0 :
                        # 更新找到设备的UI
                        # self._device = all_devices[0]
                        # self._device.open()
                        # self._device.set_raw_data_handler(self.raw_data_handler)
                        # for report in self._device.find_output_reports():
                        #     if out_usage in report:
                        #         self._out_report = out_usage

                        if need_update_ui:
                            need_update_ui = False
                            logging.debug("Signal emit 连接成功")
                            if self.device_detect_signal:
                                self.device_detect_signal.emit(
                                    "连接成功(%s&%s)" % (str(all_devices[0].vendor_name), str(all_devices[0].product_name)))
                            self.queClear()
                    else:
                        # 设备已经打开,不能继续查询,等设备断开后继续查询
                        self._disconEvent.wait()
                        self._disconEvent.clear()

                except Exception as e:
                    need_update_ui = True
                    logging.debug(str(e))
            time.sleep(.200)


    def __init__(self):
        super().__init__()
        self._recv_buf = b''
        self._resp_que = Queue()
        self._abort = False
        self._recv_dat = False
        self._device = None
        self._expect_len = 0
        self.stop_detect_event = threading.Event()
        self._detectProcess = threading.Thread(target=self.deviceDetectThread,args=())
        self._disconEvent = threading.Event()

    def getDeviceList(self):
        return hid.HidDeviceFilter(vendor_id=self.target_vendor_id).get_devices()

    def open(self, device):
        if self._device and self._device.is_opened():
            self._device.close()
        self._device = device
        self._device.open()
        self._recv_buf = b''
        self.queClear()
        self._expect_len = 0
        out_usage = hid.get_full_usage_id(self.usage_page, self.usage_id)
        self._device.set_raw_data_handler(self.raw_data_handler)
        for report in self._device.find_output_reports():
            if out_usage in report:
                self._out_report = out_usage
                break


    def startDeviceDetect(self):
        # self.device_detect_signal = signal
        self._detectProcess.start()

    def stopDeviceDetect(self):
        # self.device_detect_signal = signal
        self.stop_detect_event.set()
        self._detectProcess.join(5)
        self.close()

    def raw_data_handler(self,data):
        """USB HID 设备接收到信息后回调函数"""
        data = bytes(data)
        # logging.info("Recv:" + data.hex())
        if self._recv_dat:
            self._recv_buf += data[1:]
            if len(self._recv_buf) >= self._expect_len:
                self._recv_dat = False
                self._resp_que.put((CMD_DAT,self._recv_buf[:self._expect_len-2]))
                self._recv_buf = b''
            return

        # 第一个字节表面后续有数据接收
        if data[1] & 0xf0 == 0x60:
            # HAVE data
            if data[1] == CMD_DAT or data[1] == CMD_RESP:
                self._recv_dat = True
                self._expect_len = (int(data[2]<<8) + int(data[3])) + 2
                self._recv_buf += data[4:]
                if len(self._recv_buf) >= self._expect_len:
                    self._recv_dat = False
                    self._resp_que.put((CMD_DAT, self._recv_buf[:self._expect_len-2]))
                    self._recv_buf = b''
        elif data[1] &0xf0 == 0x90:
            if data[1]  == 0x90 and data[2] == 0x00:
                self._resp_que.put((CMD_OK, None))
            else:
                self._resp_que.put((SW_INCORRECT_DATA, None))

        # windows sends empty report when disconnecting
        if data.__eq__(65 * b'\x00'):
            self._disconEvent.set()

    def write(self, data, timeout=5):
        if not self._device.is_plugged():
            raise Exception("ADC: 未检测到ADC校准板")
        self.queClear()

        input = data + b'\x00' * (64 - len(data)%64)

        for idx in range(int(len(data) / 64)+1):
            buf = b'\x00'
            buf += input[idx*64:idx*64 + 64]
            # logging.info("write:" + buf.hex())
            self._device.send_output_report(buf)
        time.sleep(.10)
        return self.getResponse(timeout)


    def getResponse(self,timeout=5):
        try:
            item = self._resp_que.get(timeout=timeout)
            return item

        except Empty as e:
            # logging.debug("Get response empty")
            return (0x6d00,None)

    def isOpened(self):
        return self._device is not None and self._device.is_opened()

    def close(self):
        if self._device and  self._device.is_opened():
            self._device.close()
            self._device = None

class VoltReader():
    def __init__(self):
        self.dev = UsbDevice()

    def getVolt(self):
        self.dev.write("\x61\x22")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        # filename="MMPT\\log\\app\\%s.log"%(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')),
                        format="%(asctime)s %(name)s %(levelname)s %(message)s",
                        datefmt='%Y-%m-%d  %H:%M:%S %a')

    is_active = False
    def _portChange(info):
        print("port change: ", info)
        if info is not None:
            usb_dev.write(b"\xF0\x30\x00\x00\x00")

    usb_dev = UsbDevice()
    # usb_dev.device_detect_signal.connect(_portChange)
    # usb_dev.startDeviceDetect()
    # time.sleep(3)
    cnt = 0
    while True:
        dev_list = usb_dev.getDeviceList()
        if len(dev_list) == 0:
            time.sleep(1)
            continue

        usb_dev.open(dev_list[0])
        while True:
            ret, data = usb_dev.write(b"\xF0\x30\x00\x00\x00")
            if ret == 97:
                val = struct.unpack('<h', data[0:2])[0]

                # if data[1]&0x80 != 0:
                #     print(data)
                #     val = -(0xffff - val)

                print(cnt, val)

            time.sleep(.10)
            cnt += 1
        usb_dev.close()
        # # if is_active:
        # while not usb_dev.isOpened():
        #     time.sleep(1)
        #     print("wait dev open")
        # ret,data = usb_dev.write(b"\xF0\x30\x00\x00\x00")
        #
        # if ret == 97:
        #     val = struct.unpack('<I',data[0:4])[0]
        #     print(cnt, val)
        # time.sleep(.500)
        # cnt += 1


