# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_app.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QMainWindow, QPushButton,
    QSizePolicy, QStackedWidget, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1550, 900)
        MainWindow.setMinimumSize(QSize(1550, 900))
        MainWindow.setMaximumSize(QSize(1550, 900))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(5, 5, 265, 890))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Plain)
        self.frame.setLineWidth(2)
        self.register_new_customer_pushButton = QPushButton(self.frame)
        self.register_new_customer_pushButton.setObjectName(u"register_new_customer_pushButton")
        self.register_new_customer_pushButton.setGeometry(QRect(7, 10, 251, 51))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(24)
        font.setBold(True)
        self.register_new_customer_pushButton.setFont(font)
        self.new_work_pushButton = QPushButton(self.frame)
        self.new_work_pushButton.setObjectName(u"new_work_pushButton")
        self.new_work_pushButton.setGeometry(QRect(7, 70, 251, 51))
        self.new_work_pushButton.setFont(font)
        self.logout_pushButton = QPushButton(self.frame)
        self.logout_pushButton.setObjectName(u"logout_pushButton")
        self.logout_pushButton.setGeometry(QRect(7, 830, 251, 51))
        self.logout_pushButton.setFont(font)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(275, 5, 1270, 890))
        self.stackedWidget.setFrameShape(QFrame.Shape.Box)
        self.stackedWidget.setLineWidth(2)
        self.register_new_customer_page = QWidget()
        self.register_new_customer_page.setObjectName(u"register_new_customer_page")
        self.stackedWidget.addWidget(self.register_new_customer_page)
        self.new_work_page = QWidget()
        self.new_work_page.setObjectName(u"new_work_page")
        self.stackedWidget.addWidget(self.new_work_page)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"REPORT LAB", None))
        self.register_new_customer_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0e23\u0e31\u0e1a\u0e43\u0e1a\u0e2a\u0e48\u0e07\u0e41\u0e25\u0e1b", None))
        self.new_work_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0e2a\u0e23\u0e49\u0e32\u0e07 REPORT", None))
        self.logout_pushButton.setText(QCoreApplication.translate("MainWindow", u"LOGOUT", None))
    # retranslateUi

