<h1><b> ATTENTION: A new SCR update has broken the functionality of the script. If you notice a "Desk Exit" dialog appear when you change a signal, please try a different server or don't use the script. </b></h1>

Reproducing this issue has been tricky, it seems to work some times but not other times. If you are affected by the issue, remember it is NOT caused by me, but rather an SCR/ROBLOX update.

<h1 align="center">SCR: SG+</h1>

<h1 align="center">
   
   ![macro-beechley_1_2](https://user-images.githubusercontent.com/47489506/165611305-da7b72a5-1492-4db0-b37a-3ce81f1aad22.gif)

</h1>


### Description
SG+ is a macro script written in Python that streamlines your signalling experience by allowing you to change a signal aspect or open a camera view with only one button press.

### Will this get me demoted? Am I safe to use this?
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
- Premade chat messages on numpad

### Planned features:
- Rewrite camera code to use the aspect code to detect the image
- Implement a visual indicator
- TRTS Audio cue 

### Known issues:
- Sometimes, pressing C to enter the camera view of a signal does not work correctly. This is due to changes in 1.9 with the signalling interface and requires a rewrite to make fully functional. Because this is a low-priority feature of this script, especially because the cameras have rendering bugs in the current version, it will not be fixed for a while until the cameras in-game are fixed.

### Controls (all configurable):

---
|Key|Action|
|---|---|
|F1|Toggle the script off/on|
|1|Change currently hovered signal to Danger|
|2|Change currently hovered signal to Caution|
|3|Change currently hovered signal to Proceed|
|C|Enter camera mode of currently hovered signal. If you are already in camera mode, it will exit camera mode|
|Numpad 1-7|Copy respective zone message to clipboard|
---

### **Installation**

## Windows
1. Download and install the latest Python3 installer from [Python Downloads Page](https://www.python.org/downloads/)
   - IMPORTANT: Make sure to check the box during installation which adds Python to PATH. Labeled something like **Add Python 3.X to PATH**
2. Download the latest release in the [Releases section of this repo](https://github.com/ElectricityMachine/SCR-SGPlus/releases/). Click on "Source Code (zip)"
   - Note: If you want the development release with all the latest changes, press the green "Code" button on the main page of this repo and press "Download ZIP". The following instructions still apply.
4. Extract the folder to your desired location. You can do this natively in Windows by opening the .zip folder and pressing "Extract all" at the top.
   - Note: If you are updating from an older version, please delete the old version of the script before extracting the new version. Failure to do so may cause conflicts and bugs.
5. Enter the folder where the script and images are stored, then in the Windows File Explorer address bar, type "cmd". A Command Prompt window should pop up. See the gif below for an example of how to do this. ![explorer_UNTq76MoQy](https://user-images.githubusercontent.com/47489506/181626707-6f58a2b6-e9e4-423e-9cb8-15d2add19cc7.gif)

6. In that CMD window, run ``pip install -r requirements.txt``. This will download all the requirements for the script to function.
7. After the installation has completed, run the ``start.bat`` batch file to start the script. A console window will appear, a beep will sound, and the macro is now active.

### License
By using this script, you MUST adhere to the license terms in the LICENSE file.

### Contact information
If you have issues or need to contact me, please reach me on Discord at ElectricityMachine (hashtag) One Seven Five Three. The Discord username is spelt that way to avoid scrapers and bots.
