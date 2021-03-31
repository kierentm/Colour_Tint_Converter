import tkinter as tk
from tkinter import ttk
import webcolors
window = tk.Tk()

def rbg_2_hex():
    r = int(R_spin.get())
    g = int(G_spin.get())
    b = int(B_spin.get())
    print(r, g, b)
    print(webcolors.rgb_to_hex((r, g, b)))

Hex_Entry_Text = tk.StringVar()

def hex_convertion():

    r_value = int(255 * float(R_spin.get()))
    g_value = int(255 * float(G_spin.get()))
    b_value = int(255 * float(B_spin.get()))

    hex_value = webcolors.rgb_to_hex((r_value, g_value, b_value))
    Hex_Entry_Text.set(hex_value)
    print(r_value, g_value, b_value)


window["bg"] = "gray30"
window.title("Colour Tint Converter")
window.geometry('400x400')

tab_control = ttk.Notebook()
main = ttk.Frame(tab_control, borderwidth=5)
main_content_1 = ttk.Frame(main, borderwidth=10, relief="groove")

main_content_2 = ttk.Frame(main, borderwidth=10, relief="groove")
settings = ttk.Frame(tab_control, borderwidth=5)

about = ttk.Frame(tab_control,)

tab_control.add(main, text='Main')
main_content_1.grid(column=1, row=2)
main_content_2.grid(column=1, row=0)

tab_control.add(settings, text='Settings')

tab_control.add(about, text='About')

tab_control.pack(side="left", expand="yes", fill='both')

#Testing Item Name
#ItemNameLabel = tk.Label(main_content_2, text="ItemName")
#ItemNameLabel.grid(column=0,row=2)
#Item_Name_Entry = tk.Entry(main_content_2, width =24)
#Item_Name_Entry.grid(column=1, row=2)

#name field

Colour_Tint_Name = tk.Entry(main_content_1, width =18, bg="gray40", fg="white", font="Calibri")
Colour_Tint_Name.grid(column=1, row=2)

#Red green and blue field


R_spin = tk.Entry(main_content_1, width =4, bg="gray40", fg="white", font="Calibri")
R_spin.grid(column=2, row=2)
R_SV = tk.StringVar()
#R_SV.trace_add("write", hex_convertion())

G_spin = tk.Entry(main_content_1, width =4, bg="gray40", fg="white", font="Calibri")
G_spin.grid(column=3, row=2)


B_spin = tk.Entry(main_content_1, width =4, bg="gray40", fg="white", font="Calibri")
B_spin.grid(column=4, row=2)



Button = tk.Button(main_content_1, width=4, text ="update", command=hex_convertion)
Button.grid(column=6, row=2)

#auto convert hex field

Hex_Value = "#FFFFFF"

Hex_spin = tk.Entry(main_content_1, textvariable=Hex_Entry_Text,width =10, bg=Hex_Value, fg="black", font="Calibri")
Hex_Entry_Text.set(Hex_Value.upper())
Hex_spin.grid(column=5, row=2)









#drop down box

#Drop_Down = ["Mult","Add"]
#Drop_Down_Variable = tk.StringVar(window)
#Drop_Down_Variable.set(Drop_Down[0])

#opt = tk.OptionMenu(tab_control, Drop_Down_Variable, *Drop_Down)
#opt.pack()

#About
AboutL = tk.Label(about, text="Tool developed by Kieren Townley-Moss and Jake Broughton")
AboutL.grid(column=0,row=2)

#Settings
SettingsL = tk.Label(settings, text="Export Location option, always on top option, minimize to tray option")
SettingsL.grid(column=0,row=2)

#rgb_convert = tk.Button(main, text="Convert", command=rbg_2_hex)
#rgb_convert.grid(column=4, row=2)


window.wm_attributes("-topmost", 1)
window.mainloop()
