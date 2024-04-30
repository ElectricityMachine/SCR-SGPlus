# Made by ElectricityMachine
# Version: 0.5.1
# Major changes: Status indicator, config file
# Description: A script to automate tasks when signalling for SCR
# Keybinds: 1 2 3 for Danger, Caution, and Proceed signal settings. C for Camera. R for Rollback Toggle.
# How to use: Hover over a signal and press the corresponding keybind to perform the action
# Limitations: Windows only, only works on primary monitor

import logging
import math
import sys
import threading
import time
import winsound
from collections.abc import Callable
from typing import Any
from update_checker import coerce

import tkinter as tk

import colorama
import mouse
import pyperclip
import tomli_w
import tomllib
import win32gui
from keyboard import add_hotkey, press_and_release
from keyboard import wait as keyboard_wait
from mss import mss
from numpy import array as np_array
from PIL.Image import Image, frombytes

import autoit
from constants import VERSION, Colors
from update_checker import check_for_updates

config = None
enabled = True
signal_mouse_coords: tuple[int, int]

logging.basicConfig(
    stream=sys.stdout,
    format="%(levelname)s: %(funcName)s: %(message)s",
)


def screen_grab(x: int, y: int, width: int, height: int):
    """Return a screenshot of the user's screen given some bounding box

    Args:
        x (int): x-coordinate
        y (int): y-coordinate
        width (int): width of the screengrab
        height (int): height of the screengrab

    Returns:
        Image: PIL-compatible Image in RGB format
    """
    with mss() as sct:
        left = x
        top = y
        right = x + width
        lower = y + height
        bbox = (math.ceil(left), math.ceil(top), math.ceil(right), math.ceil(lower))
        im = sct.grab(bbox)
        return frombytes("RGB", im.size, im.bgra, "raw", "BGRX")


def move_mouse(x: int, y: int, speed: int = 1):
    autoit.mouse_move(x, y, speed)


def update_label(text, colour):
    label.config(text=text, fg="white", bg="green" if enabled else "red")


def move_text_pos(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x_position = (screen_width - window_width) // 2
    y_position = int(screen_height * 0.04)
    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")


def toggle_label_visibility(root):
    if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Roblox":
        root.deiconify()
    else:
        root.withdraw()

    root.after(100, lambda: toggle_label_visibility(root))

def create_update_label(root):
    global label
    root.overrideredirect(True)
    root.attributes("-alpha", 0.85)
    root.attributes("-topmost", True)
    label = tk.Label(root, text="SG+", bg="green", fg="white", font=("Consolas", 24))
    label.pack(fill="both", expand=True)
    move_text_pos(root)

    toggle_label_visibility(root)


def sleep_frames(frames: int, minwait: float = 0) -> None:
    logging.debug(f"Sleeping for {frames} frame(s)")
    one_frame_time = round((1000 / config["average_fps"]) * 10**-3, 4)
    time.sleep(max((frames * one_frame_time), minwait))


def is_able_to_run():
    return enabled and win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Roblox"


def check_able_to_run(callback: Callable[..., Any]) -> None | Callable[..., Any]:
    logging.debug("called")

    def wrapper(*args):
        if is_able_to_run() and callable(callback):
            logging.debug("able to run")
            return callback(*args)
        else:
            logging.debug("not able to run, returning")
            return None

    return wrapper


@check_able_to_run
def click_signal(sig: str) -> None:
    logging.debug("called")
    coord = mouse.get_position()
    mouse.click("left")
    sleep_frames(3)
    result, image = scan_for_dialog("signal", coord[0], coord[1])
    if result:
        logging.debug("scan_for_dialog returned true")
        sleep_frames(3)
        press_and_release(sig)
        press_and_release("backspace")


def calculate_bbox(rect: tuple) -> tuple[int, int, int, int]:
    return (rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1])


