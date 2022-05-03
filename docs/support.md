# Supported systems, compatibility, troubleshooting & more
## Tested on...
- Linux → Debian → Ubuntu → PopOS:
  - My main system, should work 100% fine

## Recommendations
The program is optimized for Python 3.8 and above, as well as Linux and Windows.

- `darkdetect`
    - Used to check whether the OS theme is dark or not
    - Supports:
        - macOS 10.14+
        - Windows 10 1607+
        - Linux with a dark GTK theme.
    - Don't meed these requirements? Don't worry! The code will still work, just 

## Troubleshooting
### Pixelated font / issues with Anaconda (Linux)
Does the font look pixelated and emojis are not loading?

![](media/conda-bug.png)

Don't worry! Try:
```
python3.10 -m pip install -r requirements.txt
python3.10 vanilla-installer/gui.py
```
...whereas `3.10` can be any (supported) version, e.g. for `3.9`: the commands with `python3.9` in the beginning (you get the point). This makes sure *Anaconda* isn't used for executing the program.

There we go!

![](media/conda-fix.png)

### `ModuleNotFoundError: No module named 'tkinter'` (Linux)
[Tkinter](https://en.wikipedia.org/wiki/Tkinter) is an important library which is needed for the program to work. Sadly, on some Linux distributions, it isn't installed by default. But don't worry, try:

```py
sudo apt-get install python-tk
```

The issue probably occurs because you haven't installed VanillaInstaller correctly. Try running `sh install/debian-based.sh` (only works on Debian-based Linux distributions, as the name suggests). This command should install all needed dependencies for VanillaInstaller automatically.

### Other GUI-related issues
```
python3.10 vanilla-installer/gui.py --safegui mode --litegui mode
```
Make sure to choose the correct version - or replace `python3.10` with `python3`, `python` or just `py`.