# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Doctor_report.ui'
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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHeaderView,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Doctor_Form(object):
    def setupUi(self, Doctor_Form):
        if not Doctor_Form.objectName():
            Doctor_Form.setObjectName(u"Doctor_Form")
        Doctor_Form.resize(1270, 890)
        Doctor_Form.setMinimumSize(QSize(1270, 890))
        Doctor_Form.setMaximumSize(QSize(1270, 890))
        self.frame = QFrame(Doctor_Form)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(5, 5, 1260, 261))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Plain)
        self.select_lab_comboBox = QComboBox(self.frame)
        self.select_lab_comboBox.addItem("")
        self.select_lab_comboBox.addItem("")
        self.select_lab_comboBox.addItem("")
        self.select_lab_comboBox.addItem("")
        self.select_lab_comboBox.setObjectName(u"select_lab_comboBox")
        self.select_lab_comboBox.setGeometry(QRect(10, 10, 241, 51))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(20)
        font.setBold(True)
        self.select_lab_comboBox.setFont(font)
        self.detail_order_treeWidget = QTreeWidget(self.frame)
        QTreeWidgetItem(self.detail_order_treeWidget)
        QTreeWidgetItem(self.detail_order_treeWidget)
        QTreeWidgetItem(self.detail_order_treeWidget)
        self.detail_order_treeWidget.setObjectName(u"detail_order_treeWidget")
        self.detail_order_treeWidget.setGeometry(QRect(260, 10, 991, 241))
        self.stuck_order_label = QLabel(self.frame)
        self.stuck_order_label.setObjectName(u"stuck_order_label")
        self.stuck_order_label.setGeometry(QRect(10, 80, 111, 31))
        self.stuck_order_label.setFont(font)
        self.stuck_order_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stuck_order_lineEdit = QLineEdit(self.frame)
        self.stuck_order_lineEdit.setObjectName(u"stuck_order_lineEdit")
        self.stuck_order_lineEdit.setGeometry(QRect(120, 70, 61, 41))
        self.stuck_order_lineEdit.setFont(font)
        self.number_report_label = QLabel(self.frame)
        self.number_report_label.setObjectName(u"number_report_label")
        self.number_report_label.setGeometry(QRect(60, 120, 141, 31))
        self.number_report_label.setFont(font)
        self.number_report_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.number_report_lineEdit = QLineEdit(self.frame)
        self.number_report_lineEdit.setObjectName(u"number_report_lineEdit")
        self.number_report_lineEdit.setGeometry(QRect(10, 150, 241, 41))
        self.number_report_lineEdit.setFont(font)
        self.number_report_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_pushButton = QPushButton(self.frame)
        self.preview_pushButton.setObjectName(u"preview_pushButton")
        self.preview_pushButton.setGeometry(QRect(10, 200, 241, 51))
        self.preview_pushButton.setFont(font)
        self.stuck_order_label_2 = QLabel(self.frame)
        self.stuck_order_label_2.setObjectName(u"stuck_order_label_2")
        self.stuck_order_label_2.setGeometry(QRect(180, 80, 71, 31))
        self.stuck_order_label_2.setFont(font)
        self.stuck_order_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_2 = QFrame(Doctor_Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(5, 270, 1011, 611))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.doctor_show_preview_webEngineView = QWebEngineView(self.frame_2)
        self.doctor_show_preview_webEngineView.setObjectName(u"doctor_show_preview_webEngineView")
        self.doctor_show_preview_webEngineView.setGeometry(QRect(10, 10, 991, 591))
        self.doctor_show_preview_webEngineView.setUrl(QUrl(u"about:blank"))
        self.send_report_pushButton = QPushButton(Doctor_Form)
        self.send_report_pushButton.setObjectName(u"send_report_pushButton")
        self.send_report_pushButton.setGeometry(QRect(1020, 380, 241, 61))
        self.send_report_pushButton.setFont(font)
        self.correct_radioButton = QRadioButton(Doctor_Form)
        self.correct_radioButton.setObjectName(u"correct_radioButton")
        self.correct_radioButton.setGeometry(QRect(1030, 330, 91, 31))
        self.correct_radioButton.setFont(font)
        self.incorrect_radioButton = QRadioButton(Doctor_Form)
        self.incorrect_radioButton.setObjectName(u"incorrect_radioButton")
        self.incorrect_radioButton.setGeometry(QRect(1150, 330, 111, 31))
        self.incorrect_radioButton.setFont(font)
        self.check_report_label = QLabel(Doctor_Form)
        self.check_report_label.setObjectName(u"check_report_label")
        self.check_report_label.setGeometry(QRect(1030, 280, 221, 41))
        self.check_report_label.setFont(font)
        self.check_report_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.return_report_pushButton = QPushButton(Doctor_Form)
        self.return_report_pushButton.setObjectName(u"return_report_pushButton")
        self.return_report_pushButton.setGeometry(QRect(1020, 450, 241, 61))
        self.return_report_pushButton.setFont(font)

        self.retranslateUi(Doctor_Form)

        QMetaObject.connectSlotsByName(Doctor_Form)
    # setupUi

    def retranslateUi(self, Doctor_Form):
        Doctor_Form.setWindowTitle(QCoreApplication.translate("Doctor_Form", u"Form", None))
        self.select_lab_comboBox.setItemText(0, QCoreApplication.translate("Doctor_Form", u"\u0e17\u0e31\u0e49\u0e07\u0e2b\u0e21\u0e14", None))
        self.select_lab_comboBox.setItemText(1, QCoreApplication.translate("Doctor_Form", u"\u0e41\u0e1a\u0e04\u0e17\u0e35\u0e40\u0e23\u0e35\u0e22\u0e27\u0e34\u0e17\u0e22\u0e32", None))
        self.select_lab_comboBox.setItemText(2, QCoreApplication.translate("Doctor_Form", u"\u0e1b\u0e23\u0e2a\u0e34\u0e15\u0e27\u0e34\u0e17\u0e22\u0e32", None))
        self.select_lab_comboBox.setItemText(3, QCoreApplication.translate("Doctor_Form", u"\u0e2d\u0e13\u0e39\u0e27\u0e34\u0e17\u0e22\u0e32", None))

        ___qtreewidgetitem = self.detail_order_treeWidget.headerItem()
        ___qtreewidgetitem.setText(6, QCoreApplication.translate("Doctor_Form", u"\u0e2a\u0e16\u0e32\u0e19\u0e30", None));
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("Doctor_Form", u"\u0e1c\u0e39\u0e49\u0e25\u0e07\u0e23\u0e32\u0e22\u0e07\u0e32\u0e19", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("Doctor_Form", u"\u0e2b\u0e49\u0e2d\u0e07\u0e1b\u0e0f\u0e34\u0e1a\u0e31\u0e15\u0e34\u0e01\u0e32\u0e23", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Doctor_Form", u"\u0e15\u0e31\u0e27\u0e2d\u0e22\u0e48\u0e32\u0e07\u0e17\u0e35\u0e48\u0e2a\u0e48\u0e07\u0e15\u0e23\u0e27\u0e08", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Doctor_Form", u"\u0e40\u0e25\u0e02\u0e17\u0e35\u0e48\u0e15\u0e31\u0e27\u0e2d\u0e22\u0e48\u0e32\u0e07", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Doctor_Form", u"\u0e40\u0e25\u0e02\u0e17\u0e35\u0e48\u0e23\u0e32\u0e22\u0e07\u0e32\u0e19", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Doctor_Form", u"\u0e27\u0e31\u0e19\u0e17\u0e35\u0e25\u0e07\u0e23\u0e32\u0e22\u0e07\u0e32\u0e19", None));

        __sortingEnabled = self.detail_order_treeWidget.isSortingEnabled()
        self.detail_order_treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.detail_order_treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(6, QCoreApplication.translate("Doctor_Form", u"\u0e23\u0e2d\u0e01\u0e32\u0e23\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19", None));
        ___qtreewidgetitem1.setText(5, QCoreApplication.translate("Doctor_Form", u"\u0e17\u0e14\u0e2a\u0e2d\u0e1a", None));
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("Doctor_Form", u"\u0e41\u0e1a\u0e04\u0e17\u0e35\u0e40\u0e23\u0e35\u0e22", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("Doctor_Form", u"\u0e44\u0e02\u0e2a\u0e31\u0e19\u0e2b\u0e25\u0e31\u0e07", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("Doctor_Form", u"555555", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Doctor_Form", u"1111111", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Doctor_Form", u"10-5-69", None));
        ___qtreewidgetitem2 = self.detail_order_treeWidget.topLevelItem(1)
        ___qtreewidgetitem2.setText(6, QCoreApplication.translate("Doctor_Form", u"\u0e23\u0e2d\u0e01\u0e32\u0e23\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19", None));
        ___qtreewidgetitem2.setText(5, QCoreApplication.translate("Doctor_Form", u"\u0e17\u0e14\u0e2a\u0e2d\u0e1a2", None));
        ___qtreewidgetitem2.setText(4, QCoreApplication.translate("Doctor_Form", u"\u0e2d\u0e13\u0e39", None));
        ___qtreewidgetitem2.setText(3, QCoreApplication.translate("Doctor_Form", u"\u0e0a\u0e34\u0e49\u0e19\u0e40\u0e19\u0e37\u0e49\u0e2d", None));
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("Doctor_Form", u"666666", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("Doctor_Form", u"2222222", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Doctor_Form", u"1-1-69", None));
        ___qtreewidgetitem3 = self.detail_order_treeWidget.topLevelItem(2)
        ___qtreewidgetitem3.setText(6, QCoreApplication.translate("Doctor_Form", u"\u0e23\u0e2d\u0e01\u0e32\u0e23\u0e22\u0e37\u0e19\u0e22\u0e31\u0e19", None));
        ___qtreewidgetitem3.setText(5, QCoreApplication.translate("Doctor_Form", u"\u0e17\u0e14\u0e2a\u0e2d\u0e1a3", None));
        ___qtreewidgetitem3.setText(4, QCoreApplication.translate("Doctor_Form", u"\u0e1b\u0e23\u0e2a\u0e34\u0e15", None));
        ___qtreewidgetitem3.setText(3, QCoreApplication.translate("Doctor_Form", u"\u0e40\u0e25\u0e37\u0e2d\u0e14", None));
        ___qtreewidgetitem3.setText(2, QCoreApplication.translate("Doctor_Form", u"77777", None));
        ___qtreewidgetitem3.setText(1, QCoreApplication.translate("Doctor_Form", u"333333", None));
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("Doctor_Form", u"2-2-68", None));
        self.detail_order_treeWidget.setSortingEnabled(__sortingEnabled)

        self.stuck_order_label.setText(QCoreApplication.translate("Doctor_Form", u"\u0e04\u0e49\u0e32\u0e07\u0e43\u0e19\u0e23\u0e30\u0e1a\u0e1a", None))
        self.number_report_label.setText(QCoreApplication.translate("Doctor_Form", u"\u0e40\u0e25\u0e02\u0e17\u0e35\u0e48\u0e23\u0e32\u0e22\u0e07\u0e32\u0e19", None))
        self.preview_pushButton.setText(QCoreApplication.translate("Doctor_Form", u"Preview", None))
        self.stuck_order_label_2.setText(QCoreApplication.translate("Doctor_Form", u"\u0e23\u0e32\u0e22\u0e07\u0e32\u0e19", None))
        self.send_report_pushButton.setText(QCoreApplication.translate("Doctor_Form", u"\u0e2a\u0e48\u0e07\u0e2d\u0e2d\u0e01\u0e23\u0e32\u0e22\u0e07\u0e32\u0e19", None))
        self.correct_radioButton.setText(QCoreApplication.translate("Doctor_Form", u"\u0e16\u0e39\u0e01\u0e15\u0e49\u0e2d\u0e07", None))
        self.incorrect_radioButton.setText(QCoreApplication.translate("Doctor_Form", u"\u0e1c\u0e34\u0e14\u0e1e\u0e25\u0e32\u0e14", None))
        self.check_report_label.setText(QCoreApplication.translate("Doctor_Form", u"\u0e04\u0e27\u0e32\u0e21\u0e16\u0e39\u0e01\u0e15\u0e49\u0e2d\u0e07\u0e02\u0e2d\u0e07\u0e23\u0e32\u0e22\u0e07\u0e32\u0e19", None))
        self.return_report_pushButton.setText(QCoreApplication.translate("Doctor_Form", u"\u0e15\u0e35\u0e01\u0e25\u0e31\u0e1a\u0e23\u0e32\u0e22\u0e07\u0e32\u0e19", None))
    # retranslateUi

