<h1 align="center">SCR: SG+</h1>

<h1 align="center">
   
   ![SGPlus](https://i.imgur.com/jcOlFuq.gif)

</h1>

<i><b> ATTENTION: A new SCR update has broken the functionality of the script. If you notice a "Desk Exit" dialog appear when you change a signal, please try a different server or don't use the script. Reproducing this issue has been tricky, it seems to work some times but not other times. If you are affected by the issue, remember it is NOT caused by me, but rather an SCR/ROBLOX update.</b><i>

---
### <u>Description</u>
SG+ is a macro script written in Python that streamlines your signalling experience by allowing you to change a signal aspect or open a camera view with only one button press.

### <u>Will this get me demoted? Am I safe to use this?</u>
**There is nothing to indicate you will be demoted or banned for using this script.** The onus is still on the signaller to signal trains in a safe and proper manner. It is not an exploit and does not automate signalling entirely. It is just to aid the signaller in their task of efficiently running their zone and keeping time. If you have had trouble with a member of staff as a result from using this script, **contact me immediately (scroll down) or open an issue.**

### Usage:
- Hover over a signal and press 1, 2, or 3, corresponding to the aspect you wish to change the signal to.
- Hover over a signal and press C to enter camera view. Once in camera view, press C again to exit.
- Press F1 to enable or disable the script. You only need to do this if you are chatting or typing things to prevent false activations.

### Features
- Only one button press is needed to change a signal aspect
- Decreases setup and train clearing time significantly
- Allows the signaller to focus on more important things than just clicking to change aspects
- Quickly get in and out of a camera view (signals only for now)
- Use numpad 1-7 to copy zone opening messages to your clipboard (1 for A, 2 for B, etc.)
- Overlay that shows whether SG+ is enabled or disabled
- Properties window which allows you to fine tune the tool to your liking including custom keybinds.
### Planned features:
- Rewrite camera code to use the aspect code to detect the image
- Implement a visual indicator
- TRTS Audio cue 
- Allowing custom keybinds for signal and camera controls, only the toggling keybind is customizable.

### Known issues:
- Camera button for platforms might be unreliable. This may require some additional attention.
- Overlay will randomly exit/crash.
- Startup failure if configuration directory is missing.
### Controls:

---
|Key|Action|
|---|---|
|F1|Toggle the script off/on|
|1|Change currently hovered signal to Danger|
|2|Change currently hovered signal to Caution|
|3|Change currently hovered signal to Proceed|
|C|Enter camera mode of currently hovered signal. If you are already in camera mode, it will exit camera mode|
|R|Change rollback setting of currently hovered signal
---

### **Installation by installer**

Download the "sgplus-installer" in the releases tab. This will add shortcuts and start menu entries for you so that you do not need to go looking for the file every time you want to run it.

### **Installation by source**

1. Download and install the latest Python3 installer from [Python Downloads Page](https://www.python.org/downloads/)
   - IMPORTANT: Make sure to check the box during installation which adds Python to PATH. Labeled something like **Add Python 3.X to PATH**
2. Download the latest release in the [Releases section of this repo](https://github.com/ElectricityMachine/SCR-SGPlus/releases/). Click on "Source Code (zip)"
   - Note: If you want the development release with all the latest changes, press the green "Code" button on the main page of this repo and press "Download ZIP". The following instructions still apply.
4. Extract the folder to your desired location. You can do this natively in Windows by opening the .zip folder and pressing "Extract all" at the top.
   - Note: If you are updating from an older version, please delete the old version of the script before extracting the new version. Failure to do so may cause conflicts and bugs.
5. Enter the folder where the script and images are stored, then in the Windows File Explorer address bar, type "cmd". A Command Prompt window should pop up. See the gif below for an example of how to do this. ![explorer_UNTq76MoQy](https://user-images.githubusercontent.com/47489506/181626707-6f58a2b6-e9e4-423e-9cb8-15d2add19cc7.gif)

6. In that CMD window, run ``pip install -r requirements.txt``. This will download all the requirements for the script to function.
7. After the installation has completed, run the ``start.bat`` batch file to start the script. A console window will appear, a beep will sound, and the macro is now active.

### **Installation by executable**

Download the archive listed in the releases tab on the right side and extract it to a folder. Run the executable contained within.

### <u>License</u>
By using this script, you MUST adhere to the license terms in the LICENSE file.

### <u>Contact information</u>
If you have issues or need to contact me, please reach me on Discord at ElectricityMachine (hashtag) One Seven Five Three. The Discord username is spelt that way to avoid scrapers and bots.

### <u>Credit</u>
* GUI and Binary: [xDistinctx](https://github.com/enigmapr0ject)
* Main logic: [ElectricityMachine](https://github.com/ElectricityMachine)
