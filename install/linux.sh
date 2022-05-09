#!/bin/bash
# Edits by RaptaG (https://github.com/RaptaG)

# Installing python-tk (according to the distro) and the python requirements
echo "INFO | Installing dependencies..."
cd /usr/bin/
if [ls apt -eq apt]; then
    sudo apt-get install python-tk
else
  if [ls pacman -eq pacman]; then
    sudo pacman -S python-tk
else
  if [ls dnf -eq dnf]; then
    sudo dnf install python-tk
else
  if [ls zypper -eq zypper]; then
    sudo zypper install python-tk
fi
pip3 install -r requirements.txt

# Downloading the installer
echo "INFO | Downloading the installer..."
git clone https://github.com/Fabulously-Optimized/vanilla-installer /tmp/vi

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
cd /tmp/vi/
mv data $dir/VanillaInstaller/scripts/data
mv vanilla-installer $dir/VanillaInstaller/scripts/installer
mv media $dir/VanillaInstaller/scripts/media
cd $dir/VanillaInstaller/scripts/installer/
chmod +x gui.py main.py theme.py

# Cleaning up
echo "INFO | Removing unnecessary files..."
cd /tmp/
rm -rf vi
cd $dir/VanillaInstaller/scripts/media/
rm -rf screenshots

# Running the script
if [ $? -eq 0 ]; then # Success output
    echo "SUCCESS | Done. Starting the script..."
    cd $dir/VanillaInstaller/scripts/installer/
    python3 gui.py
    if [ $? -ne 0 ]; then # Failure output
        echo "WARNING | Python script had an issue and terminated!"
        exit
    fi
else
    echo "ERROR | Dependencies should not be installed. Please run the script again."
    echo "Exiting..."
    exit
fi
exit 1
