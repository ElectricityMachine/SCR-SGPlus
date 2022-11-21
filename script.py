# ElectricityMachine
# Version: 0.2.9
# Description: A script to automate tasks when signalling for SCR
# Keybinds: 1 2 3 for Danger, Caution, and Proceed signal settings. C for Camera
# How to use: Hover over a signal and press the corresponding keybind to perform the action
import pyautogui
from pyautogui import *
import time
import math
import autoit
import keyboard
from torch import equal
import win32api
import win32gui
import winsound
import PIL
import PIL.ImageGrab
import pygetwindow
import requests
import colorama
import pyperclip

starttime = time.time()
colorama.init() # Needed to work on Windows devices, see colorama docs

version = "v0.2.9"
key_wait = 0
backspace_wait = 0
dialog_wait = 0.085
debug = False
check_for_update = True

color_vals ={
	(0, 201, 0), # Lit Green
	(204, 153, 0), # Lit Yellow
	(213, 0, 0), # Lit Red
	(0, 94, 0), # Unlit Green
	(96, 60, 0), # Unlit Yellow
	(99, 0, 0), # Unlit Red
}

disable = False
running = False

EXPECTED_CONFIGS = ["toggle_sgplus", "proceed_signal", "warning_signal", "danger_signal", 
	"zone_message_A_hotkey", "zone_message_B_hotkey", "zone_message_C_hotkey", "zone_message_D_hotkey",
	"zone_message_E_hotkey", "zone_message_F_hotkey", "zone_message_G_hotkey", "zone_message_A", 
	"zone_message_B", "zone_message_C", "zone_message_D", "zone_message_E", "zone_message_F", "zone_message_G"]

ZONE_COPY_MESSAGES = {
		'A': "Zone A (Stepford Area, Willowfield, Whitefield branches) is now under manual signalling control.",
		'B': "Zone B (St. Helens Bridge, Coxly, Beaulieu Park corridor) is now under manual signalling control.",
		'C': "Zone C (Stepford Airport Area) is now under manual siganlling control.",
		'D': "Zone D (Morganstown to Leighton West) is now under manual signalling control.",
		'E': "Zone E (Llyn-by-the-Sea to Edgemead) is now under manual signalling control.",
		'F': "Zone F (Benton area + Waterline up to not including Airport West and Morganstown) is now under manual signalling control.",
		'G': "Zone G (James St. to Esterfield) is now under manual signalling control."
	}

def update_check():
	if not check_for_update: return
	URL = "https://api.github.com/repos/ElectricityMachine/SCR-SGPlus/releases/latest"
	r = requests.get(url = URL)
	data = r.json()
	if version != data["tag_name"]:
		print(colorama.Fore.RED + "NOTICE: A new update is available for SG+!")
		print(colorama.Fore.RED + "It is always recommended to update to the latest version. To do so, go to https://github.com/ElectricityMachine/SCR-SGPlus")
		print(colorama.Fore.RED + "and follow the instructions under \"Installation\"")
		print(colorama.Fore.WHITE)

def able_to_run():
	global disable
	global running
	if disable:
		if debug: print("Unable to run: Disabled")
		return False
	elif running:
		if debug: print("Unable to run: Already running")
		return False
	elif win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "Roblox": #TODO: REPLACE THIS BEFORE PUSH
		if debug: print("Unable to run: Not ROBLOX")
		return False
	else:
		return True

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
		if debug: print("CAMERA: Not found")
		return
	else:
		x, y = output
		if debug: print(output)
		time.sleep(0.016)
		autoit.mouse_click("left", x, y, 1, 2)
		time.sleep(0.016)
		output = pyautogui.locateCenterOnScreen(
			'camera.png', grayscale=True, confidence=0.8)
		time.sleep(0.016)
		print(output)
		if output == None:
			if debug: print("CAMERA: None found after button press")
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
		time.sleep(dialog_wait) # Wait for a set time before checking if the dialog actually pops up. This ensures there should be no time where the script screengrabs and the dialog isn't open after clicking on a signal.
		start_time_perf = time.perf_counter()

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
		uppershelf = upper.crop((0, upperh/2, upperw, upperh/2 + 2))
		imagesToProcess = [lowershelf, uppershelf]
		
		flag = False
		for image in imagesToProcess:
			for i in range(math.ceil(image.width/1.6)):
				for val in color_vals:
					if i == 0 or image.height == 0: break
					r, g, b = image.getpixel((i, image.height - 1))
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
			if debug: print("IMAGE DETECTION: Dialog not found") # If you encounter this but the dialog is on the screen, please submit an issue on GitHub detailing 
			return False
	elif type == "station":
		if debug: print("None")

