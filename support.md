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

## Having problems?
### Issues with Anaconda (Linux)
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