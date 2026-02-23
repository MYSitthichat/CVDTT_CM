# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'monocular_form.ui'
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
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
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
        self.show_word_frame = QFrame(Report_Form)
        self.show_word_frame.setObjectName(u"show_word_frame")
        self.show_word_frame.setGeometry(QRect(290, 150, 901, 711))
        self.show_word_frame.setFrameShape(QFrame.Shape.Box)
        self.show_word_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.show_word_frame.setLineWidth(2)
        self.form_preview_pushButton = QPushButton(Report_Form)
        self.form_preview_pushButton.setObjectName(u"form_preview_pushButton")
        self.form_preview_pushButton.setGeometry(QRect(830, 50, 201, 71))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(20)
        font.setBold(True)
        self.form_preview_pushButton.setFont(font)
        self.preview_word_webEngineView = QWebEngineView(Report_Form)
        self.preview_word_webEngineView.setObjectName(u"preview_word_webEngineView")
        self.preview_word_webEngineView.setGeometry(QRect(301, 160, 881, 691))
        self.preview_word_webEngineView.setUrl(QUrl(u"about:blank"))
        self.save_pushButton = QPushButton(Report_Form)
        self.save_pushButton.setObjectName(u"save_pushButton")
        self.save_pushButton.setGeometry(QRect(1050, 50, 211, 71))
        self.save_pushButton.setFont(font)
        self.label = QLabel(Report_Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(140, 20, 49, 16))
        self.PCR_FIP_radioButton = QRadioButton(Report_Form)
        self.PCR_FIP_radioButton.setObjectName(u"PCR_FIP_radioButton")
        self.PCR_FIP_radioButton.setGeometry(QRect(50, 70, 101, 20))
        font1 = QFont()
        font1.setFamilies([u"TH Niramit AS"])
        font1.setPointSize(24)
        font1.setBold(True)
        self.PCR_FIP_radioButton.setFont(font1)
        self.PCR_real_time_radioButton = QRadioButton(Report_Form)
        self.PCR_real_time_radioButton.setObjectName(u"PCR_real_time_radioButton")
        self.PCR_real_time_radioButton.setGeometry(QRect(180, 70, 221, 20))
        self.PCR_real_time_radioButton.setFont(font1)
        self.PCR_FeLV_radioButton = QRadioButton(Report_Form)
        self.PCR_FeLV_radioButton.setObjectName(u"PCR_FeLV_radioButton")
        self.PCR_FeLV_radioButton.setGeometry(QRect(420, 70, 131, 20))
        self.PCR_FeLV_radioButton.setFont(font1)
        self.PCR_ASF_radioButton = QRadioButton(Report_Form)
        self.PCR_ASF_radioButton.setObjectName(u"PCR_ASF_radioButton")
        self.PCR_ASF_radioButton.setGeometry(QRect(570, 70, 211, 20))
        self.PCR_ASF_radioButton.setFont(font1)
        self.barcode_mono_tableView = QTableView(Report_Form)
        self.barcode_mono_tableView.setObjectName(u"barcode_mono_tableView")
        self.barcode_mono_tableView.setGeometry(QRect(40, 240, 211, 371))
        self.barcode_mono_tableView.setFrameShape(QFrame.Shape.Box)
        self.select_barcode_mono__pushButton = QPushButton(Report_Form)
        self.select_barcode_mono__pushButton.setObjectName(u"select_barcode_mono__pushButton")
        self.select_barcode_mono__pushButton.setGeometry(QRect(40, 630, 211, 51))
        self.select_barcode_mono__pushButton.setFont(font)
        self.barcode_mono_lineEdit = QLineEdit(Report_Form)
        self.barcode_mono_lineEdit.setObjectName(u"barcode_mono_lineEdit")
        self.barcode_mono_lineEdit.setGeometry(QRect(40, 180, 211, 40))
        font2 = QFont()
        font2.setFamilies([u"TH Niramit AS"])
        font2.setPointSize(14)
        font2.setBold(True)
        self.barcode_mono_lineEdit.setFont(font2)
        self.barcode_label = QLabel(Report_Form)
        self.barcode_label.setObjectName(u"barcode_label")
        self.barcode_label.setGeometry(QRect(110, 140, 81, 31))
        self.barcode_label.setFont(font)

        self.retranslateUi(Report_Form)

        QMetaObject.connectSlotsByName(Report_Form)
    # setupUi

    def retranslateUi(self, Report_Form):
        Report_Form.setWindowTitle(QCoreApplication.translate("Report_Form", u"Form", None))
        self.form_preview_pushButton.setText(QCoreApplication.translate("Report_Form", u"Form Preview ", None))
        self.save_pushButton.setText(QCoreApplication.translate("Report_Form", u"\u0e1a\u0e31\u0e19\u0e17\u0e36\u0e01", None))
        self.label.setText("")
        self.PCR_FIP_radioButton.setText(QCoreApplication.translate("Report_Form", u"PCR FIP", None))
        self.PCR_real_time_radioButton.setText(QCoreApplication.translate("Report_Form", u"PCR real time AHS", None))
        self.PCR_FeLV_radioButton.setText(QCoreApplication.translate("Report_Form", u"PCR FeLV", None))
        self.PCR_ASF_radioButton.setText(QCoreApplication.translate("Report_Form", u"PCR real time ASF", None))
        self.select_barcode_mono__pushButton.setText(QCoreApplication.translate("Report_Form", u"\u0e40\u0e25\u0e37\u0e2d\u0e01\u0e23\u0e32\u0e22\u0e01\u0e32\u0e23\u0e19\u0e35\u0e49", None))
        self.barcode_label.setText(QCoreApplication.translate("Report_Form", u"Barcode", None))
    # retranslateUi

