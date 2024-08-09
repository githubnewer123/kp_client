from UI.product_main import Ui_ProductMainWindow
from PyQt5 import QtWidgets
import sys,cgitb,logging
from mes.mes import Mes
from view.mes_login_view import MesLoginView
from view.tqc_order_view  import OrderView
from view.tqc_main_controller import CheckView
from manager.window_manager import WindowsManager
from view.auto_update_view import AutoUpdateView



class ProductMainView(Ui_ProductMainWindow):

    def __init__(self):
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

        self.mes = Mes()

        self.login_view = MesLoginView(self.mes)
        self.login_view.show()
        self.login_view.exec()

        self.order_view = OrderView(self.mes)
        self.order_view.show()
        self.order_view.exec()

        self.order_view = CheckView(self.mes,self.mes.getActiveOrder(),self.order_view.orderinfo)
        self.order_view.show()
        self.order_view.exec()




