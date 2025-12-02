# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'micro_report.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QSizePolicy, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1270, 890)
        MainWindow.setMinimumSize(QSize(1270, 890))
        MainWindow.setMaximumSize(QSize(1270, 890))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.micro_page_label = QLabel(self.centralwidget)
        self.micro_page_label.setObjectName(u"micro_page_label")
        self.micro_page_label.setGeometry(QRect(1150, 0, 121, 31))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(20)
        self.micro_page_label.setFont(font)
        self.report_label = QLabel(self.centralwidget)
        self.report_label.setObjectName(u"report_label")
        self.report_label.setGeometry(QRect(60, 10, 160, 40))
        self.report_label.setMinimumSize(QSize(160, 40))
        self.report_label.setMaximumSize(QSize(160, 40))
        self.report_label.setFont(font)
        self.report_treeWidget = QTreeWidget(self.centralwidget)
        self.report_treeWidget.setObjectName(u"report_treeWidget")
        self.report_treeWidget.setGeometry(QRect(0, 50, 1100, 500))
        self.report_treeWidget.setMinimumSize(QSize(1100, 500))
        self.report_treeWidget.setMaximumSize(QSize(1100, 500))
        self.report_treeWidget.setFont(font)
        self.report_treeWidget.header().setDefaultSectionSize(175)
        MainWindow.setCentralWidget(self.centralwidget)
        self.report_treeWidget.raise_()
        self.micro_page_label.raise_()
        self.report_label.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.micro_page_label.setText(QCoreApplication.translate("MainWindow", u"micro bio page", None))
        self.report_label.setText(QCoreApplication.translate("MainWindow", u"\u0e23\u0e32\u0e22\u0e07\u0e32\u0e19\u0e2d\u0e13\u0e39\u0e0a\u0e35\u0e27\u0e27\u0e34\u0e17\u0e22\u0e32", None))
        ___qtreewidgetitem = self.report_treeWidget.headerItem()
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("MainWindow", u"\u0e23\u0e30\u0e14\u0e31\u0e1a\u0e04\u0e27\u0e32\u0e21\u0e40\u0e23\u0e48\u0e07\u0e14\u0e48\u0e27\u0e19", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("MainWindow", u"\u0e01\u0e32\u0e23\u0e40\u0e01\u0e47\u0e1a\u0e23\u0e31\u0e01\u0e29\u0e32", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"\u0e2b\u0e49\u0e2d\u0e07\u0e1b\u0e0f\u0e34\u0e1a\u0e31\u0e15\u0e34\u0e01\u0e32\u0e23", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"\u0e0a\u0e19\u0e34\u0e14\u0e2a\u0e31\u0e15\u0e27\u0e4c", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e25\u0e02\u0e01\u0e32\u0e23\u0e15\u0e23\u0e27\u0e08", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u0e27\u0e31\u0e19\u0e17\u0e35\u0e48\u0e23\u0e31\u0e1a\u0e40\u0e04\u0e2a", None));
    # retranslateUi

