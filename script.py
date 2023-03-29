# ElectricityMachine
# Version: 0.3.1
# Major changes: Add toggle rollback, improved reliability, major speed improvements, chat warning
# Description: A script to automate tasks when signalling for SCR
# Keybinds: 1 2 3 for Danger, Caution, and Proceed signal settings. C for Camera. R for Rollback Toggle.
# How to use: Hover over a signal and press the corresponding keybind to perform the action
# Limitations: Windows only, only works on primary monitor

import math
import time
import winsound

import autoit
import colorama
from PIL.Image import frombytes
from keyboard import add_hotkey, press_and_release, wait as keyboard_wait
import pyperclip
from requests import get as requests_get
import win32gui
import mouse
from mss import mss
from time import perf_counter

colorama.init()  # Needed to work on Windows devices, see colorama docs

version = "v0.3.1"
fps = 60 # Set your average FPS here
ping = 100 # Set your average ping here
debug = False # If true, will enable debug prints if they're specified
check_for_update = False


color_dialog_buttons = {
    (0, 201, 0),  # Lit Green
    (204, 153, 0),  # Lit Yellow
    (213, 0, 0),  # Lit Red
    (0, 94, 0),  # Unlit Green
    (96, 60, 0),  # Unlit Yellow
    (99, 0, 0),  # Unlit Red
}

color_more = (92, 89, 89)  # Color of gray button w/ 3 dots
color_menu = (194, 186, 189)  # Side menu main color
color_camera_exit = (255, 255, 255)  # White "X" on the close button in camera view
color_dialog_white = (227, 218, 218)  # White elements in the signal dialog
color_viewcamera = (147, 0, 207)  # Purple "View Camera" button

disabled = False
signal_mouse_coords = None  # Mouse coordinates used to return cursor to signal when exiting camera/rollback
one_frame_time = round((1000 / fps) * 10 ** -3, 4) # Calculate time for 1 frame and round to 4 decimal places


def update_check():
    # TODO: Implement better version check functionality instead of just difference in strings
    if not check_for_update:
        return
    URL = "https://api.github.com/repos/ElectricityMachine/SCR-SGPlus/releases/latest"
    r = requests_get(url=URL)
    data = r.json()
    if version != data["tag_name"]:
        print(colorama.Fore.RED + "NOTICE: A new update is available for SG+!")
        print(colorama.Fore.RED + "It is always recommended to update to the latest version. To do so, go to https://github.com/ElectricityMachine/SCR-SGPlus")
        print(colorama.Fore.RED + "and follow the instructions under \"Installation\"")
        print(colorama.Fore.WHITE)


def able_to_run():
    if disabled:
        if debug:
            print("Unable to run: Disabled")
        return False
    elif win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "Roblox":
        if debug:
            print("Unable to run: Not ROBLOX")
        return False
    else:
        return True


def color_approx_eq(color1, color2): # Checks if a color is equal to another color within a tolerance of 7
    return abs(color1[0] - color2[0]) <= 7 and abs(color1[1] - color2[1]) <= 7 and abs(color1[2] - color2[2]) <= 7


def screen_grab(x, y, width, height):
    with mss() as sct:
        # Calculate bbox
        left = x
        top = y
        right = x + width
        lower = y + height
        bbox = (math.ceil(left), math.ceil(top), math.ceil(right), math.ceil(lower))
        # Grab the image
        im = sct.grab(bbox)
        # Convert to PIL image for compatibility
        newimage = frombytes('RGB', im.size, im.bgra, 'raw', 'BGRX')
        return newimage

def mouse_click():
    mouse.press("left")
    mouse.release("left")

def sleep(frames, minwait=0):
    if minwait != 0:
        print(max((frames * one_frame_time), minwait))
        time.sleep(max((frames * one_frame_time), minwait))
    else:
        time.sleep(frames * one_frame_time)


