# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'parasite_form.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHeaderView,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QTableView, QWidget)

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
        self.Faces_radioButton = QRadioButton(Report_Form)
        self.Faces_radioButton.setObjectName(u"Faces_radioButton")
        self.Faces_radioButton.setGeometry(QRect(40, 40, 91, 20))
        font1 = QFont()
        font1.setFamilies([u"TH Niramit AS"])
        font1.setPointSize(24)
        font1.setBold(True)
        self.Faces_radioButton.setFont(font1)
        self.comboBox = QComboBox(Report_Form)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(30, 80, 261, 41))
        self.Faces_dog_cat_radioButton = QRadioButton(Report_Form)
        self.Faces_dog_cat_radioButton.setObjectName(u"Faces_dog_cat_radioButton")
        self.Faces_dog_cat_radioButton.setGeometry(QRect(150, 40, 181, 20))
        self.Faces_dog_cat_radioButton.setFont(font1)
        self.radioButton_3 = QRadioButton(Report_Form)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setGeometry(QRect(340, 40, 91, 20))
        self.radioButton_3.setFont(font1)
        self.radioButton_4 = QRadioButton(Report_Form)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setGeometry(QRect(440, 40, 181, 20))
        self.radioButton_4.setFont(font1)
        self.comboBox_2 = QComboBox(Report_Form)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(300, 80, 251, 41))
        self.comboBox_3 = QComboBox(Report_Form)
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setGeometry(QRect(560, 80, 231, 41))
        self.barcode_para_tableView = QTableView(Report_Form)
        self.barcode_para_tableView.setObjectName(u"barcode_para_tableView")
        self.barcode_para_tableView.setGeometry(QRect(40, 240, 211, 371))
        self.barcode_para_tableView.setFrameShape(QFrame.Shape.Box)
        self.select_barcode_para__pushButton = QPushButton(Report_Form)
        self.select_barcode_para__pushButton.setObjectName(u"select_barcode_para__pushButton")
        self.select_barcode_para__pushButton.setGeometry(QRect(40, 630, 211, 51))
        self.select_barcode_para__pushButton.setFont(font)
        self.barcode_para_lineEdit = QLineEdit(Report_Form)
        self.barcode_para_lineEdit.setObjectName(u"barcode_para_lineEdit")
        self.barcode_para_lineEdit.setGeometry(QRect(40, 180, 211, 40))
        font2 = QFont()
        font2.setFamilies([u"TH Niramit AS"])
        font2.setPointSize(14)
        font2.setBold(True)
        self.barcode_para_lineEdit.setFont(font2)
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
        self.Faces_radioButton.setText(QCoreApplication.translate("Report_Form", u"Faces", None))
        self.Faces_dog_cat_radioButton.setText(QCoreApplication.translate("Report_Form", u"Faces Dog Cat", None))
        self.radioButton_3.setText(QCoreApplication.translate("Report_Form", u"Blood", None))
        self.radioButton_4.setText(QCoreApplication.translate("Report_Form", u"Identification", None))
        self.select_barcode_para__pushButton.setText(QCoreApplication.translate("Report_Form", u"\u0e40\u0e25\u0e37\u0e2d\u0e01\u0e23\u0e32\u0e22\u0e01\u0e32\u0e23\u0e19\u0e35\u0e49", None))
        self.barcode_label.setText(QCoreApplication.translate("Report_Form", u"Barcode", None))
    # retranslateUi

