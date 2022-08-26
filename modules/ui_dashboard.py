# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dashboard.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .assets_rc import *
class Ui_Dashboard(object):
    def setupUi(self, Dashboard):
        if not Dashboard.objectName():
            Dashboard.setObjectName(u"Dashboard")
        Dashboard.resize(592, 482)
        Dashboard.setAcceptDrops(False)
        icon = QIcon()
        icon.addFile(u":/Icon/img/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        Dashboard.setWindowIcon(icon)
        Dashboard.setStyleSheet(u"#centralwidget {\n"
"        background-image: url(:/BackgroundImage/img/background.png);\n"
"        background-repeat: no-repeat; \n"
"        background-position: center;\n"
" }")
        self.centralwidget = QWidget(Dashboard)
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
        self.dashboardTitle.setGeometry(QRect(0, 0, 571, 61))
        font1 = QFont()
        font1.setFamily(u"Consolas")
        font1.setPointSize(10)
        self.dashboardTitle.setFont(font1)
        self.dashboardTitle.setStyleSheet(u"color: rgb(247,183,183);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.dashboardTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.exitButton = QPushButton(self.dropShadowFrame)
        self.exitButton.setObjectName(u"exitButton")
        self.exitButton.setGeometry(QRect(490, 430, 75, 23))
        font2 = QFont()
        font2.setFamily(u"Consolas")
        self.exitButton.setFont(font2)
        self.exitButton.setStyleSheet(u"color: rgba(255, 255, 255, 255);\n"
"background-color: rgb(133,242,208);")
        self.versionTitle = QLabel(self.dropShadowFrame)
        self.versionTitle.setObjectName(u"versionTitle")
        self.versionTitle.setGeometry(QRect(10, 430, 81, 31))
        self.versionTitle.setFont(font1)
        self.versionTitle.setStyleSheet(u"color: rgb(237,232,253);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.versionTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.initialiseButton = QPushButton(self.dropShadowFrame)
        self.initialiseButton.setObjectName(u"initialiseButton")
        self.initialiseButton.setEnabled(True)
        self.initialiseButton.setGeometry(QRect(10, 70, 171, 31))
        self.initialiseButton.setFont(font2)
        self.initialiseButton.setStyleSheet(u"color: rgba(255, 255, 255, 255);\n"
"background-color: rgb(133,242,208);")
        self.consoleOutput = QLabel(self.dropShadowFrame)
        self.consoleOutput.setObjectName(u"consoleOutput")
        self.consoleOutput.setGeometry(QRect(200, 380, 271, 71))
        self.consoleOutput.setFont(font1)
        self.consoleOutput.setStyleSheet(u"color: rgb(247,183,183);\n"
"background-color: rgba(255, 255, 255, 0); \n"
"border: 1px solid;\n"
"border-color: rgb(247,183,183);")
        self.consoleOutput.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.consoleOutput.setWordWrap(True)
        self.consoleHeader = QLabel(self.dropShadowFrame)
        self.consoleHeader.setObjectName(u"consoleHeader")
        self.consoleHeader.setGeometry(QRect(200, 340, 91, 31))
        self.consoleHeader.setFont(font1)
        self.consoleHeader.setStyleSheet(u"color: rgb(237,232,253);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.consoleHeader.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.enableButton = QPushButton(self.dropShadowFrame)
        self.enableButton.setObjectName(u"enableButton")
        self.enableButton.setEnabled(True)
        self.enableButton.setGeometry(QRect(10, 120, 171, 31))
        self.enableButton.setFont(font2)
        self.enableButton.setStyleSheet(u"color: rgba(255, 255, 255, 255);\n"
"background-color: rgb(133,242,208);")
        self.statusText = QLabel(self.dropShadowFrame)
        self.statusText.setObjectName(u"statusText")
        self.statusText.setGeometry(QRect(480, 340, 91, 31))
        self.statusText.setFont(font1)
        self.statusText.setStyleSheet(u"color: rgb(237,232,253);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.statusText.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.statusTitle = QLabel(self.dropShadowFrame)
        self.statusTitle.setObjectName(u"statusTitle")
        self.statusTitle.setGeometry(QRect(380, 340, 91, 31))
        self.statusTitle.setFont(font1)
        self.statusTitle.setStyleSheet(u"color: rgb(237,232,253);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.statusTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.creditsButton = QPushButton(self.dropShadowFrame)
        self.creditsButton.setObjectName(u"creditsButton")
        self.creditsButton.setEnabled(True)
        self.creditsButton.setGeometry(QRect(10, 170, 81, 31))
        self.creditsButton.setFont(font2)
        self.creditsButton.setStyleSheet(u"color: rgba(255, 255, 255, 255);\n"
"background-color: rgb(133,242,208);")
        self.githubButton = QPushButton(self.dropShadowFrame)
        self.githubButton.setObjectName(u"githubButton")
        self.githubButton.setEnabled(True)
        self.githubButton.setGeometry(QRect(100, 170, 81, 31))
        self.githubButton.setFont(font2)
        self.githubButton.setStyleSheet(u"color: rgba(255, 255, 255, 255);\n"
"background-color: rgb(133,242,208);")
        self.reportButton = QPushButton(self.dropShadowFrame)
        self.reportButton.setObjectName(u"reportButton")
        self.reportButton.setEnabled(True)
        self.reportButton.setGeometry(QRect(10, 210, 81, 31))
        self.reportButton.setFont(font2)
        self.reportButton.setStyleSheet(u"color: rgba(255, 255, 255, 255);\n"
"background-color: rgb(255, 0, 0);")
        self.howtoButton = QPushButton(self.dropShadowFrame)
        self.howtoButton.setObjectName(u"howtoButton")
        self.howtoButton.setEnabled(True)
        self.howtoButton.setGeometry(QRect(100, 210, 81, 31))
        self.howtoButton.setFont(font2)
        self.howtoButton.setStyleSheet(u"color: rgba(255, 255, 255, 255);\n"
"background-color: rgb(204, 153, 0);")
        self.creditsTitle = QLabel(self.dropShadowFrame)
        self.creditsTitle.setObjectName(u"creditsTitle")
        self.creditsTitle.setGeometry(QRect(10, 250, 221, 71))
        self.creditsTitle.setFont(font1)
        self.creditsTitle.setStyleSheet(u"color: rgb(247,183,183);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.creditsTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.creditsTitle.setWordWrap(True)
        self.howtomenu = QWidget(self.dropShadowFrame)
        self.howtomenu.setObjectName(u"howtomenu")
        self.howtomenu.setGeometry(QRect(220, 60, 341, 191))
        self.howtomenu.setStyleSheet(u"border: 1px solid;\n"
"border-color: rgb(247,183,183);")
        self.redSignal = QLabel(self.howtomenu)
        self.redSignal.setObjectName(u"redSignal")
        self.redSignal.setGeometry(QRect(0, 60, 32, 31))
        self.redSignal.setFont(font1)
        self.redSignal.setStyleSheet(u"color: rgb(237,232,253);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.redSignal.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.redSignal_2 = QLabel(self.howtomenu)
        self.redSignal_2.setObjectName(u"redSignal_2")
        self.redSignal_2.setGeometry(QRect(0, 100, 31, 31))
        self.redSignal_2.setFont(font1)
        self.redSignal_2.setStyleSheet(u"color: rgb(237,232,253);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.redSignal_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.redSignal_2.setWordWrap(True)
        self.redSignal_4 = QLabel(self.howtomenu)
        self.redSignal_4.setObjectName(u"redSignal_4")
        self.redSignal_4.setGeometry(QRect(0, 140, 32, 31))
        self.redSignal_4.setFont(font1)
        self.redSignal_4.setStyleSheet(u"color: rgb(237,232,253);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.redSignal_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.versionTitle_2 = QLabel(self.howtomenu)
        self.versionTitle_2.setObjectName(u"versionTitle_2")
        self.versionTitle_2.setGeometry(QRect(40, 60, 301, 31))
        self.versionTitle_2.setFont(font1)
        self.versionTitle_2.setStyleSheet(u"color: rgb(237,232,253);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.versionTitle_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.versionTitle_2.setWordWrap(True)
        self.versionTitle_3 = QLabel(self.howtomenu)
        self.versionTitle_3.setObjectName(u"versionTitle_3")
        self.versionTitle_3.setGeometry(QRect(40, 100, 301, 31))
        self.versionTitle_3.setFont(font1)
        self.versionTitle_3.setStyleSheet(u"color: rgb(237,232,253);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.versionTitle_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.versionTitle_3.setWordWrap(True)
        self.versionTitle_4 = QLabel(self.howtomenu)
        self.versionTitle_4.setObjectName(u"versionTitle_4")
        self.versionTitle_4.setGeometry(QRect(40, 140, 301, 31))
        self.versionTitle_4.setFont(font1)
        self.versionTitle_4.setStyleSheet(u"color: rgb(237,232,253);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.versionTitle_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.versionTitle_4.setWordWrap(True)
        self.versionTitle_5 = QLabel(self.howtomenu)
        self.versionTitle_5.setObjectName(u"versionTitle_5")
        self.versionTitle_5.setGeometry(QRect(0, 0, 341, 51))
        self.versionTitle_5.setFont(font1)
        self.versionTitle_5.setStyleSheet(u"color: rgb(237,232,253);\n"
"background-color: rgba(255, 255, 255, 0); ")
        self.versionTitle_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.autoUpdateBox = QCheckBox(self.dropShadowFrame)
        self.autoUpdateBox.setObjectName(u"autoUpdateBox")
        self.autoUpdateBox.setGeometry(QRect(10, 260, 171, 17))
        self.autoUpdateBox.setStyleSheet(u"color: #12af86;\n"
"font-size:10pt; \n"
"font-weight:600; ")

        self.verticalLayout.addWidget(self.dropShadowFrame)

        Dashboard.setCentralWidget(self.centralwidget)

        self.retranslateUi(Dashboard)

        QMetaObject.connectSlotsByName(Dashboard)
    # setupUi

    def retranslateUi(self, Dashboard):
        Dashboard.setWindowTitle(QCoreApplication.translate("Dashboard", u"Signaller+", None))
        self.sgTitle.setText(QCoreApplication.translate("Dashboard", u"<html><head/><body><p><span style=\" font-size:18pt; font-weight:600; color:#12af86;\">SG+</span></p></body></html>", None))
        self.dashboardTitle.setText(QCoreApplication.translate("Dashboard", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600; font-style:italic; color:#12af86;\">Dashboard</span></p></body></html>", None))
        self.exitButton.setText(QCoreApplication.translate("Dashboard", u"Exit", None))
        self.versionTitle.setText(QCoreApplication.translate("Dashboard", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:600; font-style:italic; color:#12af86;\">v0.3</span></p></body></html>", None))
        self.initialiseButton.setText(QCoreApplication.translate("Dashboard", u"Initialise", None))
        self.consoleOutput.setText(QCoreApplication.translate("Dashboard", u"<html><head/><body><p><br/></p></body></html>", None))
        self.consoleHeader.setText(QCoreApplication.translate("Dashboard", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; font-style:italic; color:#12af86;\">Console:</span></p></body></html>", None))
        self.enableButton.setText(QCoreApplication.translate("Dashboard", u"Enable", None))
        self.statusText.setText(QCoreApplication.translate("Dashboard", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ff0000;\">Disabled</span></p></body></html>", None))
        self.statusTitle.setText(QCoreApplication.translate("Dashboard", u"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; font-weight:600; color:#12af86;\">Status:</span></p></body></html>", None))
        self.creditsButton.setText(QCoreApplication.translate("Dashboard", u"Credits", None))
        self.githubButton.setText(QCoreApplication.translate("Dashboard", u"GitHub", None))
        self.reportButton.setText(QCoreApplication.translate("Dashboard", u"Report Issue", None))
        self.howtoButton.setText(QCoreApplication.translate("Dashboard", u"How To Use", None))
        self.creditsTitle.setText("")
        self.redSignal.setText(QCoreApplication.translate("Dashboard", u"<html><head/><body><p><img src=\":/Signals/img/red.png\"/></p></body></html>", None))
        self.redSignal_2.setText(QCoreApplication.translate("Dashboard", u"<html><head/><body><p><img src=\":/Signals/img/amber1.png\"/></p></body></html>", None))
        self.redSignal_4.setText(QCoreApplication.translate("Dashboard", u"<html><head/><body><p><img src=\":/Signals/img/green.png\"/></p></body></html>", None))
        self.versionTitle_2.setText(QCoreApplication.translate("Dashboard", u"<html><head/><body><p><span style=\" font-size:9pt; font-weight:600; font-style:italic; color:#ff0000;\">Press 1 while hovering over the signal with your cursor to set to danger.</span></p></body></html>", None))
        self.versionTitle_3.setText(QCoreApplication.translate("Dashboard", u"<html><head/><body><p><span style=\" font-size:9pt; font-weight:600; font-style:italic; color:#cc9900;\">Press 2 while hovering over the signal with your cursor to set to caution.</span></p></body></html>", None))
        self.versionTitle_4.setText(QCoreApplication.translate("Dashboard", u"<html><head/><body><p><span style=\" font-size:9pt; font-weight:600; font-style:italic; color:#12af86;\">Press 3 while hovering over the signal with your cursor to set to proceed.</span></p></body></html>", None))
        self.versionTitle_5.setText(QCoreApplication.translate("Dashboard", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; text-decoration: underline; color:#12af86;\">How To Use</span></p></body></html>", None))
        self.autoUpdateBox.setText(QCoreApplication.translate("Dashboard", u"Auto Update Check", None))
    # retranslateUi

