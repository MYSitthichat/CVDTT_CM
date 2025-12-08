# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_app.ui'
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
from PySide6.QtWidgets import (QApplication, QCommandLinkButton, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_login_MainWindow(object):
    def setupUi(self, login_MainWindow):
        if not login_MainWindow.objectName():
            login_MainWindow.setObjectName(u"login_MainWindow")
        login_MainWindow.resize(600, 250)
        login_MainWindow.setMinimumSize(QSize(600, 250))
        login_MainWindow.setMaximumSize(QSize(600, 250))
        login_MainWindow.setSizeIncrement(QSize(600, 250))
        self.centralwidget = QWidget(login_MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.user_lineEdit = QLineEdit(self.centralwidget)
        self.user_lineEdit.setObjectName(u"user_lineEdit")
        self.user_lineEdit.setGeometry(QRect(140, 30, 341, 41))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(24)
        font.setBold(True)
        self.user_lineEdit.setFont(font)
        self.user_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_lineEdit.setClearButtonEnabled(True)
        self.user_label = QLabel(self.centralwidget)
        self.user_label.setObjectName(u"user_label")
        self.user_label.setGeometry(QRect(50, 40, 81, 21))
        self.user_label.setFont(font)
        self.password_label = QLabel(self.centralwidget)
        self.password_label.setObjectName(u"password_label")
        self.password_label.setGeometry(QRect(50, 110, 81, 21))
        self.password_label.setFont(font)
        self.password_lineEdit = QLineEdit(self.centralwidget)
        self.password_lineEdit.setObjectName(u"password_lineEdit")
        self.password_lineEdit.setGeometry(QRect(140, 100, 341, 41))
        self.password_lineEdit.setFont(font)
        self.password_lineEdit.setAutoFillBackground(False)
        self.password_lineEdit.setCursorPosition(0)
        self.password_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_lineEdit.setClearButtonEnabled(False)
        self.login_pushButton = QPushButton(self.centralwidget)
        self.login_pushButton.setObjectName(u"login_pushButton")
        self.login_pushButton.setGeometry(QRect(140, 170, 151, 51))
        font1 = QFont()
        font1.setFamilies([u"TH Niramit AS"])
        font1.setPointSize(20)
        font1.setBold(True)
        self.login_pushButton.setFont(font1)
        self.cancel_pushButton = QPushButton(self.centralwidget)
        self.cancel_pushButton.setObjectName(u"cancel_pushButton")
        self.cancel_pushButton.setGeometry(QRect(330, 170, 151, 51))
        self.cancel_pushButton.setFont(font1)
        self.forgot_password_commandLinkButton = QCommandLinkButton(self.centralwidget)
        self.forgot_password_commandLinkButton.setObjectName(u"forgot_password_commandLinkButton")
        self.forgot_password_commandLinkButton.setGeometry(QRect(485, 100, 111, 41))
        login_MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(login_MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        login_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(login_MainWindow)

        QMetaObject.connectSlotsByName(login_MainWindow)
    # setupUi

    def retranslateUi(self, login_MainWindow):
        login_MainWindow.setWindowTitle(QCoreApplication.translate("login_MainWindow", u"LOGIN", None))
        self.user_label.setText(QCoreApplication.translate("login_MainWindow", u"USER ::", None))
        self.password_label.setText(QCoreApplication.translate("login_MainWindow", u"PASS ::", None))
        self.login_pushButton.setText(QCoreApplication.translate("login_MainWindow", u"LOGIN", None))
        self.cancel_pushButton.setText(QCoreApplication.translate("login_MainWindow", u"CANCEL", None))
        self.forgot_password_commandLinkButton.setText(QCoreApplication.translate("login_MainWindow", u"\u0e25\u0e37\u0e21\u0e23\u0e2b\u0e31\u0e2a\u0e1c\u0e48\u0e32\u0e19", None))
    # retranslateUi

