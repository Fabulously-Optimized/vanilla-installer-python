#!/usr/bin/env bash
# Distros tested: PopOS 21, 22 LTS
# Edits by RaptaG (https://github.com/RaptaG)

echo "INFO | Installing dependencies..."
sudo apt-get install python-tk
pip3 install -r requirements.txt
git clone https://github.com/Fabulously-Optimized/vanilla-installer/ $dir
cd $dir/vanilla-installer/
chmod +x gui.py
if [ $? -eq 0 ]; then # Success
    echo "SUCCESS | Done. Starting the script..."
    python3 vanilla-installer/gui.py
    
    if [ $? -eq 0 ]; then # Failure
        echo "WARNING | Python script terminated!"
    else
        echo "ERROR | Python script had an issue!"
    fi
else
    echo "ERROR | Dependencies should not be installed. Exiting."
fi
