# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'receive_lab.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTableView,
    QWidget)

class Ui_receive_lab_Form(object):
    def setupUi(self, receive_lab_Form):
        if not receive_lab_Form.objectName():
            receive_lab_Form.setObjectName(u"receive_lab_Form")
        receive_lab_Form.resize(1270, 890)
        receive_lab_Form.setMinimumSize(QSize(1270, 890))
        receive_lab_Form.setMaximumSize(QSize(1270, 890))
        receive_lab_Form.setSizeIncrement(QSize(1270, 890))
        receive_lab_Form.setBaseSize(QSize(1270, 890))
        self.tableView = QTableView(receive_lab_Form)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(5, 60, 1261, 251))
        self.tableView.setFrameShape(QFrame.Shape.Box)
        self.clear_pushButton = QPushButton(receive_lab_Form)
        self.clear_pushButton.setObjectName(u"clear_pushButton")
        self.clear_pushButton.setGeometry(QRect(1105, 5, 161, 51))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(20)
        font.setBold(True)
        self.clear_pushButton.setFont(font)
        self.barcode_lineEdit = QLineEdit(receive_lab_Form)
        self.barcode_lineEdit.setObjectName(u"barcode_lineEdit")
        self.barcode_lineEdit.setGeometry(QRect(110, 10, 261, 41))
        self.barcode_lineEdit.setFont(font)
        self.barcode_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.barcode_label = QLabel(receive_lab_Form)
        self.barcode_label.setObjectName(u"barcode_label")
        self.barcode_label.setGeometry(QRect(10, 20, 91, 31))
        self.barcode_label.setFont(font)
        self.detail_lab_order_frame = QFrame(receive_lab_Form)
        self.detail_lab_order_frame.setObjectName(u"detail_lab_order_frame")
        self.detail_lab_order_frame.setGeometry(QRect(5, 320, 551, 561))
        self.detail_lab_order_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.detail_lab_order_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.tableView_2 = QTableView(self.detail_lab_order_frame)
        self.tableView_2.setObjectName(u"tableView_2")
        self.tableView_2.setGeometry(QRect(10, 50, 531, 501))
        self.tableView_2.setFrameShape(QFrame.Shape.Box)
        self.barcode_label_3 = QLabel(self.detail_lab_order_frame)
        self.barcode_label_3.setObjectName(u"barcode_label_3")
        self.barcode_label_3.setGeometry(QRect(20, 10, 201, 31))
        self.barcode_label_3.setFont(font)
        self.from_lab_order_frame = QFrame(receive_lab_Form)
        self.from_lab_order_frame.setObjectName(u"from_lab_order_frame")
        self.from_lab_order_frame.setGeometry(QRect(565, 320, 701, 561))
        self.from_lab_order_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.from_lab_order_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.tableView_3 = QTableView(self.from_lab_order_frame)
        self.tableView_3.setObjectName(u"tableView_3")
        self.tableView_3.setGeometry(QRect(10, 50, 681, 201))
        self.tableView_3.setFrameShape(QFrame.Shape.Box)
        self.barcode_label_2 = QLabel(self.from_lab_order_frame)
        self.barcode_label_2.setObjectName(u"barcode_label_2")
        self.barcode_label_2.setGeometry(QRect(10, 10, 141, 31))
        self.barcode_label_2.setFont(font)
        self.export_pushButton = QPushButton(self.from_lab_order_frame)
        self.export_pushButton.setObjectName(u"export_pushButton")
        self.export_pushButton.setGeometry(QRect(530, 260, 161, 51))
        self.export_pushButton.setFont(font)
        self.search_pushButton = QPushButton(receive_lab_Form)
        self.search_pushButton.setObjectName(u"search_pushButton")
        self.search_pushButton.setGeometry(QRect(380, 5, 161, 51))
        self.search_pushButton.setFont(font)

        self.retranslateUi(receive_lab_Form)

        QMetaObject.connectSlotsByName(receive_lab_Form)
    # setupUi

    def retranslateUi(self, receive_lab_Form):
        receive_lab_Form.setWindowTitle(QCoreApplication.translate("receive_lab_Form", u"Form", None))
        self.clear_pushButton.setText(QCoreApplication.translate("receive_lab_Form", u"CLEAR", None))
        self.barcode_label.setText(QCoreApplication.translate("receive_lab_Form", u"BARCODE", None))
        self.barcode_label_3.setText(QCoreApplication.translate("receive_lab_Form", u"\u0e23\u0e32\u0e22\u0e25\u0e30\u0e40\u0e2d\u0e35\u0e22\u0e14\u0e01\u0e32\u0e23\u0e15\u0e23\u0e27\u0e08", None))
        self.barcode_label_2.setText(QCoreApplication.translate("receive_lab_Form", u"\u0e44\u0e1f\u0e25\u0e4c TEMPLATE", None))
        self.export_pushButton.setText(QCoreApplication.translate("receive_lab_Form", u"EXPORT", None))
        self.search_pushButton.setText(QCoreApplication.translate("receive_lab_Form", u"\u0e04\u0e49\u0e19\u0e2b\u0e32", None))
    # retranslateUi

