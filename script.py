# ElectricityMachine
# Version: 0.3.1-alpha
# Major changes: Python 12 support, refactor
# Description: A script to automate tasks when signalling for SCR
# Keybinds: 1 2 3 for Danger, Caution, and Proceed signal settings. C for Camera. R for Rollback Toggle.
# How to use: Hover over a signal and press the corresponding keybind to perform the action
# Limitations: Windows only, only works on primary monitor

import math
import time
from typing import Literal

from collections.abc import Callable
import winsound
import logging
import autoit
import sys
import colorama
import mouse
import pyperclip
import win32gui
import threading
from numpy import array as np_array, allclose as np_allclose
from settings import AVG_FPS, VERSION, AVG_PING, DEBUG_ENABLED, UPDATE_CHECK_ENABLED, Colors
from keyboard import add_hotkey, press_and_release
from keyboard import wait as keyboard_wait
from mss import mss
from PIL.Image import frombytes, Image
from requests import get as requests_get

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if DEBUG_ENABLED else logging.INFO)
enabled = True
signal_mouse_coords: tuple = ()  # Mouse coordinates used to return cursor to signal when exiting camera/rollback
one_frame_time = round((1000 / AVG_FPS) * 10**-3, 4)


def update_check() -> None:
    logging.debug("update_check: called")
    """Fetch the latest release version from the GitHub repo and inform the user if an update is available"""
    # TODO: Implement better version check functionality instead of just difference in strings
    # TODO: Use async for this function somehow, so we don't block.
    if not UPDATE_CHECK_ENABLED:
        return
    URL = "https://api.github.com/repos/ElectricityMachine/SCR-SGPlus/releases/latest"
    r = requests_get(url=URL)
    data = r.json()
    if VERSION != data["tag_name"]:
        print(f"{colorama.Fore.RED}NOTICE: A new update is available for SG+!")
        print(
            "It is always recommended to update to the latest version. To do so, go to https://github.com/ElectricityMachine/SCR-SGPlus"
        )
        print('and follow the instructions under "Installation"')
        print(colorama.Fore.WHITE)


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
        # Convert to PIL image for compatibility
        return frombytes("RGB", im.size, im.bgra, "raw", "BGRX")


def mouse_click(button: Literal["left", "right"]) -> None:
    mouse.press(button)
    mouse.release(button)


def move_mouse(x: int, y: int, speed=1):
    autoit.mouse_move(x, y, speed)


def sleep_frames(frames: int, minwait=0) -> None:
    logging.debug(f"Sleeping for {frames} frame(s)")
    time.sleep(max((frames * one_frame_time), minwait))


def check_able_to_run(callback: Callable) -> None | Callable:
    logging.debug("check_able_to_run: called")

    def wrapper(*args):
        if (
            enabled
            and win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Roblox"
            and callback is not None
            and callable(callback)
        ):
            logging.debug("check_able_to_run: able to run")
            return callback(*args)
        else:
            logging.debug("check_able_to_run: not able to run, returning")
            return None

    return wrapper


@check_able_to_run
def click_signal(sig: str) -> None:
    logging.debug("click_signal: called")
    coord = mouse.get_position()
    mouse_click("left")
    time.sleep(one_frame_time * 2)
    if scan_for_dialog("signal", coord[0], coord[1]):
        logging.debug("click_signal: scan_for_dialog returned true")
        time.sleep(one_frame_time * 3)
        press_and_release(sig)
        time.sleep(AVG_PING / 4_000)
        press_and_release("backspace")


@check_able_to_run
def click_rollback() -> None:
    logging.debug("click_rollback: called")
    mousex, mousey = mouse.get_position()
    mouse_click("left")
    sleep_frames(2)
    if scan_for_dialog("exitcamera"):
        logging.debug("click_rollback: scan_for_dialog(exitcamera) returned true")
        return
    elif scan_for_dialog("signal", mousex, mousey):
        logging.debug("click_rollback: scan_for_dialog(signal) returned true, pressing enter")
        press_and_release("enter")
    else:
        logging.debug("return path in click_rollback")
        return
    logging.debug("click_rollback: execute main body outside if-elif path")
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

    move_mouse(x=rollback_position[0], y=rollback_position[1], speed=1)
    mouse_click("left")
    sleep_frames(3)
    press_and_release("backspace, backspace")
    move_mouse(mousex, mousey, speed=0)
    return


