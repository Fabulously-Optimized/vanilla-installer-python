#!/usr/bin/env/bash
# Enhanced by RaptaG (https://github.com/RaptaG)

# Crash checker
set -e

# Directory selection (default ~/.minecraft)
echo -n "SELECT | Enter the directory you want (Press Enter to skip): "
read dir
if [ -z $dir ]; then
    dir="$HOME/.minecraft"
fi

# Downloading the installer, installing python-tk and the python requirements
download() {
    echo "INFO | Downloading the installer..."
    git clone https://github.com/Fabulously-Optimized/vanilla-installer /tmp/fovi

    echo "INFO | Downloading the dependencies..."
    pip install tk > /dev/null 2>&1
    cd /tmp/fovi/
    pip3 install -r requirements.txt > /dev/null 2>&1
}

# Moving the python scripts to the selected directory, making them executable
install() {
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
}

# Cleaning up
cleanup() {
    echo "INFO | Removing unnecessary files..."
    cd /tmp/
    rm -rf fovi
    cd $dir/VanillaInstaller/scripts/media/
    rm -r screenshots
}

# Running the script
download "$@"
install "$@"
cleanup "$@"

echo "SUCCESS | Starting the script..."
cd $dir/VanillaInstaller/scripts/installer/
python3 gui.py
