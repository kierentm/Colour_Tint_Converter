import tkinter as tk
from tkinter.messagebox import showinfo

# --- classes ---

class App():

    def __init__(self, master):
        self.master = master

        button_bonus = tk.Button(master, text="Window", command=self.popup_window)
        button_bonus.pack(fill='x')

        button_showinfo = tk.Button(master, text="ShowInfo", command=self.popup_showinfo)
        button_showinfo.pack(fill='x')

        button_close = tk.Button(master, text="Close", command=master.destroy)
        button_close.pack(fill='x')

    def popup_window(self):
        window = tk.Toplevel()

        label = tk.Label(window, text="Hello World!")
        label.pack(fill='x', padx=50, pady=5)

        button_close = tk.Button(window, text="Close", command=window.destroy)
        button_close.pack(fill='x')

    def popup_showinfo(self):
        showinfo("ShowInfo", "Hello World!")

# --- main ---

root = tk.Tk()
app = App(root)
root.mainloop()