@check_able_to_run
def click_camera() -> None:
    logging.debug("click_camera: called")
    global signal_mouse_coords
    if scan_for_dialog("exitcamera"):
        logging.debug("click_camera: scan_for_dialog(exitcamera) returned true, pressing backspace twice")
        for _ in range(2):
            press_and_release("backspace")
        if signal_mouse_coords:
            move_mouse(signal_mouse_coords[0], signal_mouse_coords[1], speed=1)
        return
    logging.debug("click_camera: exitcamera dialog not found, executing main body")
    signal_mouse_coords = mouse.get_position()
    mouse_click("left")
    sleep_frames(2)
    if scan_for_dialog("signal"):
        logging.debug("click_camera: signal scan_for_dialog found")
        press_and_release("enter")
        camera_y = 0.92133
    elif scan_for_dialog("uncontrolled"):
        logging.debug("click_camera: uncontrolled signal found in click_camera")
        press_and_release("enter")
        # sleep_frames(2)
        camera_y = 0.80137 if scan_for_dialog("viewcamera") == 0 else 0.92133
        x = "lower number" if camera_y == 0.80137 else "upper number"
        logging.debug(f"click_camera: uncontrolled scan_for_dialog true in click_camera with x-value of {x}")
    else:
        logging.debug("click_camera: return none path in click_camera")
        return
    logging.debug("click_camera: outside if-elif path")
    window = win32gui.GetForegroundWindow()
    rect = win32gui.GetClientRect(window)

    bbox = [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]
    _x = bbox[0]
    _y = bbox[1]
    w = bbox[2]
    h = bbox[3]

    zone_screen_height, zone_screen_width, zone_screen_x = calculate_zone_screen(w, h)

    camera_x = zone_screen_width * 0.89414 + zone_screen_x
    camera_y = camera_y * h
    camera_position = win32gui.ClientToScreen(window, (int(camera_x), int(camera_y)))

    sleep_frames(1)
    move_mouse(x=camera_position[0], y=camera_position[1], speed=2)
    mouse_click("left")
    return


def calculate_zone_screen(window_width: int, window_height: int) -> tuple:
    ZONE_SCREEN_HEIGHT_RATIO = 0.97735
    ZONE_SCREEN_WIDTH_RATIO = 1.34105
    zone_screen_height = math.ceil(ZONE_SCREEN_HEIGHT_RATIO * window_height)
    zone_screen_width = math.ceil(zone_screen_height * ZONE_SCREEN_WIDTH_RATIO)
    zone_screen_x = math.ceil(window_width / 2 - zone_screen_width / 2)
    return zone_screen_height, zone_screen_width, zone_screen_x


def toggle_disable() -> None:
    global enabled
    logging.debug(f"toggle_disable called: enabled is {enabled}")
    enabled = not enabled
    beep = threading.Thread(target=lambda: winsound.Beep(500, 100) if enabled else winsound.Beep(400, 100))
    beep.start()


def scan_for_dialog(type: str, mousex=0, mousey=0) -> bool | int | bool:
    logging.debug("scan_for_dialog: called")
    if mousex is mousey and mousex == 0:
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
        return find_controlled_sig_dialog(h, mousex, mousey)
    elif type == "uncontrolled":
        return find_uncontrolled_sig_dialog(h, mousex, mousey)
    elif type == "viewcamera":
        return find_camera_buttons(h, w, window)

    return False


