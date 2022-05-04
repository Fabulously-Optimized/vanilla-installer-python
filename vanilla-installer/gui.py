# IMPORTS
import os
import sys
import tkinter
import logging
import argparse
import webbrowser
import tkinter.messagebox
import minecraft_launcher_lib

from tkinter import filedialog # otherwise, this is not working properly for some reason

# LOCAL
import main
import theme

PATH_FILE = 'data/mc-path.txt'

if not os.path.exists(PATH_FILE):
    try:
        path = minecraft_launcher_lib.utils.get_minecraft_directory()
    except Exception as e: # any error could happen, really.
        logging.error(f'Could not get Minecraft path: {e}')
        open(PATH_FILE, 'w').write('') # empty file
    else:
        open(PATH_FILE, 'w').write(path)

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument('--safegui', type=bool)
parser.add_argument('--litegui', type=bool)
args = parser.parse_args()

font = 'Yu Gothic UI' if os.name == 'nt' else 'URW Gothic' 

if args.litegui:
    win = tkinter.Tk()
else:
    win = tkinter.Tk(baseName='VanillaInstaller', className='VanillaInstaller')
    #win.wm_attributes('-type', 'splash')

win.title('🧰 Fabulously Optimized · VanillaInstaller')
win.config(bg=theme.load()['bg'])

if not args.safegui:
    win.geometry('500x400')
    win.minsize(500, 400) 
    win.maxsize(500, 400) 

win.iconphoto(False, tkinter.PhotoImage(file='media/icon.png'))

# ============================================================

action_row = tkinter.Frame(win, width=400, relief='flat', bd=0, bg=theme.load()['bg'], background=theme.load()['bg'], borderwidth=0)
action_row.pack()

# Theme Switch
tkinter.Button(action_row,
    fg=theme.load()['fg'],
    bg=theme.load()['dark'],
    text='Dark Theme' if theme.is_dark() else 'Light Theme',
    font=(font, 20),
    relief='flat',
    command=theme.toggle,
    borderwidth=0,
    highlightthickness=0,
    activeforeground=theme.load()['fg'],
    activebackground=theme.load()['accent']
).pack(side='left')

def info():
    """Opens the info website
    """
    webbrowser.open('https://github.com/Fabulously-Optimized/vanilla-installer/blob/main/README.md')

# Info Button
tkinter.Button(action_row,
    fg=theme.load()['accent'],
    bg=theme.load()['dark'],
    text='Info',
    font=(font, 20),
    relief='flat',
    command=info,
    borderwidth=0,
    highlightthickness=0,
    activeforeground=theme.load()['fg'],
    activebackground=theme.load()['accent']
).pack(side='left')

# Exit
tkinter.Button(action_row,
    fg=theme.load()['critical'],
    bg=theme.load()['dark'],
    text='Exit',
    font=(font, 20),
    relief='flat',
    command=sys.exit,
    borderwidth=0,
    highlightthickness=0,
    activeforeground=theme.load()['fg'],
    activebackground=theme.load()['accent']
).pack(side='left')

# Title Label
title_label = tkinter.Label(win,
    fg=theme.load()['fg'],
    bg=theme.load()['bg'],
    text='VanillaInstaller',
    font=(font, 30, 'bold'),
    pady=20,
    relief='flat',
    borderwidth=0,
)
title_label.pack()

# Minecraft path label
path_label = tkinter.Label(win,
    fg=theme.load()['accent'],
    bg=theme.load()['bg'],
    text='cd/fontejd/',
    font=(font, 20),
    pady=10,
    relief='flat',
    borderwidth=0,
)
path_label.pack()

# Changing the Minecraft path
def display_path():
    path_label['text'] = open(PATH_FILE).read()

def path_selection():
    path = filedialog.askdirectory(initialdir='/',title="Select Minecraft path")
    
    if isinstance(path, str): # avoid errors with tuples
        open(PATH_FILE, 'w').write(path)
    
    display_path()

path_button = tkinter.Button(win,
    fg=theme.load()['fg'],
    bg=theme.load()['dark'],
    text='Change Minecraft Path',
    font=(font, 20),
    relief='flat',
    command=path_selection,
    highlightthickness=0,
    borderwidth=0,
    activeforeground=theme.load()['fg'],
    activebackground=theme.load()['accent']
)
path_button.pack()

def run():
    """Starts the installer.
    """
    title_label['font'] = (font, 20, 'italic')
    title_label['text'] = 'Preparing...'
    path_label.destroy()
    path_button.destroy()
    run_button.destroy()
    
    main.run(widget=title_label)

run_button = tkinter.Button(win,
    fg=theme.load()['bg'],
    bg=theme.load()['ok'],
    text='RUN',
    pady=10,
    font=(font, 26, 'bold'),
    relief='flat',
    command=run,
    highlightthickness=0,
    borderwidth=0,
    activeforeground=theme.load()['fg'],
    activebackground=theme.load()['accent']
)
run_button.pack()

display_path()
win.mainloop()