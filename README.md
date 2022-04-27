<h1 align="center">SCR: SG+</h1>

<h1 align="center">
   
   ![macro-beechley_1_2](https://user-images.githubusercontent.com/47489506/165611305-da7b72a5-1492-4db0-b37a-3ce81f1aad22.gif)

</h1>


### Description
SG+ is a macro script written in Python that streamlines your signalling experience by automating clicking signals to change aspects.

### Will this get me demoted? Am I safe to use this?
**There is nothing to indicate you will be demoted or banned for using this script.** The onus is still on the signaller to signal trains in a safe and proper manner. It is not an exploit and does not automate signalling entirely. It is just to aid the signaller in their task of efficiently running their zone and keeping time. If you have had trouble with a member of staff as a result from using this script, **contact me immediately (scroll down) or open an issue.**

### Usage:
- Hover over a signal and press 1, 2, or 3, corresponding to the aspect you wish to change the signal to.
- Hover over a signal and press C to enter camera view. Once in camera view, press C again to exit.
- Press F1 to enable or disable the script. You only need to do this if you are chatting or typing things.

### Features
- Automates changing signal aspects, allowing you to clear trains quickly
- Lightweight and optimized
- Only works while ROBLOX is focused and the script is enabled, thus providing safety so you don't inadvertantly press a key and you aren't hovered over a signal
- Audio cue when the script is enabled or disabled
- Very few to no false positives, meaning that if you press a key, the script will not run 99.9% of the time if there's no signal dialog. Please be aware that sometimes the script fails to pick up the dialog in very limited circumstances (see below) and that your mouse will click no matter what when you press 1-3.

### Planned features:
- Rewrite camera code to use the aspect code to detect the image
- Implement a visual indicator
- Premade chat messages on numpad

### Known issues:
- If you are fully zoomed out, sometimes a signal on the very edge of your screen will not register. To fix, zoom in or manually click the signal aspect. So far, this has only happened at Beechley Station for me, but YMMV.

### Controls:

---
|Key|Action|
|---|---|
|F1|Toggle the script off/on|
|1|Change currently hovered signal to Danger|
|2|Change currently hovered signal to Caution|
|3|Change currently hovered signal to Proceed|
|C|Enter camera mode of currently hovered signal. If you are already in camera mode, it will exit camera mode|
---

### **Installation**

## Windows
1. Download and install the latest Python3 installer from [Python Downloads Page](https://www.python.org/downloads/)
   - IMPORTANT: Make sure to check the box during installation which adds Python to PATH. Labeled something like **Add Python 3.X to PATH**
2. Download the latest release in the [Releases section of this repo](https://github.com/ElectricityMachine/SCR-SGPlus/releases/). Click on "Source Code (zip)"
   - Note: If you want the development release with all the latest changes, press the green "Code" button on the main page of this repo and press "Download ZIP". The following instructions still apply.
4. Extract the folder to your desired location.
5. Enter the folder where the script and images are stored, then in the Windows File Explorer address bar, type "cmd". A Command Prompt window should pop up.
6. In that CMD window, run ``pip install -r requirements.txt``. This will download all the requirements for the script to function.
7. After the installation has completed, run ``python script.py``. A console window will appear and the macro is now active.

### License
By using this script, you MUST adhere to the license terms in the LICENSE file.

### Contact information
If you have issues or need to contact me, please reach me on Discord at ElectricityMachine (hashtag) One Seven Five Three. The Discord username is spelt that way to avoid scrapers and bots.