def find_uncontrolled_sig_dialog(h: int, mousex: int, mousey: int) -> bool:
    logging.debug("find_uncontrolled_sig_dialog: called")
    dialogbox_height = math.ceil(h * 0.125)
    dialogbox_width = math.ceil(dialogbox_height * 2)
    dialogbox_x = math.floor(mousex - dialogbox_width / 2)
    dialogbox_y = math.floor(mousey - dialogbox_height)

    capture = screen_grab(dialogbox_x, dialogbox_y, dialogbox_width, dialogbox_height * 2).convert("RGB")
    w, h = capture.size
    upper = capture.crop((0, 0, w, h / 2))
    lower = capture.crop((0, h / 2, w, h))
    upperw, upperh = upper.size
    width, height = lower.size
    lowershelf = lower.crop((0, height * 0.33, width / 2, height * 1 / 3 + 2))
    upper = capture.crop((0, 0, w, h / 2))
    upperw, upperh = upper.size
    uppershelf = upper.crop((0, upperh * 0.1, upperw / 2, upperh * 0.1 + 2))
    imagesToProcess = [lowershelf, uppershelf]

    for image in imagesToProcess:
        logging.debug("find_uncontrolled_sig_dialog: iterating images")
        if check_color_percentage_single(image, Colors.COLOR_DIALOG_WHITE):
            logging.debug("find_uncontrolled_sig_dialog: image loop: numpy white pixels returned success")
            return True
    logging.debug("find_uncontrolled_sig_dialog: return false path")
    return False


def find_controlled_sig_dialog(h: int, mousex: int, mousey: int) -> bool:
    logging.debug("find_controlled_sig: called")
    dialogbox_height = math.ceil(h * 0.125)
    dialogbox_width = math.ceil(dialogbox_height * 2)
    dialogbox_x = math.floor(mousex - dialogbox_width / 2)
    dialogbox_y = math.floor(mousey - dialogbox_height)

    capture = screen_grab(dialogbox_x, dialogbox_y, dialogbox_width, dialogbox_height * 2).convert("RGB")
    w, h = capture.size
    upper = capture.crop((0, 0, w, h / 2))
    lower = capture.crop((0, h / 2, w, h))
    upperw, upperh = upper.size
    width, height = lower.size
    lowershelf = lower.crop((0, height * 0.66, width, height * 0.66 + 3))
    uppershelf = upper.crop((0, upperh * 0.4, upperw, upperh * 0.4 + 2))
    imagesToProcess = [lowershelf, uppershelf]
    logging.debug("find_controlled_sig_dialog: made it to generator")
    result = any(
        check_color_percentage_single(image, Colors.COLOR_DIALOG_WHITE, threshold=0.01)
        and check_color_multiple(image, Colors.COLOR_DIALOG_BUTTONS)
        for image in imagesToProcess
    )  # this doesn't run if check for white pixels is false. must change TODO
    logging.debug(f"find_controlled_sig_dialog: result: {result}")
    return result


def find_camera_buttons(h: int, w: int, windowID: int):
    logging.debug("find_camera_button: called")
    zone_screen_height, zone_screen_width, zone_screen_x = calculate_zone_screen(w, h)

    camerabutton_height = math.ceil(h * 0.125 * 0.375)
    camerabutton_width = math.ceil(camerabutton_height * 2 / 0.375)
    camerabutton_x = zone_screen_width * 0.79760 + zone_screen_x
    camerabutton_y = h * 0.80629

    screen_cords = win32gui.ClientToScreen(windowID, (int(camerabutton_x), int(camerabutton_y)))
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
        if check_color_single(image, Colors.COLOR_VIEWCAMERA):
            logging.debug(
                f"View camera button found. We got {0 if image==imagesToProcess[0] else 1} (0=upper, 1=lower)"
            )
            return 0 if image == imagesToProcess[0] else 1
    logging.debug("find_camera_buttons: none found")
    return False


def color_approx_eq_np(color1: tuple, color2: tuple, threshold=10) -> bool:
    """Check if a color is equal to another color within a given value

    Args:
        color1 (tuple): First RGB color to check against
        color2 (tuple): Second RGB color to check against
        tolerance (int, optional): How many units of R, G, or B to tolerate. Defaults to 10.

    Returns:
        bool: Whether or not the colors are approximately equal to eachother
    """
    # Get the absolute value of the difference between the arrays
    return np_allclose(color1, color2, atol=threshold)


