"""
Most important functions of VanillaInstaller.
"""
# IMPORTS

# Standard library
import io
import json
import os
import sys
import logging
import logging.handlers  # pylance moment
import subprocess
import pathlib
import base64
import zipfile

# External
import requests
import minecraft_launcher_lib as mll
import click
if sys.version.startswith("3.11"):
    import tomllib as toml
else:
    import tomli as toml

# LOCAL
import theme

PATH_FILE = str(pathlib.Path("data/mc-path.txt").resolve())
FOLDER_LOC = ""


def set_dir(path: str) -> str | None:
    """Sets the Minecraft game directory.

    Args:
        path (str): The path to the Minecraft game directory.
    """
    if path:  # only strings can be written
        path_nobackslash = str(rf"{path}".replace("\\", "/"))
        path_nobackslash = str(rf"{path_nobackslash}".replace(".minecraft", ""))
    else:
        logging.critical("path must be passed!")
        return Exception
    # If the path is none, it will cause the script to fail.
    # In that case, return the default directory.
    if path_nobackslash is not None:
        with open(PATH_FILE, "w", encoding="utf-8") as file:
            file.write(path_nobackslash)
        return path_nobackslash
    if path_nobackslash != "":
        with open(PATH_FILE, "w", encoding="utf-8") as file:
            file.write(path_nobackslash)
        return path_nobackslash
    path_nobackslash_minecraft = mll.utils.get_minecraft_directory()
    path_nobackslash = path_nobackslash_minecraft.replace(".minecraft", "")
    with open(PATH_FILE, "w", encoding="utf-8") as file:
        file.write(path_nobackslash)
    return path_nobackslash


def get_dir() -> str:
    """Returns the Minecraft game directory.

    Returns:
        str: Path
    """
    try:
        path = open(PATH_FILE, encoding="utf-8").read()
    except OSError:
        logging.exception("No mc_path.txt found. Calling set_dir.")
        default_dir = str(
            mll.utils.get_minecraft_directory()
        )  # Without this, it gives an error every time
        path = set_dir(default_dir)
    return path


def newest_version() -> str:
    """Returns the latest version of Minecraft.

    Returns:
      str: The latest Minecraft version
    """
    return mll.utils.get_latest_version()["release"]


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
        logging.warning("Cannot find logo locally. Trying to download...")
        url = "https://avatars.githubusercontent.com/u/92206402"
        if (response := requests.get(url)).status_code == 200:
            png_content = response.content
        else:
            logging.critical("Could not get the FO logo over the network.")

    b64logo = base64.b64encode(png_content).decode("utf-8")
    return f"data:image/png;base64,{b64logo}"

def get_version():
    version = "v1.0.0-unstable"
    return version

def init() -> None:
    """Initialization for VanillaInstaller."""
    # SET INSTALLATION PATH
    if not os.path.exists(PATH_FILE):
        try:
            path = mll.utils.get_minecraft_directory().replace(".minecraft", "")
            set_dir(path)
        except Exception as error_code:  # any error could happen, really.
            logging.error(
                f"Could not get Minecraft path: {error_code}\nUsing default path based on OS."
            )
            # The first two `startswith` are simply a precaution, since Python previously used a different number for different Linux kernels.
            # The `startswith` for Windows is if they ever change it to `win64` or something, but I doubt that.
            # See https://docs.python.org/3.10/library/sys.html#sys.platform for more.
            if sys.platform.startswith("win"):
                path = os.path.expanduser("~/AppData/Roaming")
                set_dir(path)
            elif sys.platform.startswith("darwin"):
                path = os.path.expanduser("~/Library/Application Support")
                set_dir(path)
            elif sys.platform.startswith("linux"):
                path = os.path.expanduser("~")
                set_dir(path)
            else:
                logging.error("Could not detect OS.")


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
            widget.master.title(f"{text} » VanillaInstaller")
            widget["text"] = text
            widget["fg"] = theme.load()[mode]

        else:
            if mode == "fg":
                logging.debug(text)
            if mode == "warn":
                logging.warning(text)
            if mode == "error":
                logging.error(text)
            if mode == "success":
                logging.info(text)
            if mode == "info":
                logging.info(text)
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
    output = logging.debug(command_output)
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
    file_path_bootstrap = get_dir() + "packwiz-installer-bootstrap.jar"
    with open(file_path_bootstrap, "wb") as file:
        file.write(download_bootstrap.content)
    packwiz_installer_bootstrap_path = get_dir() + "packwiz-installer-bootstrap.jar"
    return str(packwiz_installer_bootstrap_path)


def install_pack(
    packwiz_installer_bootstrap: str,
    mc_version: str,
    mc_dir: str,
    widget=None,
    interface: str = "GUI",
):
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
            f"Installed Fabulously Optimized for MC {mc_version}!\nThe installer has finished.",
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
    profiles = json.loads(launcher_profiles_path.read_bytes())

    profile = {
        "lastVersionId": version_id,
        "name": "Fabulously Optimized",
        "type": "custom",
        "icon": fo_to_base64(),
        "gameDir": mc_dir, # Not sure about this
        # "javaArgs": "I dunno if fabric installer sets any javaArgs by itself" 
    }

    profiles["profiles"]["FO"] = profile
    profiles_json = json.dumps(profiles, indent=4)
    launcher_profiles_path.write_text(profiles_json)

def run(
    widget=None,
    mc_dir: str = mll.utils.get_minecraft_directory(),
    interface: str = "GUI",
) -> None:
    """Runs Fabric's installer and then installs Fabulously Optimized.

    Args:
        widget (optional): The widget to update. This is only used when interface is set to GUI. Defaults to None.
        mc_dir (str, optional): The directory to use. Defaults to the default directory based on your OS.
        interface (str, optional): The interface to use, either CLI or GUI. Defaults to "GUI".
    """
    text_update("Starting Fabric Installation...", widget=widget, interface=interface)
    version = install_fabric(
        mc_version=newest_version(),
        mc_dir=mc_dir,
    )

    text_update("Starting Pack Download...", widget=widget, interface=interface)
    packwiz_bootstrap = download_pack(widget=widget, interface=interface)

    text_update("Starting Pack Installation...", widget=widget, interface=interface)
    install_pack(
        mc_version=newest_version(),
        packwiz_installer_bootstrap=packwiz_bootstrap,
        mc_dir=mc_dir
    )
    text_update("Setting profiles...", widget=widget, interface=interface)
    create_profile(mc_dir, version)


def start_log() -> None:
    """Starts logging for VanillaInstaller."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    try:
        handler = logging.handlers.RotatingFileHandler(
            filename="logs/vanilla_installer.log",
            encoding="utf-8",
            maxBytes=32 * 1024 * 1024,  # 32 MiB
            backupCount=5,  # Rotate through 5 files
        )
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    except Exception:
        # for some reason logging keeps failing, since it's not crucial just pass
        # As such this print()s to stdout
        print("ERROR | Unable to start logging, logging to stdout")
        print("ERROR | Error code: 0xDEADBEEF")

    logging.info("Starting VanillaInstaller")
    logger = logging.getLogger("VanillaInstaller")


if __name__ == "__main__":
    init()  # start initialization
    start_log()  # start logging in case of issues
