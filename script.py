# ElectricityMachine
# Version: 0.3.1-alpha
# Major changes: Python 12 support, refactor
# Description: A script to automate tasks when signalling for SCR
# Keybinds: 1 2 3 for Danger, Caution, and Proceed signal settings. C for Camera. R for Rollback Toggle.
# How to use: Hover over a signal and press the corresponding keybind to perform the action
# Limitations: Windows only, only works on primary monitor

import math
import time
import winsound

import autoit
import colorama
import mouse
import pyperclip
import win32gui
from keyboard import add_hotkey, press_and_release
from keyboard import wait as keyboard_wait
from mss import mss
from PIL.Image import frombytes
from requests import get as requests_get

colorama.init()  # Needed to work on Windows devices, see colorama docs

VERSION = "v0.3.1-alpha"
AVG_FPS = 60  # Set your average FPS here
AVG_PING = 0  # Set your average ping here
DEBUG = True  # If true, will enable debug prints if they're specified
UPDATE_CHECK_ENABLED = False  # If true, will run check_for_update() on startup


COLORS = {
    "COLOR_DIALOG_BUTTONS": [
        (0, 201, 0),  # Lit Green
        (204, 153, 0),  # Lit Yellow
        (213, 0, 0),  # Lit Red
        (0, 94, 0),  # Unlit Green
        (96, 60, 0),  # Unlit Yellow
        (99, 0, 0),  # Unlit Red
    ],
    "COLOR_MORE": (92, 89, 89),  # Color of gray button w/ 3 dots
    "COLOR_MENU": (194, 186, 189),  # Side menu main color
    "COLOR_CAMERA_EXIT": (255, 255, 255),  # White "X" on the close button in camera view
    "COLOR_DIALOG_WHITE": (227, 218, 218),  # White elements in the signal dialog
    "COLOR_VIEWCAMERA": (147, 0, 207),  # Purple "View Camera" button
}


disabled = False
signal_mouse_coords = None  # Mouse coordinates used to return cursor to signal when exiting camera/rollback
one_frame_time = round((1000 / AVG_FPS) * 10**-3, 4)  # Calculate time for 1 frame and round to 4 decimal places


def update_check():
    """Fetch the latest release version from the GitHub repo and inform the user if an update is available"""
    # TODO: Implement better version check functionality instead of just difference in strings
    if not UPDATE_CHECK_ENABLED:
        return
    URL = "https://api.github.com/repos/ElectricityMachine/SCR-SGPlus/releases/latest"
    r = requests_get(url=URL)
    data = r.json()
    if VERSION != data["tag_name"]:
        print(f"{colorama.Fore.RED}NOTICE: A new update is available for SG+!")
        print(
            colorama.Fore.RED
            + "It is always recommended to update to the latest version. To do so, go to https://github.com/ElectricityMachine/SCR-SGPlus"
        )
        print(f'{colorama.Fore.RED}and follow the instructions under "Installation"')
        print(colorama.Fore.WHITE)


def color_approx_eq(color1, color2, tolerance: int = 7):
    """Check if a color is equal to another color within a tolerance of 7"""
    return (
        abs(color1[0] - color2[0]) <= tolerance
        and abs(color1[1] - color2[1]) <= tolerance
        and abs(color1[2] - color2[2]) <= tolerance
    )


def screen_grab(x, y, width, height):
    with mss() as sct:
        left = x
        top = y
        right = x + width
        lower = y + height
        bbox = (math.ceil(left), math.ceil(top), math.ceil(right), math.ceil(lower))
        im = sct.grab(bbox)
        # Convert to PIL image for compatibility
        return frombytes("RGB", im.size, im.bgra, "raw", "BGRX")


def mouseclick_left():
    mouse.press("left")
    mouse.release("left")


def sleep_frames(frames, minwait=0):
    if minwait != 0:
        print(max((frames * one_frame_time), minwait))
        time.sleep(max((frames * one_frame_time), minwait))
    else:
        time.sleep(frames * one_frame_time)


def check_able_to_run(callback):
    def wrapper(*args):
        if callback is not None and callable(callback) and not disabled:
            return callback(*args)

    return wrapper


