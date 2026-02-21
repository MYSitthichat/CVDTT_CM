# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'merg_report_form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QTableView, QWidget)

class Ui_MergForm(object):
    def setupUi(self, MergForm):
        if not MergForm.objectName():
            MergForm.setObjectName(u"MergForm")
        MergForm.resize(1270, 890)
        MergForm.setMinimumSize(QSize(1270, 890))
        MergForm.setMaximumSize(QSize(1270, 890))
        MergForm.setSizeIncrement(QSize(1270, 890))
        MergForm.setBaseSize(QSize(1270, 890))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(20)
        font.setBold(True)
        MergForm.setFont(font)
        self.barcode_lineEdit = QLineEdit(MergForm)
        self.barcode_lineEdit.setObjectName(u"barcode_lineEdit")
        self.barcode_lineEdit.setGeometry(QRect(85, 10, 191, 41))
        self.barcode_label = QLabel(MergForm)
        self.barcode_label.setObjectName(u"barcode_label")
        self.barcode_label.setGeometry(QRect(5, 15, 71, 41))
        self.search_pushButton = QPushButton(MergForm)
        self.search_pushButton.setObjectName(u"search_pushButton")
        self.search_pushButton.setGeometry(QRect(280, 10, 101, 41))
        self.from_list_tableView = QTableView(MergForm)
        self.from_list_tableView.setObjectName(u"from_list_tableView")
        self.from_list_tableView.setGeometry(QRect(5, 55, 381, 171))
        self.show_report_pushButton = QPushButton(MergForm)
        self.show_report_pushButton.setObjectName(u"show_report_pushButton")
        self.show_report_pushButton.setGeometry(QRect(255, 230, 130, 50))
        self.show_report_progressBar = QProgressBar(MergForm)
        self.show_report_progressBar.setObjectName(u"show_report_progressBar")
        self.show_report_progressBar.setGeometry(QRect(10, 230, 240, 50))
        self.show_report_progressBar.setValue(24)
        self.show_report_progressBar.setTextVisible(False)
        self.export_frame = QFrame(MergForm)
        self.export_frame.setObjectName(u"export_frame")
        self.export_frame.setGeometry(QRect(5, 290, 380, 591))
        self.export_frame.setFrameShape(QFrame.Shape.Box)
        self.export_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.combine_page_pushButton = QPushButton(self.export_frame)
        self.combine_page_pushButton.setObjectName(u"combine_page_pushButton")
        self.combine_page_pushButton.setGeometry(QRect(250, 10, 125, 51))
        self.Export_pushButton = QPushButton(self.export_frame)
        self.Export_pushButton.setObjectName(u"Export_pushButton")
        self.Export_pushButton.setGeometry(QRect(235, 535, 141, 51))
        self.show_report_frame = QFrame(MergForm)
        self.show_report_frame.setObjectName(u"show_report_frame")
        self.show_report_frame.setGeometry(QRect(390, 11, 875, 870))
        self.show_report_frame.setFrameShape(QFrame.Shape.Box)
        self.show_report_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.report_webEngineView = QWebEngineView(self.show_report_frame)
        self.report_webEngineView.setObjectName(u"report_webEngineView")
        self.report_webEngineView.setGeometry(QRect(7, 7, 860, 855))
        self.report_webEngineView.setUrl(QUrl(u"about:blank"))

        self.retranslateUi(MergForm)

        QMetaObject.connectSlotsByName(MergForm)
    # setupUi

    def retranslateUi(self, MergForm):
        MergForm.setWindowTitle(QCoreApplication.translate("MergForm", u"Form", None))
        self.barcode_label.setText(QCoreApplication.translate("MergForm", u"Barcode", None))
        self.search_pushButton.setText(QCoreApplication.translate("MergForm", u"\u0e04\u0e49\u0e19\u0e2b\u0e32", None))
        self.show_report_pushButton.setText(QCoreApplication.translate("MergForm", u"\u0e41\u0e2a\u0e14\u0e07\u0e23\u0e32\u0e22\u0e07\u0e32\u0e19", None))
        self.combine_page_pushButton.setText(QCoreApplication.translate("MergForm", u"\u0e43\u0e1a\u0e1b\u0e30\u0e2b\u0e19\u0e49\u0e32", None))
        self.Export_pushButton.setText(QCoreApplication.translate("MergForm", u"\u0e2a\u0e48\u0e07\u0e2d\u0e2d\u0e01\u0e23\u0e32\u0e22\u0e07\u0e32\u0e19", None))
    # retranslateUi

