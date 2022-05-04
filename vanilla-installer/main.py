import logging
import requests

def text_update(widget, text):
    if widget:
        widget['text'] = text
    else:
        logging.info(text)

def download_fabric(widget=None): # https://github.com/max-niederman/fabric-quick-setup/blob/40c959c6cd2295c679576680fab3cda2b15222f5/fabric_quick_setup/cli.py#L69 (nice)
    installers = requests.get('https://meta.fabricmc.net/v2/versions/installer').json()
    download = requests.get(installers[0]['url'])
    file_name = download.url.split('/')[-1]
    
    text_update(widget, f'Downloading Fabric ({int(download.headers["Content-Length"])//1000} KB)...')
    open(file_name, 'wb').write(download.content)
    
    return file_name

def install_fabric():
    f'java -jar {installer_path} server -snapshot -mcversion {mc_version} -dir {mc_dir}'


def run(widget=None):
    """Starts the installation process.
    """
    text_update(widget, 'Downloading Fabric...')
    download_fabric(widget=widget)
    # text_update(widget, '')