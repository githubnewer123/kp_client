

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OrderDialog(object):
    def setupUi(self, OrderDialog):
        OrderDialog.setObjectName("OrderDialog")
        OrderDialog.resize(940, 600)

        self.centralwidget = QtWidgets.QWidget(OrderDialog)
        self.centralwidget.setObjectName("centralwidget")

        self.order_table_widget = QtWidgets.QTableWidget(OrderDialog)
        self.order_table_widget.setGeometry(QtCore.QRect(20, 20, 900, 400))
        self.order_table_widget.setAcceptDrops(True)
        self.order_table_widget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.order_table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.order_table_widget.setProperty("showDropIndicator", False)
        self.order_table_widget.setDragDropOverwriteMode(False)
        self.order_table_widget.setAlternatingRowColors(False)
        self.order_table_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.order_table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.order_table_widget.setShowGrid(False)
        self.order_table_widget.setGridStyle(QtCore.Qt.NoPen)
        self.order_table_widget.setWordWrap(False)
        self.order_table_widget.setCornerButtonEnabled(False)
        self.order_table_widget.setObjectName("order_table_widget")
        self.order_table_widget.setColumnCount(0)
        self.order_table_widget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.order_table_widget.setVerticalHeaderItem(0, item)
        self.order_table_widget.verticalHeader().setVisible(True)

        self.label = QtWidgets.QLabel(OrderDialog)
        self.label.setGeometry(QtCore.QRect(10, 430, 130, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(150, 430, 700, 30))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.aboot_label = QtWidgets.QLabel(OrderDialog)
        self.aboot_label.setGeometry(QtCore.QRect(10, 480, 130, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.aboot_label.setFont(font)
        self.aboot_label.setObjectName("label")

        self.aboot_progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.aboot_progressBar.setGeometry(QtCore.QRect(150, 480, 700, 30))
        self.aboot_progressBar.setProperty("value", 0)
        self.aboot_progressBar.setObjectName("progressBar")

        self.label_n = QtWidgets.QLabel(OrderDialog)
        self.label_n.setGeometry(QtCore.QRect(0, 430, 850, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        self.label_n.setFont(font)
        self.label_n.setObjectName("label_n")
        self.label_n.setStyleSheet("background-color: #F0F0F0")

        self.label_x = QtWidgets.QLabel(OrderDialog)
        self.label_x.setGeometry(QtCore.QRect(0, 480, 850, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        self.label_x.setFont(font)
        self.label_x.setObjectName("label_n")
        self.label_x.setStyleSheet("background-color: #F0F0F0")


        self.ok_btn = QtWidgets.QPushButton(OrderDialog)
        self.ok_btn.setGeometry(QtCore.QRect(170, 540, 120, 50))
        self.ok_btn.setObjectName("ok_btn")

        self.exit_btn = QtWidgets.QPushButton(OrderDialog)
        self.exit_btn.setGeometry(QtCore.QRect(630, 540, 120, 50))
        self.exit_btn.setObjectName("exit_btn")

        self.label_station = QtWidgets.QLabel(OrderDialog)
        self.label_station.setGeometry(QtCore.QRect(380, 540, 100, 50))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        self.label_station.setFont(font)
        self.label_station.setObjectName("label_station")

        self.station_num_cbox = QtWidgets.QComboBox(OrderDialog)
        self.station_num_cbox.setGeometry(QtCore.QRect(480, 540, 100, 50))
        # self.station_num_cbox.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.station_num_cbox.setObjectName("station_num_cbox")

        self.retranslateUi(OrderDialog)
        QtCore.QMetaObject.connectSlotsByName(OrderDialog)

    def retranslateUi(self, OrderDialog):
        _translate = QtCore.QCoreApplication.translate
        OrderDialog.setWindowTitle(_translate("OrderDialog", "订单选择"))
        self.label.setText("固件下载进度")
        self.aboot_label.setText("aboot下载进度")
        # self.label.setVisible(False)
        # self.progressBar.setVisible(False)
        # self.label_n.setVisible(False)
        self.label_station.setText("工位号")
        self.ok_btn.setText(_translate("OrderDialog", "确认选择"))
        self.exit_btn.setText(_translate("OrderDialog", "退出"))

