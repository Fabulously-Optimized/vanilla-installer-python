"""
Theme & design of the Tkinter GUI application
"""

import sys
import os
import tkinter
import tkinter.messagebox
import pathlib

import darkdetect

FILE = str(pathlib.Path("data/theme.txt").resolve())


def init():
    """Checks if the theme file exists and creates it if not.
    Also checks the theme of the OS and edits the file accordingly.
    """
    if not os.path.exists("data/"):
        os.mkdir("data/")

    if not os.path.exists(FILE):
        with open(FILE, "w", encoding="utf-8") as file:
            file.write("dark" if darkdetect.isDark() is True else "light")


def is_dark(to_dark: bool = None) -> bool:
    """Change or get the status of dark mode.

    Args:
        to_dark (bool, optional): Status. Defaults to None (just get status, without editing it).

    Returns:
        bool: theme
    """
    if to_dark is False:
        return open(FILE, "w", encoding="utf-8").write("light")
    if to_dark is True:
        return open(FILE, "w", encoding="utf-8").write("dark")
    return open(FILE, encoding="utf-8").read() == "dark"

# colors from catppuccin latte and mocha https://github.com/catppuccin/catppuccin
dark_theme = {
    "blue": "#89b4fa",
    "lavender": "#b4befe",
    "text": "#cdd6f4",
    "subtext1": "#bac2de",
    "subtext0": "#a6adc8",
    "overlay2": "#9399b2",
    "overlay0": "#7f849c",
    "surface2": "#585b70",
    "surface1": "#45475a",
    "surface0": "#313244",
    "base": "#1e1e2e",
    "crust": "#11111b",
}

light_theme = {
    "blue": "#1E66F5",
    "lavender": "#7287FD",
    "text": "#4C4F69",
    "subtext1": "#5c5f77",
    "subtext0": "#6C6F85",
    "overlay2": "#7C7F93",
    "overlay0": "#9CA0B0",
    "surface2": "#acb0be",
    "surface1": "#bcc0cc",
    "surface0": "#CCD0DA",
    "base": "#EFF1F5",
    "crust": "#DCE0E8",
}


def load() -> dict:
    """Returns the current theme dictionary.

    Returns:
        dict: The colors palette.
    """
    return dark_theme if is_dark() else light_theme


def toggle():
    """Switches between dark and light theme.

    Args:
        popup (bool, optional): Wether to show a informational popup
        which asks to exit the program. Defaults to True.
    """
    is_dark(to_dark=not is_dark())


init()

if __name__ == "__main__":
    print("Dark Mode?", is_dark())
    print("Theme dictionary:", load())
