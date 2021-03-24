import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("400x400")

root.title("Colour Tint Converter")
root.geometry('450x400')

# # Tab Initialization
# tab_control = ttk.Notebook()
# main = ttk.Frame(tab_control, borderwidth=5)
#
# # Tab Setup
# main_content = ttk.Frame(main, borderwidth=5, relief="groove")
#
# # Adding Tabs
# tab_control.add(main, text='Main')
#
# # Placing Tab Frames
# main_content.pack(side="bottom", expand="yes", fill='both')
# tab_control.pack(side="bottom", expand="yes", fill='both')

tab_parent = ttk.Notebook(root)

home_tab = ttk.Frame(tab_parent)
settings_tab = ttk.Frame(tab_parent)
about_tab = ttk.Frame(tab_parent)

tab_parent.add(home_tab, text="Home")
tab_parent.add(settings_tab, text="Settings")
tab_parent.add(about_tab, text="About")

tab_parent.pack(expand=1, fill="both")


class RemovableTint(tk.Frame):
    instances = []

    def __init__(self, parent_frame):
        tk.Frame.__init__(self, parent_frame, height=5, pady=1)

        self.colour_tint_name = tk.Entry(self, width=15, font="Calibri")
        self.r_spin = tk.Entry(self, width=4, font="Calibri")
        self.g_spin = tk.Entry(self, width=4, font="Calibri")
        self.b_spin = tk.Entry(self, width=4, font="Calibri")
        self.hex_spin = tk.Entry(self, width=10, font="Calibri")
        self.update = tk.Button(self, text="Update", font="Calibri")
        self.remove = tk.Button(self, font="Calibri",
                                text="X", command=self.destroy)

        self.colour_tint_name.pack(fill="both", side="left", expand=True)
        self.r_spin.pack(fill="both", side="left")
        self.g_spin.pack(fill="both", side="left")
        self.b_spin.pack(fill="both", side="left")
        self.hex_spin.pack(fill="both", side="left")
        self.update.pack(fill="both", side="left")
        self.remove.pack(fill="both", side="left")


def add_frame():
    RemovableTint(home_tab).pack(fill=tk.X)


btn = tk.Button(home_tab, text="Add Entry", width=50, command=add_frame)
btn.pack(side="bottom", fill=tk.X)
home_tab.rowconfigure(0, weight=1)
home_tab.columnconfigure(0, weight=1)
home_tab.mainloop()
