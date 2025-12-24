# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lab_edite_form.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTextEdit, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_lab_Edite_form_Form(object):
    def setupUi(self, lab_Edite_form_Form):
        if not lab_Edite_form_Form.objectName():
            lab_Edite_form_Form.setObjectName(u"lab_Edite_form_Form")
        lab_Edite_form_Form.resize(1270, 890)
        lab_Edite_form_Form.setMinimumSize(QSize(1270, 890))
        lab_Edite_form_Form.setMaximumSize(QSize(1270, 890))
        lab_Edite_form_Form.setSizeIncrement(QSize(1270, 890))
        lab_Edite_form_Form.setBaseSize(QSize(1270, 890))
        self.list_detail_treeWidget = QTreeWidget(lab_Edite_form_Form)
        __qtreewidgetitem = QTreeWidgetItem(self.list_detail_treeWidget)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        self.list_detail_treeWidget.setObjectName(u"list_detail_treeWidget")
        self.list_detail_treeWidget.setGeometry(QRect(5, 5, 1261, 361))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(20)
        font.setBold(True)
        self.list_detail_treeWidget.setFont(font)
        self.list_detail_treeWidget.header().setMinimumSectionSize(50)
        self.list_detail_treeWidget.header().setDefaultSectionSize(300)
        self.Edte_form_pushButton = QPushButton(lab_Edite_form_Form)
        self.Edte_form_pushButton.setObjectName(u"Edte_form_pushButton")
        self.Edte_form_pushButton.setGeometry(QRect(210, 370, 171, 61))
        self.Edte_form_pushButton.setFont(font)
        self.Delete_form_pushButton = QPushButton(lab_Edite_form_Form)
        self.Delete_form_pushButton.setObjectName(u"Delete_form_pushButton")
        self.Delete_form_pushButton.setGeometry(QRect(420, 370, 171, 61))
        self.Delete_form_pushButton.setFont(font)
        self.lab_name_label = QLabel(lab_Edite_form_Form)
        self.lab_name_label.setObjectName(u"lab_name_label")
        self.lab_name_label.setGeometry(QRect(10, 450, 71, 31))
        self.lab_name_label.setFont(font)
        self.lab_name_comboBox = QComboBox(lab_Edite_form_Form)
        self.lab_name_comboBox.setObjectName(u"lab_name_comboBox")
        self.lab_name_comboBox.setGeometry(QRect(80, 445, 710, 41))
        self.Download_form_pushButton = QPushButton(lab_Edite_form_Form)
        self.Download_form_pushButton.setObjectName(u"Download_form_pushButton")
        self.Download_form_pushButton.setGeometry(QRect(5, 370, 171, 61))
        self.Download_form_pushButton.setFont(font)
        self.detail_from_label = QLabel(lab_Edite_form_Form)
        self.detail_from_label.setObjectName(u"detail_from_label")
        self.detail_from_label.setGeometry(QRect(10, 570, 101, 31))
        self.detail_from_label.setFont(font)
        self.detail_from_textEdit = QTextEdit(lab_Edite_form_Form)
        self.detail_from_textEdit.setObjectName(u"detail_from_textEdit")
        self.detail_from_textEdit.setGeometry(QRect(5, 605, 785, 275))
        self.detail_from_textEdit.setFont(font)
        self.form_name_label = QLabel(lab_Edite_form_Form)
        self.form_name_label.setObjectName(u"form_name_label")
        self.form_name_label.setGeometry(QRect(10, 490, 111, 31))
        self.form_name_label.setFont(font)
        self.form_name_lineEdit = QLineEdit(lab_Edite_form_Form)
        self.form_name_lineEdit.setObjectName(u"form_name_lineEdit")
        self.form_name_lineEdit.setGeometry(QRect(5, 525, 785, 41))
        self.form_name_lineEdit.setFont(font)
        self.form_name_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.save_form_pushButton = QPushButton(lab_Edite_form_Form)
        self.save_form_pushButton.setObjectName(u"save_form_pushButton")
        self.save_form_pushButton.setGeometry(QRect(620, 370, 171, 61))
        self.save_form_pushButton.setFont(font)
        self.new_lab_frame = QFrame(lab_Edite_form_Form)
        self.new_lab_frame.setObjectName(u"new_lab_frame")
        self.new_lab_frame.setGeometry(QRect(800, 370, 465, 511))
        self.new_lab_frame.setFrameShape(QFrame.Shape.Box)
        self.new_lab_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.new_lab_name_label = QLabel(self.new_lab_frame)
        self.new_lab_name_label.setObjectName(u"new_lab_name_label")
        self.new_lab_name_label.setGeometry(QRect(10, 50, 71, 31))
        self.new_lab_name_label.setFont(font)
        self.new_lab_detail_label = QLabel(self.new_lab_frame)
        self.new_lab_detail_label.setObjectName(u"new_lab_detail_label")
        self.new_lab_detail_label.setGeometry(QRect(10, 150, 101, 31))
        self.new_lab_detail_label.setFont(font)
        self.save_new_lab_pushButton = QPushButton(self.new_lab_frame)
        self.save_new_lab_pushButton.setObjectName(u"save_new_lab_pushButton")
        self.save_new_lab_pushButton.setGeometry(QRect(285, 445, 171, 61))
        self.save_new_lab_pushButton.setFont(font)
        self.add_new_lab_label = QLabel(self.new_lab_frame)
        self.add_new_lab_label.setObjectName(u"add_new_lab_label")
        self.add_new_lab_label.setGeometry(QRect(180, 10, 111, 31))
        self.add_new_lab_label.setFont(font)
        self.new_lab_name_lineEdit = QLineEdit(lab_Edite_form_Form)
        self.new_lab_name_lineEdit.setObjectName(u"new_lab_name_lineEdit")
        self.new_lab_name_lineEdit.setGeometry(QRect(810, 460, 445, 41))
        self.new_lab_name_lineEdit.setFont(font)
        self.new_lab_name_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.new_lab_detail_textEdit = QTextEdit(lab_Edite_form_Form)
        self.new_lab_detail_textEdit.setObjectName(u"new_lab_detail_textEdit")
        self.new_lab_detail_textEdit.setGeometry(QRect(810, 559, 445, 251))
        self.new_lab_detail_textEdit.setFont(font)

        self.retranslateUi(lab_Edite_form_Form)

        QMetaObject.connectSlotsByName(lab_Edite_form_Form)
    # setupUi

    def retranslateUi(self, lab_Edite_form_Form):
        lab_Edite_form_Form.setWindowTitle(QCoreApplication.translate("lab_Edite_form_Form", u"Form", None))
        ___qtreewidgetitem = self.list_detail_treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("lab_Edite_form_Form", u"\u0e23\u0e32\u0e22\u0e25\u0e30\u0e40\u0e2d\u0e35\u0e22\u0e14", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("lab_Edite_form_Form", u"\u0e08\u0e33\u0e19\u0e27\u0e19\u0e41\u0e1a\u0e1a\u0e1f\u0e2d\u0e23\u0e4c\u0e21", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("lab_Edite_form_Form", u"\u0e0a\u0e37\u0e48\u0e2d\u0e41\u0e25\u0e1b", None));

        __sortingEnabled = self.list_detail_treeWidget.isSortingEnabled()
        self.list_detail_treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.list_detail_treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("lab_Edite_form_Form", u"4", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("lab_Edite_form_Form", u"Bacteria", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("lab_Edite_form_Form", u"\u0e43\u0e2b\u0e49\u0e22\u0e32\u0e25\u0e30\u0e21\u0e31\u0e49\u0e07", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("lab_Edite_form_Form", u"1", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("lab_Edite_form_Form", u"Bac PCR", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem3.setText(2, QCoreApplication.translate("lab_Edite_form_Form", u"\u0e2b\u0e23\u0e37\u0e2d\u0e44\u0e21\u0e48\u0e43\u0e2b\u0e49\u0e14\u0e35", None));
        ___qtreewidgetitem3.setText(1, QCoreApplication.translate("lab_Edite_form_Form", u"1", None));
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("lab_Edite_form_Form", u"Bac qPCR", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem1.child(2)
        ___qtreewidgetitem4.setText(2, QCoreApplication.translate("lab_Edite_form_Form", u"\u0e43\u0e2b\u0e49\u0e14\u0e35\u0e01\u0e27\u0e48\u0e32", None));
        ___qtreewidgetitem4.setText(1, QCoreApplication.translate("lab_Edite_form_Form", u"1", None));
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("lab_Edite_form_Form", u"Bac Ex", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem1.child(3)
        ___qtreewidgetitem5.setText(2, QCoreApplication.translate("lab_Edite_form_Form", u"\u0e44\u0e21\u0e48\u0e43\u0e2b\u0e49\u0e42\u0e27\u0e49\u0e22\u0e22\u0e22", None));
        ___qtreewidgetitem5.setText(1, QCoreApplication.translate("lab_Edite_form_Form", u"1", None));
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("lab_Edite_form_Form", u"Bac CCPr", None));
        self.list_detail_treeWidget.setSortingEnabled(__sortingEnabled)

        self.Edte_form_pushButton.setText(QCoreApplication.translate("lab_Edite_form_Form", u"\u0e40\u0e1e\u0e34\u0e48\u0e21\u0e41\u0e1a\u0e1a\u0e1f\u0e2d\u0e23\u0e4c\u0e21", None))
        self.Delete_form_pushButton.setText(QCoreApplication.translate("lab_Edite_form_Form", u"\u0e25\u0e1a\u0e41\u0e1a\u0e1a\u0e1f\u0e2d\u0e23\u0e4c\u0e21", None))
        self.lab_name_label.setText(QCoreApplication.translate("lab_Edite_form_Form", u"\u0e0a\u0e37\u0e48\u0e2d\u0e41\u0e25\u0e1b", None))
        self.Download_form_pushButton.setText(QCoreApplication.translate("lab_Edite_form_Form", u"\u0e14\u0e32\u0e27\u0e19\u0e4c\u0e42\u0e2b\u0e25\u0e14\u0e1f\u0e2d\u0e23\u0e4c\u0e21", None))
        self.detail_from_label.setText(QCoreApplication.translate("lab_Edite_form_Form", u"\u0e23\u0e32\u0e22\u0e25\u0e30\u0e40\u0e2d\u0e35\u0e22\u0e14", None))
        self.form_name_label.setText(QCoreApplication.translate("lab_Edite_form_Form", u"\u0e0a\u0e37\u0e48\u0e2d\u0e41\u0e1a\u0e1a\u0e1f\u0e2d\u0e23\u0e4c\u0e21", None))
        self.save_form_pushButton.setText(QCoreApplication.translate("lab_Edite_form_Form", u"\u0e1a\u0e31\u0e19\u0e17\u0e36\u0e01\u0e41\u0e1a\u0e1a\u0e1f\u0e2d\u0e23\u0e4c\u0e21", None))
        self.new_lab_name_label.setText(QCoreApplication.translate("lab_Edite_form_Form", u"\u0e0a\u0e37\u0e48\u0e2d\u0e41\u0e25\u0e1b", None))
        self.new_lab_detail_label.setText(QCoreApplication.translate("lab_Edite_form_Form", u"\u0e23\u0e32\u0e22\u0e25\u0e30\u0e40\u0e2d\u0e35\u0e22\u0e14", None))
        self.save_new_lab_pushButton.setText(QCoreApplication.translate("lab_Edite_form_Form", u"\u0e1a\u0e31\u0e19\u0e17\u0e36\u0e01", None))
        self.add_new_lab_label.setText(QCoreApplication.translate("lab_Edite_form_Form", u"\u0e40\u0e1e\u0e34\u0e48\u0e21\u0e41\u0e25\u0e1b\u0e43\u0e2b\u0e21\u0e48", None))
    # retranslateUi

