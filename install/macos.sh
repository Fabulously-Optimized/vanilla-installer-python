#!/usr/bin/env bash
# Made by RaptaG (https://github.com/RaptaG)

# Root permission checker
if [ $EUID -ne 0 ]; then
  echo "ERROR | Root permissions are needed for the script to work. Please run sudo ./$(basename $0)" >&2
  exit 1
fi

# Installing python-tk and the python requirements
echo "INFO | Installing dependencies..."
brew install python-tk
pip3 install -r requirements.txt

# Downloading the installer
echo "INFO | Downloading the installer..."
tmp=$(mktemp -d)
git clone https://github.com/Fabulously-Optimized/vanilla-installer /$tmp/vi

# Making it executable, moving it to the selected directory
echo "INFO | Installing the installer..."
cd /$tmp/vi/vanilla-installer/
chmod +x gui.py
cp gui.py $dir

# Cleaning up
echo "INFO | Removing unnecessary files..."
rm -r $tmp

# Running the script
if [ $? -eq 0 ]; then # Success output
    echo "SUCCESS | Done. Starting the script..."
    cd $dir
    python3 gui.py
    if [ $? -eq 0 ]; then # Failure output
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
