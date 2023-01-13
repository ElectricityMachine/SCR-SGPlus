# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'update.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)
from .resources_rc import *
class Ui_UpdateWindow(object):
    def setupUi(self, UpdateWindow):
        if not UpdateWindow.objectName():
            UpdateWindow.setObjectName(u"UpdateWindow")
        UpdateWindow.resize(513, 285)
        UpdateWindow.setAcceptDrops(False)
        icon = QIcon()
        icon.addFile(u":/images/icon.ico", QSize(), QIcon.Normal, QIcon.Off)
        UpdateWindow.setWindowIcon(icon)
        UpdateWindow.setStyleSheet(u"QPushButton {\n"
"	border: 1px solid rgb(239, 239, 239);\n"
"	border-radius: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid rgb(239, 239, 239);\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid rgb(204, 105, 161);\n"
"}\n"
"QWidget {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 175, 189, 255), stop:1 rgba(255, 195, 160, 255));\n"
"}\n"
"")
        self.centralwidget = QWidget(UpdateWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.dropShadowFrame = QFrame(self.centralwidget)
        self.dropShadowFrame.setObjectName(u"dropShadowFrame")
        self.dropShadowFrame.setStyleSheet(u"QFrame {	\n"
"	background-color: rgba(255, 255, 255, .15);\n"
"}")
        self.dropShadowFrame.setFrameShape(QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.dropShadowFrame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 491, 41))
        self.label.setStyleSheet(u"font: 81 14pt \"Raleway ExtraBold\";\n"
"color: rgb(239, 239, 239);\n"
"")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label_2 = QLabel(self.dropShadowFrame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 60, 491, 121))
        self.label_2.setStyleSheet(u"font: 81 14pt \"Raleway ExtraBold\";\n"
"color: rgb(204, 105, 161);")
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.updateButton = QPushButton(self.dropShadowFrame)
        self.updateButton.setObjectName(u"updateButton")
        self.updateButton.setGeometry(QRect(110, 210, 111, 23))
        self.updateButton.setStyleSheet(u"color: rgb(204, 105, 161);")
        self.skipButton = QPushButton(self.dropShadowFrame)
        self.skipButton.setObjectName(u"skipButton")
        self.skipButton.setGeometry(QRect(274, 210, 111, 23))
        self.skipButton.setStyleSheet(u"color: rgb(204, 105, 161);")

        self.verticalLayout.addWidget(self.dropShadowFrame)

        UpdateWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(UpdateWindow)

        QMetaObject.connectSlotsByName(UpdateWindow)
    # setupUi

    def retranslateUi(self, UpdateWindow):
        UpdateWindow.setWindowTitle(QCoreApplication.translate("UpdateWindow", u"SG+", None))
        self.label.setText(QCoreApplication.translate("UpdateWindow", u"Update for SG+ available!", None))
        self.label_2.setText(QCoreApplication.translate("UpdateWindow", u"<html><head/><body><p align=\"justify\">It is <span style=\" text-decoration: underline;\">always</span> recommended to update to the latest version. To do so, click the update button below and follow the instructions under &quot;<span style=\" font-style:italic;\">Installation</span>&quot;.</p></body></html>", None))
        self.updateButton.setText(QCoreApplication.translate("UpdateWindow", u"Update", None))
        self.skipButton.setText(QCoreApplication.translate("UpdateWindow", u"Skip", None))
    # retranslateUi