@check_able_to_run
def click_rollback() -> None:
    logging.debug("called")
    mousex, mousey = mouse.get_position()
    mouse.click("left")
    sleep_frames(2)
    if scan_for_dialog("exitcamera"):
        logging.debug("scan_for_dialog(exitcamera) returned true")
        return
    result, image = scan_for_dialog("signal", mousex, mousey)
    if result:
        logging.debug("scan_for_dialog(signal) returned true, pressing enter")
        press_and_release("enter")
    else:
        logging.debug("return path")
        return
    logging.debug("click_rollback: execute main body outside if-elif path")
    window = win32gui.GetForegroundWindow()
    rect = win32gui.GetClientRect(window)

    x, y, window_width, window_height = calculate_bbox(rect)
    zone_screen_height, zone_screen_width, zone_screen_x, zone_screen_y = calculate_zone_screen(
        window_width, window_height
    )

    rollback_x_edge = int(zone_screen_width * 0.795 + zone_screen_x)
    rollback_x = int(zone_screen_width * 0.80 + zone_screen_x)
    rollback_y = int(0.69518 * window_height)
    rollback_edge_position = win32gui.ClientToScreen(window, (rollback_x_edge, rollback_y))
    rollback_position = win32gui.ClientToScreen(window, (rollback_x, rollback_y))
    move_mouse(x=rollback_edge_position[0], y=rollback_position[1], speed=0)
    move_mouse(x=rollback_position[0], y=rollback_position[1], speed=2)

    mouse.click("left")
    sleep_frames(1)
    press_and_release("backspace")
    press_and_release("backspace")
    move_mouse(mousex, mousey, speed=0)
    return


@check_able_to_run
def toggle_signal_sidemenu() -> None:
    logging.debug("\n\n\n\n\n\ncalled")
    mousex, mousey = mouse.get_position()
    window = win32gui.GetForegroundWindow()
    rect = win32gui.GetClientRect(window)

    x, y, w, h = calculate_bbox(rect)
    if find_camera_buttons(h, w, window) is not False:
        logging.debug("dialogbox found, closing menus")
        press_and_release("backspace")
        press_and_release("backspace")
        return
    logging.debug("after return")
    mouse.click("left")
    sleep_frames(2)
    result, image = scan_for_dialog("signal", mousex, mousey)
    if result:
        logging.debug("scan_for_dialog(signal) returned true, pressing enter")
        press_and_release("enter")
        return
    elif scan_for_dialog("uncontrolled", mousex, mousey):
        logging.debug("uncontrolled signal found, pressing enter")
        press_and_release("enter")
        return


@check_able_to_run
def click_camera() -> None:
    logging.debug("called")
    global signal_mouse_coords

    if scan_for_dialog("exitcamera"):
        logging.debug("scan_for_dialog(exitcamera) returned true, pressing backspace twice")
        press_and_release("backspace")
        press_and_release("backspace")
        if signal_mouse_coords:
            move_mouse(signal_mouse_coords[0], signal_mouse_coords[1], speed=1)
        return
    logging.debug("exitcamera dialog not found, executing main body")
    signal_mouse_coords = mouse.get_position()
    mouse.click("left")
    sleep_frames(2)
    result, dialogbox_image = scan_for_dialog("signal")
    if result:
        logging.debug("signal scan_for_dialog found")
        press_and_release("enter")
        camera_y = 0.92133
    elif scan_for_dialog("uncontrolled", image=dialogbox_image):
        logging.debug("uncontrolled signal found in click_camera")
        window = win32gui.GetForegroundWindow()
        rect = win32gui.GetClientRect(window)

        x, y, w, h = calculate_bbox(rect)
        press_and_release("enter")
        sleep_frames(2)
        result = find_camera_buttons(h, w, window)
        logging.debug(f"result is {result}")
        if result is False:
            logging.debug("returning because result is False, no dialog found")
            return
        camera_y = 0.80137 if result == 1 else 0.92133
        x = "lower number" if camera_y == 0.80137 else "upper number"
        logging.debug(f"uncontrolled scan_for_dialog true in click_camera with x-value of {x}")
    else:
        logging.debug("return none path in click_camera")
        return
    logging.debug("outside if-elif path")
    window = win32gui.GetForegroundWindow()
    rect = win32gui.GetClientRect(window)

    x, y, w, h = calculate_bbox(rect)

    zone_screen_height, zone_screen_width, zone_screen_x, zone_screen_y = calculate_zone_screen(w, h)

    camera_x_edge = int(zone_screen_width * 0.795 + zone_screen_x)
    camera_x = int(zone_screen_width * 0.80 + zone_screen_x)
    camera_y = int(camera_y * h)
    camera_middle_position = win32gui.ClientToScreen(window, (camera_x_edge, camera_y))
    camera_position = win32gui.ClientToScreen(window, (camera_x, camera_y))

    move_mouse(x=camera_middle_position[0], y=camera_position[1], speed=0)
    move_mouse(x=camera_position[0], y=camera_position[1], speed=2)
    mouse.click("left")
    return