@check_able_to_run
def click_signal(sig):
    coord = mouse.get_position()
    mouseclick_left()
    time.sleep(one_frame_time * 3)
    if scan_for_dialog("signal", coord[0], coord[1]):
        time.sleep(one_frame_time * 2)
        press_and_release(sig)
        time.sleep(AVG_PING / 4_000)
        press_and_release("backspace")


def move_mouse(x, y, speed=1):
    autoit.mouse_move(x, y, speed)


@check_able_to_run
def click_rollback():
    mousex, mousey = mouse.get_position()
    mouseclick_left()
    sleep_frames(2)
    if scan_for_dialog("exitcamera"):
        return
    elif scan_for_dialog("signal", mousex, mousey):
        press_and_release("enter")
    else:
        return
    window = win32gui.GetForegroundWindow()
    rect = win32gui.GetClientRect(window)

    bbox = [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]
    _x = bbox[0]
    _y = bbox[1]
    window_width = bbox[2]
    window_height = bbox[3]
    zone_screen_height, zone_screen_width, zone_screen_x = calculate_zone_screen(window_width, window_height)

    rollback_x = zone_screen_width * 0.89955 + zone_screen_x
    rollback_y = 0.69518 * window_height
    rollback_position = win32gui.ClientToScreen(window, (int(rollback_x), int(rollback_y)))

    move_mouse(x=rollback_position[0], y=rollback_position[1], speed=2)
    mouseclick_left()
    sleep_frames(3)  # Ensure mouseclick registers
    press_and_release("backspace, backspace")
    move_mouse(mousex, mousey, speed=1)
    return


@check_able_to_run
def click_camera():
    global signal_mouse_coords
    if scan_for_dialog("exitcamera"):
        for _ in range(3):
            press_and_release("backspace")
        if signal_mouse_coords:
            move_mouse(signal_mouse_coords[0], signal_mouse_coords[1], speed=1)
        return
    signal_mouse_coords = mouse.get_position()
    mouseclick_left()
    sleep_frames(2, 0.02)
    if scan_for_dialog("signal"):
        press_and_release("enter")
        camera_y = 0.92133
    elif scan_for_dialog("uncontrolled"):
        press_and_release("enter")
        sleep_frames(2)
        camera_y = 0.80137 if scan_for_dialog("viewcamera") == 0 else 0.92133
    else:
        return

    window = win32gui.GetForegroundWindow()
    rect = win32gui.GetClientRect(window)

    bbox = [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]
    _x = bbox[0]
    _y = bbox[1]
    w = bbox[2]
    h = bbox[3]

    # zone_screen_height = math.ceil(0.97735 * h)
    # zone_screen_width = math.ceil(zone_screen_height * 1.34105)
    # zone_screen_x = math.ceil(w / 2 - zone_screen_width / 2)

    zone_screen_height, zone_screen_width, zone_screen_x = calculate_zone_screen(w, h)

    camera_x = zone_screen_width * 0.89414 + zone_screen_x
    camera_y = camera_y * h
    camera_position = win32gui.ClientToScreen(window, (int(camera_x), int(camera_y)))

    sleep_frames(1)
    move_mouse(x=camera_position[0], y=camera_position[1], speed=2)
    mouseclick_left()
    return


def calculate_zone_screen(window_width, window_height):
    zone_screen_height = math.ceil(0.97735 * window_height)
    zone_screen_width = math.ceil(zone_screen_height * 1.34105)
    zone_screen_x = math.ceil(window_width / 2 - zone_screen_width / 2)
    return zone_screen_height, zone_screen_width, zone_screen_x


def toggle_disable():
    global disabled
    if disabled:
        disabled = False
        winsound.Beep(500, 100)
    else:
        disabled = True
        winsound.Beep(400, 100)


