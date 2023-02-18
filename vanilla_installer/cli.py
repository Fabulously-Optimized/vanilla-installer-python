# Copyright (C) Fabulously Optimized 2022
# Licensed under the MIT License. The full license text can be found at https://github.com/Fabulously-Optimized/vanilla-installer/blob/main/LICENSE.md.
"""A CLI interface for Vanilla Installer."""
## Imports

import asyncio
import logging
import webbrowser
import sys

# External
import asyncclick as click
import minecraft_launcher_lib as mll

# Local
try:
    from vanilla_installer import gui as external_gui
except ImportError:
    pass
from vanilla_installer import main

logging.getLogger("asyncio").setLevel(logging.DEBUG)


@click.group(
    "vanilla-installer", context_settings=dict(help_option_names=["-h", "--help"])
)
async def vanilla_installer():
    pass


@vanilla_installer.command(
    "install", help="Install Fabulously Optimized to the specified directory."
)
@click.option(
    "--minecraft-dir",
    "-m",
    "minecraft_dir",
    help="The directory to install to. Defaults to the default directory based on your OS.",
)
@click.option(
    "--version",
    "-v",
    "version",
    help="The version of Minecraft to install Fabulously Optimized for. Defaults to the latest FO supports.",
)
@click.option(
    "--java-version",
    "-j",
    "java_ver",
    help="The version of Java to use. Defaults to the correct version based on --version. Can be 8, 16, 17.1, or 17.3. THIS IS A DEBUG OPTION, DO NOT USE IF YOU DON'T KNOW WHAT YOU'RE DOING.",
)
async def install(minecraft_dir, version, java_ver):
    if minecraft_dir is None or minecraft_dir == "":
        minecraft_dir = mll.utils.get_minecraft_directory()
    if version is None or version == "":
        version = main.newest_version()
    if java_ver is None or java_ver == "" or java_ver not in [8, 16, 17.1, 17.3]:
        if version.startswith("1.16"):
            java_ver = 8
        elif version.startswith("1.17"):
            java_ver = 16
        else:
            java_ver = 17.3
    try:
        await main.run(minecraft_dir, version, java_ver, "CLI")
    except TypeError:
        pass


@vanilla_installer.command("version", help="Show the version number and exit.")
async def version():
    version = main.get_version()
    click.echo(f"Vanilla Installer {version}")


@vanilla_installer.command("gui", help="Launch the GUI.", deprecated=True)
async def gui():
    try:
        if external_gui: pass
        else: pass
    except NameError:
        click.echo("The GUI is not installed, so this command will not function.")
        sys.exit(1)
    click.echo(f"Running Vanilla Installer-GUI {main.get_version()}")
    try:
        await external_gui.run()
    except TypeError:
        pass
    click.echo(
        "GUI was closed. Usually this is intentional, if there was an error it was likely printed above."
    )


@vanilla_installer.group("about", help="Shows information about the program.")
async def about():
    pass


@about.command("bug-report", help="Report a bug or crash in Vanilla Installer.")
async def bug():
    click.echo(
        "Press any key to open GitHub with the bug template in your web browser..."
    )
    user_input = input()
    if user_input is not None:
        try:
            await webbrowser.open(
                "https://github.com/Fabulously-Optimized/vanilla-installer/issues/new?labels=bug&template=bug.yml&title=%5BBug%5D%3A+"
            )
        except TypeError:
            pass


@about.command("feature", help="Request a feature of Vanilla Installer.")
async def feature():
    click.echo(
        "Press any key to open GitHub with the feature request template in your web browser..."
    )
    user_input = input()
    if user_input is not None:
        try:
            await webbrowser.open(
                "https://github.com/Fabulously-Optimized/vanilla-installer/issues/new?labels=enhancement&template=enhancement.yml&title=%5BFeature+Request%5D%3A+"
            )
        except TypeError:
            pass


@about.command("licensing", help="Shows licensing details on the program.")
async def licensing():
    click.echo(
        "Vanilla Installer is licensed under the MIT License.\nLicensed works, modifications, and larger works may be distributed under different terms and without source code.\nFor the full text, please see https://github.com/Fabulously-Optimized/vanilla-installer/blob/main/LICENSE.md.\nFor more about open-source licenses, see https://choosealicense.com."
    )


if __name__ == "__main__":
    asyncio.run(vanilla_installer())
