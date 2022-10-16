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


def load() -> dict:
    """Returns the current theme dictionary.

    Returns:
        dict: The colors palette.
    """
    if is_dark():
        return {
            "fg": "#FFFFFF",
            "bg": "#0E0F13",
            "dark": "#202023",
            "error": "#fc3b19",
            "warn": "#fc9d19",
            "success": "#28ff02",
            "accent": "#008AE6",
            "info": "#ff66ff",
        }
    return {
        "fg": "#000000",
        "bg": "#FFFFFF",
        "dark": "#EEEEEE",
        "error": "#fc3b19",
        "warn": "#fc9d19",
        "success": "#28ff02",
        "accent": "#008AE6",
        "info": "#ff66ff",
    }


def toggle(popup: bool = True):
    """Switches between dark and light theme.

    Args:
        popup (bool, optional): Wether to show a informational popup
        which asks to exit the program. Defaults to True.
    """
    is_dark(to_dark=not is_dark())

    if popup:
        if tkinter.messagebox.askyesno(
            title="Theme Toggle",
            message="""The changes will apply after restarting.
Exit program now?
(You need to start the program again manually).""",
        ):
            sys.exit(0)

init()

if __name__ == "__main__":
    print("Dark Mode?", is_dark())
    print("Theme dictionary:", load())
