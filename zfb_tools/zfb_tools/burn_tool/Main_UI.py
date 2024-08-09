# coding: utf-8
import sys,threading, time,os,configparser
from burn_tool.kp_send_recive.KP_send_receive import Kp_send
from burn_tool.kp_send_recive.KP_send_receive_com2 import Kp_send_com2
from burn_tool.kp_send_recive.KP_send_receive_com3 import Kp_send_com3
from burn_tool.kp_send_recive.KP_send_receive_com4 import Kp_send_com4
from burn_tool.kp_send_recive.KP_send_receive_com5 import Kp_send_com5
from burn_tool.kp_send_recive.KP_send_receive_com6 import Kp_send_com6

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
import serial.tools.list_ports
from burn_tool.kp_zfb.demo_get_available_device_count import csi_kp_get_available_device_count
from burn_tool.kp_zfb.KrBurn_Dialog import Ui_Dialog
import common.utils as Utils

class Main_ui(Ui_Dialog,QDialog):
    # 创建一个信号，用于在完成工作时发出通知
    signal_show_message = pyqtSignal(str)
    combobox_add = pyqtSignal(list)

    def __init__(self,mes,cfg,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # self.setWindowTitle("CMBT-V1.7.0")
        self.setWindowTitle("芯片烧入工具")
        # 设置界面颜色为浅灰色背景，深蓝色文本
        self.setStyleSheet("background-color: #7EA8B0;")
        # app = QtWidgets.QApplication(sys.argv)
        # Window = QtWidgets.QMainWindow()  # 注意窗口类型
        # super().setupUi(Window)
        # # Window.setFixedSize(Window.width(), Window.height())#禁止放大
        # 设置窗口图标
        # icon = QIcon(r".\c.png")  # 图片标题
        # self.setWindowIcon(icon)

        self.mes = mes
        self.cfg = cfg
        self.order = self.mes.getActiveOrder()
        self.Init()  # 初始化一些变量和订单信息
        self.revise()  # 界面优化
        self.SuperText_init()  # 超级文本初始化
        self.txt_version()  # 软件版本说明

        self.detect_thread = threading.Thread(target=self.device_loop, args=())
        self.detect_thread.setDaemon(True)
        self.detect_thread.start()

        self.comboBox_currentText()  # 下拉列表点击获取串口
        self.connect_signals()  # 连接信号

    def device_loop(self):
        self.com_list1 = self.getAtPortList1()  # 获得com列表
        self.combobox_add.emit(self.com_list1)
        while True:
            new_port = self.getAtPortList1()  # 获得com列表

            if new_port == self.com_list1:
                time.sleep(.5)
                continue
            if len(new_port) != len(self.com_list1):
                self.com_list1 = new_port
                self.combobox_add.emit(self.com_list1)

    def combobox(self,com_list1):
        current_selection = self.comboBox.currentText()
        current_selection2 = self.comboBox_2.currentText()
        current_selection3 = self.comboBox_3.currentText()
        current_selection4 = self.comboBox_4.currentText()
        current_selection5 = self.comboBox_5.currentText()
        current_selection6 = self.comboBox_6.currentText()

        comboBoxes = [self.comboBox, self.comboBox_2, self.comboBox_3, self.comboBox_4, self.comboBox_5, self.comboBox_6]
        for comboBox in comboBoxes:
            comboBox.clear()  # 清空现有的选项
        # 每个 QComboBox 添加项
        for item in com_list1:
            for comboBox in comboBoxes:
                comboBox.addItem(item)

        # self.comboBox.addItem("/dev/ttyACM12")
        def set_current_text_if_in_list(comboBox, current, com_list):
            if current and current in com_list:
                comboBox.setCurrentText(current)
            else:
                comboBox.setCurrentIndex(0)
        set_current_text_if_in_list(self.comboBox, current_selection, self.com_list1)
        set_current_text_if_in_list(self.comboBox_2, current_selection2, self.com_list1)
        set_current_text_if_in_list(self.comboBox_3, current_selection3, self.com_list1)
        set_current_text_if_in_list(self.comboBox_4, current_selection4, self.com_list1)
        set_current_text_if_in_list(self.comboBox_5, current_selection5, self.com_list1)
        set_current_text_if_in_list(self.comboBox_6, current_selection6, self.com_list1)

    def getAtPortList1(self, filter="USB"):
        list_com = []
        list1 = list(serial.tools.list_ports.comports())
        for port in list1:
            if filter in port[1]:
                list_com.append(port[0])
        return list_com

    def Init(self):
        self.freq_com1 = 0
        self.freq_com2 = 0
        self.freq_com3 = 0
        self.freq_com4 = 0
        self.freq_com5 = 0
        self.freq_com6 = 0
        self.total_time = 0  # 初始化总次数为0
        self.cos_fail_time = 0
        self.kr_fail_time = 0
        self.pass_time = 0
        self.index = 0  # 初始化页面ID
        self.com_opening = []

        self.kp_send = Kp_send()  # 实例化这个类
        self.kp_send_com2 = Kp_send_com2()  # 实例化这个类
        self.kp_send_com3 = Kp_send_com3()
        self.kp_send_com4 = Kp_send_com4()
        self.kp_send_com5 = Kp_send_com5()
        self.kp_send_com6 = Kp_send_com6()

        self.kp_send.dev = None
        self.kp_send_com2.dev = None
        self.kp_send_com3.dev = None
        self.kp_send_com4.dev = None
        self.kp_send_com5.dev = None
        self.kp_send_com6.dev = None

        #显示订单信息
        self.label_4.setText(Utils.getAppVersion())
        self.label_54.setText(self.order.order_id)
        self.label_56.setText(self.order.project_name)
        self.label_58.setText(self.order.material_id)
        self.label_60.setText(self.order.erp_material_id)
        self.label_62.setText(str(self.order.getProductTotal()))
        self.label_64.setText(self.order.project_version)

    def connect_signals(self):
        self.combobox_add.connect(self.combobox)
        self.pushButton.clicked.connect(self.Thread_start)  # 链接线程1
        self.pushButton_7.clicked.connect(self.Thread_start2)  # 链接线程2
        self.pushButton_9.clicked.connect(self.Thread_start3)  # 链接线程3
        self.pushButton_11.clicked.connect(self.Thread_start4)  # 链接线程4
        self.pushButton_13.clicked.connect(self.Thread_start5)  # 链接线程3
        self.pushButton_15.clicked.connect(self.Thread_start6)  # 链接线程4

        self.pushButton_3.clicked.connect(self.get_serial_info)  # 串口列表刷新
        self.pushButton_2.clicked.connect(self.com_close1)  # 关闭串口位置1
        self.pushButton_8.clicked.connect(self.com_close2)  # 关闭串口位置2
        self.pushButton_10.clicked.connect(self.com_close3)  # 关闭串口位置3
        self.pushButton_12.clicked.connect(self.com_close4)  # 关闭串口位置4
        self.pushButton_14.clicked.connect(self.com_close5)  # 关闭串口位置5
        self.pushButton_16.clicked.connect(self.com_close6)  # 关闭串口位置6

        self.pushButton_5.clicked.connect(self.clear_text)  # 清除文本信息
        self.pushButton_6.clicked.connect(self.Available_count_thread)  # 刷新可用数量显示
        self.signal_show_message.connect(self.msgBox)
        # self.pushButton_2.clicked.connect(self.page_QDialog) #子页面显示
        self.tabWidget.currentChanged.connect(self.tab_changed)  # 连接 currentChanged 信号到槽函数 tab_changed
        self.kp_send.signal_send_connect_messagebox_com1.connect(self.msgBox)
        self.kp_send_com2.signal_send_connect_messagebox_com2.connect(self.msgBox)
        self.kp_send_com3.signal_send_connect_messagebox_com3.connect(self.msgBox)
        self.kp_send_com4.signal_send_connect_messagebox_com4.connect(self.msgBox)
        self.kp_send_com5.signal_send_connect_messagebox_com5.connect(self.msgBox)
        self.kp_send_com6.signal_send_connect_messagebox_com6.connect(self.msgBox)

        self.kp_send.signal_send_connect_com1.connect(self.signalEmit_show_connect_com1)  # 连接信号槽函数显示
        self.kp_send.signal_send_SuperText_com1.connect(self.signalEmit_show_SuperText_com1)  # 超级文本显示
        self.kp_send.signal_send_pass_fail_com1.connect(self.signalEmit_show_pass_fail_com1)  # 判断pass fail
        self.kp_send.signal_send_freq_com1.connect(self.signalEmit_show_freq_com1)  # 拉取次数
        self.kp_send.signal_send_pass_freq_com1.connect(self.signalEmit_show_pass_freq_com1)  # 成功次数
        self.kp_send.signal_send_cos_fail_freq_com1.connect(self.signalEmit_show_cos_fail_freq_com1)  # cos失败次数
        self.kp_send.signal_send_kr_fail_freq_com1.connect(self.signalEmit_show_kr_fail_freq_com1)  # kr失败次数

        self.kp_send_com2.signal_send_connect_com2.connect(self.signalEmit_show_connect_com2)  # 连接信号槽函数显示
        self.kp_send_com2.signal_send_SuperText_com2.connect(self.signalEmit_show_SuperText_com2)  # 超级文本显示
        self.kp_send_com2.signal_send_pass_fail_com2.connect(self.signalEmit_show_pass_fail_com2)  # 判断pass fail
        self.kp_send_com2.signal_send_freq_com2.connect(self.signalEmit_show_freq_com2)  # 拉取次数
        self.kp_send_com2.signal_send_pass_freq_com2.connect(self.signalEmit_show_pass_freq_com2)  # 成功次数
        self.kp_send_com2.signal_send_cos_fail_freq_com2.connect(self.signalEmit_show_cos_fail_freq_com2)  # cos失败次数
        self.kp_send_com2.signal_send_kr_fail_freq_com2.connect(self.signalEmit_show_kr_fail_freq_com2)  # kr失败次数
        #
        self.kp_send_com3.signal_send_connect_com3.connect(self.signalEmit_show_connect_com3)  # 连接信号槽函数显示
        self.kp_send_com3.signal_send_SuperText_com3.connect(self.signalEmit_show_SuperText_com3)  # 超级文本显示
        self.kp_send_com3.signal_send_pass_fail_com3.connect(self.signalEmit_show_pass_fail_com3)  # 判断pass fail
        self.kp_send_com3.signal_send_freq_com3.connect(self.signalEmit_show_freq_com3)  # 拉取次数
        self.kp_send_com3.signal_send_pass_freq_com3.connect(self.signalEmit_show_pass_freq_com3)  # 成功次数
        self.kp_send_com3.signal_send_cos_fail_freq_com3.connect(self.signalEmit_show_cos_fail_freq_com3)  # cos失败次数
        self.kp_send_com3.signal_send_kr_fail_freq_com3.connect(self.signalEmit_show_kr_fail_freq_com3)  # kr失败次数
        #
        self.kp_send_com4.signal_send_connect_com4.connect(self.signalEmit_show_connect_com4)  # 连接信号槽函数显示
        self.kp_send_com4.signal_send_SuperText_com4.connect(self.signalEmit_show_SuperText_com4)  # 超级文本显示
        self.kp_send_com4.signal_send_pass_fail_com4.connect(self.signalEmit_show_pass_fail_com4)  # 判断pass fail
        self.kp_send_com4.signal_send_freq_com4.connect(self.signalEmit_show_freq_com4)  # 拉取次数
        self.kp_send_com4.signal_send_pass_freq_com4.connect(self.signalEmit_show_pass_freq_com4)  # 成功次数
        self.kp_send_com4.signal_send_cos_fail_freq_com4.connect(self.signalEmit_show_cos_fail_freq_com4)  # cos失败次数
        self.kp_send_com4.signal_send_kr_fail_freq_com4.connect(self.signalEmit_show_kr_fail_freq_com4)  # kr失败次数

        self.kp_send_com5.signal_send_connect_com5.connect(self.signalEmit_show_connect_com5)  # 连接信号槽函数显示
        self.kp_send_com5.signal_send_SuperText_com5.connect(self.signalEmit_show_SuperText_com5)  # 超级文本显示
        self.kp_send_com5.signal_send_pass_fail_com5.connect(self.signalEmit_show_pass_fail_com5)  # 判断pass fail
        self.kp_send_com5.signal_send_freq_com5.connect(self.signalEmit_show_freq_com5)  # 拉取次数
        self.kp_send_com5.signal_send_pass_freq_com5.connect(self.signalEmit_show_pass_freq_com5)  # 成功次数
        self.kp_send_com5.signal_send_cos_fail_freq_com5.connect(self.signalEmit_show_cos_fail_freq_com5)  # cos失败次数
        self.kp_send_com5.signal_send_kr_fail_freq_com5.connect(self.signalEmit_show_kr_fail_freq_com5)  # kr失败次数

        self.kp_send_com6.signal_send_connect_com6.connect(self.signalEmit_show_connect_com6)  # 连接信号槽函数显示
        self.kp_send_com6.signal_send_SuperText_com6.connect(self.signalEmit_show_SuperText_com6)  # 超级文本显示
        self.kp_send_com6.signal_send_pass_fail_com6.connect(self.signalEmit_show_pass_fail_com6)  # 判断pass fail
        self.kp_send_com6.signal_send_freq_com6.connect(self.signalEmit_show_freq_com6)  # 拉取次数
        self.kp_send_com6.signal_send_pass_freq_com6.connect(self.signalEmit_show_pass_freq_com6)  # 成功次数
        self.kp_send_com6.signal_send_cos_fail_freq_com6.connect(self.signalEmit_show_cos_fail_freq_com6)  # cos失败次数
        self.kp_send_com6.signal_send_kr_fail_freq_com6.connect(self.signalEmit_show_kr_fail_freq_com6)  # kr失败次数

    def Thread_start(self):
        try:
            if self.kp_send.dev is None or not self.kp_send.dev.is_open:
                self.kp_send._stop_event.clear()  # 重置停止事件的状态为未设置
                self.thread1 = threading.Thread(target=self.kp_send.Start_send, args=(self.mes,self.cfg))# 线程1 执行KP拉取
                self.textEdit.append('尝试连接：{}'.format(self.kp_send.port))
                self.thread1.daemon = True
                self.thread1.start()
            else:
                raise Exception("串口已打开")
        except Exception as e:
            QMessageBox.warning(self, 'tips!', str(e), QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)

    def Thread_start2(self):
        try:
            if self.kp_send_com2.dev is None or not self.kp_send_com2.dev.is_open:
                self.kp_send_com2._stop_event.clear()  # 重置停止事件的状态为未设置
                self.thread2 = threading.Thread(target=self.kp_send_com2.Start_send, args=(self.mes,self.cfg))# 线程2 执行KP拉取
                self.textEdit_2.append('尝试连接：{}'.format(self.kp_send_com2.port))
                self.thread2.daemon = True
                self.thread2.start()
            else:
                raise Exception("串口已打开")
        except Exception as e:
            QMessageBox.warning(self, 'tips!', str(e), QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)

    def Thread_start3(self):
        try:
            if self.kp_send_com3.dev is None or not self.kp_send_com3.dev.is_open:
                self.kp_send_com3._stop_event.clear()  # 重置停止事件的状态为未设置
                self.thread3 = threading.Thread(target=self.kp_send_com3.Start_send, args=(self.mes,self.cfg))# 线程3 执行KP拉取
                self.textEdit_3.append('尝试连接：{}'.format(self.kp_send_com3.port))
                self.thread3.daemon = True
                self.thread3.start()
            else:
                raise Exception("串口已打开")
        except Exception as e:
            QMessageBox.warning(self, 'tips!', str(e), QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)

    def Thread_start4(self):
        try:
            if self.kp_send_com4.dev is None or not self.kp_send_com4.dev.is_open:
                self.kp_send_com4._stop_event.clear()  # 重置停止事件的状态为未设置
                self.thread4 = threading.Thread(target=self.kp_send_com4.Start_send, args=(self.mes,self.cfg))# 线程4 执行KP拉取
                self.textEdit_4.append('尝试连接：{}'.format(self.kp_send_com4.port))
                self.thread4.daemon = True
                self.thread4.start()
            else:
                raise Exception("串口已打开")
        except Exception as e:
            QMessageBox.warning(self, 'tips!', str(e), QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)

    def Thread_start5(self):
        try:
            if self.kp_send_com5.dev is None or not self.kp_send_com5.dev.is_open:
                self.kp_send_com5._stop_event.clear()  # 重置停止事件的状态为未设置
                self.thread5 = threading.Thread(target=self.kp_send_com5.Start_send, args=(self.mes,self.cfg))# 线程5 执行KP拉取
                self.textEdit_5.append('尝试连接：{}'.format(self.kp_send_com5.port))
                self.thread5.daemon = True
                self.thread5.start()
            else:
                raise Exception("串口已打开")
        except Exception as e:
            QMessageBox.warning(self, 'tips!', str(e), QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)

    def Thread_start6(self):
        try:
            if self.kp_send_com6.dev is None or not self.kp_send_com6.dev.is_open:
                self.kp_send_com6._stop_event.clear()  # 重置停止事件的状态为未设置
                self.thread6 = threading.Thread(target=self.kp_send_com6.Start_send, args=(self.mes,self.cfg))# 线程6 执行KP拉取
                self.textEdit_6.append('尝试连接：{}'.format(self.kp_send_com6.port))
                self.thread6.daemon = True
                self.thread6.start()
            else:
                raise Exception("串口已打开")
        except Exception as e:
            QMessageBox.warning(self, 'tips!', str(e), QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)

    def Com_choose(self):
        self.kp_send.port = self.comboBox.currentText() #获得下拉内容
        self.kp_send_com2.port = self.comboBox_2.currentText() #获得下拉内容
        self.kp_send_com3.port = self.comboBox_3.currentText() #获得下拉内容
        self.kp_send_com4.port = self.comboBox_4.currentText() #获得下拉内容
        self.kp_send_com5.port = self.comboBox_5.currentText() #获得下拉内容
        self.kp_send_com6.port = self.comboBox_6.currentText() #获得下拉内容

    def revise(self):
        if self.kp_send.license_name is not None and self.kp_send.license_name.strip() != '':
            self.label_13.setText('{}剩余数量:'.format(self.kp_send.license_name))
        else:
            self.label_13.setText('{}剩余数量:'.format(self.kp_send.pull_model))
        self.label_18.setText('已关闭')  ###串口关闭初始化
        self.label_19.setText('已关闭')  ###
        self.label_20.setText('已关闭')  ###
        self.label_21.setText('已关闭')  ###
        self.label_40.setText('已关闭')  ###
        self.label_42.setText('已关闭')  ###

        self.label_6.clear() #次数清除
        self.label_8.clear()
        self.label_10.clear()
        self.label_26.clear()
        self.label_27.clear()
        self.label_30.clear()
        self.label_33.clear()
        self.label_36.clear()
        self.label_28.clear()
        self.label_31.clear()
        self.label_34.clear()
        self.label_37.clear()
        self.label_29.clear()
        self.label_32.clear()
        self.label_35.clear()
        self.label_38.clear()
        self.label_45.clear()
        self.label_46.clear()
        self.label_47.clear()
        self.label_48.clear()
        self.label_49.clear()
        self.label_50.clear()
        self.label_51.clear()
        self.label_52.clear()

        # 使用样式表设置按钮的渐变色背景
        self.pushButton.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色
        self.pushButton_2.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色
        self.pushButton_3.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色
        self.pushButton_5.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色
        self.pushButton_6.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色
        self.pushButton_7.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色
        self.pushButton_8.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色
        self.pushButton_9.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色
        self.pushButton_10.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色
        self.pushButton_11.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色
        self.pushButton_12.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色
        self.pushButton_13.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色
        self.pushButton_14.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色
        self.pushButton_15.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色
        self.pushButton_16.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FFFFFF, stop:1 #ADD8E6);")  # 设置渐变色

    def signalEmit_show_connect_com1(self,connect):
        self.label_18.show()
        if connect == "已关闭":
            self.label_18.setStyleSheet("color: rgb(0, 0, 0)")
        else:
            self.label_18.setStyleSheet("color: rgb(0, 255, 0)")
        self.label_18.setText(connect)  # 文本显示已关闭

    def signalEmit_show_connect_com2(self,connect):
        self.label_19.show()
        if connect == "已关闭":
            self.label_19.setStyleSheet("color: rgb(0, 0, 0)")
        else:
            self.label_19.setStyleSheet("color: rgb(0, 255, 0)")
        self.label_19.setText(connect) #文本显示已连接

    def signalEmit_show_connect_com3(self,connect):
        self.label_20.show()
        if connect == "已关闭":
            self.label_20.setStyleSheet("color: rgb(0, 0, 0)")
        else:
            self.label_20.setStyleSheet("color: rgb(0, 255, 0)")
        self.label_20.setText(connect) #文本显示已连接

    def signalEmit_show_connect_com4(self,connect):
        self.label_21.show()
        if connect == "已关闭":
            self.label_21.setStyleSheet("color: rgb(0, 0, 0)")
        else:
            self.label_21.setStyleSheet("color: rgb(0, 255, 0)")
        self.label_21.setText(connect) #文本显示已连接

    def signalEmit_show_connect_com5(self,connect):
        self.label_40.show()
        if connect == "已关闭":
            self.label_40.setStyleSheet("color: rgb(0, 0, 0)")
        else:
            self.label_40.setStyleSheet("color: rgb(0, 255, 0)")
        self.label_40.setText(connect) #文本显示已连接

    def signalEmit_show_connect_com6(self,connect):
        self.label_42.show()
        if connect == "已关闭":
            self.label_42.setStyleSheet("color: rgb(0, 0, 0)")
        else:
            self.label_42.setStyleSheet("color: rgb(0, 255, 0)")
        self.label_42.setText(connect) #文本显示已连接

    def signalEmit_show_freq_com1(self,freq):
        self.label_6.show()
        self.label_6.setText(str(freq)) #文本显示次数

    def signalEmit_show_pass_freq_com1(self,freq):
        self.label_8.show()
        self.label_8.setText(str(freq)) #文本显示成功的次数

    def signalEmit_show_cos_fail_freq_com1(self,freq):
        self.label_10.show()
        self.label_10.setText(str(freq)) #文本显示失败的次数
        self.label_10.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_kr_fail_freq_com1(self,freq):
        self.label_26.show()
        self.label_26.setText(str(freq)) #文本显示失败的次数
        self.label_26.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_freq_com2(self,freq):
        self.label_27.show()
        self.label_27.setText(str(freq)) #文本显示次数

    def signalEmit_show_pass_freq_com2(self,freq):
        self.label_30.show()
        self.label_30.setText(str(freq)) #文本显示成功的次数

    def signalEmit_show_cos_fail_freq_com2(self,freq):
        self.label_33.show()
        self.label_33.setText(str(freq)) #文本显示失败的次数
        self.label_33.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_kr_fail_freq_com2(self,freq):
        self.label_36.show()
        self.label_36.setText(str(freq))  # 文本显示失败的次数
        self.label_36.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_freq_com3(self,freq):
        self.label_28.show()
        self.label_28.setText(str(freq)) #文本显示次数

    def signalEmit_show_pass_freq_com3(self,freq):
        self.label_31.show()
        self.label_31.setText(str(freq)) #文本显示成功的次数

    def signalEmit_show_cos_fail_freq_com3(self,freq):
        self.label_34.show()
        self.label_34.setText(str(freq)) #文本显示失败的次数
        self.label_34.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_kr_fail_freq_com3(self,freq):
        self.label_37.show()
        self.label_37.setText(str(freq))  # 文本显示失败的次数
        self.label_37.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_freq_com4(self,freq):
        self.label_29.show()
        self.label_29.setText(str(freq)) #文本显示次数

    def signalEmit_show_pass_freq_com4(self,freq):
        self.label_32.show()
        self.label_32.setText(str(freq)) #文本显示成功的次数

    def signalEmit_show_cos_fail_freq_com4(self,freq):
        self.label_35.show()
        self.label_35.setText(str(freq)) #文本显示失败的次数
        self.label_35.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_kr_fail_freq_com4(self,freq):
        self.label_38.show()
        self.label_38.setText(str(freq))  # 文本显示失败的次数
        self.label_38.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_freq_com5(self,freq):
        self.label_45.show()
        self.label_45.setText(str(freq)) #文本显示次数

    def signalEmit_show_pass_freq_com5(self,freq):
        self.label_49.show()
        self.label_49.setText(str(freq)) #文本显示成功的次数

    def signalEmit_show_cos_fail_freq_com5(self,freq):
        self.label_48.show()
        self.label_48.setText(str(freq)) #文本显示失败的次数
        self.label_48.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_kr_fail_freq_com5(self,freq):
        self.label_52.show()
        self.label_52.setText(str(freq))  # 文本显示失败的次数
        self.label_52.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_freq_com6(self,freq):
        self.label_46.show()
        self.label_46.setText(str(freq)) #文本显示次数

    def signalEmit_show_pass_freq_com6(self,freq):
        self.label_50.show()
        self.label_50.setText(str(freq)) #文本显示成功的次数

    def signalEmit_show_cos_fail_freq_com6(self,freq):
        self.label_47.show()
        self.label_47.setText(str(freq)) #文本显示失败的次数
        self.label_47.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_kr_fail_freq_com6(self,freq):
        self.label_51.show()
        self.label_51.setText(str(freq))  # 文本显示失败的次数
        self.label_51.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_SuperText_com1(self,text):
        self.textEdit.append(text) #添加超级文本

    def signalEmit_show_SuperText_com2(self,text):
        self.textEdit_2.append(text) #添加超级文本

    def signalEmit_show_SuperText_com3(self,text):
        self.textEdit_3.append(text) #添加超级文本

    def signalEmit_show_SuperText_com4(self,text):
        self.textEdit_4.append(text) #添加超级文本

    def signalEmit_show_SuperText_com5(self,text):
        self.textEdit_5.append(text) #添加超级文本

    def signalEmit_show_SuperText_com6(self,text):
        self.textEdit_6.append(text) #添加超级文本

    def signalEmit_show_Progress(self,progress):
        self.progressBar.setProperty("value", progress) #进度条显示

    def signalEmit_show_pass_fail_com1(self,PASS):
        self.label_2.show()
        self.label_2.setText(PASS)
        if PASS == 'PASS':
            self.label_2.setStyleSheet("color: rgb(0, 255, 0)")
        else:
            self.label_2.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_pass_fail_com2(self,PASS):
        self.label_22.show()
        self.label_22.setText(PASS)
        if PASS == 'PASS':
            self.label_22.setStyleSheet("color: rgb(0, 255, 0)")
        else:
            self.label_22.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_pass_fail_com3(self,PASS):
        self.label_23.show()
        self.label_23.setText(PASS)
        if PASS == 'PASS':
            self.label_23.setStyleSheet("color: rgb(0, 255, 0)")
        else:
            self.label_23.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_pass_fail_com4(self,PASS):
        self.label_24.show()
        self.label_24.setText(PASS)
        if PASS == 'PASS':
            self.label_24.setStyleSheet("color: rgb(0, 255, 0)")
        else:
            self.label_24.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_pass_fail_com5(self,PASS):
        self.label_43.show()
        self.label_43.setText(PASS)
        if PASS == 'PASS':
            self.label_43.setStyleSheet("color: rgb(0, 255, 0)")
        else:
            self.label_43.setStyleSheet("color: rgb(255, 0, 0)")

    def signalEmit_show_pass_fail_com6(self,PASS):
        self.label_44.show()
        self.label_44.setText(PASS)
        if PASS == 'PASS':
            self.label_44.setStyleSheet("color: rgb(0, 255, 0)")
        else:
            self.label_44.setStyleSheet("color: rgb(255, 0, 0)")

    # def gettext_freq(self,get_freq):
        # if get_freq.isnumeric():
            # self.progressBar.setMinimum(0)  ###初始化进度条
            # self.progressBar.setProperty("value", 0)  ###
            # self.progressBar.setMaximum(int(get_freq))  ###
            # print('设置的拉取次数为：{}'.format(get_freq))
            # self.textEdit.append('设置的拉取次数为：{}'.format(get_freq))
        # else:
        #     print('请配置pull_freq为数字,默认为100')
        #     self.textEdit.append('请配置pull_freq为数字,默认为100')

    def Available_count_thread(self):
        self.count_thread = threading.Thread(target=self.Available_device_count_flushed)  # 线程5 查询license可用数量
        self.count_thread.daemon = True
        self.count_thread.start()

    def Available_device_count_flushed(self):#############服务器剩余次数刷新显示
        try:
            available_device_count = csi_kp_get_available_device_count()
            print(available_device_count)
            if available_device_count == None or available_device_count < 0:
                print("网络")
                raise Exception("检查网络或依赖文件是否出错！")
            else:
                self.label_15.setText(str(available_device_count))
                self.kp_send.my_function("刷新剩余数量：{}".format(str(available_device_count)))
        except Exception as e:
            self.signal_show_message.emit(str(e))

    #打开子页面
    # def page_QDialog(self):
    #     UrcInfo = UrcInfoDialog()
    #     UrcInfo.exec_()

    # def start_test(self):
    #     self.msgBox('未选择文件')

    def msgBox(self, info):
        res = QMessageBox.warning(self, "提示窗口", info, QMessageBox.Yes)
        # return True if (QMessageBox.Yes == res) else False

    def get_serial_info(self):  # 获取可用串口列表
        current_selection = self.comboBox.currentText()
        current_selection2 = self.comboBox_2.currentText()
        current_selection3 = self.comboBox_3.currentText()
        current_selection4 = self.comboBox_4.currentText()
        current_selection5 = self.comboBox_5.currentText()
        current_selection6 = self.comboBox_6.currentText()
        comboBoxes = [self.comboBox, self.comboBox_2, self.comboBox_3, self.comboBox_4, self.comboBox_5, self.comboBox_6]
        for comboBox in comboBoxes:
            comboBox.clear()  # 清空现有的选项

        # 打印可用串口列表
        self.com_list = []
        self.plist = list(serial.tools.list_ports.comports())
        if len(self.plist) <= 0:
            print('未找到串口')
            qm = QMessageBox.warning(self, '提示窗口', '未找到串口!请检查接线和电脑接口。',
                                     QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
            if qm == QMessageBox.Yes:
                print('Yes')
            else:
                print('No')
        else:
            for i in list(self.plist):
                self.comboBox.addItem(i.device)
                self.comboBox_2.addItem(i.device)
                self.comboBox_3.addItem(i.device)
                self.comboBox_4.addItem(i.device)
                self.comboBox_5.addItem(i.device)
                self.comboBox_6.addItem(i.device)
                self.com_list.append(i.device)
                # print(self.com_list)
            if self.index == 0:
                self.textEdit.append('串口列表：{}'.format(self.com_list))  # 打印串口列表
            elif self.index == 1:
                self.textEdit_2.append('串口列表：{}'.format(self.com_list))  # 打印串口列表
            elif self.index == 2:
                self.textEdit_3.append('串口列表：{}'.format(self.com_list))  # 打印串口列表
            elif self.index == 3:
                self.textEdit_4.append('串口列表：{}'.format(self.com_list))  # 打印串口列表
            elif self.index == 4:
                self.textEdit_5.append('串口列表：{}'.format(self.com_list))  # 打印串口列表
            elif self.index == 5:
                self.textEdit_6.append('串口列表：{}'.format(self.com_list))  # 打印串口列表

        def set_current_text_if_in_list(comboBox, current, com_list):
            if current and current in com_list:
                comboBox.setCurrentText(current)
            else:
                comboBox.setCurrentIndex(0)
        set_current_text_if_in_list(self.comboBox, current_selection, self.com_list)
        set_current_text_if_in_list(self.comboBox_2, current_selection2, self.com_list)
        set_current_text_if_in_list(self.comboBox_3, current_selection3, self.com_list)
        set_current_text_if_in_list(self.comboBox_4, current_selection4, self.com_list)
        set_current_text_if_in_list(self.comboBox_5, current_selection5, self.com_list)
        set_current_text_if_in_list(self.comboBox_6, current_selection6, self.com_list)


    def comboBox_currentText(self):
            self.Com_choose()#选择第一项com口
            self.comboBox.currentIndexChanged.connect(self.Com_choose)  # 链接槽，选择com口
            self.comboBox_2.currentIndexChanged.connect(self.Com_choose)
            self.comboBox_3.currentIndexChanged.connect(self.Com_choose)
            self.comboBox_4.currentIndexChanged.connect(self.Com_choose)
            self.comboBox_5.currentIndexChanged.connect(self.Com_choose)
            self.comboBox_6.currentIndexChanged.connect(self.Com_choose)


            # print(self.kp_send.get_cur_time(), '当前串口：', self.kp_send.port)
            # self.kp_send.my_function('当前串口：{}'.format(self.kp_send.port))
            # self.textEdit.append('当前串口：{}'.format(self.kp_send.port)) #添加超级文本
            # self.textEdit_2.append('当前串口：{}'.format(self.kp_send.port)) #添加超级文本
            # self.textEdit_3.append('当前串口：{}'.format(self.kp_send.port)) #添加超级文本
            # self.textEdit_4.append('当前串口：{}'.format(self.kp_send.port)) #添加超级文本

    def com_close1(self):
        try:
            if self.kp_send.dev == None or not self.kp_send.dev.is_open:
                raise Exception("串口已关闭")
            self.kp_send.stop()
            self.kp_send.dev.close()  # 关闭串口
            # self.kp_send.dev = None  # 关闭串口
            # 创建一个新的QFont对象，并设置字体加粗

            self.label_18.setText('已关闭')
            self.label_18.setStyleSheet("color: rgb(0, 0, 0)")
            self.textEdit.append('串口已关闭，当前串口为：{}'.format(self.kp_send.port))  # 添加超级文本
            self.label_6.clear()
            self.label_8.clear()
            self.label_10.clear()
            self.label_26.clear()
            # self.label_2.clear()

        except Exception as e:
            QMessageBox.warning(self, 'tips!', str(e), QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
            print('异常：', e)

    def com_close2(self):
        try:
            if self.kp_send_com2.dev == None or not self.kp_send_com2.dev.is_open:
                raise Exception("串口已关闭")
            self.kp_send_com2.stop()
            self.kp_send_com2.dev.close()  # 关闭串口
            # self.kp_send_com2.dev = None  # 关闭串口
            self.label_19.setText('已关闭')
            self.label_19.setStyleSheet("color: rgb(0, 0, 0)")
            self.textEdit_2.append('串口已关闭，当前串口为：{}'.format(self.kp_send_com2.port))  # 添加超级文本
            self.label_27.clear()
            self.label_30.clear()
            self.label_33.clear()
            self.label_36.clear()
            # self.label_22.clear()

        except Exception as e:
            QMessageBox.warning(self, 'tips!', str(e), QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
            print('异常：', e)

    def com_close3(self):
        try:
            if self.kp_send_com3.dev == None or not self.kp_send_com3.dev.is_open:
                raise Exception("串口已关闭")
            self.kp_send_com3.stop()
            self.kp_send_com3.dev.close()  # 关闭串口
            # self.kp_send_com3.dev = None  # 关闭串口
            self.label_20.setText('已关闭')
            self.label_20.setStyleSheet("color: rgb(0, 0, 0)")
            self.textEdit_3.append('串口已关闭，当前串口为：{}'.format(self.kp_send_com3.port))  # 添加超级文本
            self.label_28.clear()
            self.label_31.clear()
            self.label_34.clear()
            self.label_37.clear()
            # self.label_23.clear()

        except Exception as e:
            QMessageBox.warning(self, 'tips!', str(e), QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
            print('异常：', e)

    def com_close4(self):
        try:
            if self.kp_send_com4.dev == None or not self.kp_send_com4.dev.is_open:
                raise Exception("串口已关闭")
            self.kp_send_com4.stop()
            self.kp_send_com4.dev.close()  # 关闭串口
            # self.kp_send_com4.dev = None  # 关闭串口
            self.label_21.setText('已关闭')
            self.label_21.setStyleSheet("color: rgb(0, 0, 0)")
            self.textEdit_4.append('串口已关闭，当前串口为：{}'.format(self.kp_send_com4.port))  # 添加超级文本
            self.label_29.clear()
            self.label_32.clear()
            self.label_35.clear()
            self.label_38.clear()
            # self.label_24.clear()

        except Exception as e:
            QMessageBox.warning(self, 'tips!', str(e), QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
            print('异常：', e)

    def com_close5(self):
        try:
            if self.kp_send_com5.dev == None or not self.kp_send_com5.dev.is_open:
                raise Exception("串口已关闭")
            self.kp_send_com5.stop()
            self.kp_send_com5.dev.close()  # 关闭串口
            # self.kp_send_com5.dev = None  # 关闭串口
            self.label_40.setText('已关闭')
            self.label_40.setStyleSheet("color: rgb(0, 0, 0)")
            self.textEdit_5.append('串口已关闭，当前串口为：{}'.format(self.kp_send_com5.port))  # 添加超级文本
            self.label_45.clear()
            self.label_49.clear()
            self.label_48.clear()
            self.label_52.clear()
            # self.label_43.clear()

        except Exception as e:
            QMessageBox.warning(self, 'tips!', str(e), QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
            print('异常：', e)

    def com_close6(self):
        try:
            if self.kp_send_com6.dev == None or not self.kp_send_com6.dev.is_open:
                raise Exception("串口已关闭")
            self.kp_send_com6.stop()
            self.kp_send_com6.dev.close()  # 关闭串口
            # self.kp_send_com6.dev = None  # 关闭串口
            self.label_42.setText('已关闭')
            self.label_42.setStyleSheet("color: rgb(0, 0, 0)")
            self.textEdit_6.append('串口已关闭，当前串口为：{}'.format(self.kp_send_com6.port))  # 添加超级文本
            self.label_50.clear()
            self.label_46.clear()
            self.label_47.clear()
            self.label_51.clear()
            # self.label_44.clear()

        except Exception as e:
            QMessageBox.warning(self, 'tips!', str(e), QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
            print('异常：', e)

    def clear_text(self):
        if self.index == 0:
            self.textEdit.clear()  # 清除文本信息
            self.textEdit.append('设置拉取的许可证名称为：{}'.format(self.kp_send.license_name))
            self.textEdit.append('设置产品型号：{}'.format(self.kp_send.pull_model))
            self.textEdit.append('设置芯片类型：{}'.format(self.kp_send.chip_type))
            self.textEdit.append('当前串口为：{}'.format(self.kp_send.port))
        elif self.index == 1:
            self.textEdit_2.clear()  # 清除文本信息
            self.textEdit_2.append('设置拉取的许可证名称为：{}'.format(self.kp_send.license_name))
            self.textEdit_2.append('设置产品型号：{}'.format(self.kp_send.pull_model))
            self.textEdit_2.append('设置芯片类型：{}'.format(self.kp_send.chip_type))
            self.textEdit_2.append('当前串口为：{}'.format(self.kp_send.port))
        elif self.index == 2:
            self.textEdit_3.clear()  # 清除文本信息
            self.textEdit_3.append('设置拉取的许可证名称为：{}'.format(self.kp_send.license_name))
            self.textEdit_3.append('设置产品型号：{}'.format(self.kp_send.pull_model))
            self.textEdit_3.append('设置芯片类型：{}'.format(self.kp_send.chip_type))
            self.textEdit_3.append('当前串口为：{}'.format(self.kp_send.port))
        elif self.index == 3:
            self.textEdit_4.clear()  # 清除文本信息
            self.textEdit_4.append('设置拉取的许可证名称为：{}'.format(self.kp_send.license_name))
            self.textEdit_4.append('设置产品型号：{}'.format(self.kp_send.pull_model))
            self.textEdit_4.append('设置芯片类型：{}'.format(self.kp_send.chip_type))
            self.textEdit_4.append('当前串口为：{}'.format(self.kp_send.port))
        elif self.index == 4:
            self.textEdit_5.clear()  # 清除文本信息
            self.textEdit_5.append('设置拉取的许可证名称为：{}'.format(self.kp_send.license_name))
            self.textEdit_5.append('设置产品型号：{}'.format(self.kp_send.pull_model))
            self.textEdit_5.append('设置芯片类型：{}'.format(self.kp_send.chip_type))
            self.textEdit_5.append('当前串口为：{}'.format(self.kp_send.port))
        elif self.index == 5:
            self.textEdit_6.clear()  # 清除文本信息
            self.textEdit_6.append('设置拉取的许可证名称为：{}'.format(self.kp_send.license_name))
            self.textEdit_6.append('设置产品型号：{}'.format(self.kp_send.pull_model))
            self.textEdit_6.append('设置芯片类型：{}'.format(self.kp_send.chip_type))
            self.textEdit_6.append('当前串口为：{}'.format(self.kp_send.port))

    # 槽函数，处理 Tab Widget 页变化事件
    def tab_changed(self, index):
        if index == 0:
            print("点击了第一页")
            # 执行第一页相关的操作
            self.index = 0
        elif index == 1:
            print("点击了第二页")
            # 执行第二页相关的操作
            self.index = 1
        elif index == 2:
            print("点击了第三页")
            # 执行第二页相关的操作
            self.index = 2
        elif index == 3:
            print("点击了第四页")
            # 执行第二页相关的操作
            self.index = 3
        elif index == 4:
            print("点击了第四页")
            # 执行第二页相关的操作
            self.index = 4
        elif index == 5:
            print("点击了第四页")
            # 执行第二页相关的操作
            self.index = 5

    def SuperText_init(self):
        self.textEdit.append('设置拉取的许可证名称为：{}'.format(self.kp_send.license_name))
        self.textEdit.append('设置产品型号：{}'.format(self.kp_send.pull_model))
        self.textEdit.append('设置芯片类型：{}'.format(self.kp_send.chip_type))
        self.textEdit_2.append('设置拉取的许可证名称为：{}'.format(self.kp_send_com2.license_name))
        self.textEdit_2.append('设置产品型号：{}'.format(self.kp_send_com2.pull_model))
        self.textEdit_2.append('设置芯片类型：{}'.format(self.kp_send_com2.chip_type))
        self.textEdit_3.append('设置拉取的许可证名称为：{}'.format(self.kp_send_com3.license_name))
        self.textEdit_3.append('设置产品型号：{}'.format(self.kp_send_com3.pull_model))
        self.textEdit_3.append('设置芯片类型：{}'.format(self.kp_send_com3.chip_type))
        self.textEdit_4.append('设置拉取的许可证名称为：{}'.format(self.kp_send_com4.license_name))
        self.textEdit_4.append('设置产品型号：{}'.format(self.kp_send_com4.pull_model))
        self.textEdit_4.append('设置芯片类型：{}'.format(self.kp_send_com4.chip_type))
        self.textEdit_5.append('设置拉取的许可证名称为：{}'.format(self.kp_send_com5.license_name))
        self.textEdit_5.append('设置产品型号：{}'.format(self.kp_send_com5.pull_model))
        self.textEdit_5.append('设置芯片类型：{}'.format(self.kp_send_com5.chip_type))
        self.textEdit_6.append('设置拉取的许可证名称为：{}'.format(self.kp_send_com6.license_name))
        self.textEdit_6.append('设置产品型号：{}'.format(self.kp_send_com6.pull_model))
        self.textEdit_6.append('设置芯片类型：{}'.format(self.kp_send_com6.chip_type))

    def txt_version(self):
        file_txt = '烧录软件版本说明.txt'
        with open(file_txt, 'w') as file:
            lines = ["CMBT-V1.70版本说明：\n",
                     "  1.添加了6个工位\n",
                     "  2.修改了串口读取方式，自动读取串口\n",
                     "  3.添加mes系统登录，订单选择\n",
                     "  \n",
                     "CMBT-V1.80版本说明：\n",
                     "  1.增加新mes系统登录\n",
                     "  2.log文件分开显示\n",
                     "  3.支付宝服务器地址改为深圳内网地址\n",
                     "  4.lisence和crc发送log的判断\n",
                     "  \n",
                     ]
            file.writelines(lines)

def panduan(flog = False):
    if flog == True:
        app = QApplication(sys.argv)
        main = Main_ui()
        # 设置界面颜色为浅灰色背景，深蓝色文本
        main.setStyleSheet("background-color: #7EA8B0;")
        main.switchToMainWindow()
        sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = Main_ui()
    # 设置界面颜色为浅灰色背景，深蓝色文本
    myWin.setStyleSheet("background-color: #7EA8B0;")
    myWin.show()
    sys.exit(app.exec_())

