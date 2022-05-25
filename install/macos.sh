#!/usr/bin/env bash
# Made by RaptaG (https://github.com/RaptaG)

# Downloading the installer, installing python-tk and the python requirements
echo "INFO | Downloading the FO Vanilla Installer..."
tmp="$(mktemp -d)"
git clone https://github.com/Fabulously-Optimized/vanilla-installer /$tmp/fovi
echo "INFO | Installing dependencies..."
pip install tk > /dev/null 2>&1
cd /$tmp/fovi/
pip3 install -r requirements.txt > /dev/null 2>&1

# Directory selection (default ~/Library/Application Support/Minecraft)
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
mv vanilla-installer installer
mv data installer media $dir/VanillaInstaller/scripts/
cd $dir/VanillaInstaller/scripts/installer/
chmod +x gui.py main.py theme.py

# Cleaning up
echo "INFO | Removing unnecessary files..."
rm -rf $tmp
cd $dir/VanillaInstaller/scripts/media/
rm -r screenshots

# Running the script
echo "SUCCESS | Done. Starting the script..."
cd $dir/VanillaInstaller/scripts/installer/
python3 gui.py