def calculate_zone_screen(window_width: int, window_height: int) -> tuple[int, int, int, int]:
    ZONE_SCREEN_HEIGHT_RATIO = 0.97735
    ZONE_SCREEN_WIDTH_RATIO = 1.34105
    zone_screen_height = math.ceil(ZONE_SCREEN_HEIGHT_RATIO * window_height)
    zone_screen_width = math.ceil(zone_screen_height * ZONE_SCREEN_WIDTH_RATIO)
    zone_screen_x = math.ceil(window_width / 2 - zone_screen_width / 2)
    zone_screen_y = math.floor(window_height * 0.0098328416912488)
    return zone_screen_height, zone_screen_width, zone_screen_x, zone_screen_y


def toggle_disable(reason: str) -> None:
    global enabled, disabled_reason
    logging.debug(f"enabled is {enabled}")
    enabled = not enabled
    beep = threading.Thread(target=lambda: winsound.Beep(500, 100) if enabled else winsound.Beep(400, 100))
    beep.start()

    if config["enable_status_indicator"]:
        update_label("SG+" if enabled else "SG-", "white")
    disabled_reason = reason


# TODO: Swap variables "h, w" for "w, h" for readability
# TODO: Get rid of this function to reduce abstraction


def scan_for_dialog(
    type: str, mousex: int = 0, mousey: int = 0, image: Image | None = None
) -> bool | int | bool | Image:
    logging.debug("called")
    if mousex == mousey and mousex == 0:
        mousex, mousey = mouse.get_position()
    window = win32gui.GetForegroundWindow()
    rect = win32gui.GetClientRect(window)

    bbox = (rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1])
    _x = bbox[0]
    _y = bbox[1]
    w = bbox[2]
    h = bbox[3]
    if type == "exitcamera":
        return find_exit_cam_button(w, bbox, window)
    elif type == "signal":
        return find_controlled_sig_dialog(w, h, mousex, mousey)
    elif type == "uncontrolled":
        return find_uncontrolled_sig_dialog(h, w, mousex, mousey, image)
    elif type == "viewcamera":
        return find_camera_buttons(h, w, window)

    return False


def find_uncontrolled_sig_dialog(h: int, w: int, mousex: int, mousey: int, dialogbox_image=None) -> bool:
    logging.debug("called")
    capture = dialogbox_image or capture_dialogbox(w, h, mousex, mousey)

    capture_width, capture_height = capture.size
    lower_x = upper_x = capture_width * 0.01
    upper_y = capture_height * 0.05
    upper = capture.crop((upper_x, upper_y, 0 + capture_width / 2.5, upper_y + 4))
    lower_y = capture_height * 0.65
    lower = capture.crop((lower_x, lower_y, 0 + capture_width / 2.5, lower_y + 4))

    imagesToProcess = [lower, upper]
    for image in imagesToProcess:
        logging.debug("iterating images")
        if check_color_percentage_single(image, Colors.COLOR_DIALOG_WHITE, compareThreshold=10):
            logging.debug("image loop: numpy white pixels returned success")
            return True
    logging.debug("return false path")
    return False


