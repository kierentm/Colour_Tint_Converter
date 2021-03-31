import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

root = tk.Tk()

root.title("Colour Tint Converter")
root.geometry('450x400')

entry_frame1 = tk.Frame(root, bd="10", relief="ridge")
entry_frame2 = tk.Frame(root, bd="10", relief="ridge")

label1 = tk.LabelFrame(entry_frame1, text="Visual")




entry_frame1.pack(side="left", fill=tk.X, expand=True)
entry_frame2.pack(side="left", fill=tk.X, expand=True)

root.wm_attributes("-topmost", 1)
root.mainloop()