# Supported systems, compatibility, troubleshooting & more

## Tested on...

- Linux → Debian → Ubuntu → PopOS:
  - My main system, should work 100% fine
- Windows 11
  - [osfanbuff63](https://github.com/osfanbuff63)'s main system, should work fine

## Recommendations

The program is optimized for Python 3.8 and above, as well as Linux and Windows.

- `darkdetect`
  - Used to check whether the OS theme is dark or not
    - Supports:
      - macOS 10.14+
      - Windows 10 1607+
      - Linux with a dark GTK theme.
    - Don't meed these requirements? Don't worry! The code will still work, just dark mode will not be detected.

## Troubleshooting

Much of this advice is outdated, so it's recommended just to make a thread in [Fabulously Optimized's Discord](https://discord.gg/yxaXtaQqdB) until this is updated.

<details>
  <summary>If you still want to look, click me.</summary>

### Pixelated font / issues with Anaconda (Linux)

Does the font look pixelated and emojis are not loading?

![Font looking pixelated due to Anaconda](/media/conda-bug.png)

Don't worry! Try the following commands (AFTER trying [install/linux.sh](/install/linux.sh)):

```bash
#!/usr/bin/env/bash
python3.10 -m pip install -r requirements.txt
python3.10 vanilla_installer/gui.py
```

...whereas `3.10` can be any (supported) version, e.g. for `3.9`: the commands with `python3.9` in the beginning (you get the point). This makes sure *Anaconda* isn't used for executing the program.

Again, you *need* more than just the pip packages - so make sure you've also followed the steps [install/linux.sh](/install/linux.sh) or [install/windows.bat](/install/windows.bat) correctly!

There we go!

![Font looking normal](/media/conda-fix.png)

### `ModuleNotFoundError: No module named 'tkinter'` (Linux only)

[Tkinter](https://en.wikipedia.org/wiki/Tkinter) is an important library which is needed for the program to work. Sadly, on some Linux distributions, it isn't installed by default. But don't worry, try:

```bash
#!/usr/bin/env/bash
sudo apt-get install python-tk
```

The issue probably occurs because you haven't installed VanillaInstaller correctly. Try running `./install/linux.sh`, as this command should install all needed dependencies for VanillaInstaller automatically.

### Other GUI-related issues

```bash
#!/usr/bin/env/bash
python3.10 vanilla_installer/gui.py --safegui mode --litegui mode
```

Make sure to choose the correct version - or replace `python3.10` with `python3`, `python` or just `py`.

### Anything else?

If you have a question that isn't covered above, feel free to make a thread in [Fabulously Optimized's Discord](https://discord.gg/yxaXtaQqdB).

</details>