def capture_dialogbox(w: int, h: int, mousex: int, mousey: int):
    dialogbox_height = math.ceil(h * 0.125)
    dialogbox_width = math.ceil(dialogbox_height * 2)
    dialogbox_x = math.floor(mousex - dialogbox_width / 2)
    dialogbox_y = math.floor(mousey - dialogbox_height)

    dialogbox_left_bound = dialogbox_x
    dialogbox_right_bound = dialogbox_x + dialogbox_width

    zone_screen_height, zone_screen_width, zsx, zsy = calculate_zone_screen(w, h)
    zone_screen_x, zone_screen_y = win32gui.ClientToScreen(win32gui.GetForegroundWindow(), (zsx, zsy))
    zone_screen_right_bound = zone_screen_x + zone_screen_width
    zone_screen_left_bound = zone_screen_x
    dialogbox_left_bound = dialogbox_x
    if zone_screen_right_bound < dialogbox_right_bound:
        dialogbox_x -= abs(zone_screen_right_bound - dialogbox_right_bound)
    elif zone_screen_left_bound > dialogbox_left_bound:
        dialogbox_x += abs(zone_screen_left_bound - dialogbox_left_bound)
    return screen_grab(dialogbox_x, dialogbox_y, dialogbox_width, dialogbox_height * 2)


def find_controlled_sig_dialog(w: int, h: int, mousex: int, mousey: int) -> tuple[bool, Image]:
    logging.debug("called")
    capture = capture_dialogbox(w, h, mousex, mousey)

    w, h = capture.size
    upper = capture.crop((0, 0, w, h / 2))
    lower = capture.crop((0, h / 2, w, h))
    upperw, upperh = upper.size
    width, height = lower.size
    lowershelf = lower.crop((0, height * 0.66, width, height * 0.66 + 3))
    uppershelf = upper.crop((0, upperh * 0.4, upperw, upperh * 0.4 + 2))
    imagesToProcess = [lowershelf, uppershelf]
    logging.debug("made it to generator")
    result = any(
        check_color_percentage_single(image, Colors.COLOR_DIALOG_WHITE, threshold=0.01)
        and check_color_multiple(image, Colors.COLOR_DIALOG_BUTTONS)
        for image in imagesToProcess
    )  # this doesn't run if check for white pixels is false. must change TODO
    logging.debug(f"result: {result}")

    return result, capture


def find_camera_buttons(h: int, w: int, windowID: int):
    logging.debug("called")
    zone_screen_height, zone_screen_width, zone_screen_x, zone_screen_y = calculate_zone_screen(w, h)

    camerabutton_height = math.ceil(h * 0.125 * 0.375)
    camerabutton_width = math.ceil(camerabutton_height * 2 / 0.375)
    camerabutton_x = zone_screen_width * 0.8 + zone_screen_x
    camerabutton_y = h * 0.82

    screen_cords = win32gui.ClientToScreen(windowID, (int(camerabutton_x), int(camerabutton_y)))
    capture = screen_grab(
        screen_cords[0],
        screen_cords[1],
        camerabutton_width,
        camerabutton_height * 2,
    )
    width, height = capture.size
    uppershelf = capture.crop((0, 0, width * 0.1, height / 4))
    lowershelf = capture.crop((0, height / 2.5, width * 0.1, height))

    imagesToProcess = [uppershelf, lowershelf]
    for image in imagesToProcess:
        if check_color_multiple(image, Colors.COLOR_VIEWCAMERA):
            logging.debug(
                f"View camera button found. We got {0 if image==imagesToProcess[0] else 1} (0=upper, 1=lower)"
            )
            return 0 if image is lowershelf else 1
    logging.debug("none found")
    return False