def click_signal(sig):
    if not able_to_run():
        return
    #t1 = perf_counter()
    # Inputs to the same signal are throttled such that you cannot change an aspect while the server is still processing your last input
    # Inputs to other signals don't seem to be throttled
    coord = mouse.get_position()
    mouse_click()
    time.sleep(one_frame_time * 3)
    result = scan_for_dialog("signal", coord[0], coord[1])
    if result:
        time.sleep(one_frame_time * 2) # Wait a few frames to ensure the dialog is on screen and the game will process our inputs
        press_and_release(sig)
        time.sleep(ping/4_000) # Ensure that our inputs are processed properly before exiting out of the dialog
        press_and_release("backspace")

def auto_setup_test():
    if not able_to_run(): 
        return
    present_pos_x, present_pos_y = mouse.get_position()
    for j in range(2):
        for i in range(1,16):
            coord = mouse.get_position()
            # Click signal red
            print(i)
            if i == 9 or i == 10:
                # autoit.mouse_move(x=present_pos_x, y=present_pos_y + 57 * i, speed=0)
                continue
            if j == 0: click_signal('1')
            elif j == 1: click_signal('3')
            # Move 50 pixels down from current position
            
            if i != 15: autoit.mouse_move(x=present_pos_x, y=round(present_pos_y + 56.5 * i), speed=0)
            #time.sleep(0.1)
        autoit.mouse_move(x=present_pos_x, y=present_pos_y, speed=1)

def click_rollback():
    if not able_to_run():
        return
    mousex, mousey = mouse.get_position()
    mouse_click()
    sleep(2)
    if scan_for_dialog("exitcamera"):  # Are we currently viewing a camera?
        return
    elif scan_for_dialog("signal", mousex, mousey):  # Is there a dialog on a signal we control?
        press_and_release("enter")
    else:  # No dialog found, no rollback toggle
        return
    window = win32gui.GetForegroundWindow()
    rect = win32gui.GetClientRect(window)

    bbox = [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]
    #x = bbox[0]
    #y = bbox[1]
    w = bbox[2]
    h = bbox[3]
    zone_screen_height = math.ceil(0.97735 * h)
    zone_screen_width = math.ceil(zone_screen_height * 1.34105)
    zone_screen_x = math.ceil(w / 2 - zone_screen_width / 2)

    rollback_x = zone_screen_width * 0.89955 + zone_screen_x
    rollback_y = 0.69518 * h
    rollback_position = win32gui.ClientToScreen(window, (int(rollback_x), int(rollback_y)))

    autoit.mouse_move(x=rollback_position[0], y=rollback_position[1], speed=2)
    mouse_click()
    sleep(3) # Ensure mouseclick registers
    press_and_release("backspace, backspace")
    autoit.mouse_move(mousex, mousey, speed=1)
    return


## MAJOR TODO: Time certain functions in old script and port them to minwait

def click_camera():
    if not able_to_run():
        return

    global signal_mouse_coords
    if scan_for_dialog("exitcamera"):  # Exit button found
        press_and_release("backspace", "backspace")
        if signal_mouse_coords:
            autoit.mouse_move(signal_mouse_coords[0], signal_mouse_coords[1], speed=1)
        return
    signal_mouse_coords = mouse.get_position()
    mouse_click()
    sleep(2, 0.02)
    if scan_for_dialog("signal"):  # Scan for controlled signal dialog
        press_and_release("enter")
        camera_y = 0.92133
    elif scan_for_dialog("uncontrolled"):
        press_and_release("enter")
        sleep(2)
        camera_y = 0.80137 if scan_for_dialog("viewcamera") == 0 else 0.92133
    else:
        return

    window = win32gui.GetForegroundWindow()
    rect = win32gui.GetClientRect(window)

    bbox = [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]
    w = bbox[2]
    h = bbox[3]

    zone_screen_height = math.ceil(0.97735 * h)
    zone_screen_width = math.ceil(zone_screen_height * 1.34105)
    zone_screen_x = math.ceil(w / 2 - zone_screen_width / 2)

    camera_x = zone_screen_width * 0.89414 + zone_screen_x
    camera_y = camera_y * h
    camera_position = win32gui.ClientToScreen(window, (int(camera_x), int(camera_y)))

    sleep(1)
    autoit.mouse_move(x=camera_position[0], y=camera_position[1], speed=2)
    mouse_click()
    return


