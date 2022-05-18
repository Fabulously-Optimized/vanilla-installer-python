#!/usr/bin/env bash
# Made by RaptaG (https://github.com/RaptaG)

# Installing python-tk
echo "INFO | Installing dependencies..."
brew install python-tk

# Downloading the installer and the python requirements
echo "INFO | Downloading the FO Vanilla Installer..."
tmp="$(mktemp -d)"
if [ -d $tmp ]; then
    rm -rf $tmp
    git clone https://github.com/Fabulously-Optimized/vanilla-installer /$tmp/fovi
else
    git clone https://github.com/Fabulously-Optimized/vanilla-installer /$tmp/fovi
fi
cd /$tmp/fovi/
pip3 install -r requirements.txt

# Directory selection (default ~/Library/Application Support/Minecraft/)
read -p "SELECT | Enter the directory you want (Press Enter to skip): " dir
if [ -z $dir ]; then
    dir="$HOME/Library/Application\ Support/Minecraft"
fi

# Making them executable, moving them to the selected directory
echo "INFO | Installing the FO Vanilla Installer..."
cd $dir/
mkdir VanillaInstaller
cd VanillaInstaller/
mkdir scripts
cd /$tmp/fovi/
mv data $dir/VanillaInstaller/scripts/data
mv vanilla-installer $dir/VanillaInstaller/scripts/installer
mv media $dir/VanillaInstaller/scripts/media
cd $dir/VanillaInstaller/scripts/installer/
chmod +x gui.py main.py theme.py

# Cleaning up
echo "INFO | Removing unnecessary files..."
rm -rf $tmp
cd $dir/VanillaInstaller/scripts/media/
rm -rf screenshots

# Running the script
if [ $? -eq 0 ]; then # Success output
    echo "SUCCESS | Done. Starting the script..."
    cd $dir/VanillaInstaller/scripts/installer/
    python3 gui.py
    if [ $? -ne 0 ]; then # Failure output
        echo "WARNING | The python script had an issue and terminated!"
        exit 1
    fi
else
    echo "ERROR | Dependencies should not be installed. Please run the script again."
    echo "Exiting..."
    exit 1
fi
