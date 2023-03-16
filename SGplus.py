# ElectricityMachine
# GUI by xDistinctx
# Version: 0.4.0
# Major changes: Add toggle rollback feature
# Description: A script to automate tasks when signalling for SCR
# Keybinds: 1 2 3 for Danger, Caution, and Proceed signal settings. C for Camera
# How to use: Hover over a signal and press the corresponding keybind to perform the action
import pyautogui
from pyautogui import *
import time
import math
import autoit
import keyboard
import win32api
import win32gui
import winsound
import PIL
import PIL.ImageGrab
import pygetwindow
import requests
import pyperclip
import pyscreeze
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import ctypes
import os
import json
import webbrowser
from modules import *
import traceback
import tempfile
disabled = None
starttime = time.time()

# TODO: Add check for pixels in signal dialog detection that figure out percentage of pixels that are of the color, and if they don't match certain tolerances (false positive), don't execute. This will solve a potential issue if backspace to leave desk ever gets fixed

version = "v0.4.0"
key_wait = 0
backspace_wait = 0
dialog_wait = 0.085
menu_wait = 0.032

color_vals = {
    (0, 201, 0),  # Lit Green
    (204, 153, 0),  # Lit Yellow
    (213, 0, 0),  # Lit Red
    (0, 94, 0),  # Unlit Green
    (96, 60, 0),  # Unlit Yellow
    (99, 0, 0),  # Unlit Red
}

color_more = (92, 89, 89)  # Grey 3 Dots
color_menu = (194, 186, 189)  # Side menu main color
color_camera_exit = (174, 10, 10)

disable = False
running = False
signal_mouse_coords = None


def update_check():
    URL = "https://api.github.com/repos/ElectricityMachine/SCR-SGPlus/releases/latest"
    r = requests.get(url=URL)
    data = r.json()
    if version != data["tag_name"]:
        return True
    else:
        return False


def able_to_run():
    global disabled
    global running
    if disabled:
        if debug:
            print("Unable to run: Disabled")
            logfile = open("log.txt", "a")
            logfile.write("Unable to run: Disabled\n")
            logfile.close()
        return False
    elif running:
        if debug:
            print("Unable to run: Already running")
            logfile = open("log.txt", "a")
            logfile.write("Unable to run: Already running\n")
            logfile.close()
        return False
    elif win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "Roblox":
        if debug:
            print("Unable to run: Not ROBLOX")
            logfile = open("log.txt", "a")
            logfile.write("Unable to run: Not ROBLOX\n")
            logfile.close()
        return False
    else:
        return True


def color_approx_eq(color1, color2):
    return abs(color1[0] - color2[0]) <= 7 and abs(color1[1] - color2[1]) <= 7 and abs(color1[2] - color2[2]) <= 7


def screen_grab(x, y, width, height):
    image = PIL.ImageGrab.grab(bbox=[x, y, x + width, y + height])
    return image


def click_signal(sig):
    if not able_to_run():
        return
    if scan_for_dialog("signal"):
        time.sleep(key_wait)
        keyboard.press_and_release(sig)
        time.sleep(backspace_wait)
        keyboard.press_and_release("backspace")


def click_camera_button():
    if not able_to_run():
        return
    # TODO: Create function that checks for the view camera button when you can't find the menu dialog

    if not able_to_run(): return
    autoit.mouse_click()
    if scan_for_dialog("signal"):
        keyboard.press_and_release("enter")
    time.sleep(0.016)
    if not scan_for_dialog("menu"):
        global signal_mouse_coords
        # TODO: Search for View Camera if dialog not found
        #       Search for close button if dialog not found. If found, press backspace and return mouse to previous coords
        if scan_for_dialog("exitcamera"):  # Exit button found
            for i in range(2):
                keyboard.press_and_release("backspace")  # Exit out of all menus
            if signal_mouse_coords: autoit.mouse_move(signal_mouse_coords.x, signal_mouse_coords.y, speed=1)
        return
    signal_mouse_coords = pyautogui.position()
    window = win32gui.GetForegroundWindow()
    rect = win32gui.GetClientRect(window)

    bbox = [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]
    x = bbox[0]
    y = bbox[1]
    w = bbox[2]
    h = bbox[3]
    zone_screen_height = math.ceil(0.97735849056603773584905660377358 * h)
    zone_screen_width = math.ceil(zone_screen_height * 1.3410553410553410553410553410553)
    zone_screen_x = math.ceil(w / 2 - zone_screen_width / 2)

    mouse_coords = pyautogui.position()
    camera_x = zone_screen_width * 0.89414414414414414414414414414414 + zone_screen_x
    camera_y = 0.91445427728613569321533923303835 * h
    camera_position = win32gui.ClientToScreen(window, (int(camera_x), int(camera_y)))

    autoit.mouse_click(x=camera_position[0], y=camera_position[1], speed=2)
    return

    # Scan for the menu on the right hand side


