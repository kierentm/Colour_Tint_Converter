import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

root = tk.Tk()

root.title("Colour Tint Converter")
root.geometry('450x400')


class PathyThing:
    def __init__(self):
        self.browsebutton2 = tk.Button(root, text="Select Save Location", command=self.getFilepast)
        self.browsebutton2.grid(row=0, column=1)
        # etc.

    def getFilepast(self):
        # open dialog box to select file
        PathyThing.pathpast = filedialog.askdirectory(initialdir="/", title="Select Directory")


pathy = PathyThing()


class FileStuff(PathyThing):
    def __init__(self):
        self.writebutton = tk.Button(root, text="Print Hello World", command=self.writehello)
        self.writebutton.grid(row=0, column=2)

    def writehello(self):
        file1 = open(f"{PathyThing.pathpast}/test.txt", "w+")
        file1.write("Hello World1")
        file1.close()


filey = FileStuff()

# def file_location():
#     location = filedialog.askdirectory()
#     return location

root.wm_attributes("-topmost", 1)
root.mainloop()