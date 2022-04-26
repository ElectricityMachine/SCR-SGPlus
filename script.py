# ElectricityMachine
# Updated 3/17/22
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

starttime = time.time()

key_wait = 0
backspace_wait = 0
dialog_wait = 0.085

color_vals ={
	# (0, 201, 0), # Lit Green
	# (204, 153, 0), # Lit Yellow
	(213, 0, 0), # Lit Red
	# (0, 94, 0), # Unlit Green
	(96, 60, 0), # Unlit Yellow
	(99, 0, 0), # Unlit Red
}

disable = False
running = False

def able_to_run():
	global disable
	global running
	if disable:
		print("Unable to run: Disabled")
		return False
	elif running:
		print("Unable to run: Already running")
		return False
	elif win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "Roblox":
		print("Unable to run: Not ROBLOX")
		return False
	else:
		return True

def color_approx_eq(color1, color2):
	return abs(color1[0] - color2[0]) <= 7 and abs(color1[1] - color2[1]) <= 7 and abs(color1[2] - color2[2]) <= 7

def screen_grab(x, y, width, height):
	image = PIL.ImageGrab.grab(bbox=[x, y, x + width, y + height])
	return image

def click_signal(sig):
	if scan_for_dialog():
		time.sleep(key_wait)
		keyboard.press_and_release(sig)
		time.sleep(backspace_wait)
		keyboard.press_and_release("backspace")


def click_camera_button():
	if not able_to_run():
		return
	if pyautogui.locateCenterOnScreen('rotate.png', confidence=0.9):
		keyboard.press_and_release("backspace")
		hwnd = win32gui.FindWindow(None, 'Roblox')
		x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
		w = x1 - x0
		h = y1 - y0
		autoit.mouse_move(math.ceil(w/2), math.ceil(h/2), 2)
		keyboard.press_and_release("backspace")
		keyboard.press_and_release("backspace")
		return
	mouseCoords = pyautogui.position()
	mouseCoordsX, mouseCoordsY = mouseCoords
	autoit.mouse_click("left")
	time.sleep(0.032)
	output = pyautogui.locateCenterOnScreen('more.png', confidence=0.8)
	time.sleep(0.016)
	if output == None:
		print("CAMERA: Not found")
		return
	else:
		x, y = output
		print(output)
		time.sleep(0.016)
		autoit.mouse_click("left", x, y, 1, 2)
		time.sleep(0.016)
		output = pyautogui.locateCenterOnScreen(
			'camera.png', grayscale=True, confidence=0.8)
		time.sleep(0.016)
		print(output)
		if output == None:
			print("CAMERA: None found after button press")
		else:
			x, y = output
			time.sleep(0.016)
			autoit.mouse_click("left", x, y, 1, 2)


def toggle_disable():
	global disable
	if disable:
		disable = not disable
		winsound.Beep(500, 100)
	else:
		disable = not disable
		winsound.Beep(400, 100)

def scan_for_dialog():
	if not able_to_run(): return
	window = win32gui.GetForegroundWindow()
	autoit.mouse_click("left")
	rect = win32gui.GetWindowRect(window)
	bbox = [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]
	time.sleep(dialog_wait) # Wait for 1 frame (60FPS) for the dialog to show up. This ensures that ideally the script will never encounter a time where you click and it doesn't show
	starttime = time.perf_counter()
	mouse_pos = pyautogui.position()
	mousex = mouse_pos[0]
	mousey = mouse_pos[1]
	x = bbox[0]
	y = bbox[1]
	w = bbox[2]
	h = bbox[3]

	dialog_box_height = math.ceil((h-32)*0.125)
	dialog_box_width = math.ceil(dialog_box_height*2)
	pixel_height = dialog_box_height * 0.171
	button_shelf = dialog_box_height/2*1.15
	dialog_box_x = mousex - dialog_box_width/2
	dialog_box_y = mousey - dialog_box_height
	
	capture = screen_grab(dialog_box_x, dialog_box_y, dialog_box_width, dialog_box_height*2)
	w, h = capture.size
	capture.convert('RGB')
	shelf = h/2*1.15 # Where the colors we need to check are
	upper = capture.crop((0,0,w,h/2)) # Upper
	lower = capture.crop((0, h/2, w, h)) # Lower
	upperw, upperh = upper.size
	lowerw, lowerh = lower.size
	lowershelf = lower.crop((0, lowerh*2/3, lowerw, lowerh*2/3 + 1))
	uppershelf = upper.crop((0, upperh/2, upperw, upperh/2 + 1))
	imagesToProcess = [lowershelf, uppershelf]
	flag = False
	for j, image in enumerate(imagesToProcess):
		for i in range(image.width):
			if i > image.width/2: break
			for i2, val in enumerate(color_vals):
				r2 = val[0]
				r, g, b = image.getpixel((i, 0))
				if color_approx_eq((r,g,b), (val)):
					flag = True
					break
			if flag:
				break
		if flag:
			break
	if flag:
		return True
	else:
		print("IMAGE DETECTION: Dialog not found") # If you encounter this but the dialog is on the screen, email me (electricitymachine (a t) tutanota (d o t) com)
		return False

old_print=print
def print(*args):
	old_print(math.trunc(time.time() - starttime))
	old_print(*args)

print("INITIALIZED!")

keyboard.add_hotkey("1", click_signal, args=["1"])
keyboard.add_hotkey("2", click_signal, args=["2"])
keyboard.add_hotkey("3", click_signal, args=["3"])
keyboard.add_hotkey("c", click_camera_button)
keyboard.add_hotkey("F1", toggle_disable)
winsound.Beep(500, 200) # Script init successful
keyboard.wait()

# async def scan_for_image():
# 	counter = 0
# 	# Scan for image for 0.25 seconds (maybe change to ticks)
# 	# Compare the pixel values and determine offset
# 	# 9.36 window y per dialog y scale
# 	# 4.15 window y per dialog x scale
# 	# total dialog aspect ratio is 2 x per y
# 	# 38 pixels below mouse on height 1024
# 	# 0.0371 pixels below per height
# 	# 75 dialog, 600 window (0.125)
# 	if counter >= 5:
# 		# Screengrab and compare pixel values
# 		# Get mouse x, y
# 		# Take image 
# 		counter = 0
# 	else:
# 		counter += 1