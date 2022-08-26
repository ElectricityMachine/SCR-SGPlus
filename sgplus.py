# ElectricityMachine & enigmapr0ject/xDistinctx
# Version: 0.3
# Description: A script to automate tasks when signalling for SCR
# Keybinds: 1 2 3 for Danger, Caution, and Proceed signal settings. C for Camera
# How to use: Hover over a signal and press the corresponding keybind to perform the action
from PySide2 import QtCore
from modules import *
import ctypes
keyboardThread = None
myappid = 'sgplus.03' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
starttime = time.time()
version = "v0.3"
key_wait = 0
backspace_wait = 0
dialog_wait = 0.085
debug = False # Enable with console output for debug dialog
check_for_update = None
webbrowserError = False
windowControlArray = [] #For sharing the master window object
color_vals ={
    (0, 201, 0), # Lit Green
    (204, 153, 0), # Lit Yellow
    (213, 0, 0), # Lit Red
    (0, 94, 0), # Unlit Green
    (96, 60, 0), # Unlit Yellow
    (99, 0, 0), # Unlit Red
}
class UpdateWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.dragPos = None
        self.ui = Ui_Updater()
        self.ui.setupUi(self)
        self.initialised = False
        self.enabled = False
        ## REMOVE TITLE BAR
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ## DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
        self.ui.yesButton.clicked.connect(self.yes)
        self.ui.noButton.clicked.connect(self.no)
    def yes(self):
        try:
            webbrowser.get("https://github.com/ElectricityMachine/SCR-SGPlus")
        except webbrowser.Error:
            global webbrowserError
            webbrowserError = True
        # Destroy window
        self.window = DashboardWindow()
        windowControlArray.append(self.window)
        self.close()
    def no(self):
        self.window = DashboardWindow()
        windowControlArray.append(self.window)
        self.close()
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()
class DashboardWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.dragPos = None
        self.ui = Ui_Dashboard()
        self.ui.setupUi(self)
        self.initialised = False
        self.enabled = False
        self.creditsEnabled = None
        self.howtoEnabled = False
        with open("config.json", "r") as configFile:
            autoUpdateSettingArray = json.load(configFile)
            configFile.close()
        self.autoUpdateSetting = autoUpdateSettingArray["auto-update"]
        if self.autoUpdateSetting == "true":
            self.ui.autoUpdateBox.setChecked(True)
        else:
            self.ui.autoUpdateBox.setChecked(False)
        ## REMOVE TITLE BAR
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ## DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
        # Hide UI stuff
        self.ui.enableButton.hide()
        self.ui.howtomenu.hide()
        # Buttons
        self.ui.autoUpdateBox.stateChanged.connect(self.autoUpdateConfig)
        self.ui.exitButton.clicked.connect(self.close)
        self.ui.initialiseButton.clicked.connect(self.initialise)
        self.ui.enableButton.clicked.connect(self.enable)
        self.ui.creditsButton.clicked.connect(self.credits)
        self.ui.githubButton.clicked.connect(self.github)
        self.ui.reportButton.clicked.connect(self.report)
        self.ui.howtoButton.clicked.connect(self.howto)
        #
        if webbrowserError:
            self.ui.consoleOutput.setText(
            '<html><head/><body><p align="left"><span style=" font-size:9pt; font-weight:600; font-style:italic; color:#ff0000;">Failed to open browser window. You can download the update here: https://github.com/ElectricityMachine/SCR-SGPlus</span></p></body></html>')
        self.show()
    def autoUpdateConfig(self):
        if self.ui.autoUpdateBox.isChecked():
            self.autoUpdateSetting = "true"
        else:
            self.autoUpdateSetting = "false"
        with open("config.json", "w") as configFile:
            json.dump({"auto-update": self.autoUpdateSetting}, configFile)
            configFile.close()
    def initialise(self):
        if not self.initialised:
            self.ui.consoleOutput.setText('<html><head/><body><p align="left"><span style=" font-size:11pt; font-weight:600; font-style:italic; color:#cc9900;">Initialising SGPlus...</span></p></body></html>')
            self.ui.consoleOutput.setText('<html><head/><body><p align="left"><span style=" font-size:11pt; font-weight:600; font-style:italic; color:#12af86;">Initialised SGPlus!</span></p></body></html>')
            self.ui.initialiseButton.setEnabled(False)
            self.ui.initialiseButton.setText('Initialised')
            self.ui.initialiseButton.setStyleSheet("""
            color: rgba(255, 255, 255, 255);
            background-color: rgb(139, 139, 139)
            """)
            self.ui.enableButton.show()
            self.initialised = True
        else:
            self.ui.consoleOutput.setText('<html><head/><body><p align="left"><span style=" font-size:11pt; font-weight:600; font-style:italic; color:#12af86;">SGPlus is already initialised.</span></p></body></html>')
    def enable(self):
        if self.enabled:
            keyboard.unhook_all_hotkeys()
            self.ui.enableButton.setText('Enable')
            self.ui.enableButton.setStyleSheet("""
            color: rgba(255, 255, 255, 255);
            background-color: rgb(133,242,208);
            """)
            self.ui.statusText.setText('<html><head/><body><p><span style=" font-size:12pt; font-weight:600; color:#ff0000;">Disabled</span></p></body></html>')
            self.enabled = False
            self.ui.consoleOutput.setText('<html><head/><body><p align="left"><span style=" font-size:11pt; font-weight:600; font-style:italic; color:#ff0000;">Disabled actions.</span></p></body></html>')
            global disable
            disable = True
        else:
            keyboard.add_hotkey(2, click_signal, args=["1"])  # 1
            keyboard.add_hotkey(3, click_signal, args=["2"])  # 2
            keyboard.add_hotkey(4, click_signal, args=["3"])  # 3
            keyboard.add_hotkey(46, click_camera_button)  # C
            self.ui.enableButton.setText('Disable')
            self.ui.enableButton.setStyleSheet("""
            color: rgba(255, 255, 255, 255);
            background-color: rgb(255,000,000);
            """)
            self.ui.statusText.setText('<html><head/><body><p><span style=" font-size:12pt; font-weight:600; color:#12af86;">Enabled</span></p></body></html>')
            self.enabled = True
            self.ui.consoleOutput.setText('<html><head/><body><p align="left"><span style=" font-size:11pt; font-weight:600; font-style:italic; color:#12af86;">Enabled actions! You are free to start signalling. For instructions, press "How to use".</span></p></body></html>')
    def credits(self):
        if not self.creditsEnabled:
            self.ui.creditsTitle.setText("""
            <html><head/><body><p align="left">
            <span style=" font-size:8pt; font-weight:600; font-style:italic; color:#ff0000;">Logic: ElectricityMachine</span><br>
            <span style=" font-size:8pt; font-weight:600; font-style:italic; color:#cc9900;">GUI: enigmapr0ject/xDistinctx</span><br>
            <span style=" font-size:8pt; font-weight:600; font-style:italic; color:#12af86;">GUI Template: Wanderson</span>
            </p></body></html>
            """)
            self.creditsEnabled = True
        else:
            self.ui.creditsTitle.setText("")
            self.creditsEnabled = False
    def github(self):
        try:
            webbrowser.get('https://github.com/ElectricityMachine/SCR-SGPlus')
        except webbrowser.Error:
            self.ui.consoleOutput.setText('<html><head/><body><p align="left"><span style=" font-size:9pt; font-weight:600; font-style:italic; color:#ff0000;">Failed to open browser. Go to: https://github.com/ElectricityMachine/SCR-SGPlus</span></p></body></html>')
    def report(self):
        try:
            webbrowser.get('https://github.com/ElectricityMachine/SCR-SGPlus/issues')
        except webbrowser.Error:
            self.ui.consoleOutput.setText('<html><head/><body><p align="left"><span style=" font-size:9pt; font-weight:600; font-style:italic; color:#ff0000;">Failed to open browser. Go to: https://github.com/ElectricityMachine/SCR-SGPlus/issues</span></p></body></html>')
    def howto(self):
        if not self.howtoEnabled:
            self.ui.howtomenu.show()
            self.howtoEnabled = True
        else:
            self.ui.howtomenu.hide()
            self.howtoEnabled = False
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()
    def close(self):
        keyboard.unhook_all_hotkeys()
        sys.exit(app.exec_())
