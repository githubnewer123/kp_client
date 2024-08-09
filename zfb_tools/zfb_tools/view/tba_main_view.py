import os
import time
from tkinter import messagebox

import requests
from PyQt5.QtWidgets import QMessageBox

from UI.tba_main import Ui_DownloadDialog
from PyQt5 import QtWidgets

from manager.window_manager import WindowsManager
from mes.tba_tqc_tool import universalTool
from view.auto_update_view import AutoUpdateView
from view.tba_calibration_view import BurnView
from view.tba_burn_controller import DownloadView
import sys,cgitb,logging
from mes.mes import Mes
from common.utils import __TBA_VERSION__

from view.mes_login_view import MesLoginView
from view.tba_order_view import OrderView

class ProductMainView(Ui_DownloadDialog):

    def check_setting(self):
        config_set = ["link_time_out",
                      "burn_time_out",
                        "burn_success_time_out",
                        "layout",
                        "calibration",
                        "path",
                      "station",
                      "order_cache"
                    ]
        for i in config_set:
            if not universalTool().read_setting(i,"setting.json"):
                return False
        path = universalTool().read_setting("path","setting.json")
        if len(path) == 0:
            return False
        return True

    def __init__(self):
        print(__TBA_VERSION__)
        app = QtWidgets.QApplication(sys.argv)
        self.main_win = QtWidgets.QMainWindow()
        super().setupUi(self.main_win)

        self.win_manager = WindowsManager()


        self.auto_update = AutoUpdateView()
        self.auto_update.show()
        res = self.auto_update.exec()
        if res == 0:
            self.main_win.close()
            sys.exit(0)

        self.res_info_list = []

        self.mes = Mes()
        self.login_view = MesLoginView(self.mes)
        self.login_view.show()
        self.login_view.exec()

        self.order_view = OrderView(self.mes)
        self.order_view.show()
        self.order_view.exec()
        name = self.order_view.name
        res = self.check_setting()
        self.orderinfo = self.order_view.orderinfo

        # fw_name = ""
        # for x in range(int(len(name)/15)):
        #         fw_name += name[int(x*15):int((x+1)*15)]+"\n"
        # fw_name += name[int((x+1)*15):]
        if res:
            self.download_view = DownloadView(self.mes.getActiveOrder(),self.mes,name,self.orderinfo)
            self.download_view.show()
            self.download_view.exec()
            self.download_view.quit()

        # try:
        #     if self.download_view.clo:
        #         sys.exit()
        #         app.exec_()
        # except AttributeError:
        #     pass

        self.burn_view = BurnView(self.mes,name)
        self.burn_view.show()
        self.burn_view.exec()

        self.burn_view.quit()

        # if self.burn_view.clo:
        #     print(e)
        #     sys.exit()
        #     app.exec_()


        # 设置固定窗口
        self.main_win.setFixedSize(self.main_win.width(), self.main_win.height())
        self.main_win.show()
        app.exec_()
        self.download_view.quit()
        sys.exit(-1)



if __name__ == "__main__":
    cgitb.enable(format='text')
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(name)s %(levelname)s %(message)s",
                        datefmt='%Y-%m-%d  %H:%M:%S %a')
    ProductMainView()