def scan_for_dialog(type):
    if not able_to_run():
        return
    if type == "signal":
        # Repeat and look for dots if no signal match is found
        mouse_pos = pyautogui.position()
        mousex = mouse_pos[0]
        mousey = mouse_pos[1]

        window = win32gui.GetForegroundWindow()
        autoit.mouse_click("left")
        rect = win32gui.GetClientRect(window)

        bbox = [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]
        x = bbox[0]
        y = bbox[1]
        w = bbox[2]
        h = bbox[3]
        # Wait for a set time before checking if the dialog actually pops up. This ensures there should be no time where the script screengrabs and the dialog isn't open after clicking on a signal.
        time.sleep(dialog_wait)
        start_time_perf = time.perf_counter()

        dialog_box_height = math.ceil((h - 32) * 0.125)
        dialog_box_width = math.ceil(dialog_box_height * 2)
        pixel_height = dialog_box_height * 0.171
        button_shelf = dialog_box_height / 2 * 1.15
        dialog_box_x = mousex - dialog_box_width / 2
        dialog_box_y = mousey - dialog_box_height

        capture = screen_grab(dialog_box_x, dialog_box_y,
                              dialog_box_width, dialog_box_height * 2)
        w, h = capture.size
        capture.convert('RGB')
        # capture.show()
        shelf = h / 2 * 1.15  # Where the colors we need to check are
        upper = capture.crop((0, 0, w, h / 2))  # Upper
        lower = capture.crop((0, h / 2, w, h))  # Lower
        upperw, upperh = upper.size
        lowerw, lowerh = lower.size
        lowershelf = lower.crop((0, lowerh * 2 / 3, lowerw, lowerh * 2 / 3 + 1))
        uppershelf = upper.crop((0, upperh / 2, upperw, upperh / 2 + 2))
        imagesToProcess = [lowershelf, uppershelf]

        flag = False
        for image in imagesToProcess:
            for i in range(math.ceil(image.width / 1.6)):
                for val in color_vals:
                    if i == 0 or image.height == 0:
                        break
                    r, g, b = image.getpixel((i, image.height - 1))
                    if color_approx_eq((r, g, b), (val)):
                        flag = True
                        break
                if flag:
                    break
            if flag:
                break
        if flag:
            return True
        else:
            if debug:
                # If you encounter this but the dialog is on the screen, please submit an issue on GitHub detailing
                print("IMAGE DETECTION: Dialog not found")
                logfile = open("log.txt", "a")
                logfile.write("IMAGE DETECTION: Dialog not found\n")
                logfile.close()
            return False
    elif type == "station":
        if debug:
            print("None")
            logfile = open("log.txt", "a")
            logfile.write("None\n")
            logfile.close()
    elif type == "menu":
        window = win32gui.GetForegroundWindow()
        rect = win32gui.GetClientRect(window)

        bbox = [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]
        x = bbox[0]
        y = bbox[1]
        w = bbox[2]
        h = bbox[3]
        zone_screen_height = math.ceil(0.97735849056603773584905660377358 * h)
        zone_screen_width = math.ceil(zone_screen_height * 1.3410553410553410553410553410553)
        zone_screen_x = math.ceil(w / 2 - zone_screen_width / 2)
        zone_screen_y = round(0.00983284169124877089478859390364 * h)

        dialog_box_height = math.ceil(h * 0.125)  # h-32 because of the title bar
        dialog_box_width = math.ceil(dialog_box_height * 2)  # Width is double the height
        dialog_box_x = zone_screen_width * 0.79760119940029985007496251874063 + zone_screen_x
        dialog_box_y = h * 0.76302851524090462143559488692232

        screen_cords = win32gui.ClientToScreen(window, (int(dialog_box_x), int(dialog_box_y)))
        time.sleep(menu_wait)
        capture = screen_grab(screen_cords[0], screen_cords[1], dialog_box_width, dialog_box_height)
        capture_w, capture_h = capture.size
        capture.convert('RGB')
        lowerw, lowerh = capture.size
        lowershelf = capture.crop((0, lowerh / 2, lowerw, lowerh / 2 + 2))
        imagesToProcess = [lowershelf]
        # lowershelf.show()
        flag = False
        for image in imagesToProcess:
            for i in range(math.ceil(image.width / 1.6)):
                for val in color_vals:
                    if i == 0 or image.height == 0:
                        break
                    r, g, b = image.getpixel((i, image.height - 1))
                    if color_approx_eq((r, g, b), (val)):
                        flag = True
                        break
                if flag:
                    break
            if flag:
                break
        if flag:
            return True
        else:
            # If not found, repeat the function but scan for view camera pixels
            if debug:
                # If you encounter this but the dialog is on the screen, please submit an issue on GitHub detailing
                print("IMAGE DETECTION: Menu's dialog not found")
                logfile = open("log.txt", "a")
                logfile.write("IMAGE DETECTION: Menu's dialog not found\n")
                logfile.close()
            return False
    elif type == "exitcamera":
        if debug:
            print("Exitcamera run")
            logfile = open("log.txt", "a")
            logfile.write("Exitcamera run\n")
            logfile.close()
        window = win32gui.GetForegroundWindow()
        rect = win32gui.GetClientRect(window)

        bbox = [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]
        x = bbox[0]
        y = bbox[1]
        w = bbox[2]
        h = bbox[3]

        camera_controls_width = 283
        camera_controls_height = 50
        camera_controls_y = 85 + y
        camera_controls_x = math.ceil(w / 2 - camera_controls_width / 2)

        exit_camera_button_y = 85 + y
        exit_camera_button_x = 0.91166077738515901060070671378092 * camera_controls_width + camera_controls_x - 5
        exit_camera_button_width = exit_camera_button_height = 50

        screen_cords = win32gui.ClientToScreen(window, (int(exit_camera_button_x), int(exit_camera_button_y)))
        capture = screen_grab(screen_cords[0], screen_cords[1], exit_camera_button_width, exit_camera_button_height)
        capture_w, capture_h = capture.size
        capture.convert('RGB')
        lowerw, lowerh = capture.size
        lowershelf = capture.crop((0, lowerh / 2, lowerw, lowerh / 2 + 2))
        imagesToProcess = [lowershelf]
        # lowershelf.show()
        flag = False
        for image in imagesToProcess:
            for i in range(math.ceil(image.width / 1.6)):
                val = color_camera_exit
                if image.height == 0:
                    break
                r, g, b = image.getpixel((i, image.height - 1))
                if color_approx_eq((r, g, b), (val)):
                    flag = True
                    break
            if flag:
                break
        if flag:
            return True
        else:
            # If not found, repeat the function but scan for view camera pixels
            if debug:
                # If you encounter this but the dialog is on the screen, please submit an issue on GitHub detailing
                print("IMAGE DETECTION: Menu's dialog not found")
                logfile = open("log.txt", "a")
                logfile.write("IMAGE DETECTION: Menu's dialog not found\n")
                logfile.close()


