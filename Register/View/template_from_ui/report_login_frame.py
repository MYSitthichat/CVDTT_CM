# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'report_login.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1400, 900)
        MainWindow.setMinimumSize(QSize(1400, 900))
        MainWindow.setMaximumSize(QSize(1400, 900))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(430, 210, 290, 190))
        self.groupBox.setMinimumSize(QSize(290, 190))
        self.groupBox.setMaximumSize(QSize(290, 190))
        self.groupBox.setStyleSheet(u"background-color: rgb(170, 255, 127);")
        self.password_lineEdit = QLineEdit(self.groupBox)
        self.password_lineEdit.setObjectName(u"password_lineEdit")
        self.password_lineEdit.setGeometry(QRect(10, 110, 270, 30))
        self.password_lineEdit.setMinimumSize(QSize(270, 30))
        self.password_lineEdit.setMaximumSize(QSize(270, 30))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(16)
        self.password_lineEdit.setFont(font)
        self.password_lineEdit.setStyleSheet(u"background-color: rgb(255,255,255);")
        self.username_label = QLabel(self.groupBox)
        self.username_label.setObjectName(u"username_label")
        self.username_label.setGeometry(QRect(10, 10, 90, 20))
        self.username_label.setMinimumSize(QSize(90, 20))
        self.username_label.setMaximumSize(QSize(90, 20))
        font1 = QFont()
        font1.setFamilies([u"TH Niramit AS"])
        font1.setPointSize(20)
        self.username_label.setFont(font1)
        self.username_lineEdit = QLineEdit(self.groupBox)
        self.username_lineEdit.setObjectName(u"username_lineEdit")
        self.username_lineEdit.setGeometry(QRect(10, 40, 270, 30))
        self.username_lineEdit.setMinimumSize(QSize(270, 30))
        self.username_lineEdit.setMaximumSize(QSize(270, 30))
        self.username_lineEdit.setFont(font)
        self.username_lineEdit.setStyleSheet(u"background-color: rgb(255,255,255);")
        self.password_label = QLabel(self.groupBox)
        self.password_label.setObjectName(u"password_label")
        self.password_label.setGeometry(QRect(10, 80, 90, 20))
        self.password_label.setMinimumSize(QSize(90, 20))
        self.password_label.setMaximumSize(QSize(90, 20))
        self.password_label.setFont(font1)
        self.login_pushButton = QPushButton(self.groupBox)
        self.login_pushButton.setObjectName(u"login_pushButton")
        self.login_pushButton.setGeometry(QRect(190, 150, 90, 30))
        self.login_pushButton.setMinimumSize(QSize(90, 30))
        self.login_pushButton.setMaximumSize(QSize(90, 30))
        self.login_pushButton.setFont(font1)
        self.login_pushButton.setStyleSheet(u"background-color: rgb(255,255,255);")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle("")
        self.username_label.setText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.password_label.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.login_pushButton.setText(QCoreApplication.translate("MainWindow", u"Login", None))
    # retranslateUi

