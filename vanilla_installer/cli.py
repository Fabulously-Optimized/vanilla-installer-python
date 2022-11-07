"""A CLI interface for VanillaInstaller."""
## Imports

import webbrowser
import asyncio
import logging

# External
import asyncclick as click
import minecraft_launcher_lib as mll

# Local
from . import gui as external_gui
from . import main

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
async def install(minecraft_dir, version):
    if minecraft_dir is None or minecraft_dir == "":
        minecraft_dir = mll.utils.get_minecraft_directory()
    if version is None or version == "":
        version = main.newest_version()
    try:
        await main.run(interface="CLI", mc_dir=minecraft_dir, version=version)
    except TypeError:
        pass


@vanilla_installer.command("version", help="Show the version number and exit.")
async def version():
    version = main.get_version()
    click.echo(f"VanillaInstaller {version}")


@vanilla_installer.command("gui", help="Launch the GUI.")
async def gui():
    click.echo(f"Running VanillaInstaller-GUI {main.get_version()}")
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


@about.command("bug-report", help="Report a bug or crash in VanillaInstaller.")
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


@about.command("feature", help="Request a feature of VanillaInstaller.")
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
        "VanillaInstaller is licensed under the MIT License.\nYou may use this program and redistribute it, with or without source code. Modified works may be under a different license, as long as the copyright notice is maintained.\nFor the full text, please see https://github.com/Fabulously-Optimized/vanilla-installer/blob/main/LICENSE.md."
    )


if __name__ == "__main__":
    asyncio.run(vanilla_installer())
