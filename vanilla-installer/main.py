"""
Most important functions of VanillaInstaller.
"""

PATH_FILE = 'data/mc-path.txt'
FOLDER_LOC = ''
TEMP_FOLDER = 'temp/'

# IMPORTS
import os
import sys
import gui
import zipfile
import logging
import requests
import webbrowser
import subprocess
import minecraft_launcher_lib as mll

# LOCAL
import theme

def set_dir(path: str) -> str:
    """Sets the Minecraft game directory.

    Args:
        path (str): The path to the Minecraft game directory.
    """
    if isinstance(path, str): # only strings can be written
        open(PATH_FILE, 'w').write(path)
        return path

def get_dir() -> str:
    """Returns the Minecraft game directory.

    Returns:
        str: Path
    """
    return open(PATH_FILE).read()
            
def newest_version() -> str:
    return mll.utils.get_latest_version()['release']
            
def get_java() -> str:
    return mll.utils.get_java_executable()

def init() -> None:
    # SET INSTALLATION PATH
    if not os.path.exists(PATH_FILE):
        try:
            path = mll.utils.get_minecraft_directory().replace('.minecraft', '')
        except Exception as e: # any error could happen, really.
            logging.error(f'Could not get Minecraft path: {e}')
            set_dir()
        else:
            set_dir(path)

    # SET 

def text_update(text: str, widget=None, mode: str='info') -> None:
    if widget:
        widget.master.title(f'{text} » VanillaInstaller')
        widget['text'] = text
        widget['fg'] = theme.load()[mode]
        
    else:
        if mode == 'fg':
            logging.debug(text)
        if mode == 'warn':
            logging.warn(text)
        if mode == 'error':
            logging.error(text)
        if mode == 'success':
            logging.info(text)

def command(text: str) -> str:
    output = logging.debug(subprocess.check_output(text.split()).decode('utf-8'))
    text_update(output, mode='fg')
    return output

def download_minecraft() -> None: # currently manually
    webbrowser.open('https://www.minecraft.net/download')

def download_fabric(widget=None) -> str: # https://github.com/max-niederman/fabric-quick-setup/blob/40c959c6cd2295c679576680fab3cda2b15222f5/fabric_quick_setup/cli.py#L69 (nice)
    installers = requests.get('https://meta.fabricmc.net/v2/versions/installer').json()
    download = requests.get(installers[0]['url'])
    file_path = TEMP_FOLDER + download.url.split('/')[-1]
    
    text_update(f'Downloading Fabric ({int(download.headers["Content-Length"])//1000} KB)...', widget)
    open(file_path, 'wb').write(download.content)
    
    return file_path

def install_fabric(installer_jar: str, mc_version: str, mc_dir: str, widget=None) -> None: # installs the Fabric launcher jar
    text_update('Installing Fabric...', widget)
    ran = command(f'{get_java()} -jar {installer_jar} client -mcversion {mc_version} -dir {mc_dir}')
    
    if ran == 0:
        text_update(f'Installed Fabric {mc_version}', widget, 'success')
    else:
        text_update(f'Could not install Fabric: {ran}', widget, 'error')

def download_pack(widget=None):
    text_update(f'Fetching Pack...', widget)

    pack_json = requests.get('https://api.github.com/repos/Fabulously-Optimized/fabulously-optimized/releases/latest').json()
    pack_file = ''

    for asset in pack_json['assets']:
        url = asset['browser_download_url']
        if 'MultiMC' in url:
            pack_file = url
            break
    
    download = requests.get(pack_file)
    text_update(f'Downloading Pack ({int(download.headers["Content-Length"])//1000} KB)...', widget)
    file_path = TEMP_FOLDER + pack_file.split('/')[-1]
    
    open(file_path, 'wb').write(download.content)
    return file_path

def install_pack(zip_file: str, widget=None):
    os.makedirs(f'{get_dir()}/', exist_ok=True)
    zipfile.ZipFile(zip_file).extractall()

def run(widget=None) -> None:
    """Starts the installation process.
    """
    text_update('Starting Fabric Download...', widget)
    installer_jar = download_fabric(widget=widget)
    
    text_update('Starting Fabric Installation...', widget)
    install_fabric(installer_jar=installer_jar, mc_version=newest_version(), mc_dir=get_dir(), widget=widget)
    
    text_update('Starting Pack Download...', widget)
    pack_zip = download_pack(widget)

    text_update('Starting Pack Installation...', widget)
    install_pack(zip_file=pack_zip, widget=widget)

def start_log():
    logging.basicConfig(
        filename='logs/main.log',
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG
    )

    logging.info('Starting VanillaInstaller')
    logger = logging.getLogger('VanillaInstaller')

init() # start initialization
start_log() # start logging in case of issues

if __name__ == '__main__':
    gui.run()