def find_exit_cam_button(w: int, bbox: tuple[int, int, int, int], window):
    logging.debug("called")
    camera_controls_width = 283
    camera_controls_x = math.ceil(w / 2 - camera_controls_width / 2)

    rect = win32gui.GetClientRect(win32gui.GetForegroundWindow())
    x, y, w, h = calculate_bbox(rect)
    exit_camera_button_y = 85 + y
    exit_camera_button_x = 0.91166 * camera_controls_width + camera_controls_x - 5
    exit_camera_button_width = 50
    exit_camera_button_height = exit_camera_button_width

    screen_cords = win32gui.ClientToScreen(window, (int(exit_camera_button_x), int(exit_camera_button_y)))
    capture = screen_grab(
        screen_cords[0],
        screen_cords[1],
        exit_camera_button_width,
        exit_camera_button_height,
    )
    width, height = capture.size
    lowershelf = capture.crop((0, height / 2, width, height / 2 + 2))
    imagesToProcess = [lowershelf]

    return all(check_color_single(image, Colors.COLOR_CAMERA_EXIT) for image in imagesToProcess)


def color_approx_eq_np(
    inputColor: tuple[int, int, int], colorToCompare: tuple[int, int, int], threshold: int = 5
) -> bool:
    """Check if a color is equal to another color within a given value

    Args:
        inputColor (tuple): First RGB color to check against
        colorToCompare (tuple): Second RGB color to check against
        threshold (int, optional): How many units of R, G, or B to tolerate. Defaults to 5.

    Returns:
        bool: Whether or not the colors are approximately equal to each other
    """
    # Calculate the absolute difference between each color component
    diff = [abs(c1 - c2) for c1, c2 in zip(inputColor, colorToCompare)]

    # Check if the maximum difference is within the threshold
    return max(diff) <= threshold


def check_color_single(image: Image, color: tuple[int, int, int], threshold: int = 7) -> bool:
    start_time = time.perf_counter()
    logging.debug("called")
    arr = np_array(image)

    # Iterate over the y-axis
    for i in range(arr.shape[0]):
        # Iterate over the x-axis
        for j in range(arr.shape[1]):
            col_to_compare = arr[i, j]
            if color_approx_eq_np(col_to_compare, color, threshold):
                logging.debug("colors similar, return True")
                logging.debug(f"Time taken was {time.perf_counter() - start_time}")
                return True
    logging.debug("no similar colors found, returning False")
    return False


def check_color_multiple(image: Image, colors: list[tuple[int, int, int]], threshold: int = 7) -> bool:
    logging.debug("called")
    arr = np_array(image)

    # Iterate over the y-axis
    for i in range(arr.shape[0]):
        # Iterate over the x-axis
        for j in range(arr.shape[1]):
            # Get the tuple from the element
            col_to_compare = arr[i, j]
            for color in colors:
                if color_approx_eq_np(col_to_compare, color, threshold):
                    logging.debug("colors similar, return True")
                    return True
    logging.debug("no similar colors found, returning False")
    return False


def check_color_percentage_single(
    image: Image, color: tuple[int, int, int], compareThreshold: int = 7, threshold: float = 0.05
) -> bool:
    logging.debug("called")
    matching_pixels = 0
    arr = np_array(image)

    # Iterate over the y-axis
    for i in range(arr.shape[0]):
        # Iterate over the x-axis
        for j in range(arr.shape[1]):
            # Get the tuple from the element
            col_to_compare = arr[i, j]
            if color_approx_eq_np(col_to_compare, color, compareThreshold):
                matching_pixels += 1
            if matching_pixels / arr.size >= threshold:
                logging.debug(f"matching pixels > {threshold * 10 ** 2}% found")
                return True
    logging.debug(f"not enough white pixels found for array size. numpixels: {matching_pixels/arr.size}")
    return False


@check_able_to_run
def send_zone_message(zone: str) -> None:
    """Copy a Zone opening message to the user's clipboard and sound an audible tone

    Args:
        zone (str): Which Zone message to copy
    """

    beep = threading.Thread(target=lambda: winsound.Beep(600, 200))
    beep.start()

    pyperclip.copy(config["zone_opening_messages"][zone])


