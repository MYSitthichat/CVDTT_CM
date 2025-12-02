# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'barcode_page.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_barcode_page_MainWindow(object):
    def setupUi(self, barcode_page_MainWindow):
        if not barcode_page_MainWindow.objectName():
            barcode_page_MainWindow.setObjectName(u"barcode_page_MainWindow")
        barcode_page_MainWindow.resize(1270, 890)
        barcode_page_MainWindow.setStyleSheet(u"font-size: 16pt;")
        self.centralwidget = QWidget(barcode_page_MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_barcode_page = QLabel(self.centralwidget)
        self.label_barcode_page.setObjectName(u"label_barcode_page")
        self.label_barcode_page.setGeometry(QRect(1090, 10, 161, 31))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_barcode_page.setFont(font)
        self.label_barcode_page.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_sender = QLabel(self.centralwidget)
        self.label_sender.setObjectName(u"label_sender")
        self.label_sender.setGeometry(QRect(20, 50, 121, 31))
        self.lineEdit_sender = QLineEdit(self.centralwidget)
        self.lineEdit_sender.setObjectName(u"lineEdit_sender")
        self.lineEdit_sender.setGeometry(QRect(20, 80, 1231, 41))
        self.label_firstname = QLabel(self.centralwidget)
        self.label_firstname.setObjectName(u"label_firstname")
        self.label_firstname.setGeometry(QRect(20, 140, 41, 31))
        self.lineEdit_firstname = QLineEdit(self.centralwidget)
        self.lineEdit_firstname.setObjectName(u"lineEdit_firstname")
        self.lineEdit_firstname.setGeometry(QRect(20, 170, 301, 41))
        self.label_lastname = QLabel(self.centralwidget)
        self.label_lastname.setObjectName(u"label_lastname")
        self.label_lastname.setGeometry(QRect(340, 140, 61, 31))
        self.lineEdit_lastname = QLineEdit(self.centralwidget)
        self.lineEdit_lastname.setObjectName(u"lineEdit_lastname")
        self.lineEdit_lastname.setGeometry(QRect(340, 170, 301, 41))
        self.label_taxid = QLabel(self.centralwidget)
        self.label_taxid.setObjectName(u"label_taxid")
        self.label_taxid.setGeometry(QRect(660, 140, 201, 31))
        self.lineEdit_taxid = QLineEdit(self.centralwidget)
        self.lineEdit_taxid.setObjectName(u"lineEdit_taxid")
        self.lineEdit_taxid.setGeometry(QRect(660, 170, 301, 41))
        self.btn_search_today = QPushButton(self.centralwidget)
        self.btn_search_today.setObjectName(u"btn_search_today")
        self.btn_search_today.setGeometry(QRect(1000, 140, 251, 51))
        self.btn_search_customer = QPushButton(self.centralwidget)
        self.btn_search_customer.setObjectName(u"btn_search_customer")
        self.btn_search_customer.setGeometry(QRect(1000, 200, 251, 51))
        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 7):
            self.tableWidget.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(20, 270, 1231, 541))
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(175)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.btn_print = QPushButton(self.centralwidget)
        self.btn_print.setObjectName(u"btn_print")
        self.btn_print.setGeometry(QRect(1080, 830, 171, 51))
        barcode_page_MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(barcode_page_MainWindow)

        QMetaObject.connectSlotsByName(barcode_page_MainWindow)
    # setupUi

    def retranslateUi(self, barcode_page_MainWindow):
        barcode_page_MainWindow.setWindowTitle(QCoreApplication.translate("barcode_page_MainWindow", u"Barcode System", None))
        self.label_barcode_page.setText(QCoreApplication.translate("barcode_page_MainWindow", u"Barcode page", None))
        self.label_sender.setText(QCoreApplication.translate("barcode_page_MainWindow", u"\u0e0a\u0e37\u0e48\u0e2d\u0e1c\u0e39\u0e49\u0e19\u0e33\u0e2a\u0e48\u0e07", None))
        self.label_firstname.setText(QCoreApplication.translate("barcode_page_MainWindow", u"\u0e0a\u0e37\u0e48\u0e2d", None))
        self.label_lastname.setText(QCoreApplication.translate("barcode_page_MainWindow", u"\u0e2a\u0e01\u0e38\u0e25", None))
        self.label_taxid.setText(QCoreApplication.translate("barcode_page_MainWindow", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e25\u0e02\u0e1c\u0e39\u0e49\u0e40\u0e2a\u0e35\u0e22\u0e20\u0e32\u0e29\u0e35", None))
        self.btn_search_today.setText(QCoreApplication.translate("barcode_page_MainWindow", u"\u0e04\u0e49\u0e19\u0e2b\u0e32\u0e40\u0e04\u0e2a\u0e43\u0e19\u0e27\u0e31\u0e19\u0e19\u0e35\u0e49", None))
        self.btn_search_customer.setText(QCoreApplication.translate("barcode_page_MainWindow", u"\u0e04\u0e49\u0e19\u0e2b\u0e32\u0e14\u0e49\u0e27\u0e22\u0e0a\u0e37\u0e48\u0e2d\u0e25\u0e39\u0e01\u0e04\u0e49\u0e32", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("barcode_page_MainWindow", u"\u0e27\u0e31\u0e19\u0e17\u0e35\u0e48\u0e23\u0e31\u0e1a\u0e40\u0e04\u0e2a", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("barcode_page_MainWindow", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e25\u0e02\u0e01\u0e32\u0e23\u0e15\u0e23\u0e27\u0e08", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("barcode_page_MainWindow", u"\u0e0a\u0e19\u0e34\u0e14\u0e2a\u0e31\u0e15\u0e27\u0e4c", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("barcode_page_MainWindow", u"\u0e2b\u0e49\u0e2d\u0e07\u0e1b\u0e0f\u0e34\u0e1a\u0e31\u0e15\u0e34\u0e01\u0e32\u0e23", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("barcode_page_MainWindow", u"\u0e01\u0e32\u0e23\u0e40\u0e01\u0e47\u0e1a\u0e23\u0e31\u0e01\u0e29\u0e32", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("barcode_page_MainWindow", u"\u0e23\u0e30\u0e14\u0e31\u0e1a\u0e04\u0e27\u0e32\u0e21\u0e14\u0e48\u0e27\u0e19", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("barcode_page_MainWindow", u"\u0e02\u0e49\u0e2d\u0e21\u0e39\u0e25\u0e40\u0e1e\u0e34\u0e48\u0e21\u0e40\u0e15\u0e34\u0e21", None));
        self.btn_print.setText(QCoreApplication.translate("barcode_page_MainWindow", u"\u0e1e\u0e34\u0e21\u0e1e\u0e4c\u0e1a\u0e32\u0e23\u0e4c\u0e42\u0e04\u0e49\u0e14", None))
    # retranslateUi

