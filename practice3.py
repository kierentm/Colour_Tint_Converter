import tkinter as tk
from tkinter import ttk
from tkinter import *

root = tk.Tk()

root.title("Colour Tint Converter")
root.geometry('450x400')

tab_control = ttk.Notebook()
settings = ttk.Frame(tab_control, borderwidth=5)
settings_content = ttk.Frame(main, borderwidth=10, relief="groove")

tab_control.add(main, text='Main')
settings_content.grid(column=1, row=2)

tab_control.pack(side="left", expand="yes", fill='both')

Colour_Tint_Name = tk.Entry(settings_content, width=18, font="Calibri")
Colour_Tint_Name.grid(column=1, row=2)

R_SV = tk.StringVar()

img = PhotoImage(file="ball.ppm")
canvas.create_image(20,20, anchor=NW, image=img)

root.wm_attributes("-topmost", 1)
root.mainloop()
