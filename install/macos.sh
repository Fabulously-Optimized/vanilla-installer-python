#!/usr/bin/env bash
# Made by RaptaG (https://github.com/RaptaG)

# Installing python-tk and the python requirements
echo "INFO | Installing dependencies..."
brew install python-tk
pip3 install -r requirements.txt

# Downloading the installer
echo "INFO | Downloading the installer..."
tmp=$(mktemp -d)
git clone https://github.com/Fabulously-Optimized/vanilla-installer /$tmp/vi

# Directory selection (default ~/Library/Application Support/Minecraft/)
read -p "Enter the directory you want (Press Enter to skip): " dir
if [ -z $dir ]; then
    dir="$HOME/Library/Application\ Support/Minecraft/"
fi

# Making them executable, moving them to the selected directory
echo "INFO | Installing the FO vanilla installer..."
cd $dir
mkdir vanilla-installer
cd /$tmp/vi/
mv data $dir/vanilla-installer/data
mv vanilla-installer $dir/vanilla-installer/installer
mv media $dir/vanilla-installer/media
cd $dir/vanilla-installer/installer/
chmod +x gui.py main.py theme.py

# Cleaning up
echo "INFO | Removing unnecessary files..."
rm -rf $tmp
cd $dir/vi/media/
rm -rf screenshots

# Running the script
if [ $? -eq 0 ]; then # Success output
    echo "SUCCESS | Done. Starting the script..."
    cd $dir
    python3 gui.py
    if [ $? -ne 0 ]; then # Failure output
        echo "WARNING | Python script terminated!"
        exit
    else
        echo "ERROR | Python script had an issue!"
        exit
    fi
else
    echo "ERROR | Dependencies should not be installed. Exiting."
    exit
fi
exit 1
