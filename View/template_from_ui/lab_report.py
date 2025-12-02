# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lab_report.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_lab_report_MainWindow(object):
    def setupUi(self, lab_report_MainWindow):
        if not lab_report_MainWindow.objectName():
            lab_report_MainWindow.setObjectName(u"lab_report_MainWindow")
        lab_report_MainWindow.resize(1270, 890)
        lab_report_MainWindow.setStyleSheet(u"font-size: 16pt;")
        self.label_barcode_search = QLabel(lab_report_MainWindow)
        self.label_barcode_search.setObjectName(u"label_barcode_search")
        self.label_barcode_search.setGeometry(QRect(20, 20, 200, 40))
        self.search_input = QLineEdit(lab_report_MainWindow)
        self.search_input.setObjectName(u"search_input")
        self.search_input.setGeometry(QRect(230, 20, 300, 40))
        self.search_button = QPushButton(lab_report_MainWindow)
        self.search_button.setObjectName(u"search_button")
        self.search_button.setGeometry(QRect(550, 20, 120, 40))
        self.label_title = QLabel(lab_report_MainWindow)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setGeometry(QRect(1050, 20, 200, 40))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.result_table = QTableWidget(lab_report_MainWindow)
        if (self.result_table.columnCount() < 4):
            self.result_table.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.result_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.result_table.setObjectName(u"result_table")
        self.result_table.setGeometry(QRect(20, 80, 1050, 780))
        self.result_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.result_table.horizontalHeader().setDefaultSectionSize(250)
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.print_button = QPushButton(lab_report_MainWindow)
        self.print_button.setObjectName(u"print_button")
        self.print_button.setGeometry(QRect(1090, 80, 160, 50))

        self.retranslateUi(lab_report_MainWindow)

        QMetaObject.connectSlotsByName(lab_report_MainWindow)
    # setupUi

    def retranslateUi(self, lab_report_MainWindow):
        lab_report_MainWindow.setWindowTitle(QCoreApplication.translate("lab_report_MainWindow", u"Lab Report", None))
        self.label_barcode_search.setText(QCoreApplication.translate("lab_report_MainWindow", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e25\u0e02\u0e1a\u0e32\u0e23\u0e4c\u0e42\u0e04\u0e49\u0e14", None))
        self.search_button.setText(QCoreApplication.translate("lab_report_MainWindow", u"\u0e04\u0e49\u0e19\u0e2b\u0e32", None))
        self.label_title.setText(QCoreApplication.translate("lab_report_MainWindow", u"Lab report", None))
        ___qtablewidgetitem = self.result_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("lab_report_MainWindow", u"\u0e27\u0e31\u0e19\u0e40\u0e14\u0e37\u0e2d\u0e19\u0e1b\u0e35\u0e17\u0e35\u0e48\u0e23\u0e31\u0e1a\u0e07\u0e32\u0e19", None));
        ___qtablewidgetitem1 = self.result_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("lab_report_MainWindow", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e25\u0e02\u0e1a\u0e32\u0e23\u0e4c\u0e42\u0e04\u0e49\u0e14", None));
        ___qtablewidgetitem2 = self.result_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("lab_report_MainWindow", u"\u0e0a\u0e37\u0e48\u0e2d\u0e1c\u0e39\u0e49\u0e2a\u0e48\u0e07", None));
        ___qtablewidgetitem3 = self.result_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("lab_report_MainWindow", u"\u0e0a\u0e37\u0e48\u0e2d\u0e2a\u0e31\u0e15\u0e27\u0e4c", None));
        self.print_button.setText(QCoreApplication.translate("lab_report_MainWindow", u"\u0e1e\u0e34\u0e21\u0e1e\u0e4c\u0e43\u0e1a\u0e2a\u0e48\u0e07\u0e41\u0e25\u0e1b", None))
    # retranslateUi

