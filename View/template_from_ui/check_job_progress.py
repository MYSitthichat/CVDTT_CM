# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'check_job_progress.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_Check_job_MainWindow(object):
    def setupUi(self, Check_job_MainWindow):
        if not Check_job_MainWindow.objectName():
            Check_job_MainWindow.setObjectName(u"Check_job_MainWindow")
        Check_job_MainWindow.resize(1270, 890)
        Check_job_MainWindow.setStyleSheet(u"font-size: 16pt;")
        self.centralwidget = QWidget(Check_job_MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_check_title = QLabel(self.centralwidget)
        self.label_check_title.setObjectName(u"label_check_title")
        self.label_check_title.setGeometry(QRect(1040, 10, 211, 31))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_check_title.setFont(font)
        self.label_check_title.setStyleSheet(u"font-size: 12pt;")
        self.label_check_title.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.tableTop = QTableWidget(self.centralwidget)
        if (self.tableTop.columnCount() < 3):
            self.tableTop.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableTop.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableTop.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableTop.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableTop.setObjectName(u"tableTop")
        self.tableTop.setGeometry(QRect(20, 60, 1000, 350))
        self.tableTop.horizontalHeader().setDefaultSectionSize(320)
        self.tableTop.horizontalHeader().setStretchLastSection(True)
        self.btn_jobs_in_system = QPushButton(self.centralwidget)
        self.btn_jobs_in_system.setObjectName(u"btn_jobs_in_system")
        self.btn_jobs_in_system.setGeometry(QRect(1040, 60, 210, 61))
        self.btn_show_details = QPushButton(self.centralwidget)
        self.btn_show_details.setObjectName(u"btn_show_details")
        self.btn_show_details.setGeometry(QRect(1040, 480, 210, 61))
        self.label_details_header = QLabel(self.centralwidget)
        self.label_details_header.setObjectName(u"label_details_header")
        self.label_details_header.setGeometry(QRect(20, 440, 200, 31))
        font1 = QFont()
        font1.setPointSize(16)
        font1.setBold(True)
        self.label_details_header.setFont(font1)
        self.tableBottom = QTableWidget(self.centralwidget)
        if (self.tableBottom.columnCount() < 4):
            self.tableBottom.setColumnCount(4)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableBottom.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableBottom.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableBottom.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableBottom.setHorizontalHeaderItem(3, __qtablewidgetitem6)
        self.tableBottom.setObjectName(u"tableBottom")
        self.tableBottom.setGeometry(QRect(20, 480, 1000, 380))
        self.tableBottom.horizontalHeader().setDefaultSectionSize(220)
        self.tableBottom.horizontalHeader().setStretchLastSection(True)
        Check_job_MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(Check_job_MainWindow)

        QMetaObject.connectSlotsByName(Check_job_MainWindow)
    # setupUi

    def retranslateUi(self, Check_job_MainWindow):
        Check_job_MainWindow.setWindowTitle(QCoreApplication.translate("Check_job_MainWindow", u"Check Job Progress", None))
        self.label_check_title.setText(QCoreApplication.translate("Check_job_MainWindow", u"Check Job progress", None))
        ___qtablewidgetitem = self.tableTop.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Check_job_MainWindow", u"\u0e27\u0e31\u0e19\u0e40\u0e27\u0e25\u0e32\u0e2a\u0e16\u0e32\u0e19\u0e30\u0e1b\u0e31\u0e08\u0e08\u0e38\u0e1a\u0e31\u0e19", None));
        ___qtablewidgetitem1 = self.tableTop.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Check_job_MainWindow", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e25\u0e02\u0e1a\u0e32\u0e23\u0e4c\u0e42\u0e04\u0e49\u0e14", None));
        ___qtablewidgetitem2 = self.tableTop.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Check_job_MainWindow", u"\u0e2a\u0e16\u0e32\u0e19\u0e30\u0e1b\u0e31\u0e08\u0e08\u0e38\u0e1a\u0e31\u0e19", None));
        self.btn_jobs_in_system.setText(QCoreApplication.translate("Check_job_MainWindow", u"\u0e07\u0e32\u0e19\u0e17\u0e35\u0e48\u0e22\u0e31\u0e07\u0e2d\u0e22\u0e39\u0e48\u0e43\u0e19\u0e23\u0e30\u0e1a\u0e1a", None))
        self.btn_show_details.setText(QCoreApplication.translate("Check_job_MainWindow", u"\u0e41\u0e2a\u0e14\u0e07\u0e23\u0e32\u0e22\u0e25\u0e30\u0e40\u0e2d\u0e35\u0e22\u0e14", None))
        self.label_details_header.setText(QCoreApplication.translate("Check_job_MainWindow", u"\u0e23\u0e32\u0e22\u0e25\u0e30\u0e40\u0e2d\u0e35\u0e22\u0e14", None))
        ___qtablewidgetitem3 = self.tableBottom.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Check_job_MainWindow", u"\u0e40\u0e27\u0e25\u0e32", None));
        ___qtablewidgetitem4 = self.tableBottom.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Check_job_MainWindow", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e25\u0e02\u0e1a\u0e32\u0e23\u0e4c\u0e42\u0e04\u0e49\u0e14", None));
        ___qtablewidgetitem5 = self.tableBottom.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Check_job_MainWindow", u"\u0e23\u0e32\u0e22\u0e25\u0e30\u0e40\u0e2d\u0e35\u0e22\u0e14", None));
        ___qtablewidgetitem6 = self.tableBottom.horizontalHeaderItem(3)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Check_job_MainWindow", u"\u0e1c\u0e39\u0e49\u0e14\u0e33\u0e40\u0e19\u0e34\u0e19\u0e07\u0e32\u0e19", None));
    # retranslateUi

