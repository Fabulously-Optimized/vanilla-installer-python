# IMPORTS
import os
import sys
import tkinter
import argparse
import tkinter.messagebox

# LOCAL
import theme

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

# Title Label
tkinter.Label(win,
    fg=theme.load()['fg'],
    bg=theme.load()['bg'],
    text='VanillaInstaller',
    font=(font, 30, 'bold'),
    pady=10,
    relief='flat',
    borderwidth=0,
).pack()

# Theme Switch
tkinter.Button(win,
    fg=theme.load()['accent'],
    bg=theme.load()['dark'],
    text='Dark Mode' if theme.is_dark() else 'Light Mode',
    font=(font, 24),
    relief='flat',
    command=theme.toggle,
    borderwidth=0,
    highlightthickness=0,
    activeforeground=theme.load()['fg'],
    activebackground=theme.load()['accent']
).pack(side='left')

# Cancel Button
tkinter.Button(win,
    fg=theme.load()['critical'],
    bg=theme.load()['dark'],
    text='Cancel',
    font=(font, 24),
    relief='flat',
    command=sys.exit,
    borderwidth=0,
    highlightthickness=0,
    activeforeground=theme.load()['fg'],
    activebackground=theme.load()['accent']
).pack(side='left')


win.mainloop()