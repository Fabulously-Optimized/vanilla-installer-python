# TESTED ON PopOS 21 and 22 LTS

cd ./
echo "INFO | Installing dependencies..."
sudo apt-get install python-tk
pip3 install -r requirements.txt
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