@check_able_to_run
def scan_for_dialog(type, mousex=0, mousey=0):
    if mousex is mousey and mousex == 0:
        mousex, mousey = mouse.get_position()
    window = win32gui.GetForegroundWindow()
    rect = win32gui.GetClientRect(window)

    bbox = [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]
    _x = bbox[0]
    _y = bbox[1]
    w = bbox[2]
    h = bbox[3]
    if type == "exitcamera":
        return find_exit_cam_button(w, bbox, window)
    elif type == "signal":
        return find_controlled_sig_dialog(h, mousex, mousey)
    elif type == "uncontrolled":
        return find_uncontrolled_sig_dialog(h, mousex, mousey)
    elif type == "viewcamera":
        return find_camera_buttons(h, w, window)


def find_camera_buttons(h, w, window):
    zone_screen_height, zone_screen_width, zone_screen_x = calculate_zone_screen(w, h)

    camerabutton_height = math.ceil(h * 0.125 * 0.375)
    camerabutton_width = math.ceil(camerabutton_height * 2 / 0.375)
    camerabutton_x = zone_screen_width * 0.79760 + zone_screen_x
    camerabutton_y = h * 0.80629

    screen_cords = win32gui.ClientToScreen(window, (int(camerabutton_x), int(camerabutton_y)))
    capture = screen_grab(
        screen_cords[0],
        screen_cords[1],
        camerabutton_width,
        camerabutton_height * 2,
    ).convert("RGB")
    width, height = capture.size
    uppershelf = capture.crop((0, 0, width, 3))
    lowershelf = capture.crop((0, height * 0.94, width, height))

    imagesToProcess = [uppershelf, lowershelf]
    for image in imagesToProcess:
        for i in range(math.ceil(image.width * 0.2)):
            if image.height == 0:
                break
            r, g, b = image.getpixel((i, image.height - 1))
            if color_approx_eq((r, g, b), COLORS["COLOR_VIEWCAMERA"]):
                return 0 if image == imagesToProcess[0] else 1
    return False


def find_uncontrolled_sig_dialog(h, mousex, mousey):
    dialogbox_height = math.ceil(h * 0.125)
    dialogbox_width = math.ceil(dialogbox_height * 2)
    dialogbox_x = mousex - dialogbox_width / 2
    dialogbox_y = mousey - dialogbox_height

    capture = screen_grab(dialogbox_x, dialogbox_y, dialogbox_width, dialogbox_height * 2).convert("RGB")
    w, h = capture.size
    upper = capture.crop((0, 0, w, h / 2))  # Upper
    lower = capture.crop((0, h / 2, w, h))  # Lower
    upperw, upperh = upper.size
    width, height = lower.size
    lowershelf = lower.crop((0, height * 0.33, width / 2, height * 1 / 3 + 2))
    upper = capture.crop((0, 0, w, h / 2))  # Upper
    upperw, upperh = upper.size
    uppershelf = upper.crop((0, upperh * 0.1, upperw / 2, upperh * 0.1 + 2))
    imagesToProcess = [lowershelf, uppershelf]

    white_pixels = 0
    for image in imagesToProcess:
        for i in range(math.ceil(image.width)):
            for i2 in range(math.ceil(image.height)):
                r, g, b = image.getpixel((i, i2))
                if color_approx_eq((r, g, b), (COLORS["COLOR_DIALOG_WHITE"])):
                    white_pixels += 1
                if white_pixels / image.width >= 0.2:  # Greater than 20% of pixels are white
                    return True

    return False


def find_controlled_sig_dialog(h, mousex, mousey):
    dialogbox_height = math.ceil(h * 0.125)
    dialogbox_width = math.ceil(dialogbox_height * 2)
    dialogbox_x = mousex - dialogbox_width / 2
    dialogbox_y = mousey - dialogbox_height

    capture = screen_grab(dialogbox_x, dialogbox_y, dialogbox_width, dialogbox_height * 2).convert("RGB")
    w, h = capture.size
    upper = capture.crop((0, 0, w, h / 2))
    lower = capture.crop((0, h / 2, w, h))
    upperw, upperh = upper.size
    width, height = lower.size
    lowershelf = lower.crop((0, height * 0.66, width, height * 0.66 + 3))
    uppershelf = upper.crop((0, upperh * 0.4, upperw, upperh * 0.4 + 2))
    imagesToProcess = [lowershelf, uppershelf]

    white_pixels = 0
    for image in imagesToProcess:
        for i in range(math.ceil(image.width / 1.6)):
            if image.height == 0:
                break
            r, g, b = image.getpixel((i, image.height - 1))
            if color_approx_eq((r, g, b), (COLORS["COLOR_DIALOG_WHITE"])):
                white_pixels += 1
            for val in COLORS["COLOR_DIALOG_BUTTONS"]:
                if color_approx_eq((r, g, b), (val)) or white_pixels / (image.width * image.height) >= 0.05:
                    return True

        return False


