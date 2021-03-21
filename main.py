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
window.title("Colour Tint Converter")
window.geometry('350x400')

tab_control = ttk.Notebook()
main = ttk.Frame(tab_control, borderwidth=5)
main_content_1 = ttk.Frame(main, borderwidth=10, relief="groove")
main_content_2 = ttk.Frame(main, borderwidth=10, relief="groove")
settings = ttk.Frame(tab_control)

about = ttk.Frame(tab_control)

tab_control.add(main, text='Main')
main_content_1.grid(column=1, row=2)
main_content_2.grid(column=1, row=0)

tab_control.add(settings, text='Settings')

tab_control.add(about, text='About')

tab_control.pack(expand=1, fill='both')

#Testing Item Name
ItemNameLabel = tk.Label(main_content_2, text="ItemName")
ItemNameLabel.grid(column=0,row=2)
Item_Name_Entry = tk.Entry(main_content_2, width =24)
Item_Name_Entry.grid(column=1, row=2)

#name field

Colour_Tint_Name = tk.Entry(main_content_1, width =24)
Colour_Tint_Name.grid(column=1, row=2)

#Red green and blue field

R_spin = tk.Entry(main_content_1, width =4)
R_spin.grid(column=2, row=2)


G_spin = tk.Entry(main_content_1, width =4)
G_spin.grid(column=3, row=2)


B_spin = tk.Entry(main_content_1, width =4)
B_spin.grid(column=4, row=2)

#auto convert hex field

Hex_spin = tk.Entry(main_content_1, width =10)
Hex_spin.grid(column=5, row=2)

#drop down box

Drop_Down = ["Mult","Add"]
Drop_Down_Variable = tk.StringVar(window)
Drop_Down_Variable.set(Drop_Down[0])

opt = tk.OptionMenu(window, Drop_Down_Variable, *Drop_Down)
opt.pack()

#rgb_convert = tk.Button(main, text="Convert", command=rbg_2_hex)
#rgb_convert.grid(column=4, row=2)


window.wm_attributes("-topmost", 1)
window.mainloop()
