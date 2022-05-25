#!/bin/bash
# Enhanced by RaptaG (https://github.com/RaptaG)

# Downloading the installer, installing python-tk and the python requirements
echo "INFO | Downloading the installer..."
git clone https://github.com/Fabulously-Optimized/vanilla-installer /tmp/fovi
echo "INFO | Installing dependencies..."
pip install tk > /dev/null 2>&1
cd /tmp/fovi/
pip3 install -r requirements.txt > /dev/null 2>&1

# Directory selection (default ~/.minecraft)
read -p "SELECT | Enter the directory you want (Press Enter to skip): " dir
if [ -z $dir ]; then
    dir="$HOME/.minecraft"
fi

# Moving the python scripts to the selected directory, making them executable
echo "INFO | Installing the FO vanilla installer..."
cd $dir/
mkdir VanillaInstaller
cd VanillaInstaller/
mkdir scripts
cd /tmp/fovi/
mv vanilla-installer installer
mv data installer media $dir/VanillaInstaller/scripts/
cd $dir/VanillaInstaller/scripts/installer/
chmod +x gui.py main.py theme.py

# Cleaning up
echo "INFO | Removing unnecessary files..."
cd /tmp/
rm -rf fovi
cd $dir/VanillaInstaller/scripts/media/
rm -r screenshots

# Running the script
echo "SUCCESS | Starting the script..."
cd $dir/VanillaInstaller/scripts/installer/
python3 gui.py