def send_zone_message(zone):
	if not able_to_run(): return
	
	winsound.Beep(600, 200)
	pyperclip.copy(ZONE_COPY_MESSAGES.get(zone))

def initConfig():
	try:
		with open("config.txt") as f:
			configs = f.readlines()
			configOptions = {}
			for line in configs:
				if len(line) > 0 and not(line.startswith("#")):  # if line is not empty and is not a comment
					equalsPos = line.find("=")
					configOptions[line[:equalsPos]] = line[equalsPos + 2:-2]  # 2's are used to exclude quotes
					try:
						EXPECTED_CONFIGS.remove(line[:equalsPos])
					except ValueError: 
						pass
			
			if len(EXPECTED_CONFIGS) > 0:
				print(colorama.Fore.YELLOW + "WARNING: Expected configs: " + str(EXPECTED_CONFIGS) + " not found! Using default configs." + colorama.Fore.WHITE)
				raise Exception  # break out of try

			keyboard.add_hotkey(configOptions["proceed_signal"], click_signal, args=["1"]) # 1
			keyboard.add_hotkey(configOptions["warning_signal"], click_signal, args=["2"]) # 2
			keyboard.add_hotkey(configOptions["danger_signal"], click_signal, args=["3"]) # 3
			keyboard.add_hotkey(configOptions["camera_view"], click_camera_button) # C
			keyboard.add_hotkey(configOptions["toggle_sgplus"], toggle_disable) # F1
			keyboard.add_hotkey(82, test) # Num 0
			keyboard.add_hotkey(configOptions["zone_message_A_hotkey"], send_zone_message, args=["A"]) # Num 1
			keyboard.add_hotkey(configOptions["zone_message_B_hotkey"], send_zone_message, args=["B"]) # Num 2
			keyboard.add_hotkey(configOptions["zone_message_C_hotkey"], send_zone_message, args=["C"]) # Num 3
			keyboard.add_hotkey(configOptions["zone_message_D_hotkey"], send_zone_message, args=["D"]) # Num 4
			keyboard.add_hotkey(configOptions["zone_message_E_hotkey"], send_zone_message, args=["E"]) # Num 5
			keyboard.add_hotkey(configOptions["zone_message_F_hotkey"], send_zone_message, args=["F"]) # Num 6
			keyboard.add_hotkey(configOptions["zone_message_G_hotkey"], send_zone_message, args=["G"]) # Num 7

			ZONE_COPY_MESSAGES["A"] = configOptions["zone_message_A"]
			ZONE_COPY_MESSAGES["B"] = configOptions["zone_message_B"]
			ZONE_COPY_MESSAGES["C"] = configOptions["zone_message_C"]
			ZONE_COPY_MESSAGES["D"] = configOptions["zone_message_D"]
			ZONE_COPY_MESSAGES["E"] = configOptions["zone_message_E"]
			ZONE_COPY_MESSAGES["F"] = configOptions["zone_message_F"]
			ZONE_COPY_MESSAGES["G"] = configOptions["zone_message_G"]
			return
	except FileNotFoundError:
		print(colorama.Fore.YELLOW + "WARNING: No config file found! Using default configs." + colorama.Fore.WHITE)
	except Exception:
		pass

	keyboard.add_hotkey(2, click_signal, args=["1"]) # 1
	keyboard.add_hotkey(3, click_signal, args=["2"]) # 2
	keyboard.add_hotkey(4, click_signal, args=["3"]) # 3
	keyboard.add_hotkey(46, click_camera_button) # C
	keyboard.add_hotkey(59, toggle_disable) # F1
	keyboard.add_hotkey(82, test) # Num 0
	keyboard.add_hotkey(79, send_zone_message, args=["A"]) # Num 1
	keyboard.add_hotkey(80, send_zone_message, args=["B"]) # Num 2
	keyboard.add_hotkey(81, send_zone_message, args=["C"]) # Num 3
	keyboard.add_hotkey(75, send_zone_message, args=["D"]) # Num 4
	keyboard.add_hotkey(76, send_zone_message, args=["E"]) # Num 5
	keyboard.add_hotkey(77, send_zone_message, args=["F"]) # Num 6
	keyboard.add_hotkey(71, send_zone_message, args=["G"]) # Num 7

def test():
	if debug: print("Number recognized")


initConfig()

# 0: 82
# 1: 79
# 2: 80
# 3: 81
# 4: 75

if update_check: update_check()
winsound.Beep(500, 200) # Script init successful
print("SG+ Successfully Initialized")

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
