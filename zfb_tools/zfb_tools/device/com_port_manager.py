from device.at_device import AtDevice
import threading,time
from PyQt5.QtCore import QObject,pyqtSignal

class AtPortManager(QObject):
    __pre_port_list = []
    __port_change_notify = None
    __port_detect_thread = None
    __port_detect_stop_even = None

    device_detect_signal = pyqtSignal(list)

    def _portDetectThread(self):
        while True:
            if self.stop_event.isSet():
                break

            if self.suspend_event.isSet():
                continue

            if self.at_check_en:
                if self.active_port is not None and len(AtDevice.getAtPortList(self.port_filter)) >= 2:
                    time.sleep(.1)
                    continue

                new_port = AtDevice.getAtPortListWithCheck(self.port_filter).copy()
                # if self.active_port is not None and len(new_port) > 0:
                #     time.sleep(.500)
                #     continue
                # # print(self.port_list[0], new_port[0])
                # if len(self.port_list) > 0 and self.port_list[0].__eq__(new_port):
                #     time.sleep(.500)
                #     continue

                # new_port = AtDevice.getAtPortListWithCheck(self.port_filter).copy()
            else:
                new_port = AtDevice.getAtPortList(self.port_filter).copy()
            if new_port == self.port_list:
                time.sleep(.500)
                continue

            if len(new_port) != len(self.port_list):
                self.port_list = new_port
                self.device_detect_signal.emit(self.port_list)
            for idx in range(len(new_port)):
                if new_port[idx][1] != self.port_list[idx][1]:
                    self.port_list = new_port
                    self.device_detect_signal.emit(self.port_list)

            if len(self.port_list) > 0:
                self.active_port = self.port_list[0]
            else:
                self.active_port = None
            time.sleep(.500)

    def stop(self):
        self.stop_event.set()
        self.detect_thread.join(2)

    def suspend(self):
        self.suspend_event.set()

    def resume(self):
        self.suspend_event.clear()

    def __init__(self, filter = "ASR Modem Device", at_check_en = False):
        super().__init__()
        self.at_check_en = at_check_en
        self.port_filter = filter
        self.stop_event = threading.Event()
        self.stop_event.clear()
        self.suspend_event = threading.Event()
        self.suspend_event.clear()
        self.active_port = None
        self.detect_thread = threading.Thread(target=self._portDetectThread, args=())
        if self.at_check_en:
            self.port_list = AtDevice.getAtPortListWithCheck(self.port_filter).copy()
        else:
            self.port_list = AtDevice.getAtPortList(self.port_filter).copy()
        self.detect_thread.setDaemon(True)
        self.detect_thread.start()