def move_and_click_rollback():
    if not able_to_run(): return
    autoit.mouse_click()
    if scan_for_dialog("exitcamera"):
        return
    elif scan_for_dialog("signal"):
        keyboard.press_and_release("enter")
    else:
        print("Rollback couldn't run due to initial dialog not found")
        return
    if not scan_for_dialog("menu"):
        print("Sidemenu not found")
        return
    window = win32gui.GetForegroundWindow()
    rect = win32gui.GetClientRect(window)

    bbox = [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]
    x = bbox[0]
    y = bbox[1]
    w = bbox[2]
    h = bbox[3]
    zone_screen_height = math.ceil(0.97735849056603773584905660377358 * h)
    zone_screen_width = math.ceil(zone_screen_height * 1.3410553410553410553410553410553)
    zone_screen_x = math.ceil(w / 2 - zone_screen_width / 2)

    mouse_coords = pyautogui.position()
    rollback_x = zone_screen_width * 0.89955022 + zone_screen_x
    rollback_y = 0.6951819075 * h
    rollback_position = win32gui.ClientToScreen(window, (int(rollback_x), int(rollback_y)))

    autoit.mouse_click(x=rollback_position[0], y=rollback_position[1], speed=2)
    time.sleep(0.016)
    keyboard.press_and_release("backspace")
    keyboard.press_and_release("backspace")
    autoit.mouse_move(mouse_coords.x, mouse_coords.y, speed=1)
    return


