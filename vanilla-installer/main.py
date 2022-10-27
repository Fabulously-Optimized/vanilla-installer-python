"""
Most important functions of VanillaInstaller.
"""
# IMPORTS

# Standard library
import io
import json
import os
import sys
import subprocess
import pathlib
import base64
from typing import Tuple
import zipfile
import re

# External
import requests
import minecraft_launcher_lib as mll
import click

if sys.version.startswith("3.11"):
    import tomllib as toml
else:
    import tomli as toml

# LOCAL
from log import logger

PATH_FILE = str(pathlib.Path("data/mc-path.txt").resolve())
TOKEN_FILE = str(pathlib.Path("data/gh-token.txt").resolve())
FOLDER_LOC = ""


def set_dir(path: str) -> str | None:
    """Sets the Minecraft game directory.

    Args:
        path (str): The path to the Minecraft game directory.
    """
    path_pl = pathlib.Path(path).resolve()
    if path is not None and path != "":
        with open(PATH_FILE, "w", encoding="utf-8") as file:
            file.write(str(path_pl))
    else:
        path_pl = pathlib.Path(mll.utils.get_minecraft_directory()).resolve()
    return str(path_pl)


def get_dir() -> str:
    """Returns the Minecraft game directory.

    Returns:
        str: Path
    """

    try:
        path = open(PATH_FILE, encoding="utf-8").read()
    except OSError:
        logger.exception("No mc_path.txt found. Calling set_dir.")
        default_dir = str(
            mll.utils.get_minecraft_directory()
        )  # Without this, it gives an error every time
        path = set_dir(default_dir)
    return path

def set_gh_auth(user: str, key: str) -> bool | None:
    """Sets the GitHub authentication details to be used by the GitHub api.
    Args:
        user (str): new username
        key (str): new key
    Returns:
        bool: whether the new user is valid or not
    """
    if key is not None and key != "" and user is not None and user != "":
        if requests.get("https://api.github.com/user", auth=(user, key)).status_code != 200:
            return False
        with open(TOKEN_FILE, "w", encoding="utf-8") as file:
            file.write(f"{user}\n{key}")
        return True
    if key == "" and user == "":
        open(TOKEN_FILE, "w").close() # empties file content
        return True
    return None

def get_gh_auth() -> Tuple[str, str] | None:
    """Returns the GitHub authentication details selected by the user, if it exists.

    Returns:
        str: User
        str: Key
    """

    try:
        file = open(TOKEN_FILE, encoding="utf-8").read()
        if file != "" and file is not None:
            auth_data = file.split("\n")
            return auth_data[0], auth_data[1]
    except:
        return None

def newest_version() -> str:
    """Returns the latest version of Minecraft.

    Returns:
      str: The latest Minecraft version
    """
    return get_pack_mc_versions()[0]


def get_java() -> str:
    """Returns the path to a Java executable.

    Returns:
      str: The path to the Java executable
    """
    return mll.utils.get_java_executable()


def fo_to_base64(png_dir: str = ".") -> str:
    """Converts the Fabulously Optimized logo from PNG format into base64.
    The directory specified in `dir` will be searched. If that fails, FO logo will be downloaded over the network.

    Args:
        dir (str): The directory to search for the logo.
    Returns:
        str: The base64 string for the FO logo.
    """

    dir_path = pathlib.Path(png_dir)
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


def get_version():
    version = "v1.0.0-dev1"
    return version