@check_able_to_run
def enabled_warning():
    # Chat key or command bar button was pressed
    """Play a warning sound if script is enabled. Disables script if config option 'auto_disable_on_chat' is set."""
    global enabled
    if enabled and config["auto_disable_on_chat"]:
        toggle_disable("CHAT")
        return
    beep = threading.Thread(target=lambda: winsound.Beep(640, 300))
    beep.start()


def auto_enable_on_enter():
    global disabled_reason
    if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Roblox" and not enabled and disabled_reason == "CHAT":
        toggle_disable("CHAT")


def init_config() -> None:
    default_config = {
        "VERSION_DO_NOT_EDIT": VERSION,
        "onboard_msg": True,
        "average_fps": 30,
        "enable_update_checker": True,
        "debug_mode_enabled": False,
        "auto_disable_on_chat": True,
        "auto_enable_on_enter": True,
        "enable_status_indicator": True,
        "keybinds": {
            "set_signal_danger": 2,
            "set_signal_caution": 3,
            "set_signal_proceed": 4,
            "toggle_signal_camera": "C",
            "toggle_macro": "F1",
            "toggle_signal_rollback": "R",
            "toggle_signal_sidemenu": "F",
            "zone_a_message": 79,
            "zone_b_message": 80,
            "zone_c_message": 81,
            "zone_d_message": 75,
            "zone_e_message": 76,
            "zone_f_message": 77,
            "zone_g_message": 71,
            "warning_keys": ["/", "'", "`"],
        },
        "zone_opening_messages": {
            "A": "Zone A (Stepford Area, Willowfield, Whitefield branches) is now under manual signalling control.",
            "B": "Zone B (St. Helens Bridge, CXY, Beaulieu Park corridor) is now under manual signalling control.",
            "C": "Zone C (Stepford Airport Area) is now under manual signalling control.",
            "D": "Zone D (Morganstown to LW) is now under manual signaling control.",
            "E": "Zone E (Llyn-by-the-Sea to Edgemead) is now under manual signalling control.",
            "F": "Zone F (Benton area + Waterline up to but not including Airport West and Morganstown) is now under manual signalling control.",
            "G": "Zone G (James St. to Esterfield) is now under manual signalling control.",
        },
    }
    try:
        with open("config.toml", "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        logging.warning("Configuration file not found! Writing default config.")
        with open("config.toml", "wb") as f:
            tomli_w.dump(default_config, f)
            return default_config


def migrate_config():
    try:
        ver_num = config["VERSION_DO_NOT_EDIT"]
    except KeyError:
        ver_num = None

    if not ver_num or (
        (coerce(ver_num) < coerce(VERSION)) and (coerce(VERSION) < coerce("0.5.0") or coerce(ver_num) < coerce("0.5"))
    ):
        # TODO: Write tests for the config migration
        # Changes made in 0.5:
        # Fix incorrect numpad keybinds (#55)
        # Auto disable on chat, re-enable on enter
        # F key opens sidemenu
        # Option for status indicator
        config["keybinds"] = {
            "set_signal_danger": 2,
            "set_signal_caution": 3,
            "set_signal_proceed": 4,
            "toggle_signal_camera": "C",
            "toggle_macro": "F1",
            "toggle_signal_rollback": "R",
            "toggle_signal_sidemenu": "F",
            "zone_a_message": 79,
            "zone_b_message": 80,
            "zone_c_message": 81,
            "zone_d_message": 75,
            "zone_e_message": 76,
            "zone_f_message": 77,
            "zone_g_message": 71,
            "warning_keys": ["/", "'", "`"],
        }
        config["auto_disable_on_chat"] = True
        config["auto_enable_on_enter"] = True
        config["enable_update_checker"] = True
        config["enable_status_indicator"] = True
        config["VERSION_DO_NOT_EDIT"] = VERSION
        with open("config.toml", "wb") as f:
            tomli_w.dump(config, f)
        logging.warning(
            "[CONFIG MIGRATION]: Your keybinds were overriden to fix an issue with the zone opening messages."
        )
        logging.warning(
            "[CONFIG MIGRATION]: This issue was introduced in 0.4.1. More info: https://github.com/ElectricityMachine/SCR-SGPlus/issues/55"
        )
        logging.warning("[CONFIG MIGRATION]: Please edit config.toml if you need to. This migration only happens once.")
        logging.warning(
            '[CONFIG MIGRATION]: A new feature to disable SG+ when opening the chat box was added. Change `auto_disable_on_chat` to "False" to disable this feature.'
        )
        logging.warning(
            '[CONFIG MIGRATION]: A new feature was added to open the signal sidemenu. Default keybind is "F". To use, hover over a signal and press it. Press again to close.'
        )
    else:
        config["VERSION_DO_NOT_EDIT"] = VERSION
        with open("config.toml", "wb") as f:
            tomli_w.dump(config, f)


if __name__ == "__main__":
    if sys.version_info < (3, 12):
        raise Exception(
            "Your Python version is incompatible with this script. Please update Python by going to https://python.org and downloading the latest version for your operating system"
        )
    config = init_config()
    migrate_config()
    log_lvl = logging.DEBUG if config["debug_mode_enabled"] else logging.INFO
    logging.getLogger().setLevel(log_lvl)

    keybinds = config["keybinds"]
    add_hotkey(keybinds["set_signal_danger"], lambda: click_signal("1"))  # 1
    add_hotkey(keybinds["set_signal_caution"], lambda: click_signal("2"))  # 2
    add_hotkey(keybinds["set_signal_proceed"], lambda: click_signal("3"))  # 3
    add_hotkey(keybinds["toggle_signal_camera"], lambda: click_camera())
    add_hotkey(keybinds["toggle_macro"], lambda: toggle_disable("F1"))
    add_hotkey(keybinds["toggle_signal_rollback"], lambda: click_rollback())
    for i in keybinds["warning_keys"]:
        add_hotkey(i, lambda: enabled_warning())
    if config["auto_enable_on_enter"]:
        add_hotkey("enter", lambda: auto_enable_on_enter())
        add_hotkey("shift+enter", lambda: auto_enable_on_enter())
    add_hotkey(keybinds["zone_a_message"], lambda: send_zone_message("A"))  # Num 1
    add_hotkey(keybinds["zone_b_message"], lambda: send_zone_message("B"))  # Num 2
    add_hotkey(keybinds["zone_c_message"], lambda: send_zone_message("C"))  # Num 3
    add_hotkey(keybinds["zone_d_message"], lambda: send_zone_message("D"))  # Num 4
    add_hotkey(keybinds["zone_e_message"], lambda: send_zone_message("E"))  # Num 5
    add_hotkey(keybinds["zone_f_message"], lambda: send_zone_message("F"))  # Num 6
    add_hotkey(keybinds["zone_g_message"], lambda: send_zone_message("G"))  # Num 7
    add_hotkey(keybinds["toggle_signal_sidemenu"], lambda: toggle_signal_sidemenu())

    colorama.init()

    if config["enable_update_checker"]:
        check_for_updates()
    else:
        logging.info("Skipping update check")
    winsound.Beep(500, 200)
    logging.info(f"SG+ {VERSION} Successfully Initialized")
    logging.info(f"Current FPS: {config["average_fps"]}")
    if config["onboard_msg"]:
        print("Thanks for using my script! If you have an issue, feel free to open an issue on GitHub or DM me")
        print("Too slow? Increase your average_fps in config.toml. 40 can work well")
        print("Script not working/dialog opens without anything happening? Decrease your average_fps")
        print("Want to change keybinds or zone messages? It's all in the same file!")
        print("Don't like the status indicator at the top? Same file, under 'enable_status_indicator'")
        print("To hide this message, change 'onboard_msg' to false in config.toml")

    if config["enable_status_indicator"]:
        root = tk.Tk()
        create_update_label(root)
        root.mainloop()
    keyboard_wait()
