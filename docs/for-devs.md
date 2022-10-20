# Information, tips and notices for developers

## General developing information

As this project is written in Python, you will need Python installed. The current recommended version is Python 3.10, however it should work on Python 3.8 and anything newer.
We have a [`gitpod`](https://gitpod.io) configuration, so click this to be automatically teleported to gitpod with development all ready for you.

<a href="https://gitpod.io#https://github.com/Fabulously-Optimized/vanilla-installer"><img alt="gitpod" height="40" src="https://cdn.jsdelivr.net/npm/@intergrav/devins-badges@2/assets/compact/supported/gitpod_vector.svg"></a>

## Project structure

📂 vanilla-installer

    📂 3.8
    📂 3.9
    📂 3.10
    📂 3.11
        These all represent code files for different versions of Python.
        The primary files contained in these folders are manifests for [`pipenv`](https://docs.pipenv.org), since you can only have one Python version defined.

    📂 data
         Configs, settings and more...
         Can change from user to user.
         DO NOT "git commit" this folder. `.gitignore` ignores this folder by default.
         And please check if it's working for users that just downloaded VanillaInstaller!

    📂 install
        Installation scripts. For dependencies and more.
        Automatically install pip packages, apt (for debian-based systems)

    📂 media
        Images, pictures, logos, covers, banners, screenshots and more

    📂 tests (not committed!)
        .gitignore ignores this folder by default.
        I wouldn't recommend "git commit"-ing this folder, especially if there isn't any code which could be useful for other developers and contributors.

    📂 vanilla-installer
        Actual Python scripts. (GUI, CLI, helpers etc.)

## Avoiding 404s

This one might be obvious, but please keep in mind to ALWAYS `Ctrl+F` before renaming a file!