def check_color_single(image: Image, color, threshold=7) -> bool:
    logging.debug("check_color_single: called")
    arr = np_array(image)

    # Iterate over the y-axis
    for i in range(arr.shape[0]):
        # Iterate over the x-axis
        for j in range(arr.shape[1]):
            col_to_compare = arr[i, j]
            if color_approx_eq_np(col_to_compare, color, threshold):
                logging.debug("check_color_single: colors similar, return True")
                return True
    logging.debug("check_color_single: no similar colors found, returning False")
    return False


def check_color_multiple(image: Image, colors: list, threshold=7) -> bool:
    logging.debug("check_color_multiple: called")
    arr = np_array(image)

    # Iterate over the y-axis
    for i in range(arr.shape[0]):
        # Iterate over the x-axis
        for j in range(arr.shape[1]):
            # Get the tuple from the element
            col_to_compare = arr[i, j]
            for color in colors:
                if color_approx_eq_np(col_to_compare, color, threshold):
                    logging.debug("check_colored_pixels_np: colors similar, return True")
                    return True
    logging.debug("check_colored_pixels_np: no similar colors found, returning False")
    return False


def check_color_percentage_single(image: Image, color: tuple, compareThreshold=7, threshold=0.05) -> bool:
    logging.debug("check_color_percentage_single: called")
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
                logging.debug(f"check_color_percentage_single: matching pixels > {threshold * 10 ** 2}% found")
                return True
    logging.debug(
        f"check_color_percentage_single: not enough white pixels found for array size. numpixels: {matching_pixels/arr.size}"
    )
    return False


def find_exit_cam_button(w: int, bbox: tuple[int, int, int, int], window):
    logging.debug("find_exit_cam_button")
    camera_controls_width = 283
    camera_controls_x = math.ceil(w / 2 - camera_controls_width / 2)

    y = bbox[1]
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
    ).convert("RGB")
    width, height = capture.size
    lowershelf = capture.crop((0, height / 2, width, height / 2 + 2))
    imagesToProcess = [lowershelf]

    return all(check_color_single(image, Colors.COLOR_CAMERA_EXIT) for image in imagesToProcess)


@check_able_to_run
def send_zone_message(zone: str) -> None:
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

    beep = threading.Thread(target=lambda: winsound.Beep(600, 200))
    beep.start()
    pyperclip.copy(switch.get(zone))


@check_able_to_run
def enabled_warning():
    """Play a warning sound if script is enabled"""
    beep = threading.Thread(target=lambda: winsound.Beep(640, 300))
    beep.start()


if __name__ == "__main__":
    add_hotkey(2, lambda: click_signal("1"))  # 1
    add_hotkey(3, lambda: click_signal("2"))  # 2
    add_hotkey(4, lambda: click_signal("3"))  # 3
    add_hotkey(46, lambda: click_camera())  # C
    add_hotkey(59, lambda: toggle_disable())  # F1
    add_hotkey("R", lambda: click_rollback())  # R
    add_hotkey("/", lambda: enabled_warning())  # / warning when opening chat while enabled
    add_hotkey("`", lambda: enabled_warning())  # Command bar
    add_hotkey("'", lambda: enabled_warning())  # Command bar
    add_hotkey(79, lambda: send_zone_message("A"))  # Num 1
    add_hotkey(80, lambda: send_zone_message("B"))  # Num 2
    add_hotkey(81, lambda: send_zone_message("C"))  # Num 3
    add_hotkey(75, lambda: send_zone_message("D"))  # Num 4
    add_hotkey(76, lambda: send_zone_message("E"))  # Num 5
    add_hotkey(77, lambda: send_zone_message("F"))  # Num 6
    add_hotkey(71, lambda: send_zone_message("G"))  # Num 7

    colorama.init()

    if UPDATE_CHECK_ENABLED:  # TODO: remove from update_check in favor of here
        update_check()
    winsound.Beep(500, 200)
    logging.info("SG+ Successfully Initialized")

    keyboard_wait()