def text_update(
    text: str, widget=None, mode: str = "info", interface: str = "GUI"
) -> None:
    """Updates the text shown on the GUI window or echoes using Click.

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
    """Runs a command with subprocess.

    Returns:
        str: The output of the command.
    """
    command_output = subprocess.check_output(text.split()).decode("utf-8")
    output = logger.debug(command_output)
    text_update(output, mode="fg")
    return output


def install_fabric(mc_version: str, mc_dir: str) -> str:
    """Installs Fabric to the vanilla launcher.

    Args:
        mc_version (str): The version of Minecraft to get information from FO's files for.
        mc_dir (str): The directory to use.

    Returns:
        str: The Fabric version id. Formatted as `fabric-loader-{fabric_version}-{game_version}`.
    """
    meta_placeholder = "https://meta.fabricmc.net/v2/versions/loader/{}/{}/profile/zip"
    pack_toml_url = f"https://raw.githubusercontent.com/Fabulously-Optimized/Fabulously-Optimized/main/Packwiz/{mc_version}/pack.toml"

    if (response := requests.get(pack_toml_url)).status_code == 200:

        pack_info: dict = toml.loads(response.text)
        game_version = pack_info.get("versions", {}).get("minecraft")
        fabric_version = pack_info.get("versions", {}).get("fabric")
        meta_url = meta_placeholder.format(game_version, fabric_version)

        if (response := requests.get(meta_url)).status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
                version_id = f"fabric-loader-{fabric_version}-{game_version}"
                path = str(pathlib.Path(mc_dir).resolve() / "versions" / version_id)
                archive.extractall(path)

    return version_id


def download_pack(widget, interface: str = "GUI") -> str:
    """Downloads the packwiz_install_bootstrap jar.

    Args:
        interface (str, optional): The interface to pass to text_update, either "CLI" or "GUI". Defaults to "GUI".
    Returns:
        str: The path to the packwiz_installer_bootstrap.jar.
    """
    text_update(f"Fetching Pack...", widget=widget, interface=interface)
    download_bootstrap = requests.get(
        "https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar"
    )
    file_path_bootstrap = pathlib.Path(get_dir()) / "packwiz-installer-bootstrap.jar"
    with open(file_path_bootstrap, "wb") as file:
        file.write(download_bootstrap.content)
    packwiz_installer_bootstrap_path = pathlib.Path(get_dir()) / "packwiz-installer-bootstrap.jar"
    return str(packwiz_installer_bootstrap_path)


def install_pack(
    packwiz_installer_bootstrap: str,
    mc_version: str,
    mc_dir: str,
    widget=None,
    interface: str = "GUI",
) -> None:
    """Installs Fabulously Optimized.

    Args:
        packwiz_installer_bootstrap (str): The path to the packwiz installer bootstrap.
        mc_version (str): The version of Minecraft to install for.
        mc_dir (str): The directory to install to.
        widget (optional): The widget to update. Defaults to None.
        interface (str, optional): The interface to pass to text_update, either "CLI" or "GUI". Defaults to "GUI".
    """
    os.chdir(mc_dir)
    os.makedirs(f"{get_dir()}/", exist_ok=True)
    pack_toml = f"https://raw.githubusercontent.com/Fabulously-Optimized/Fabulously-Optimized/main/Packwiz/{mc_version}/pack.toml"
    try:
        ran = command(f"{get_java()} -jar {packwiz_installer_bootstrap} {pack_toml}")
        text_update(
            f"Installed Fabulously Optimized for MC {mc_version}.",
            widget,
            "success",
            interface=interface,
        )
    except Exception:
        text_update(
            f"Could not install Fabulously Optimized: {ran}",
            widget,
            "error",
            interface=interface,
        )


def create_profile(mc_dir: str, version_id: str) -> None:
    """Creates a profile in the vanilla launcher.

    Args:
        mc_dir (str): The path to the **default** Minecraft directory.
        version_id (str): The version of Minecraft to create a profile for.
    """
    launcher_profiles_path = pathlib.Path(mc_dir) / "launcher_profiles.json"

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

def get_pack_mc_versions() -> list[str]:
    """Gets a list of all the versions FO currently supports
    """
    exp = re.compile(r'\d+\.\d+(\.\d+)?')
    return_value = []
    try:
        auth = None
        authdata = get_gh_auth()
        if authdata is not None:
            user, key = authdata
            auth = (user, key)
        response = requests.get(
            "https://api.github.com/repos/Fabulously-Optimized/fabulously-optimized/contents/Packwiz", auth=auth).json()
        for response_content in response:
            if exp.search(response_content["name"]):
                return_value.append(response_content["name"])
        return_value.sort()
        return_value.reverse()
    except requests.exceptions.RequestException as e:
        logger.exception(f"Couldn't get minecraft versions:{e}")
    return return_value


def run(
    widget=None,
    mc_dir: str = mll.utils.get_minecraft_directory(),
    version: str = None,
    interface: str = "GUI",
) -> None:
    """Runs Fabric's installer and then installs Fabulously Optimized.

    Args:
        widget (optional): The widget to update. This is only used when interface is set to GUI. Defaults to None.
        mc_dir (str, optional): The directory to use. Defaults to the default directory based on your OS.
        version (str, optional): The version to install. Defaults to the newest version
        interface (str, optional): The interface to use, either CLI or GUI. Defaults to "GUI".
    """
    set_dir(mc_dir)

    if not pathlib.Path(mc_dir).resolve().exists():
        pathlib.Path(mc_dir).resolve().mkdir()

    if version is None:
        # the default version is set here instead of an argument because it slows down the startup
        # (by about ~0.05 seconds in my testing. but it might vary based on internet speeds)
        version = newest_version()
    text_update(
        "Installing Fabulously Optimized...", widget=widget, interface=interface
    )
    fabric_version = install_fabric(
        mc_version=version,
        mc_dir=mc_dir,
    )

    text_update(
        "Starting the Fabulously Optimized download...",
        widget=widget,
        interface=interface,
    )
    packwiz_bootstrap = download_pack(widget=widget, interface=interface)

    text_update(
        "Installing Fabulously Optimized...", widget=widget, interface=interface
    )
    install_pack(
        mc_version=version,
        packwiz_installer_bootstrap=packwiz_bootstrap,
        mc_dir=mc_dir,
    )
    text_update("Setting profiles...", widget=widget, interface=interface)
    create_profile(mc_dir, fabric_version)
