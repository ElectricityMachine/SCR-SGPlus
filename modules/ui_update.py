# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'update.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .assets_rc import *
class Ui_Updater(object):
    def setupUi(self, Updater):
        if not Updater.objectName():
            Updater.setObjectName(u"Updater")
        Updater.resize(452, 248)
        Updater.setAcceptDrops(False)
        icon = QIcon()
        icon.addFile(u":/Icon/img/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        Updater.setWindowIcon(icon)
        Updater.setStyleSheet(u"#centralwidget {\n"
"        background-image: url(:/BackgroundImage/img/background.png);\n"
"        background-repeat: no-repeat; \n"
"        background-position: center;\n"
" }")
        self.centralwidget = QWidget(Updater)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.dropShadowFrame = QFrame(self.centralwidget)
        self.dropShadowFrame.setObjectName(u"dropShadowFrame")
        self.dropShadowFrame.setStyleSheet(u"QFrame {	\n"
"	background-color: rgba(255, 255, 255, .45);\n"
"    border-radius: 10px;\n"
"}")
        self.dropShadowFrame.setFrameShape(QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QFrame.Raised)
        self.sgTitle = QLabel(self.dropShadowFrame)
        self.sgTitle.setObjectName(u"sgTitle")
        self.sgTitle.setGeometry(QRect(10, 0, 271, 61))
        font = QFont()
        font.setFamily(u"Consolas")
        font.setPointSize(40)
        self.sgTitle.setFont(font)
        self.sgTitle.setStyleSheet(u"color: rgb(237,232,253);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.sgTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.dashboardTitle = QLabel(self.dropShadowFrame)
        self.dashboardTitle.setObjectName(u"dashboardTitle")
        self.dashboardTitle.setGeometry(QRect(0, 0, 431, 61))
        font1 = QFont()
        font1.setFamily(u"Consolas")
        font1.setPointSize(10)
        self.dashboardTitle.setFont(font1)
        self.dashboardTitle.setStyleSheet(u"color: rgb(247,183,183);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.dashboardTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.noButton = QPushButton(self.dropShadowFrame)
        self.noButton.setObjectName(u"noButton")
        self.noButton.setEnabled(True)
        self.noButton.setGeometry(QRect(240, 170, 141, 31))
        font2 = QFont()
        font2.setFamily(u"Consolas")
        self.noButton.setFont(font2)
        self.noButton.setStyleSheet(u"color: rgba(255, 255, 255, 255);\n"
"background-color: rgb(133,242,208);")
        self.yesButton = QPushButton(self.dropShadowFrame)
        self.yesButton.setObjectName(u"yesButton")
        self.yesButton.setEnabled(True)
        self.yesButton.setGeometry(QRect(50, 170, 141, 31))
        self.yesButton.setFont(font2)
        self.yesButton.setStyleSheet(u"color: rgba(255, 255, 255, 255);\n"
"background-color: rgb(133,242,208);")
        self.dashboardTitle_2 = QLabel(self.dropShadowFrame)
        self.dashboardTitle_2.setObjectName(u"dashboardTitle_2")
        self.dashboardTitle_2.setGeometry(QRect(0, 70, 431, 71))
        self.dashboardTitle_2.setFont(font1)
        self.dashboardTitle_2.setStyleSheet(u"color: rgb(247,183,183);\n"
"background-color: rgba(255, 255, 255, 0); \n"
"border: 1px solid rgb(247,183,183);")
        self.dashboardTitle_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.dashboardTitle_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.dropShadowFrame)

        Updater.setCentralWidget(self.centralwidget)

        self.retranslateUi(Updater)

        QMetaObject.connectSlotsByName(Updater)
    # setupUi

    def retranslateUi(self, Updater):
        Updater.setWindowTitle(QCoreApplication.translate("Updater", u"Signaller+", None))
        self.sgTitle.setText(QCoreApplication.translate("Updater", u"<html><head/><body><p><span style=\" font-size:18pt; font-weight:600; color:#12af86;\">SG+</span></p></body></html>", None))
        self.dashboardTitle.setText(QCoreApplication.translate("Updater", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600; font-style:italic; color:#12af86;\">Update Available</span></p></body></html>", None))
        self.noButton.setText(QCoreApplication.translate("Updater", u"No", None))
        self.yesButton.setText(QCoreApplication.translate("Updater", u"Yes", None))
        self.dashboardTitle_2.setText(QCoreApplication.translate("Updater", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; font-style:italic; color:#12af86;\">There is an update available for SGPlus. Would you like to be taken to the download page?</span></p><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; font-style:italic; color:#ff0000;\">(You can disable this in the settings!)</span></p></body></html>", None))
    # retranslateUi

