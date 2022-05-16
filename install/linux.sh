#!/bin/bash
# Edits by RaptaG (https://github.com/RaptaG)

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
if [ -d vi ]; then
	rm -rf vi
    git clone https://github.com/Fabulously-Optimized/vanilla-installer /tmp/vi
else
	git clone https://github.com/Fabulously-Optimized/vanilla-installer /tmp/vi
fi
cd /tmp/vi/
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
        exit 1
    fi
else
    echo "ERROR | Dependencies should not be installed. Please run the script again."
    echo "Exiting..."
    exit 1
fi