def checkUpdate():
    data = requests.get(url="https://api.github.com/repos/ElectricityMachine/SCR-SGPlus/releases/latest").json()
    if version != data["tag_name"]:
        return 1
    else:
        return 0
# Check if file exists
if not os.path.isfile("config.json"):
    defaultSetting = {"auto-update": "true"}
    jsonDict = json.dumps(defaultSetting)
    with open("config.json", "w") as config:
        config.write(jsonDict)
        config.close()
    with open("config.json", "r") as f:
        settings = json.load(f)
        f.close()
else:
    with open("config.json", "r") as f:
        settings = json.load(f)
        f.close()
### Logic ###
def color_approx_eq(color1, color2):
    return abs(color1[0] - color2[0]) <= 7 and abs(color1[1] - color2[1]) <= 7 and abs(color1[2] - color2[2]) <= 7


def screen_grab(x, y, width, height):
    image = PIL.ImageGrab.grab(bbox=[x, y, x + width, y + height])
    return image


def click_signal(sig):
    if scan_for_dialog("signal"):
        time.sleep(key_wait)
        keyboard.press_and_release(sig)
        time.sleep(backspace_wait)
        keyboard.press_and_release("backspace")
        if sig == "1":
            signalColour = "#ff0000"
            signalAspect = "Danger"
        elif sig == "2":
            signalColour = "#cc9900"
            signalAspect = "Caution"
        else:
            signalColour = "#12af86"
            signalAspect = "Proceed"
        masterWindow = windowControlArray[0]
        masterWindow.ui.consoleOutput.setText(f"<html><head/><body><p align=\"left\">Signal was set to: <span style=\" font-size:11pt; font-weight:600; font-style:bold; color:{signalColour};\">{signalAspect}</span></p></body></html>")

