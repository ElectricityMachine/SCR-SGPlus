# SG+: an SCR signalling macro

## What is it?
SG+ is a Python macro script that speeds up your signalling by allowing you to open the camera view, toggle rollback settings, and change signal aspects with one button and no mouse clicking.


## But won't this get me demoted?
**You will not be banned or demoted just for using this script.** The responsibility is still on the signaller to route trains in a safe and proper manner. It is not an exploit and does not automate signalling entirely; it only speeds up common actions. If you've encountered trouble with a member of staff while using this script, [contact me as soon as possible](#contact-information) or open an issue.

## Installation

### Binary (preferred)
1. Download sgplus.exe from the [latest releases page](https://github.com/ElectricityMachine/SCR-SGPlus/releases/latest)
2. Run **sgplus.exe**. **Some antiviruses may detect the program as malware.** If you receive a SmartScreen popup, click "More Info" then press "Run Anyway." This is a false-positive, you may have to add an exclusion to your antivirus software for the program to run. Any binary attached to a release is the same as the one built automatically [here](https://github.com/ElectricityMachine/SCR-SGPlus/blob/master/.github/workflows/build.yaml)

### From Source
This method is intended for those who want to contribute to the project or modify the script.
1. Download and install the latest Python 3 installer from the [Python Downloads Page](https://www.python.org/downloads/)
   - Make sure to check the box during installation which adds Python to PATH. Labeled something like **Add Python 3.X to PATH**
2. Download the latest release in the [Releases section of this repo](https://github.com/ElectricityMachine/SCR-SGPlus/releases/latest). Click on "Source Code (zip)"
   - Note: If you want the development release with all the latest changes, press the green "Code" button on the main page of this repo and press "Download ZIP". The following instructions still apply.
3. Extract the folder to your desired location. You can do this natively in Windows by opening the .zip folder and pressing "Extract all" at the top.
   - Note: If you are updating from an older version, please delete the old version of the script before extracting the new version. Failure to do so may cause conflicts and bugs.
4. Run ``install.bat`` and answer the prompts.

## Usage
- Launch the program by running the .exe or ``start.bat``
- Mouse over a signal, then:
  - press 1, 2, or 3, corresponding to the desired signal aspect.
  - press C to enter camera view, press C again to exit.
  - press R to toggle rollback.
  - press F to enter or exit the signal's side menu.
- Press F1 to enable or disable the script.
- Use numpad 1-7 (1 is A, 2 is B, etc.) to copy zone opening messages to your clipboard.

## Configuration

After your first startup, a ``config.toml`` file will be placed in the directory the script is located in. If you want to change the default keybinds, speed up/slow down the script, or change the zone opening messages, you can edit this file. Although most of it should be self-explanatory, there is a caveat with the keybinds:
- Because of how the script interfaces with the keyboard, setting a key as ``"1"`` will also trigger anything bound to ``Num 1``, and vice versa. To solve this, SG+'s default configuration uses scancodes, identifying the specific key we want to bind to. [Here is a list of all Windows scancodes](https://kippykip.com/b3ddocs/commands/scancodes.htm).
   - Example: If I want to change the camera button to F, I would go into ``config.toml`` and edit ``toggle_signal_camera = "C"`` to ``toggle_signal_camera = "F"``, or using scancodes from that webpage, ``toggle_signal_camera = 46``.
- A future release of SG+ will greatly simplify this procedure.

## I've found an issue!
Great! Please [open an issue](https://github.com/ElectricityMachine/SCR-SGPlus/issues/new) or contact me below.

Some issues include (but are **not** limited to):
- Script fails to run or install
- Certain signals do not respond to the script when trying to change aspects or enter/exit camera view
- Entering/exiting camera view or toggling rollback does not work
- Script locks up after some time (#60)

## Roadmap
- [ ] TRTS Audible Warning
- [x] Visual script status indicator (#36)
- [ ] Automatic terminus station setup
- [ ] Interactive keybind prompts/config (#34)
- [ ] Automatic rollback preferences (#37)
- [ ] Become FPS-independent
- [ ] (Possibly) Rewrite in Rust or another performant language

See the [open issues](https://github.com/ElectricityMachine/SCR-SGPlus/issues) for a full list of proposed features (and known issues).

##### License
By using this script, you must adhere to the license terms in the LICENSE file.

##### Contact information
Discord: @electricity.machine
ROBLOX: Electricity_Machine