def toggle_disable():
    global disabled
    if disabled:
        disabled = False
        winsound.Beep(500, 100)
    else:
        disabled = True
        winsound.Beep(400, 100)


def scan_for_dialog(type, mousex=0, mousey=0):
    if not able_to_run():
        return
    if mousex is mousey and mousex == 0:
        mousex, mousey = mouse.get_position()
    window = win32gui.GetForegroundWindow()
    rect = win32gui.GetClientRect(window)

    bbox = [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]
    #x = bbox[0]
    y = bbox[1]
    w = bbox[2]
    h = bbox[3]
    if type == "signal": # Gray signal dialog
        dialogbox_height = math.ceil(h * 0.125)
        dialogbox_width = math.ceil(dialogbox_height * 2)
        dialogbox_x = mousex - dialogbox_width / 2
        dialogbox_y = mousey - dialogbox_height

        capture = screen_grab(dialogbox_x, dialogbox_y, dialogbox_width, dialogbox_height * 2)
        w, h = capture.size
        capture.convert('RGB')
        upper = capture.crop((0, 0, w, h / 2))  # Upper
        lower = capture.crop((0, h / 2, w, h))  # Lower
        upperw, upperh = upper.size
        width, height = lower.size
        lowershelf = lower.crop((0, height * 0.66, width, height * 0.66 + 3)) # A 2-3 pixel high cropped image of the middle of the dialog
        uppershelf = upper.crop((0, upperh * 0.4, upperw, upperh * 0.4 + 2))
        imagesToProcess = [lowershelf, uppershelf]

        def process_images():
            white_pixels = 0
            for image in imagesToProcess:
                for i in range(math.ceil(image.width / 1.6)): # Don't bother checking too much of the image
                    for val in color_dialog_buttons:
                        if i == 0 or image.height == 0:
                            break
                        r, g, b = image.getpixel((i, image.height - 1))
                        if color_approx_eq((r, g, b), (color_dialog_white)): # Count the number of white pixels to avoid false positives
                            white_pixels += 1
                        elif color_approx_eq((r, g, b), (val)): # Do we have a button color?
                            if white_pixels / (image.width * image.height) >= 0.05:  # >5% of pixels are white
                                return True
            print("Nay")
        return True if process_images() else False
    elif type == "exitcamera": # Red "X" button at the top of screen when in a camera view
        camera_controls_width = 283
        camera_controls_x = math.ceil(w / 2 - camera_controls_width / 2)

        exit_camera_button_y = 85 + y
        exit_camera_button_x = 0.91166 * camera_controls_width + camera_controls_x - 5
        exit_camera_button_width = exit_camera_button_height = 50

        screen_cords = win32gui.ClientToScreen(window, (int(exit_camera_button_x), int(exit_camera_button_y)))
        capture = screen_grab(screen_cords[0], screen_cords[1], exit_camera_button_width, exit_camera_button_height)
        capture.convert('RGB')
        width, height = capture.size
        lowershelf = capture.crop((0, height / 2, width, height / 2 + 2))
        imagesToProcess = [lowershelf]
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
    elif type == "uncontrolled": # Gray signal dialog that isn't controlled by us
        dialogbox_height = math.ceil(h * 0.125)
        dialogbox_width = math.ceil(dialogbox_height * 2)
        dialogbox_x = mousex - dialogbox_width / 2
        dialogbox_y = mousey - dialogbox_height

        capture = screen_grab(dialogbox_x, dialogbox_y, dialogbox_width, dialogbox_height * 2)
        w, h = capture.size
        capture.convert('RGB')
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
        flag = False
        for image in imagesToProcess:
            for i in range(math.ceil(image.width)):
                for i2 in range(math.ceil(image.height)):
                    r, g, b = image.getpixel((i, i2))
                    if color_approx_eq((r, g, b), (color_dialog_white)):
                        white_pixels += 1
                    if white_pixels / image.width >= 0.2:  # Greater than 20% of pixels are white
                        flag = True
                        break
                if flag:
                    break
            if flag:
                break
        if flag:
            return True
        else:
            return False
    elif type == "viewcamera": # Purple "View Camera" button in sidemenu
        t1 = perf_counter()
        zone_screen_height = math.ceil(0.97735 * h)
        zone_screen_width = math.ceil(zone_screen_height * 1.34105)
        zone_screen_x = math.ceil(w / 2 - zone_screen_width / 2)

        camerabutton_height = math.ceil(h * 0.125 * 0.375)
        camerabutton_width = math.ceil(camerabutton_height * 2 / 0.375)
        camerabutton_x = zone_screen_width * 0.79760 + zone_screen_x
        camerabutton_y = h * 0.80629

        screen_cords = win32gui.ClientToScreen(window, (int(camerabutton_x), int(camerabutton_y)))
        capture = screen_grab(screen_cords[0], screen_cords[1], camerabutton_width, camerabutton_height * 2)
        capture.convert('RGB')
        width, height = capture.size
        uppershelf = capture.crop((0, 0, width, 3))
        lowershelf = capture.crop((0, height * 0.94, width, height))

        imagesToProcess = [uppershelf, lowershelf]
        flag = False
        for image in imagesToProcess:
            for i in range(math.ceil(image.width * 0.2)):
                for val in color_viewcamera:
                    if i == 0 or image.height == 0:
                        break
                    r, g, b = image.getpixel((i, image.height - 1))
                    if color_approx_eq((r, g, b), color_viewcamera):
                        flag = True
                        break
                if flag:
                    break
            if flag:
                break
        if flag:
            t2 = perf_counter()
            if image == imagesToProcess[0]:
                print((t2 - t1) * 10 ** 3)
                return 0  # Upper button
            else:
                print((t2 - t1) * 10 ** 3)
                return 1  # Lower button
        else:
            return False