def click_camera_button():
    if pyautogui.locateCenterOnScreen('img/rotate.png', confidence=0.9):
        keyboard.press_and_release("backspace")
        hwnd = win32gui.FindWindow(None, 'Roblox')
        x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        w = x1 - x0
        h = y1 - y0
        autoit.mouse_move(math.ceil(w / 2), math.ceil(h / 2), 2)
        keyboard.press_and_release("backspace")
        keyboard.press_and_release("backspace")
        return
    mouseCoords = pyautogui.position()
    mouseCoordsX, mouseCoordsY = mouseCoords
    autoit.mouse_click("left")
    time.sleep(0.032)
    output = pyautogui.locateCenterOnScreen('img/more.png', confidence=0.8)
    time.sleep(0.016)
    if output is None:
        if debug: print("CAMERA: Not found")
        masterWindow = windowControlArray[0]
        masterWindow.ui.consoleOutput.setText("<html><head/><body><p align=\"left\"><span style=\" font-size:9pt; font-weight:600; font-style:italic; color:#ff0000;\">Camera not found</span></p></body></html>")
        return
    else:
        x, y = output
        if debug: print(output)
        time.sleep(0.016)
        autoit.mouse_click("left", x, y, 1, 2)
        time.sleep(0.032)
        output = pyautogui.locateCenterOnScreen(
            'img/camera.png', confidence=0.8)
        time.sleep(0.032)
        print(output)
        if output is None:
            if debug: print("CAMERA: None found after button press")
            masterWindow = windowControlArray[0]
            masterWindow.ui.consoleOutput.setText("<html><head/><body><p align=\"left\"><span style=\" font-size:9pt; font-weight:600; font-style:italic; color:#ff0000;\">Camera button not found.</span></p></body></html>")
            return
        else:
            x, y = output
            time.sleep(0.016)
            autoit.mouse_click("left", x, y, 1, 2)
def able_to_run():
    if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "Roblox":
        if debug: print("Unable to run: Not ROBLOX")
        masterWindow = windowControlArray[0]
        masterWindow.ui.consoleOutput.setText("<html><head/><body><p align=\"left\"><span style=\" font-size:9pt; font-weight:600; font-style:italic; color:#ff0000;\">Unable to run: ROBLOX is not in the foreground.</span></p></body></html>")
        return False
    else:
        return True
def scan_for_dialog(type):
    if not able_to_run(): return
    if type == "signal":
        mouse_pos = pyautogui.position()
        mousex = mouse_pos[0]
        mousey = mouse_pos[1]

        window = win32gui.GetForegroundWindow()
        autoit.mouse_click("left")
        rect = win32gui.GetWindowRect(window)

        bbox = [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]
        x = bbox[0]
        y = bbox[1]
        w = bbox[2]
        h = bbox[3]
        time.sleep(
            dialog_wait)  # Wait for a set time before checking if the dialog actually pops up. This ensures there should be no time when the script screengrabs and the dialog isn't open after clicking on a signal.
        start_time_perf = time.perf_counter()

        dialog_box_height = math.ceil((h - 32) * 0.125)
        dialog_box_width = math.ceil(dialog_box_height * 2)
        pixel_height = dialog_box_height * 0.171
        button_shelf = dialog_box_height / 2 * 1.15
        dialog_box_x = mousex - dialog_box_width / 2
        dialog_box_y = mousey - dialog_box_height

        capture = screen_grab(dialog_box_x, dialog_box_y, dialog_box_width, dialog_box_height * 2)
        w, h = capture.size
        capture.convert('RGB')
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
                    if i == 0 or image.height == 0: break
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
            if debug: print(
                "IMAGE DETECTION: Dialog not found")  # If you encounter this but the dialog is on the screen, please submit an issue on GitHub detailing
            masterWindow = windowControlArray[0]
            masterWindow.ui.consoleOutput.setText("<html><head/><body><p align=\"left\"><span style=\" font-size:9pt; font-weight:600; font-style:italic; color:#ff0000;\">Image detection: dialog not found.</span></p></body></html>")
            return False
    elif type == "station" and debug: print("None")
#############

if __name__ == "__main__":
    if settings["auto-update"] == 'true':
        update = checkUpdate()
        if update == 1:
            app = QApplication(sys.argv)
            app.setWindowIcon(QIcon('img/icon.png'))
            window = UpdateWindow()
            window.show()
            sys.exit(app.exec_())
        else:
            app = QApplication(sys.argv)
            app.setWindowIcon(QIcon('img/icon.png'))
            window = DashboardWindow()
            windowControlArray.append(window)
            sys.exit(app.exec_())
    else:
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon('img/icon.png'))
        window = DashboardWindow()
        windowControlArray.append(window)
        sys.exit(app.exec_())