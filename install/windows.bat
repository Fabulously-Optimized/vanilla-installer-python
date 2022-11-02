:: Mostly untested
:: By osfanbuff63

setlocal

set temp_dir=%TMP%\fovi
cd %TMP%
mkdir fovi
cd %temp_dir%
goto download

:download
echo "INFO | Downloading the installer..."
git clone https://github.com/Fabulously-Optimized/vanilla-installer %temp_dir%

echo "INFO | Downloading the dependencies..."
cd .\fovi
pip install -r requirements.txt > C:\nul 2>&1
goto install

:install
:: Decided to not make this select on install since I'm not sure how to do that effectively
:: if someone wants to do that please do
echo "INFO | Installing the FO vanilla installer..."
set dir=%AppData%\.minecraft
cd %dir%
mkdir VanillaInstaller
cd VanillaInstaller
mkdir scripts
cd %temp_dir%
move vanilla_installer installer
move data %dir%\VanillaInstaller\scripts\
move installer %dir%\VanillaInstaller\scripts\
move media %dir%\VanillaInstaller\scripts\
cd %dir%\VanillaInstaller\scripts\installer\
goto cleanup

:cleanup
echo "INFO | Removing unnecessary files..."
cd %TMP%
rd /s /q fovi
cd %dir%\VanillaInstaller\scripts\media\
rd \s \q screenshots
goto start

:start
echo "SUCCESS | Starting the script..."
cd %dir%\VanillaInstaller\scripts\installer\
python gui.py
