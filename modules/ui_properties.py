# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'properties.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QLabel,
    QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)
from .resources_rc import *
class Ui_PropertiesWindow(object):
    def setupUi(self, PropertiesWindow):
        if not PropertiesWindow.objectName():
            PropertiesWindow.setObjectName(u"PropertiesWindow")
        PropertiesWindow.resize(552, 281)
        PropertiesWindow.setAcceptDrops(False)
        icon = QIcon()
        icon.addFile(u":/images/icon.ico", QSize(), QIcon.Normal, QIcon.Off)
        PropertiesWindow.setWindowIcon(icon)
        PropertiesWindow.setStyleSheet(u"QPushButton {\n"
"	border: 1px solid rgb(239, 239, 239);\n"
"	border-radius: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid rgb(239, 239, 239);\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid rgb(204, 105, 161);\n"
"}\n"
"#dropShadowFrame {	\n"
"	background-color: rgba(255, 255, 255, .15);\n"
"}\n"
"QWidget {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 175, 189, 255), stop:1 rgba(255, 195, 160, 255));\n"
"}\n"
"QLabel {\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}\n"
"")
        self.centralwidget = QWidget(PropertiesWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.dropShadowFrame = QFrame(self.centralwidget)
        self.dropShadowFrame.setObjectName(u"dropShadowFrame")
        self.dropShadowFrame.setStyleSheet(u"")
        self.dropShadowFrame.setFrameShape(QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.dropShadowFrame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 141, 31))
        self.label.setStyleSheet(u"font: 81 14pt \"Raleway ExtraBold\";\n"
"color: rgb(239, 239, 239);\n"
"")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label_2 = QLabel(self.dropShadowFrame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 40, 311, 31))
        self.label_2.setStyleSheet(u"font: 81 14pt \"Raleway ExtraBold\";\n"
"color: rgb(204, 105, 161);")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setWordWrap(False)
        self.updateButton = QPushButton(self.dropShadowFrame)
        self.updateButton.setObjectName(u"updateButton")
        self.updateButton.setGeometry(QRect(410, 190, 111, 23))
        self.updateButton.setStyleSheet(u"color: rgb(204, 105, 161);")
        self.skipButton = QPushButton(self.dropShadowFrame)
        self.skipButton.setObjectName(u"skipButton")
        self.skipButton.setGeometry(QRect(410, 230, 111, 23))
        self.skipButton.setStyleSheet(u"color: rgb(204, 105, 161);")
        self.actionDelay = QPlainTextEdit(self.dropShadowFrame)
        self.actionDelay.setObjectName(u"actionDelay")
        self.actionDelay.setGeometry(QRect(10, 120, 111, 31))
        self.actionDelay.setMinimumSize(QSize(10, 10))
        self.actionDelay.setStyleSheet(u"background-color: rgba(255, 255, 255, .15);\n"
"color: rgb(255, 255, 255);\n"
"border-bottom-left-radius :0px;\n"
"border-bottom-right-radius :0px;\n"
"border: 1px solid white;")
        self.actionDelay.setReadOnly(True)
        self.label_3 = QLabel(self.dropShadowFrame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 100, 111, 20))
        self.label_3.setStyleSheet(u"font: 81 14pt \"Raleway ExtraBold\";\n"
"color: rgb(239, 239, 239);\n"
"")
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setWordWrap(True)
        self.toggleHotkey = QPlainTextEdit(self.dropShadowFrame)
        self.toggleHotkey.setObjectName(u"toggleHotkey")
        self.toggleHotkey.setGeometry(QRect(10, 190, 111, 31))
        self.toggleHotkey.setMinimumSize(QSize(10, 10))
        self.toggleHotkey.setStyleSheet(u"background-color: rgba(255, 255, 255, .15);\n"
"color: rgb(255, 255, 255);\n"
"border-bottom-left-radius :0px;\n"
"border-bottom-right-radius :0px;\n"
"border: 1px solid white;")
        self.toggleHotkey.setReadOnly(True)
        self.label_4 = QLabel(self.dropShadowFrame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 170, 111, 20))
        self.label_4.setStyleSheet(u"font: 81 14pt \"Raleway ExtraBold\";\n"
"color: rgb(239, 239, 239);\n"
"")
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setWordWrap(True)
        self.label_5 = QLabel(self.dropShadowFrame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(150, 100, 111, 20))
        self.label_5.setStyleSheet(u"font: 81 14pt \"Raleway ExtraBold\";\n"
"color: rgb(239, 239, 239);\n"
"")
        self.label_5.setAlignment(Qt.AlignCenter)
        self.label_5.setWordWrap(True)
        self.enabledOnStart = QCheckBox(self.dropShadowFrame)
        self.enabledOnStart.setObjectName(u"enabledOnStart")
        self.enabledOnStart.setGeometry(QRect(150, 120, 101, 31))
        self.enabledOnStart.setAutoFillBackground(False)
        self.enabledOnStart.setStyleSheet(u"color: #fff;\n"
"background-color: rgba(255, 255, 255, 0);\n"
"font: 8pt \"MS Shell Dlg 2\";")
        self.animationDuration = QPlainTextEdit(self.dropShadowFrame)
        self.animationDuration.setObjectName(u"animationDuration")
        self.animationDuration.setGeometry(QRect(150, 190, 111, 31))
        self.animationDuration.setMinimumSize(QSize(10, 10))
        self.animationDuration.setStyleSheet(u"background-color: rgba(255, 255, 255, .15);\n"
"color: rgb(255, 255, 255);\n"
"border-bottom-left-radius :0px;\n"
"border-bottom-right-radius :0px;\n"
"border: 1px solid white;")
        self.animationDuration.setReadOnly(True)
        self.label_6 = QLabel(self.dropShadowFrame)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(150, 170, 111, 20))
        self.label_6.setStyleSheet(u"font: 81 14pt \"Raleway ExtraBold\";\n"
"color: rgb(239, 239, 239);\n"
"")
        self.label_6.setAlignment(Qt.AlignCenter)
        self.label_6.setWordWrap(True)
        self.label_7 = QLabel(self.dropShadowFrame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(280, 100, 111, 20))
        self.label_7.setStyleSheet(u"font: 81 14pt \"Raleway ExtraBold\";\n"
"color: rgb(239, 239, 239);\n"
"")
        self.label_7.setAlignment(Qt.AlignCenter)
        self.label_7.setWordWrap(True)
        self.debugMode = QCheckBox(self.dropShadowFrame)
        self.debugMode.setObjectName(u"debugMode")
        self.debugMode.setGeometry(QRect(280, 120, 101, 31))
        self.debugMode.setAutoFillBackground(False)
        self.debugMode.setStyleSheet(u"color: #fff;\n"
"background-color: rgba(255, 255, 255, 0);\n"
"font: 8pt \"MS Shell Dlg 2\";")
        self.changeHotkey = QPushButton(self.dropShadowFrame)
        self.changeHotkey.setObjectName(u"changeHotkey")
        self.changeHotkey.setGeometry(QRect(10, 220, 111, 23))
        self.changeHotkey.setStyleSheet(u"color: rgb(204, 105, 161);")
        self.label_8 = QLabel(self.dropShadowFrame)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(420, 1, 111, 41))
        self.label_8.setStyleSheet(u"font: 81 14pt \"Raleway ExtraBold\";\n"
"color: rgb(239, 239, 239);\n"
"")
        self.label_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_8.setWordWrap(True)

        self.verticalLayout.addWidget(self.dropShadowFrame)

        PropertiesWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(PropertiesWindow)

        QMetaObject.connectSlotsByName(PropertiesWindow)
    # setupUi

    def retranslateUi(self, PropertiesWindow):
        PropertiesWindow.setWindowTitle(QCoreApplication.translate("PropertiesWindow", u"SG+", None))
        self.label.setText(QCoreApplication.translate("PropertiesWindow", u"<html><head/><body><p align=\"center\">SG+ Properties</p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("PropertiesWindow", u"<html><head/><body><p align=\"center\">Click a box to change it's setting.</p></body></html>", None))
        self.updateButton.setText(QCoreApplication.translate("PropertiesWindow", u"Apply", None))
        self.skipButton.setText(QCoreApplication.translate("PropertiesWindow", u"Close", None))
        self.actionDelay.setPlainText("")
        self.label_3.setText(QCoreApplication.translate("PropertiesWindow", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:8pt;\">Action Delay</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("PropertiesWindow", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:8pt;\">Toggle Hotkey</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("PropertiesWindow", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:8pt;\">Enabled on start</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.enabledOnStart.setToolTip(QCoreApplication.translate("PropertiesWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.enabledOnStart.setText("")
        self.label_6.setText(QCoreApplication.translate("PropertiesWindow", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:8pt;\">Animation duration</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("PropertiesWindow", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:8pt;\">Debug Mode</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.debugMode.setToolTip(QCoreApplication.translate("PropertiesWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.debugMode.setText("")
        self.changeHotkey.setText(QCoreApplication.translate("PropertiesWindow", u"Change", None))
        self.label_8.setText(QCoreApplication.translate("PropertiesWindow", u"<html><head/><body><p><span style=\" font-size:8pt; font-style:italic;\">Developed by Electricity_Machine and xDistinctx</span></p></body></html>", None))
    # retranslateUi

