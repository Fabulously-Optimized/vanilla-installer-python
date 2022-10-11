"""A CLI interface for VanillaInstaller."""
# Standard library imports

# External
import click

# Local
import main


@click.command()
@click.option("--minecraft-dir", "-m", "minecraft_dir")
def install(minecraft_dir):
    main.run()
