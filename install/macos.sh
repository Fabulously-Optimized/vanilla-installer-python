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

# Directory selection (default /usr/local/bin)
read -p "Enter the directory you want (Press Enter to skip): " dir
if [ -z $dir ]; then
    dir="/usr/local/bin/"
fi

# Making it executable, moving it to the selected directory
echo "INFO | Installing the installer..."
cd /$tmp/vi/vanilla-installer/
chmod +x gui.py
cp gui.py $dir

# Cleaning up
echo "INFO | Removing unnecessary files..."
rm -rf $tmp

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
