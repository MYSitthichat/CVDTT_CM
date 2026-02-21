# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'send_report_pdf.ui'
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

class Ui_Report_Form(object):
    def setupUi(self, Report_Form):
        if not Report_Form.objectName():
            Report_Form.setObjectName(u"Report_Form")
        Report_Form.resize(1270, 890)
        Report_Form.setMinimumSize(QSize(1270, 890))
        Report_Form.setMaximumSize(QSize(1270, 890))
        Report_Form.setSizeIncrement(QSize(1270, 890))
        Report_Form.setBaseSize(QSize(1270, 890))
        self.show_pdf_frame = QFrame(Report_Form)
        self.show_pdf_frame.setObjectName(u"show_pdf_frame")
        self.show_pdf_frame.setGeometry(QRect(234, 115, 1031, 771))
        self.show_pdf_frame.setFrameShape(QFrame.Shape.Box)
        self.show_pdf_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.show_pdf_frame.setLineWidth(2)
        self.location_file_lineEdit = QLineEdit(Report_Form)
        self.location_file_lineEdit.setObjectName(u"location_file_lineEdit")
        self.location_file_lineEdit.setGeometry(QRect(320, 20, 321, 40))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(14)
        font.setBold(True)
        self.location_file_lineEdit.setFont(font)
        self.location_file_label = QLabel(Report_Form)
        self.location_file_label.setObjectName(u"location_file_label")
        self.location_file_label.setGeometry(QRect(240, 20, 81, 31))
        font1 = QFont()
        font1.setFamilies([u"TH Niramit AS"])
        font1.setPointSize(20)
        font1.setBold(True)
        self.location_file_label.setFont(font1)
        self.search_location_file_pushButton = QPushButton(Report_Form)
        self.search_location_file_pushButton.setObjectName(u"search_location_file_pushButton")
        self.search_location_file_pushButton.setGeometry(QRect(650, 17, 140, 45))
        self.search_location_file_pushButton.setFont(font1)
        self.convert_file_progressBar = QProgressBar(Report_Form)
        self.convert_file_progressBar.setObjectName(u"convert_file_progressBar")
        self.convert_file_progressBar.setGeometry(QRect(320, 80, 311, 23))
        self.convert_file_progressBar.setValue(50)
        self.convert_file_progressBar.setTextVisible(False)
        self.clear_location_file_pushButton = QPushButton(Report_Form)
        self.clear_location_file_pushButton.setObjectName(u"clear_location_file_pushButton")
        self.clear_location_file_pushButton.setGeometry(QRect(800, 17, 140, 45))
        self.clear_location_file_pushButton.setFont(font1)
        self.send_report_file_pushButton = QPushButton(Report_Form)
        self.send_report_file_pushButton.setObjectName(u"send_report_file_pushButton")
        self.send_report_file_pushButton.setGeometry(QRect(1125, 60, 140, 45))
        self.send_report_file_pushButton.setFont(font1)
        self.convert_word_to_pdf_pushButton = QPushButton(Report_Form)
        self.convert_word_to_pdf_pushButton.setObjectName(u"convert_word_to_pdf_pushButton")
        self.convert_word_to_pdf_pushButton.setGeometry(QRect(650, 67, 140, 45))
        self.convert_word_to_pdf_pushButton.setFont(font1)
        self.preview_pdf_webEngineView = QWebEngineView(Report_Form)
        self.preview_pdf_webEngineView.setObjectName(u"preview_pdf_webEngineView")
        self.preview_pdf_webEngineView.setGeometry(QRect(245, 125, 1011, 751))
        self.preview_pdf_webEngineView.setUrl(QUrl(u"about:blank"))
        self.barcode_label = QLabel(Report_Form)
        self.barcode_label.setObjectName(u"barcode_label")
        self.barcode_label.setGeometry(QRect(80, 30, 81, 31))
        self.barcode_label.setFont(font1)
        self.barcode_lineEdit = QLineEdit(Report_Form)
        self.barcode_lineEdit.setObjectName(u"barcode_lineEdit")
        self.barcode_lineEdit.setGeometry(QRect(5, 70, 211, 40))
        self.barcode_lineEdit.setFont(font)
        self.barcode_tableView = QTableView(Report_Form)
        self.barcode_tableView.setObjectName(u"barcode_tableView")
        self.barcode_tableView.setGeometry(QRect(5, 121, 211, 371))
        self.barcode_tableView.setFrameShape(QFrame.Shape.Box)
        self.select_barcode_pushButton = QPushButton(Report_Form)
        self.select_barcode_pushButton.setObjectName(u"select_barcode_pushButton")
        self.select_barcode_pushButton.setGeometry(QRect(5, 500, 211, 51))
        self.select_barcode_pushButton.setFont(font1)

        self.retranslateUi(Report_Form)

        QMetaObject.connectSlotsByName(Report_Form)
    # setupUi

    def retranslateUi(self, Report_Form):
        Report_Form.setWindowTitle(QCoreApplication.translate("Report_Form", u"Form", None))
        self.location_file_label.setText(QCoreApplication.translate("Report_Form", u"\u0e17\u0e35\u0e48\u0e2d\u0e22\u0e39\u0e48\u0e44\u0e1f\u0e25\u0e4c", None))
        self.search_location_file_pushButton.setText(QCoreApplication.translate("Report_Form", u"\u0e04\u0e49\u0e19\u0e2b\u0e32", None))
        self.clear_location_file_pushButton.setText(QCoreApplication.translate("Report_Form", u"clear", None))
        self.send_report_file_pushButton.setText(QCoreApplication.translate("Report_Form", u"\u0e2a\u0e48\u0e07\u0e23\u0e32\u0e22\u0e07\u0e32\u0e19", None))
        self.convert_word_to_pdf_pushButton.setText(QCoreApplication.translate("Report_Form", u"\u0e41\u0e1b\u0e25\u0e07\u0e40\u0e1b\u0e47\u0e19 PDF", None))
        self.barcode_label.setText(QCoreApplication.translate("Report_Form", u"Barcode", None))
        self.select_barcode_pushButton.setText(QCoreApplication.translate("Report_Form", u"\u0e40\u0e25\u0e37\u0e2d\u0e01\u0e23\u0e32\u0e22\u0e01\u0e32\u0e23\u0e19\u0e35\u0e49", None))
    # retranslateUi

