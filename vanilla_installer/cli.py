"""A CLI interface for VanillaInstaller."""
## Imports

# External
import click
import minecraft_launcher_lib as mll

# Local
from . import gui as external_gui
from . import main


@click.group("vanilla-installer")
def vanilla_installer():
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
def install(minecraft_dir, version):
    if minecraft_dir is None or minecraft_dir == "":
        minecraft_dir = mll.utils.get_minecraft_directory()
    if version is None or version == "":
        version = main.newest_version()
    main.run(interface="CLI", mc_dir=minecraft_dir, version=version)


@vanilla_installer.command("version", help="Show the version number and exit.")
def version():
    version = main.get_version()
    click.echo(f"VanillaInstaller {version}")


@vanilla_installer.command("gui", help="Launch the GUI.")
def gui():
    click.echo(f"Running VanillaInstaller-GUI {main.get_version()}")
    external_gui.run()
    click.echo(
        "GUI was closed. Usually this is intentional, if there was an error it was likely printed above."
    )


if __name__ == "__main__":
    vanilla_installer()