def find_exit_cam_button(w, bbox, window):
    camera_controls_width = 283
    camera_controls_x = math.ceil(w / 2 - camera_controls_width / 2)

    y = bbox[1]
    exit_camera_button_y = 85 + y
    exit_camera_button_x = 0.91166 * camera_controls_width + camera_controls_x - 5
    exit_camera_button_width = exit_camera_button_height = 50

    screen_cords = win32gui.ClientToScreen(window, (int(exit_camera_button_x), int(exit_camera_button_y)))
    capture = screen_grab(
        screen_cords[0],
        screen_cords[1],
        exit_camera_button_width,
        exit_camera_button_height,
    ).convert("RGB")
    width, height = capture.size
    lowershelf = capture.crop((0, height / 2, width, height / 2 + 2))
    imagesToProcess = [lowershelf]

    lowershelf.load()

    for image in imagesToProcess:
        if image.height == 0:
            break
        for i in range(math.ceil(image.width / 1.6)):
            r, g, b = image.getpixel((i, image.height - 1))
            if color_approx_eq((r, g, b), (COLORS["COLOR_CAMERA_EXIT"])):
                return True

    return False


@check_able_to_run
def send_zone_message(zone: str):
    """Copy a Zone opening message to the user's clipboard and sound an audible tone

    Args:
        zone (str): Which Zone message to copy
    """
    switch = {
        "A": "Zone A (Stepford Area, Willowfield, Whitefield branches) is now under manual signalling control.",
        "B": "Zone B (St. Helens Bridge, Coxly, Beaulieu Park corridor) is now under manual signalling control.",
        "C": "Zone C (Stepford Airport Area) is now under manual signalling control.",
        "D": "Zone D (Morganstown to Leighton West) is now under manual signalling control.",
        "E": "Zone E (Llyn-by-the-Sea to Edgemead) is now under manual signalling control.",
        "F": "Zone F (Benton area + Waterline up to but not including Airport West and Morganstown) is now under manual signalling control.",
        "G": "Zone G (James St. to Esterfield) is now under manual signalling control.",
    }

    winsound.Beep(600, 200)
    pyperclip.copy(switch.get(zone))


@check_able_to_run
def enabled_warning():
    """Play a warning beep if script is enabled"""
    winsound.Beep(640, 300)


if __name__ == "__main__":
    add_hotkey(2, click_signal, args=["1"])  # 1
    add_hotkey(3, click_signal, args=["2"])  # 2
    add_hotkey(4, click_signal, args=["3"])  # 3
    add_hotkey(46, click_camera)  # C
    add_hotkey(59, toggle_disable)  # F1
    add_hotkey("R", click_rollback)  # R
    add_hotkey("/", enabled_warning)  # / warning when opening chat while enabled
    add_hotkey("`", enabled_warning)  # Command bar
    add_hotkey("'", enabled_warning)  # Command bar
    add_hotkey(79, send_zone_message, args=["A"])  # Num 1
    add_hotkey(80, send_zone_message, args=["B"])  # Num 2
    add_hotkey(81, send_zone_message, args=["C"])  # Num 3
    add_hotkey(75, send_zone_message, args=["D"])  # Num 4
    add_hotkey(76, send_zone_message, args=["E"])  # Num 5
    add_hotkey(77, send_zone_message, args=["F"])  # Num 6
    add_hotkey(71, send_zone_message, args=["G"])  # Num 7

    if update_check:
        update_check()
    winsound.Beep(500, 200)
    print("SG+ Successfully Initialized")
    keyboard_wait()
