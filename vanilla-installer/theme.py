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
    "red": "#f38ba8",
    "blue": "#89b4fa",
    "lavender": "#b4befe",
    "text": "#cdd6f4",
    "label": "#bac2de", # catppuccin subtext1
    "subtitle": "#a6adc8", # catppuccin subtext0
    "icon": "#9399b2", # catppuccin overlay2
    "installbuttonpressed": "#7f849c", #catppuccin overlay0
    "buttonpressed": "#585b70", # catppuccin surface2
    "buttonhovered": "#45475a", # catppuccin surface1
    "button": "#313244", # catppuccin surface0
    "base": "#1e1e2e",
    "crust": "#11111b",
}

light_theme = {
    "red": "#d20f39",
    "blue": "#1E66F5",
    "lavender": "#7287FD",
    "text": "#4C4F69",
    "label": "#5c5f77", # catppuccin subtext1
    "subtitle": "#6C6F85", # catppuccin subtext0
    "icon": "#7C7F93", # catppuccin overlay2
    "installbuttonpressed": "#9CA0B0", #catppuccin overlay0
    "buttonpressed": "#acb0be", # catppuccin surface2
    "buttonhovered": "#bcc0cc", # catppuccin surface1
    "button": "#CCD0DA", # catppuccin surface0
    "base": "#EFF1F5",
    "crust": "#DCE0E8",
}


def load() -> dict:
    """Returns the current theme dictionary.

    Returns:
        dict: The colors palette.
    """
    return dark_theme if is_dark() else light_theme


def toggle() -> None:
    """Switches between dark and light theme."""
    is_dark(to_dark=not is_dark())


init()

if __name__ == "__main__":
    print("Dark Mode?", is_dark())
    print("Theme dictionary:", load())
