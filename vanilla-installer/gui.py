# IMPORTS
import os
import tkinter
import tkinter.messagebox

# LOCAL
import theme

font = 'Yu Gothic UI' if os.name == 'nt' else 'URW Gothic' 
print(font)

win = tkinter.Tk()
win.title('🧰 Fabulously Optimized · VanillaInstaller')
win.config(bg=theme.load()['bg'])
win.geometry('500x400')

win.iconphoto(False, tkinter.PhotoImage(file='media/icon.png'))

tkinter.Button(win, text='🌑 Theme' if theme.is_dark() else '☀️ Theme',
    relief='flat',
    command=theme.toggle,
    fg=theme.load()['fg'],
    bg=theme.load()['bg'],
    font=(font, 30, 'bold'),
    activeforeground=theme.load()['fg'],
    activebackground=theme.load()['light']
).pack(side='left')

win.mainloop()