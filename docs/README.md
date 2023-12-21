<h1 align="center">SCR: SG+</h1>


### Description
SG+ is a macro script written in Python that streamlines your signalling experience by allowing you to change a signal aspect, open a camera view, toggle rollback, or announce your signalling presence with just one button press.

### Will this get me demoted?
**You will not be banned or demoted just from using this script.** The responsibility is still on the signaller to signal trains in a safe and proper manner. It is not an exploit and does not automate signalling entirely, rather, it aims to speed up commonly performed actions. If you've encountered trouble with a member of staff while using this script, please [contact me as soon as possible](#contact-information), or open a new issue.

### Usage:
- Hover over a signal and:
  - press 1, 2, or 3, corresponding to the desired signal aspect.
  - press C to enter camera view. Once in camera view, press C again to exit.
  - press R to toggle rollback.
- Press F1 to enable or disable the script. You only need to do this if you are chatting or typing things to prevent false activations.
- Use numpad 1-7 (1 is A, 2 is B, etc.) to copy zone opening messages to your clipboard.

### Features
- Speedily change signal aspects
- Quickly get in and out of a camera view (signals only for now)
- Toggle rollback on or off
- Easily copy zone opening messages to your clipboard with the numpad
- Audible warning if you try to chat or run commands with the macro enabled

### Limitations:
- Windows only
- Primary monitor only

### Controls:

---
|Key|Action|
|---|---|
|F1|Toggle the script off/on|
|1|Change currently hovered signal to Danger|
|2|Change currently hovered signal to Caution|
|3|Change currently hovered signal to Proceed|
|C|Enter camera mode of the currently hovered signal. If you are already in camera mode, it will exit camera mode|
|R|Toggle rollback of the currently hovered signal
|Numpad 1-7|Copy the opening message for each zone (1 for zone A, 2 for zone B, etc.)|
---

### **Installation**

#### Binary (.exe file)
1. Download sgplus.exe from the [latest releases page](https://github.com/ElectricityMachine/SCR-SGPlus/releases/latest)
2. Run **sgplus.exe**.
**Note:** Some antiviruses may detect the program as malware. This is a false-positive, as such you may have to add an exclusion to your antivirus software for the program to run. Any binary attached to a release is the same as the one built automatically [here](https://github.com/ElectricityMachine/SCR-SGPlus/actions/workflows/build.yml)

#### Source (running script directly)
Note: This method is for those who wish to contribute to the project, for those who don't like the idea of running an exe file, or for those who like manual labour.
1. Download and install the latest Python 3 installer from the [Python Downloads Page](https://www.python.org/downloads/)
   - Make sure to check the box during installation which adds Python to PATH. Labeled something like **Add Python 3.X to PATH**
2. Download the latest release in the [Releases section of this repo](https://github.com/ElectricityMachine/SCR-SGPlus/releases/latest). Click on "Source Code (zip)"
   - Note: If you want the development release with all the latest changes, press the green "Code" button on the main page of this repo and press "Download ZIP". The following instructions still apply.
3. Extract the folder to your desired location. You can do this natively in Windows by opening the .zip folder and pressing "Extract all" at the top.
   - Note: If you are updating from an older version, please delete the old version of the script before extracting the new version. Failure to do so may cause conflicts and bugs.
4. Run ``install.bat`` and answer the prompts.
5. After the installation has completed, run ``start.bat`` to start the script. A console window will appear, a beep will sound, and the macro is now active.

### I've found an issue!
Great! Please [open an issue](https://github.com/ElectricityMachine/SCR-SGPlus/issues/new) or contact me below.

Some issues include (but are not limited to):
- Script fails to run or install
- Certain signals do not respond to the script when trying to change aspects or enter/exit camera view
- Entering/exiting camera view or toggling rollback does not work

##### License
By using this script, you must adhere to the license terms in the LICENSE file.

##### Contact information
Discord: @electricity.machine
ROBLOX: Electricity_Machine
