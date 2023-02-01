# Information, tips and notices for developers

## General developing information

As this project is written in Python, you will need Python installed. The current recommended version is Python 3.10, however it should work on Python 3.8 and anything newer.
We have a [`gitpod`](https://gitpod.io) configuration, so click this to be automatically teleported to gitpod with development all ready for you.

<a href="https://gitpod.io#https://github.com/Fabulously-Optimized/vanilla-installer"><img alt="gitpod" height="40" src="https://cdn.jsdelivr.net/npm/@intergrav/devins-badges@2/assets/compact/supported/gitpod_vector.svg"></a>

## Project structure

📂 vanilla-installer

    📂 install
        Installation scripts. For dependencies and more.
        Automatically install pip packages, apt (for debian-based systems)

    📂 media
        Images, pictures, logos, covers, banners, screenshots and more

    📂 vanilla_installer
        Actual Python scripts. (GUI, CLI, helpers etc.)

## Avoiding 404s

This one might be obvious, but please keep in mind to ALWAYS `Ctrl+F` before renaming a file!
