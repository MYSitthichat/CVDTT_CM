# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lab_received_sample.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_lab_received_MainWindow(object):
    def setupUi(self, lab_received_MainWindow):
        if not lab_received_MainWindow.objectName():
            lab_received_MainWindow.setObjectName(u"lab_received_MainWindow")
        lab_received_MainWindow.resize(1270, 890)
        self.label_title = QLabel(lab_received_MainWindow)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setGeometry(QRect(1050, 20, 200, 30))
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_search = QLabel(lab_received_MainWindow)
        self.label_search.setObjectName(u"label_search")
        self.label_search.setGeometry(QRect(30, 50, 200, 40))
        font1 = QFont()
        font1.setPointSize(15)
        self.label_search.setFont(font1)
        self.le_search = QLineEdit(lab_received_MainWindow)
        self.le_search.setObjectName(u"le_search")
        self.le_search.setGeometry(QRect(240, 50, 400, 40))
        self.le_search.setFont(font1)
        self.table_staff = QTableWidget(lab_received_MainWindow)
        if (self.table_staff.columnCount() < 3):
            self.table_staff.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_staff.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_staff.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_staff.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.table_staff.setObjectName(u"table_staff")
        self.table_staff.setGeometry(QRect(30, 120, 1021, 200))
        self.table_staff.setFont(font1)
        self.table_staff.horizontalHeader().setStretchLastSection(True)
        self.btn_select = QPushButton(lab_received_MainWindow)
        self.btn_select.setObjectName(u"btn_select")
        self.btn_select.setGeometry(QRect(1069, 120, 191, 60))
        self.btn_select.setFont(font1)
        self.label_barcode = QLabel(lab_received_MainWindow)
        self.label_barcode.setObjectName(u"label_barcode")
        self.label_barcode.setGeometry(QRect(30, 380, 250, 40))
        self.label_barcode.setFont(font1)
        self.le_barcode = QLineEdit(lab_received_MainWindow)
        self.le_barcode.setObjectName(u"le_barcode")
        self.le_barcode.setGeometry(QRect(230, 380, 341, 40))
        self.le_barcode.setFont(font1)
        self.label_datetime = QLabel(lab_received_MainWindow)
        self.label_datetime.setObjectName(u"label_datetime")
        self.label_datetime.setGeometry(QRect(30, 450, 250, 40))
        self.label_datetime.setFont(font1)
        self.dt_received = QDateTimeEdit(lab_received_MainWindow)
        self.dt_received.setObjectName(u"dt_received")
        self.dt_received.setGeometry(QRect(230, 450, 250, 40))
        self.dt_received.setFont(font1)
        self.dt_received.setCalendarPopup(True)
        self.label_receiver = QLabel(lab_received_MainWindow)
        self.label_receiver.setObjectName(u"label_receiver")
        self.label_receiver.setGeometry(QRect(30, 520, 250, 40))
        self.label_receiver.setFont(font1)
        self.le_receiver = QLineEdit(lab_received_MainWindow)
        self.le_receiver.setObjectName(u"le_receiver")
        self.le_receiver.setGeometry(QRect(230, 520, 341, 40))
        self.le_receiver.setFont(font1)
        self.label_receiver_id = QLabel(lab_received_MainWindow)
        self.label_receiver_id.setObjectName(u"label_receiver_id")
        self.label_receiver_id.setGeometry(QRect(540, 520, 200, 40))
        self.label_receiver_id.setFont(font1)
        self.label_receiver_id.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.le_receiver_id = QLineEdit(lab_received_MainWindow)
        self.le_receiver_id.setObjectName(u"le_receiver_id")
        self.le_receiver_id.setGeometry(QRect(750, 520, 301, 40))
        self.le_receiver_id.setFont(font1)
        self.btn_save = QPushButton(lab_received_MainWindow)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setGeometry(QRect(1070, 510, 191, 60))
        self.btn_save.setFont(font1)

        self.retranslateUi(lab_received_MainWindow)

        QMetaObject.connectSlotsByName(lab_received_MainWindow)
    # setupUi

    def retranslateUi(self, lab_received_MainWindow):
        lab_received_MainWindow.setWindowTitle(QCoreApplication.translate("lab_received_MainWindow", u"Lab Received Sample", None))
        lab_received_MainWindow.setStyleSheet("")
        self.label_title.setText(QCoreApplication.translate("lab_received_MainWindow", u"Lab Received sample", None))
        self.label_search.setText(QCoreApplication.translate("lab_received_MainWindow", u"\u0e04\u0e49\u0e19\u0e2b\u0e32\u0e0a\u0e37\u0e48\u0e2d\u0e40\u0e08\u0e49\u0e32\u0e2b\u0e19\u0e49\u0e32\u0e17\u0e35\u0e48", None))
        ___qtablewidgetitem = self.table_staff.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("lab_received_MainWindow", u"\u0e0a\u0e37\u0e48\u0e2d", None));
        ___qtablewidgetitem1 = self.table_staff.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("lab_received_MainWindow", u"\u0e19\u0e32\u0e21\u0e2a\u0e01\u0e38\u0e25", None));
        ___qtablewidgetitem2 = self.table_staff.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("lab_received_MainWindow", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e25\u0e02\u0e1b\u0e23\u0e30\u0e08\u0e33\u0e15\u0e31\u0e27", None));
        self.btn_select.setText(QCoreApplication.translate("lab_received_MainWindow", u"\u0e40\u0e25\u0e37\u0e2d\u0e01\u0e23\u0e32\u0e22\u0e0a\u0e37\u0e48\u0e2d", None))
        self.label_barcode.setText(QCoreApplication.translate("lab_received_MainWindow", u"\u0e23\u0e2b\u0e31\u0e2a\u0e1a\u0e32\u0e23\u0e4c\u0e42\u0e04\u0e49\u0e14\u0e2a\u0e34\u0e48\u0e07\u0e2a\u0e48\u0e07\u0e15\u0e23\u0e27\u0e08", None))
        self.label_datetime.setText(QCoreApplication.translate("lab_received_MainWindow", u"\u0e27\u0e31\u0e19\u0e40\u0e27\u0e25\u0e32\u0e17\u0e35\u0e48\u0e23\u0e31\u0e1a\u0e2a\u0e34\u0e48\u0e07\u0e2a\u0e48\u0e07\u0e15\u0e23\u0e27\u0e08", None))
        self.label_receiver.setText(QCoreApplication.translate("lab_received_MainWindow", u"\u0e1c\u0e39\u0e49\u0e23\u0e31\u0e1a\u0e2a\u0e34\u0e48\u0e07\u0e2a\u0e48\u0e07\u0e15\u0e23\u0e27\u0e08", None))
        self.label_receiver_id.setText(QCoreApplication.translate("lab_received_MainWindow", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e25\u0e02\u0e1b\u0e23\u0e30\u0e08\u0e33\u0e15\u0e31\u0e27", None))
        self.btn_save.setText(QCoreApplication.translate("lab_received_MainWindow", u"\u0e1a\u0e31\u0e19\u0e17\u0e36\u0e01\u0e02\u0e49\u0e2d\u0e21\u0e39\u0e25", None))
    # retranslateUi

