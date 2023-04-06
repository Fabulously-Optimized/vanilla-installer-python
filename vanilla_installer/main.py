# Copyright (C) Fabulously Optimized 2023
# Licensed under the MIT License. The full license text can be found at https://github.com/Fabulously-Optimized/vanilla-installer/blob/main/LICENSE.md.
"""
Most important functions of Vanilla Installer.
"""
# IMPORTS

import base64
import io
import json
import os
import platform
import subprocess
import zipfile
from pathlib import Path
from typing import Optional

import click
import minecraft_launcher_lib as mll
import requests
import tomlkit as toml

# Local
from vanilla_installer import __version__, config, log

logger = log.logger

FOLDER_LOC = ""


def set_dir(path: str = mll.utils.get_minecraft_directory()) -> str | None:
    """
    Sets the Minecraft game directory.

    Args:
        path (str): The path to the Minecraft game directory.
    """
    path_pl = Path(path).resolve()
    config.write("path", str(path_pl))
    return str(path_pl)


def get_dir() -> str:
    """
    Returns the Minecraft game directory.

    Returns:
        str: Path
    """

    path = config.read()
    return path["config"]["path"]


def newest_version() -> str:
    """
    Returns the latest version of Minecraft that FO supports.

    Returns:
      str: The latest Minecraft version that FO supports.
    """
    return get_pack_mc_versions()[0]


def find_mc_java(java_ver: float = 17.3) -> str:
    """
    Gets the path to the Java executable downloaded from the vanilla launcher.

    Args:
        java_ver (float, optional): The Java version to find. Can be 8, 16, 17.1, or 17.3 Defaults to 17.3 and falls back to it if the integer is invalid.

    Returns:
        str: The complete path to the Java executable.
    """
    if platform.system() == "Windows":
        program_files = os.environ["PROGRAMFILES(X86)"]
        if java_ver == 8:
            java = str(
                Path(
                    f"{program_files}/Minecraft Launcher/runtime/java-runtime-legacy/windows-x64/java-runtime-legacy/bin/javaw.exe"
                )
            )
        elif java_ver == 16:
            java = str(
                Path(
                    f"{program_files}/Minecraft Launcher/runtime/java-runtime-alpha/windows-x64/java-runtime-alpha/bin/javaw.exe"
                )
            )
        elif java_ver == 17.1:
            java = str(
                Path(
                    f"{program_files}/Minecraft Launcher/runtime/java-runtime-beta/windows-x64/java-runtime-beta/bin/javaw.exe"
                )
            )
        else:
            java = str(
                Path(
                    f"{program_files}/Minecraft Launcher/runtime/java-runtime-gamma/windows-x64/java-runtime-gamma/bin/javaw.exe"
                )
            )
    elif platform.system() == "Linux":
        if java_ver == 8:
            java = str(
                Path(
                    "~/.minecraft/runtime/java-runtime-legacy/linux/java-runtime-legacy/bin/java"
                ).resolve()
            )
        elif java_ver == 16:
            java = str(
                Path(
                    "~/.minecraft/runtime/java-runtime-alpha/linux/java-runtime-alpha/bin/java"
                ).resolve()
            )
        elif java_ver == 17.1:
            java = str(
                Path(
                    "~/.minecraft/runtime/java-runtime-beta/linux/java-runtime-beta/bin/java"
                ).resolve()
            )
        else:
            java = str(
                Path(
                    "~/.minecraft/runtime/java-runtime-gamma/linux/java-runtime-gamma/bin/java"
                ).resolve()
            )
    elif platform.system("Mac"):  # all of this may or may not work
        if java_ver == 8:
            java = str(
                Path(
                    "/Applications/Minecraft.app/Contents/MacOS/launcher/runtime/java-runtime-legacy/darwin/java-runtime-legacy/bin/java"
                )
            )
        elif java_ver == 16:
            java = str(
                Path(
                    "/Applications/Minecraft.app/Contents/MacOS/launcher/runtime/java-runtime-alpha/darwin/java-runtime-alpha/bin/java"
                )
            )
        elif java_ver == 17.1:
            java = str(
                Path(
                    "/Applications/Minecraft.app/Contents/MacOS/launcher/runtime/java-runtime-beta/darwin/java-runtime-beta/bin/java"
                )
            )
        else:
            java = str(
                Path(
                    "/Applications/Minecraft.app/Contents/MacOS/launcher/runtime/java-runtime-gamma/darwin/java-runtime-gamma/bin/java"
                )
            )

    return java


def get_java(java_ver: float = 17.3) -> str:
    """
    Gets the path to a Java executable.
    If the user doesn't have a JRE/JDK installed on the system, it will default to the Microsoft
    OpenJDK / Microsoft JDK build that the vanilla launcher installs when you run Minecraft.

    Args:
        java_ver (float, optional): The Java version to find. Can be 8, 16, 17.1 (Java 17.0.1) or 17.3 (Java 17.0.3). Defaults to 17.3, and falls back to 17.3 if the integer is invalid.

    Returns:
        str: The complete path to the Java executable.
    """
    java = mll.utils.get_java_executable()
    if java is None or java == "":
        java = find_mc_java(java_ver)
    return java


