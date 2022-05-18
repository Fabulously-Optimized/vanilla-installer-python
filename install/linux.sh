#!/bin/bash
# RaptaG's remade version (https://github.com/RaptaG)

# Installing python-tk (according to the distro)
echo "INFO | Installing dependencies..."
cd /usr/bin/
if [ -f apt ]; then
    sudo apt-get install python-tk
else
  if [ -f pacman ]; then
    sudo pacman -S python-tk
else
  if [ -f dnf ]; then
    sudo dnf install python-tk
else
  if [ -f zypper ]; then
    sudo zypper install python-tk
fi

# Downloading the installer and the python requirements
echo "INFO | Downloading the installer..."
cd /tmp/
if [ -d fovi ]; then
	rm -rf fovi
    git clone https://github.com/Fabulously-Optimized/vanilla-installer /tmp/fovi
else
	git clone https://github.com/Fabulously-Optimized/vanilla-installer /tmp/fovi
fi
cd /tmp/fovi/
pip3 install -r requirements.txt

# Directory selection (default ~/.minecraft/)
read -p "SELECT | Enter the directory you want (Press Enter to skip): " dir
if [ -z $dir ]; then
    dir="$HOME/.minecraft"
fi

# Making them executable, moving them to the selected directory
echo "INFO | Installing the FO vanilla installer..."
cd $dir/
mkdir VanillaInstaller
cd VanillaInstaller/
mkdir scripts
cd /tmp/fovi/
mv data $dir/VanillaInstaller/scripts/data
mv vanilla-installer $dir/VanillaInstaller/scripts/installer
mv media $dir/VanillaInstaller/scripts/media
cd $dir/VanillaInstaller/scripts/installer/
chmod +x gui.py main.py theme.py

# Cleaning up
echo "INFO | Removing unnecessary files..."
cd /tmp/
rm -rf fovi
cd $dir/VanillaInstaller/scripts/media/
rm -rf screenshots

# Running the script
if [ $? -eq 0 ]; then # Success output
    echo "SUCCESS | Done. Starting the script..."
    cd $dir/VanillaInstaller/scripts/installer/
    python3 gui.py
    if [ $? -ne 0 ]; then # Failure output
        echo "WARNING | The python script had an issue and terminated!"
        exit
    fi
else
    echo "ERROR | Dependencies should not be installed. Please run the script again."
    echo "Exiting..."
    exit
fi
