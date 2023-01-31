# Copyright (C) Fabulously Optimized 2022
# Licensed under the MIT License. The full license text can be found at https://github.com/Fabulously-Optimized/vanilla-installer/blob/main/LICENSE.md.
"""
Theme & design of the PySide6 GUI.
"""

import pathlib
from vanilla_installer import config
from vanilla_installer.log import logger

FILE = str(pathlib.Path("data/theme.txt").resolve())


def is_dark(to_dark: bool = None) -> str:
    """Change or get the status of dark mode.

    Args:
        to_dark (bool, optional): Status. Defaults to None (just get status, without editing it).

    Returns:
        str: The theme.
    """
    if to_dark is False:
        return config.write("theme", "light")
    if to_dark is True:
        return config.write("theme", "dark")
    output = config.read()
    return output["config"]["theme"]


# colors from catppuccin latte and mocha https://github.com/catppuccin/catppuccin
dark_theme = {
    "red": "#f38ba8",
    "blue": "#89b4fa",
    "lavender": "#b4befe",
    "text": "#cdd6f4",
    "label": "#bac2de",  # catppuccin subtext1
    "subtitle": "#a6adc8",  # catppuccin subtext0
    "icon": "#9399b2",  # catppuccin overlay2
    "installbuttonpressed": "#7f849c",  # catppuccin overlay0
    "buttonpressed": "#585b70",  # catppuccin surface2
    "buttonhovered": "#45475a",  # catppuccin surface1
    "button": "#313244",  # catppuccin surface0
    "base": "#1e1e2e",
    "crust": "#11111b",
}

light_theme = {
    "red": "#d20f39",
    "blue": "#1E66F5",
    "lavender": "#7287FD",
    "text": "#4C4F69",
    "label": "#5c5f77",  # catppuccin subtext1
    "subtitle": "#6C6F85",  # catppuccin subtext0
    "icon": "#7C7F93",  # catppuccin overlay2
    "installbuttonpressed": "#9CA0B0",  # catppuccin overlay0
    "buttonpressed": "#acb0be",  # catppuccin surface2
    "buttonhovered": "#bcc0cc",  # catppuccin surface1
    "button": "#CCD0DA",  # catppuccin surface0
    "base": "#EFF1F5",
    "crust": "#DCE0E8",
}


def load() -> dict:
    """Returns the current theme dictionary.

    Returns:
        dict: The colors palette.
    """
    return dark_theme if is_dark("dark") else light_theme


def toggle() -> None:
    """Switches between dark and light theme."""
    is_dark(is_dark() == "dark")


if __name__ == "__main__":
    logger.debug("theme module being initialized.")
    logger.debug("Dark Mode?", is_dark())
    logger.debug("Theme dictionary:", load())
