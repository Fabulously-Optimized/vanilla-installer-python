# TESTED ON PopOS 21 and 22 LTS

cd ./
echo "INFO | Installing dependencies..."

sudo apt install python-tk # for tkinter
sudo apt install libnotify-bin # for pynotifier

pip3 install -r requirements.txt # for pip dependencies

if [ $? -eq 0 ]; then # success
    echo "SUCCESS | Done. Starting the script..."
    python3 vanilla-installer/gui.py
    
    if [ $? -eq 0 ]; then # success
        echo "WARNING | Python script terminated!"
    else
        echo "ERROR | Python script had an issue!"
    fi
else
    echo "ERROR | Dependencies should not be installed. Exiting."
fi