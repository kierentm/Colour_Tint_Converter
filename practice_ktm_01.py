import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

root = tk.Tk()

root.title("Colour Tint Converter")
root.geometry('450x400')

FrameTopButton = tk.Frame(root, bd="10")

plus_i = tk.PhotoImage(file="UI_Images\Plus_Icon_Test4.png")
pipette_i = tk.PhotoImage(file="UI_Images\Pipette_Icon4.png")

Button1 = tk.Button(FrameTopButton, image=plus_i, bg="#393a40", activebackground="#212124", bd="3")
Button1.pack(side="left", fill=tk.X, expand=True)

Button2= tk.Button(FrameTopButton, image=pipette_i, fg="#00ff00", bg="#393a40", activebackground="#212124", bd="3")
Button2.pack(side="left", fill=tk.X, expand=True)

FrameTopButton.pack(side="top", fill=tk.X, expand=True)

root.wm_attributes("-topmost", 1)
root.mainloop()