def fo_to_base64(png_dir: str = ".") -> str:
    """
    Converts the Fabulously Optimized logo from PNG format into base64.
    The directory specified in `dir` will be searched. If that fails, FO logo will be downloaded over the network.

    Args:
        dir (str): The directory to search for the logo.
    Returns:
        str: The base64 string for the FO logo.
    """

    dir_path = Path(png_dir)
    png_content = bytes()

    if (png_path := dir_path / "fo.png").exists():
        png_content = png_path.read_bytes()
    else:
        logger.warning("Cannot find logo locally. Trying to download...")
        url = "https://avatars.githubusercontent.com/u/92206402"
        if (response := requests.get(url)).status_code == 200:
            png_content = response.content
        else:
            logger.critical("Could not get the FO logo over the network.")
    b64logo = base64.b64encode(png_content).decode("utf-8")
    return f"data:image/png;base64,{b64logo}"


def get_version() -> str:
    return __version__


def text_update(
    text: str, widget=None, mode: str = "info", interface: str = "GUI"
) -> None:
    """
    Updates the text shown on the GUI window or echoes using Click.

    Args:
        text (str): The text to display
        widget (optional): The widget. Defaults to None.
        mode (str, optional): The type of message to log. Defaults to "info".
        interface (str, optional): The interface to display to. Defaults to "GUI", possible values are "GUI" and "CLI".
    """
    if interface != "CLI":
        if widget:
            widget.setText(text)

        else:
            if mode == "fg":
                logger.debug(text)
            if mode == "warn":
                logger.warning(text)
            if mode == "error":
                logger.error(text)
            if mode == "success":
                logger.info(text)
            if mode == "info":
                logger.info(text)
    else:
        if mode == "error":
            click.echo(text, err=True)
        else:
            click.echo(text)


def command(text: str) -> str:
    """
    Runs a command with subprocess.

    Returns:
        str: The output of the command.
    """
    command_output = subprocess.check_output(text.split()).decode("utf-8")
    output = logger.debug(command_output)
    return output


def install_fabric(mc_version: str, mc_dir: str) -> str:
    """
    Installs Fabric to the vanilla launcher.

    Args:
        mc_version (str): The version of Minecraft to get information from FO's files for.
        mc_dir (str): The directory to use.

    Returns:
        str: The Fabric version id. Formatted as `fabric-loader-{fabric_version}-{game_version}`.
    """
    meta_placeholder = "https://meta.fabricmc.net/v2/versions/loader/{}/{}/profile/zip"
    pack_toml_url = convert_version(mc_version)

    # if (response := requests.get(pack_toml_url)).status_code == 200:
    response = requests.get(pack_toml_url)
    pack_info = toml.parse(response.text)
    game_version = pack_info["versions"]["minecraft"]
    fabric_version = pack_info["versions"]["fabric"]
    meta_url = meta_placeholder.format(game_version, fabric_version)

    response = requests.get(meta_url)
    version_id = f"fabric-loader-{fabric_version}-{game_version}"
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        path = str(Path(mc_dir).resolve() / "versions")
        archive.extractall(path)

    return version_id


def download_pack(widget, interface: str = "GUI") -> str:
    """
    Downloads the packwiz_install_bootstrap jar.

    Args:
        interface (str, optional): The interface to pass to text_update, either "CLI" or "GUI". Defaults to "GUI".
    Returns:
        str: The path to the packwiz_installer_bootstrap.jar.
    """
    text_update("Fetching Pack...", widget, "info", interface)
    download_bootstrap = requests.get(
        "https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar"
    )
    file_path_bootstrap = Path(get_dir()) / "packwiz-installer-bootstrap.jar"
    with open(file_path_bootstrap, "wb") as file:
        file.write(download_bootstrap.content)
    packwiz_installer_bootstrap_path = (
        Path(get_dir()) / "packwiz-installer-bootstrap.jar"
    )
    return str(packwiz_installer_bootstrap_path)


def install_pack(
    packwiz_installer_bootstrap: str,
    mc_version: str,
    mc_dir: str,
    widget=None,
    interface: str = "GUI",
    java_ver: float = 17.3,
) -> None:
    """
    Installs Fabulously Optimized.

    Args:
        packwiz_installer_bootstrap (str): The path to the packwiz installer bootstrap.
        mc_version (str): The version of Minecraft to install for.
        mc_dir (str): The directory to install to.
        widget (optional): The widget to update. Defaults to None.
        interface (str, optional): The interface to pass to text_update, either "CLI" or "GUI". Defaults to "GUI".
        java_ver (float): The Java version to use. Defaults to 17.3
    """
    logger.debug("Installing the pack now.")
    os.chdir(mc_dir)
    os.makedirs(f"{get_dir()}/", exist_ok=True)
    pack_toml = convert_version(mc_version)
    try:
        command(
            f"{get_java(java_ver)} -jar {packwiz_installer_bootstrap} {pack_toml} --timeout 0"
        )
        logger.info(
            f"Completed installing Fabulously Optimized for Minecraft {mc_version}"
        )
        text_update(
            f"Installed Fabulously Optimized for Minecraft {mc_version}.",
            widget,
            "success",
            interface=interface,
        )
    except Exception as e:
        logger.exception(f"Could not install Fabulously Optimized: {e}")
        text_update(
            f"Could not install Fabulously Optimized: {e}",
            widget,
            "error",
            interface,
        )


