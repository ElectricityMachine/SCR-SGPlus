# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import PIL, PIL.ImageGrab, autoit, keyboard, math, pyautogui, requests, time, json, sys, os, webbrowser, win32gui, winsound
from multiprocessing import Process
# GUI FILE
from .ui_dashboard import Ui_Dashboard
from .ui_update import Ui_Updater
