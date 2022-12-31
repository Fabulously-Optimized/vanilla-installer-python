# Usage

This varies between platform, so select your OS here:
**[Windows](#windows)** - **[macOS](#macos)** - **[Linux](#linux)**

## Windows

For most users on Windows, we recommend the binary version.

1. Open the [releases page][1] and download the file with the `.exe` extension. (Example: `Vanilla Installer-GUI v0.1.0.exe`)
2. If it asks you where to save your file, select your Downloads folder (`C:\Users\username\Downloads`)
3. Navigate to the Downloads folder and double-click the file you just downloaded.
4. Select the Minecraft version and directory, and click `Install`.
5. You're all done!

## macOS

Currently, the Vanilla Installer fails to compile on macOS, so you'll have to use the Linux method below.
It's recommended to install Python using [Homebrew](https://brew.sh), however installers from [python.org](https://python.org) should also work fine.

**If** you know something about why it might fail to compile (it can't find the PySide6 Qt resources directory), please join [our discord][2] and mention it to us.

## Linux

Because of Linux having many different package managers, we've decided to make the way to install on Linux via `pip`, or building from source using `python` and `poetry`, which isn't covered here.

1. Install Python 3.8 or higher (3.11 recommended) from your package manager - for example `sudo apt install python3` or `sudo pacman -S python3`
2. Run `pip3 install vanilla-installer[gui]`.
3. Then you can run `vanilla-installer-gui` to launch the program. If you have issues, try `python3 -m vanilla_installer gui`.

[1]: https://github.com/Fabulously-Optimized/vanilla-installer/releases/latest
[2]: https://discord.gg/fabulously-optimized-859124104644788234
