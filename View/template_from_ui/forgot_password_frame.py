# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'forgot_password.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_forgot_password_Form(object):
    def setupUi(self, forgot_password_Form):
        if not forgot_password_Form.objectName():
            forgot_password_Form.setObjectName(u"forgot_password_Form")
        forgot_password_Form.resize(600, 300)
        forgot_password_Form.setMinimumSize(QSize(600, 300))
        forgot_password_Form.setMaximumSize(QSize(600, 300))
        forgot_password_Form.setSizeIncrement(QSize(600, 300))
        forgot_password_Form.setBaseSize(QSize(600, 300))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(20)
        font.setBold(True)
        forgot_password_Form.setFont(font)
        self.FP_email_lineEdit = QLineEdit(forgot_password_Form)
        self.FP_email_lineEdit.setObjectName(u"FP_email_lineEdit")
        self.FP_email_lineEdit.setGeometry(QRect(90, 20, 421, 51))
        self.FP_email_label = QLabel(forgot_password_Form)
        self.FP_email_label.setObjectName(u"FP_email_label")
        self.FP_email_label.setGeometry(QRect(20, 30, 61, 31))
        self.FP_email_label.setFont(font)
        self.FP_new_password_lineEdit = QLineEdit(forgot_password_Form)
        self.FP_new_password_lineEdit.setObjectName(u"FP_new_password_lineEdit")
        self.FP_new_password_lineEdit.setGeometry(QRect(170, 90, 341, 51))
        self.FP_new_password_label = QLabel(forgot_password_Form)
        self.FP_new_password_label.setObjectName(u"FP_new_password_label")
        self.FP_new_password_label.setGeometry(QRect(20, 100, 141, 31))
        self.FP_new_password_label.setFont(font)
        self.FP_new_password_check_lineEdit = QLineEdit(forgot_password_Form)
        self.FP_new_password_check_lineEdit.setObjectName(u"FP_new_password_check_lineEdit")
        self.FP_new_password_check_lineEdit.setGeometry(QRect(170, 160, 341, 51))
        self.FP_new_password_check_label = QLabel(forgot_password_Form)
        self.FP_new_password_check_label.setObjectName(u"FP_new_password_check_label")
        self.FP_new_password_check_label.setGeometry(QRect(20, 170, 141, 31))
        self.FP_new_password_check_label.setFont(font)
        self.FP_save_pushButton = QPushButton(forgot_password_Form)
        self.FP_save_pushButton.setObjectName(u"FP_save_pushButton")
        self.FP_save_pushButton.setGeometry(QRect(170, 230, 151, 51))
        self.FP_save_pushButton.setFont(font)
        self.FP_cancel_pushButton = QPushButton(forgot_password_Form)
        self.FP_cancel_pushButton.setObjectName(u"FP_cancel_pushButton")
        self.FP_cancel_pushButton.setGeometry(QRect(360, 230, 151, 51))
        self.FP_cancel_pushButton.setFont(font)
        self.FP_check_email_pushButton = QPushButton(forgot_password_Form)
        self.FP_check_email_pushButton.setObjectName(u"FP_check_email_pushButton")
        self.FP_check_email_pushButton.setGeometry(QRect(515, 20, 81, 51))
        self.FP_check_email_pushButton.setFont(font)
        self.FP_check_email_pushButton.setStyleSheet(u"")
        self.FP_Password_like_label = QLabel(forgot_password_Form)
        self.FP_Password_like_label.setObjectName(u"FP_Password_like_label")
        self.FP_Password_like_label.setGeometry(QRect(530, 170, 41, 41))
        self.FP_Password_like_label.setFont(font)

        self.retranslateUi(forgot_password_Form)

        QMetaObject.connectSlotsByName(forgot_password_Form)
    # setupUi

    def retranslateUi(self, forgot_password_Form):
        forgot_password_Form.setWindowTitle(QCoreApplication.translate("forgot_password_Form", u"Form", None))
        self.FP_email_label.setText(QCoreApplication.translate("forgot_password_Form", u"Email :", None))
        self.FP_new_password_label.setText(QCoreApplication.translate("forgot_password_Form", u"New Passwrod :", None))
        self.FP_new_password_check_label.setText(QCoreApplication.translate("forgot_password_Form", u"New Passwrod :", None))
        self.FP_save_pushButton.setText(QCoreApplication.translate("forgot_password_Form", u"\u0e1a\u0e31\u0e19\u0e17\u0e36\u0e01", None))
        self.FP_cancel_pushButton.setText(QCoreApplication.translate("forgot_password_Form", u"\u0e22\u0e01\u0e40\u0e25\u0e34\u0e01", None))
        self.FP_check_email_pushButton.setText(QCoreApplication.translate("forgot_password_Form", u"\u0e40\u0e0a\u0e47\u0e04", None))
        self.FP_Password_like_label.setText("")
    # retranslateUi

