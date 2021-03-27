import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

root = tk.Tk()

root.title("Colour Tint Converter")
root.geometry('450x400')

entry_frame = tk.Frame(root, bd="10")

plus_ico = tk.PhotoImage(file="UI_Images\Plus_Icon_Test4.png")
pipette_ico = tk.PhotoImage(file="UI_Images\Pipette_Icon4.png")

entry_btn = tk.Button(entry_frame, image=plus_ico, bg="#393a40", activebackground="#212124", bd="3", command=add_frame)
entry_btn.pack(side="left", fill=tk.X, expand=True)

colour_btn= tk.Button(entry_frame, image=pipette_ico, fg="#00ff00", bg="#393a40", activebackground="#212124", bd="3")
Button2.pack(side="left", fill=tk.X, expand=True)

entry_frame.pack(side="top", fill=tk.X, expand=True)

root.wm_attributes("-topmost", 1)
root.mainloop()