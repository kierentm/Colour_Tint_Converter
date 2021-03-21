import tkinter as tk
from tkinter import ttk
import webcolors


def rbg_2_hex():
    r = int(R_spin.get())
    g = int(G_spin.get())
    b = int(B_spin.get())
    print(r, g, b)
    print(webcolors.rgb_to_hex((r, g, b)))


window = tk.Tk()
window.title("Colour Picker")
window.geometry('300x500')

tab_control = ttk.Notebook(window)

main = ttk.Frame(tab_control)
settings = ttk.Frame(tab_control)
hotkeys = ttk.Frame(tab_control)
about = ttk.Frame(tab_control)

tab_control.add(main, text='Main')
tab_control.add(settings, text='Settings')
tab_control.add(hotkeys, text='Hotkeys')
tab_control.add(about, text='About')

tab_control.pack(expand=1, fill='both')

rbg_label = tk.Label(main, text="RGB", font=("Arial Bold", 10))
rbg_label.grid(column=0, row=1)

R_spin = tk.Spinbox(main, from_=0, to=255, width=5)
R_spin.grid(column=0, row=2)

G_spin = tk.Spinbox(main, from_=0, to=255, width=5)
G_spin.grid(column=1, row=2)

B_spin = tk.Spinbox(main, from_=0, to=255, width=5)
B_spin.grid(column=2, row=2)

rgb_convert = tk.Button(main, text="Convert", command=rbg_2_hex)
rgb_convert.grid(column=3, row=2)

window.wm_attributes("-topmost", 1)
window.mainloop()