def create_profile(mc_dir: str, version_id: str) -> None:
    """
    Creates a profile in the vanilla launcher.

    Args:
        mc_dir (str): The path to the Minecraft directory.
        version_id (str): The version of Minecraft to create a profile for.
    """
    launcher_profiles_path = (
        Path(mll.utils.get_minecraft_directory()) / "launcher_profiles.json"
    )

    try:
        profiles = json.loads(launcher_profiles_path.read_bytes())
    except Exception:
        logger.error(f"Launcher profile not found at {launcher_profiles_path}.")

    profile = {
        "lastVersionId": version_id,
        "name": "Fabulously Optimized",
        "type": "custom",
        "icon": fo_to_base64(),
        "gameDir": mc_dir,  # Not sure about this
        # "javaArgs": "I dunno if fabric installer sets any javaArgs by itself"
    }

    profiles["profiles"]["FO"] = profile
    profiles_json = json.dumps(profiles, indent=4)
    launcher_profiles_path.write_text(profiles_json)


def get_pack_mc_versions() -> dict:
    """
    Gets a list of all the versions FO currently supports.
    """

    return_value = dict()
    try:
        try:
            response = requests.get(
                "https://raw.githubusercontent.com/Fabulously-Optimized/vanilla-installer/main/vanilla_installer/assets/versions.json"
            ).json()
        except requests.exceptions.RequestException or response.status_code != "200":
            # This should never happen unless a) there's no internet connection, b) the file was deleted or is missing in a development case.
            # In this case, fall back to a local file since in the latter you'll likely have the whole repo cloned.
            # For this to work, you need to be in the root directory of the repository running this, otherwise the files will not be found.
            logger.warning("GitHub failed, falling back to local...")
            try:
                local_path = (
                    Path("vanilla_installer/assets").resolve() / "versions.json"
                )
            except:
                local_path = Path("assets").resolve() / "versions.json"
            response = json.loads(local_path.read_bytes())

        return_value = dict(response)
        return return_value
    except requests.exceptions.RequestException as e:
        logger.exception(f"Couldn't get minecraft versions: {e}")


def convert_version(input_mcver: str) -> str:
    """
    Converts a version string to the appropriate FO pack.toml

    Args:
        input_mcver (str): The Minecraft version to find.

    Returns:
        str: The converted version as a direct JSDelivr URL.
    """
    versions = get_pack_mc_versions()
    return_value = versions.get(input_mcver)
    if return_value is None:
        raise TypeError("Invalid or unsupported Minecraft version.")
    else:
        return return_value


def run(
    mc_dir: str = mll.utils.get_minecraft_directory(),
    version: Optional[str] = None,
    java_ver: float = 17.3,
    interface: str = "GUI",
    widget=None,
) -> None:
    """
    Runs Fabric's installer and then installs Fabulously Optimized.

    Args:
        widget (optional): The widget to update. This is only used when interface is set to GUI. Defaults to None.
        mc_dir (str, optional): The directory to use. Defaults to the default directory based on your OS.
        version (str, optional): The version to install. Defaults to the newest version
        interface (str, optional): The interface to use, either CLI or GUI. Defaults to "GUI".
    """
    logger.debug("Install function called, setting given directory.")
    set_dir(mc_dir)

    if not Path(mc_dir).resolve().exists():
        logger.warning("Given path did not exist; creating.")
        Path(mc_dir).resolve().mkdir()

    if version is None:
        # the default version is set here instead of an argument because it slows down the startup
        # (by about ~0.05 seconds in my testing. but it might vary based on internet speeds)
        logger.warning("Version was not passed, defaulting to the latest version.")
        version = newest_version()
    logger.info("Calling install_fabric to install Fabric.")
    text_update("Installing Fabric...", widget, "info", interface)
    fabric_version = install_fabric(version, mll.utils.get_minecraft_directory())
    logger.debug("Downloading FO - calling download_pack.")
    text_update(
        "Starting the Fabulously Optimized download...",
        widget,
        "info",
        interface,
    )
    packwiz_bootstrap = download_pack(widget, interface)
    logger.info("Installing FO, Packwiz will run.")
    text_update("Installing Fabulously Optimized...", widget, "info", interface)
    install_pack(
        packwiz_bootstrap,
        version,
        mc_dir,
        widget,
        java_ver,
    )
    logger.info("Setting the profile.")
    text_update("Setting profiles...", widget, "info", interface)
    create_profile(mc_dir, fabric_version)
    text_update("Complete!", widget, "info", interface)
    logger.info("Success!")