def send_zone_message(zone):
    if not able_to_run():
        return
    switch = {
        'A': "Zone A (Stepford Area, Willowfield, Whitefield branches) is now under manual signalling control.",
        'B': "Zone B (St. Helens Bridge, Coxly, Beaulieu Park corridor) is now under manual signalling control.",
        'C': "Zone C (Stepford Airport Area) is now under manual signalling control.",
        'D': "Zone D (Morganstown to Leighton West) is now under manual signalling control.",
        'E': "Zone E (Llyn-by-the-Sea to Edgemead) is now under manual signalling control.",
        'F': "Zone F (Benton area + Waterline up to but not including Airport West and Morganstown) is now under manual signalling control.",
        'G': "Zone G (James St. to Esterfield) is now under manual signalling control."
    }

    winsound.Beep(600, 200)
    pyperclip.copy(switch.get(zone))


def enabled_warning():
    if not able_to_run():
        return
    if not disabled:
        winsound.Beep(640, 300)

if __name__ == "__main__":
    add_hotkey('g', auto_setup_test)
    add_hotkey(2, click_signal, args=["1"])  # 1
    add_hotkey(3, click_signal, args=["2"])  # 2
    add_hotkey(4, click_signal, args=["3"])  # 3
    add_hotkey(46, click_camera)  # C
    add_hotkey(59, toggle_disable)  # F1
    add_hotkey('R', click_rollback)  # R
    add_hotkey('/', enabled_warning)  # / warning when opening chat while enabled
    add_hotkey('`', enabled_warning)  # Command bar
    add_hotkey('\'', enabled_warning)  # Command bar
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