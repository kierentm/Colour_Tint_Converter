# import tkinter as tk
# from tkinter import ttk
#
# root = tk.Tk()
#
# root.title("Colour Tint Converter")
# root.geometry('450x400')
#
# tab_control = ttk.Notebook()
# main = ttk.Frame(tab_control, borderwidth=5)
# main_content_1 = ttk.Frame(main, borderwidth=10, relief="groove")
#
# tab_control.add(main, text='Main')
# main_content_1.grid(column=1, row=2)
#
# tab_control.pack(side="left", expand="yes", fill='both')
#
# Colour_Tint_Name = tk.Entry(main_content_1, width=18, font="Calibri")
# Colour_Tint_Name.grid(column=1, row=2)
#
# R_SV = tk.StringVar()
#
# class EntryWithPlaceholder(tk.Entry)
#
# root.wm_attributes("-topmost", 1)
# root.mainloop()

import tkinter as tk

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

if __name__ == "__main__":
    root = tk.Tk()
    username = EntryWithPlaceholder(root, "username")
    password = EntryWithPlaceholder(root, "password", 'blue')
    username.pack()
    password.pack()
    root.mainloop()