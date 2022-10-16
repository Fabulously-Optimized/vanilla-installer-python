"""A CLI interface for VanillaInstaller."""
# Standard library imports
import sys

# External
import click

# Local
import main


@click.group("vanilla-installer")
def vanilla_installer():
    pass


@vanilla_installer.command(
    "install", help="Install Fabulously Optimized to the specified directory."
)
@click.option(
    "--minecraft-dir", "-m", "minecraft_dir", help="The directory to install to."
)
def install(minecraft_dir):
    main.run(mc_dir=minecraft_dir, interface="CLI")


@vanilla_installer.command("version", help="Show the version number and exit.")
def version():
    version = main.get_version()
    click.echo(f"VanillaInstaller {version}")


if __name__ == "__main__":
    vanilla_installer()