def send_zone_message(zone):
    if not able_to_run():
        return
    switch = {
        'A': "Zone A (Stepford Area, Willowfield, Whitefield branches) is now under manual signalling control.",
        'B': "Zone B (St. Helens Bridge, Coxly, Beaulieu Park corridor) is now under manual signalling control.",
        'C': "Zone C (Stepford Airport Area) is now under manual siganlling control.",
        'D': "Zone D (Morganstown to Leighton West) is now under manual signalling control.",
        'E': "Zone E (Llyn-by-the-Sea to Edgemead) is now under manual signalling control.",
        'F': "Zone F (Benton area + Waterline up to not including Airport West and Morganstown) is now under manual signalling control.",
        'G': "Zone G (James St. to Esterfield) is now under manual signalling control."
    }

    winsound.Beep(600, 200)
    pyperclip.copy(switch.get(zone))


def print_screensize():
    window = win32gui.GetForegroundWindow()
    rect = win32gui.GetClientRect(window)
    print(rect[2], rect[3])


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    '''
    finished = Signal()  # QtCore.Signal
    error = Signal(tuple)
    result = Signal(object)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()  # QtCore.Slot
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class Overlay(QMainWindow):
    """
    Top most window
    """

    def __init__(self):
        # Parent constructor
        QMainWindow.__init__(self)
        # Set window flags
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # Translucent background
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Properties
        with open("config/config.json", "r") as f:
            self.config = json.load(f)
            f.close()
        self.setStyleSheet("""
        QMainWindow {
            background-color: rgba(255, 255, 255, 0);
        }
        QLabel{
            border: 1px solid rgba(239, 239, 239, 0.15);
            border-radius: 5px;
        }
        QPushButton {
        border: 1px solid rgb(239, 239, 239);
        border-radius: 5px;
            }
        QPushButton:hover {
            border: 2px solid rgb(239, 239, 239);
            }
        QPushButton:pressed {
            border: 2px solid rgb(204, 105, 161);
            }
        """)
        self.animation: QPropertyAnimation | None = None
        self.button: QPushButton | None = None
        self.button2: QPushButton | None = None
        self.button3: QPushButton | None = None
        self.disabled = not self.config["enabledOnStart"]
        global disabled
        disabled = self.disabled
        self.label: QLabel | None = QLabel(self)
        self.separator: QLabel | None = QLabel(self)
        self.layout: QVBoxLayout | None = QVBoxLayout()
        self.threadpool = QThreadPool()
        self.originalGeometry = None
        self.originalLabelGeometry = None
        self.newX = None
        self.newY = None
        self.rt = None
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        screensize: tuple = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        # Window modifiers
        self.move(0, 0)
        self.resize(screensize[0] * 0.1, screensize[1] * 0.035)
        self.setWindowOpacity(0.6)
        self.setWindowTitle("SG+")
        self.setWindowIcon(QIcon("img/icon.ico"))
        self.originalGeometry = self.geometry()
        # Label modifiers
        if self.disabled:
            self.label.setText("SG+: Disabled")
            self.label.setStyleSheet("background-color: red; color: white; font-size: 20px; font: 14pt \"Raleway Bold\";")
        else:
            self.label.setText("SG+: Enabled")
            self.label.setStyleSheet("background-color: green; color: white; font-size: 20px; font: 14pt \"Raleway Bold\";")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(self.width(), self.height())
        self.separator.setText("----------")
        self.separator.setStyleSheet("background-color: grey; color: grey;")
        self.separator.resize(self.width(), int(self.height() * 0.2))
        # Layout modifiers
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.separator)
        # Move separator to under the label
        self.separator.move(0, self.height())
        self.setLayout(self.layout)

        keyboard.add_hotkey(self.config["toggle_key"], self.toggle_disable)  # F1

        if not self.disabled:
            self.add_hotkeys()

    def add_hotkeys(self):
        keyboard.add_hotkey(2, click_signal, args=["1"])  # 1
        keyboard.add_hotkey(3, click_signal, args=["2"])  # 2
        keyboard.add_hotkey(4, click_signal, args=["3"])  # 3
        keyboard.add_hotkey(46, click_camera_button)  # C
        keyboard.add_hotkey('R', move_and_click_rollback)  # R
        keyboard.add_hotkey('G', print_screensize)
        keyboard.add_hotkey(79, send_zone_message, args=["A"])  # Num 1
        keyboard.add_hotkey(80, send_zone_message, args=["B"])  # Num 2
        keyboard.add_hotkey(81, send_zone_message, args=["C"])  # Num 3
        keyboard.add_hotkey(75, send_zone_message, args=["D"])  # Num 4
        keyboard.add_hotkey(76, send_zone_message, args=["E"])  # Num 5
        keyboard.add_hotkey(77, send_zone_message, args=["F"])  # Num 6
        keyboard.add_hotkey(71, send_zone_message, args=["G"])  # Num 7
        winsound.Beep(500, 100)

    def remove_hotkeys(self):
        keyboard.remove_hotkey(2)
        keyboard.remove_hotkey(3)
        keyboard.remove_hotkey(4)
        keyboard.remove_hotkey(46)
        keyboard.remove_hotkey('R')
        keyboard.remove_hotkey('G')
        keyboard.remove_hotkey(79)
        keyboard.remove_hotkey(80)
        keyboard.remove_hotkey(81)
        keyboard.remove_hotkey(75)
        keyboard.remove_hotkey(76)
        keyboard.remove_hotkey(77)
        keyboard.remove_hotkey(71)
        winsound.Beep(400, 100)

    def toggle_disable(self):
        global disabled
        if disabled:
            self.disabled = False
            disabled = False
            worker = Worker(self.add_hotkeys)
            self.threadpool.start(worker)
            self.label.setText("SG+: Enabled")
            self.label.setStyleSheet("background-color: green; color: white; font-size: 20px; font: 14pt \"Raleway Bold\";")
            if self.button is not None:
                self.button.setText("Disable")
                self.button.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 175, 189, 255), stop:1 rgba(255, 195, 160, 255)); color: red; font-size: 20px;")
        else:
            # Remove all hotkeys
            worker = Worker(self.remove_hotkeys)
            self.threadpool.start(worker)
            self.disabled = True
            disabled = True
            self.label.setText("SG+: Disabled")
            self.label.setStyleSheet(
                "background-color: red; color: white; font-size: 20px; font: 14pt \"Raleway Bold\";")
            if self.button is not None:
                self.button.setText("Enable")
                self.button.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 175, 189, 255), stop:1 rgba(255, 195, 160, 255)); color: green; font-size: 20px;")

    def enterEvent(self, event):
        """
        When hovering over the window
        :param event:
        :return:
        """

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(self.config["animation_duration"])
        self.animation.setStartValue(self.originalGeometry)
        self.animation.setEndValue(QRect(self.x(), self.y(), self.width(), 155))
        self.animation.start()

        self.setWindowOpacity(0.9)

        # Add buttons under the label
        if self.disabled:
            self.button = QPushButton("Enable", self)
            self.button.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 175, 189, 255), stop:1 rgba(255, 195, 160, 255)); color: green; font-size: 20px;")
        else:
            self.button = QPushButton("Disable", self)
            self.button.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 175, 189, 255), stop:1 rgba(255, 195, 160, 255)); color: red; font-size: 20px;")
        self.button.clicked.connect(self.toggle_disable)
        # Move button to under the separator
        self.button.move(0, self.height() + self.separator.height())
        self.button.resize(self.width(), self.height())

        # Add to layout
        self.layout.addWidget(self.button)
        # Display button
        self.button.show()

        # Add Properties button under self.button
        self.button2 = QPushButton("Properties", self)
        self.button2.clicked.connect(self.propertiesOpen)
        # Move button to under the Enable button
        self.button2.move(0, self.height() + self.separator.height() + self.button.height())
        self.button2.resize(self.width(), self.height())
        self.button2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 175, 189, 255), stop:1 rgba(255, 195, 160, 255));; color: white; font-size: 20px;")
        # Add to layout
        self.layout.addWidget(self.button2)
        # Display button
        self.button2.show()

        # Add Exit button under self.button2
        self.button3 = QPushButton("Exit", self)
        self.button3.clicked.connect(self.close)
        # Move button to under the Properties button
        self.button3.move(0, self.height() + self.separator.height() + self.button.height() + self.button2.height())
        self.button3.resize(self.width(), self.height())
        self.button3.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 175, 189, 255), stop:1 rgba(255, 195, 160, 255)); color: white; font-size: 20px;")
        # Add to layout
        self.layout.addWidget(self.button3)
        # Display button
        self.button3.show()

    def leaveEvent(self, event):
        """
        When leaving the window
        :param event:
        :return:
        """
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(round(self.config["animation_duration"]))
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(QRect(self.x(), self.y(), self.width(), 36))
        self.animation.start()

        self.setWindowOpacity(0.6)

    # Make overlay window draggable
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
        self.newX = self.x()
        self.newY = self.y()
        self.originalGeometry = QRect(self.newX, self.newY, self.width(), self.height())

    def propertiesOpen(self):
        self.disabled = True
        global disabled
        disabled = True
        self.remove_hotkeys()
        keyboard.remove_hotkey(self.config["toggle_key"])
        self.properties = Properties()
        self.properties.show()
        self.close()


class Update(QMainWindow):
    """
    Update window
    """

    def __init__(self):
        QMainWindow.__init__(self)
        self.window = None
        self.dragPos = None
        self.ui = Ui_UpdateWindow()
        self.ui.setupUi(self)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
        self.ui.skipButton.clicked.connect(self.skip)
        self.ui.updateButton.clicked.connect(self.update)

    def update(self):
        """
        Update button
        """
        webbrowser.get().open("https://github.com/ElectricityMachine/SCR-SGPlus/releases")
        self.close()

    def skip(self):
        """
        Skip button
        :return:
        """
        self.window = Overlay()
        self.window.show()
        self.close()

    def mousePressEvent(self, event):
        """
        Mouse press event
        :param event:
        """
        self.dragPos = event.globalPos().toPoint()

class Properties(QMainWindow):
    """
    Update window
    """

    def __init__(self):
        QMainWindow.__init__(self)
        self.timer = None
        self.window = None
        self.dragPos = None
        self.key = None
        self.threadpool = QThreadPool()
        self.ui = Ui_PropertiesWindow()
        self.ui.setupUi(self)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
        self.ui.skipButton.clicked.connect(self.skip)
        self.ui.updateButton.clicked.connect(self.update)
        self.ui.changeHotkey.clicked.connect(self.changeHotkey)

        with open("config/config.json", "r") as f:
            self.config = json.load(f)
            f.close()
        self.key = self.config["toggle_key"]
        self.ui.animationDuration.setPlainText(str(round(self.config["animation_duration"])) + "ms")
        # Convert key code to key name
        keycode = self.config["toggle_key"]
        if keycode == 59:
            keyname = "F1"
        else:
            keyname = keycode.upper()
        self.ui.toggleHotkey.setPlainText(keyname)
        self.ui.enabledOnStart.setChecked(self.config["enabledOnStart"])
        self.ui.debugMode.setChecked(self.config["debug"])
        self.ui.actionDelay.setPlainText(str(self.config["key_wait"]) + "ms")

        self.ui.actionDelay.setReadOnly(False)
        self.ui.animationDuration.setReadOnly(False)

    def changeHotkey(self):
        def waitForKeyPress():
            # Record keypress until the first key is pressed
            self.key = keyboard.read_key()
            print(self.key)
        self.ui.label_2.setText('<html><head/><body><p align="center">Press any key to assign this hotkey.</p></body></html>')
        # Wait for key press, in multithread
        self.worker = Worker(waitForKeyPress)
        self.worker.signals.result.connect(self.keyPress)
        self.threadpool.start(self.worker)

    def keyPress(self):
        self.ui.label_2.setText('<html><head/><body><p align="center">Click a box to change it\'s setting.</p></body></html>')
        self.ui.toggleHotkey.setPlainText(self.key.upper())


    def update(self):
        # Get values for all the fields
        animationDuration = self.ui.animationDuration.toPlainText().replace("ms", "")
        actionDelay = self.ui.actionDelay.toPlainText().replace("ms", "")
        try:
            animationDuration = int(animationDuration)
            actionDelay = int(actionDelay)
        except ValueError:
            animationDuration = 100
            actionDelay = 0
        toggleHotkey = self.ui.toggleHotkey.toPlainText()
        enabledOnStart = self.ui.enabledOnStart.isChecked()
        debugMode = self.ui.debugMode.isChecked()
        actionDelay = self.ui.actionDelay.toPlainText().replace("ms", "")
        configArray = {"key_wait": int(actionDelay), "backspace_wait": 0, "dialog_wait": 0.085, "debug": debugMode, "check_for_update": self.config["check_for_update"], "animation_duration": animationDuration, "enabledOnStart": enabledOnStart, "toggle_key": self.key}
        # Convert to JSON object and write to file
        jsonArray = json.dumps(configArray)
        with open("config/config.json", "w") as f:
            f.write(jsonArray)
            f.close()
        self.ui.updateButton.setText("Saved!")
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda: self.ui.updateButton.setText("Apply"))
        self.timer.start(100)


    def skip(self):
        self.mainWindow = Overlay()
        self.mainWindow.show()
        self.close()

    def mousePressEvent(self, event):
        """
        Mouse press event
        :param event:
        """
        self.dragPos = event.globalPos().toPoint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('img/icon.ico'))
    pixmap = QPixmap('img/splash.png')
    splash = QSplashScreen(pixmap)
    splash.show()
    app.processEvents()
    if not os.path.exists(os.getcwd() + "/config/config.json"):
        with open(os.getcwd() + "/config/config.json", "w") as f:
            # Create dict for JSON
            config = {"key_wait": 0, "backspace_wait": 0, "dialog_wait": 0.085, "debug": False, "check_for_update": True, "animation_duration": 100, "enabledOnStart": False, "toggle_key": "f1"}
            # Write dict to JSON
            json.dump(config, f)
            f.close()
    else:
        with open(os.getcwd() + "/config/config.json", "r") as f:
            config = json.load(f)
            f.close()
    if config["debug"]:
        logfile = open("log.txt", "w")
        logfile.close()
    dialog_wait = config["dialog_wait"]
    key_wait = config["key_wait"]
    backspace_wait = config["backspace_wait"]
    debug = config["debug"]

    if "NUITKA_ONEFILE_PARENT" in os.environ:
        splash_filename = os.path.join(
            tempfile.gettempdir(),
            "onefile_%d_splash_feedback.tmp" % int(os.environ["NUITKA_ONEFILE_PARENT"]),
        )

        if os.path.exists(splash_filename):
            os.unlink(splash_filename)

    if config["check_for_update"]:
        if update_check():
            window = Update()
            window.show()
            splash.finish(window)
            sys.exit(app.exec())
        else:
            window = Overlay()
            window.show()
            splash.finish(window)
            sys.exit(app.exec())
    else:
        window = Overlay()
        window.show()
        splash.finish(window)
        sys.exit(app.exec())
