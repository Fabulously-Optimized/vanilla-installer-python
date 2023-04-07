# Copyright (C) Fabulously Optimized 2023
# Licensed under the MIT License. The full license text can be found at https://github.com/Fabulously-Optimized/vanilla-installer/blob/main/LICENSE.md.
"""
The Configuration System for Vanilla Installer.
"""
import logging
import os
import platform
from pathlib import Path

import minecraft_launcher_lib as mll
import tomlkit
from tomlkit import toml_file

logger = logging.getLogger(__name__)

FILE_PATH = str(Path("vanilla_installer.toml").resolve())


def init():
    """
    Initialise the config file with the default values.
    This should **only** be run if the config file does not exist, as it will delete the file
    if it already exists, which will overwrite any user-set settings - which you don't want to do for obvious reasons.
    """
    config_file = tomlkit.document()
    # TODO: Add actual docs and URL for this
    config_file.add(tomlkit.comment("Read more about this file at <insert_wiki_url>"))
    config_file.add(tomlkit.nl())

    config = tomlkit.table()
    # maybe call darkdetect from here?
    # might want to just leave this alone to be honest
    config.add("theme", "dark")
    config.add(
        tomlkit.comment(
            "Whether to use FO's directory or ask the user for a custom one."
        )
    )
    config.add("fo_dir", True)
    config.add(tomlkit.comment("This is only used is fo_dir (above) is false."))
    config.add("path", mll.utils.get_minecraft_directory())
    if platform.system() == "Windows":
        font = "Inter Regular"
    else:
        font = "Inter"
    config.add(
        tomlkit.comment(
            "Only Inter (Inter Regular on Windows) and OpenDyslexic are currently supported."
        )
    )
    config.add("font", font)

    config_file.add("config", config)
    file = toml_file.TOMLFile(FILE_PATH)
    try:
        file.write(config_file)
    except FileExistsError:
        logger.exception("Config file already exists, overwriting.")
        os.remove(FILE_PATH)
        file.write(config_file)


def read() -> dict:
    """
    Read from the config file.

    Returns:
        dict: The config file, reformatted into a dict-like format.
    """
    config_file = toml_file.TOMLFile(FILE_PATH)
    try:
        return config_file.read()
    except FileNotFoundError:
        logger.exception("No config file found, (re-)initializing.")
        init()
        return config_file.read()


def write(key: str, value: str) -> None:
    """
    Write to the config file.
    This is a mostly internal function used to write to the config file from a user interface.

    Args:
        key (str): The key to write to.
        value (str): The value to write to `key`.
    """
    config_file = read()
    try:
        # as this is the only category we use right now, this is hardcoded
        config_file["config"][key]
    except KeyError as e:
        logger.critical("Could not find key.")
        raise KeyError("Invalid key.") from e
    # read 5 lines above
    config_file["config"][key] = value
    toml_file.TOMLFile(FILE_PATH).write(config_file)
