import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from convert import nonlinearsrgbtolinear
import webcolors
import webbrowser
from configparser import ConfigParser

# TODO: Currently setting root geometry twice

root = tk.Tk()
#  root.geometry("400x400")

root.title("Colour Tint Converter")
root.geometry('450x400')

# Initialise Tab Parent Notebook
tab_parent = ttk.Notebook(root)

# Define Tabs - MAIN TABS TO REFERENCE
home_frame = ttk.Frame(tab_parent, borderwidth=5, relief="groove")
settings_frame = ttk.Frame(tab_parent, borderwidth=5, relief="groove")
hotkeys_frame = ttk.Frame(tab_parent, borderwidth=5, relief="groove")
about_frame = ttk.Frame(tab_parent, borderwidth=5, relief="groove")
btn_frame_left = ttk.Frame(home_frame, borderwidth=5, relief="groove")
btn_frame_right = ttk.Frame(home_frame, borderwidth=5, relief="groove")

# Add Tabs to Tab Parent
tab_parent.add(home_frame, text="Home")
tab_parent.add(settings_frame, text="Settings")
tab_parent.add(hotkeys_frame, text="Hotkeys")
tab_parent.add(about_frame, text="About")

# Pack Tabs into Layout
tab_parent.pack(expand=1, fill="both")

# Load Config
config = ConfigParser()

config.read('config.ini')

if not config.has_section('main'):
    config.add_section('main')
    with open('config.ini', 'w') as f:
        config.write(f)


# TODO: Toggle Dark mode

# TODO: Add hotkeys (update all colours, toggle keep on top .etc)

# TODO: Add Comments
# TODO: Add program icon
# TODO: Make text white when all three numbers are below 0.1 (practically black)
# TODO: Figure out if entry boxes can have grey text label when nothing is in the box
# TODO: Add colour picker tool

class Home:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.btn = tk.Button(home_frame, text="Add Entry", width=5, command=add_frame)
        self.btn2 = tk.Button(home_frame, text="Export .txt", command=filewrite)

        self.btn.pack(side="bottom", fill=tk.X)
        self.btn2.pack(side="bottom", fill=tk.X)

        root.bind('<KeyPress>', on_key_press)

    def my_function(self):
        pass


class About:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        # Add content to about frame
        self.AboutContent = tk.Label(self.master, text="Tool developed by Kieren Townley-Moss,"
                                                       " Jake Broughton and "
                                                       "Alex Todd")
        self.github = tk.Label(self.master, text="Github", fg="blue", cursor="hand2")

        self.AboutContent.grid(column=0, row=0, sticky='w')
        self.github.grid(column=0, row=1, sticky='w')

        self.github.bind("<Button-1>", lambda e: self.github_click("https://github.com/kierentm/Colour_Tint_Converter"))

    def github_click(self, url):
        webbrowser.open_new(url)


class Settings:
    on_top_var = tk.IntVar()
    dark_mode = tk.IntVar()
    dummy1 = tk.IntVar()
    dummy2 = tk.IntVar()
    directory = tk.StringVar

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.save_button = tk.Button(self.master, text="Save", width=10, command=self.update_settings)

        self.label_frame = tk.LabelFrame(self.master, text="Visual")
        self.hotkey_frame = tk.LabelFrame(self.master, text="Hotkeys")

        self.on_top = tk.Checkbutton(self.label_frame, text="Keep window on top", variable=Settings.on_top_var)
        self.dark_mode = tk.Checkbutton(self.label_frame, text="Dark Mode", variable=Settings.dark_mode)

        self.hotkey1 = tk.Checkbutton(self.hotkey_frame, text="Dummy 1", variable=Settings.dummy1)
        self.hotkey2 = tk.Checkbutton(self.hotkey_frame, text="Dummy 2", variable=Settings.dummy2)

        self.directory_button = tk.Button(self.master, text="Select Save Location", command=self.getFilepast)


        #.label_frame.grid(column=0, row=0, sticky='w')
        self.label_frame.grid(column=0, row=0, sticky='w', pady=5)
        self.hotkey_frame.grid(column=0, row=1, sticky='w', pady=5)
        self.on_top.grid(column=0, row=1, sticky='w')
        self.dark_mode.grid(column=0, row=2, sticky='w')
        self.hotkey1.grid(column=0, row=1, sticky='w')
        self.hotkey2.grid(column=0, row=2, sticky='w')
        self.directory_button.grid(column=0, row=3, sticky='w')
        self.save_button.grid(column=0, row=10, sticky='w')


    def update_settings(self):
        root.attributes('-topmost', Settings.on_top_var.get())
        print(Settings.on_top_var.get())
        print(Settings.dark_mode.get())

    def getFilepast(self):
        # open dialog box to select file
        self.pathpast = filedialog.askdirectory(initialdir="/", title="Select Directory")
        config.set('main', 'SaveLocation', self.pathpast)
        with open('config.ini', 'w') as f:
            config.write(f)
        print(f"From within function = {self.pathpast}")


# Class to generate placeholder objects
class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="_", color='grey', font="Calibri"):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self.font = font

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


# Class to generate tint frame objects
class RemovableTint(tk.Frame):
    instances = []

    # TODO: Refactor some names (eg. spin)

    def __init__(self, parent_frame):
        # Adds instance to list of instances
        RemovableTint.instances.append(self)

        # TODO: Remove redundant self. tags
        # Initialise all entry boxes and buttons
        tk.Frame.__init__(self, parent_frame, height=5, pady=1)
        self.hex_entry_var = tk.StringVar()
        self.colour_tint_name = EntryWithPlaceholder(self, "Colour Name")
        self.r_spin = EntryWithPlaceholder(self, "0")
        self.g_spin = EntryWithPlaceholder(self, "0")
        self.b_spin = EntryWithPlaceholder(self, "0")
        self.hex_spin = tk.Entry(self, width=8, font="Calibri", textvariable=self.hex_entry_var, state="disabled")
        self.colour_spin = tk.Entry(self, width=4)
        self.remove = tk.Button(self, font="Calibri", text="X", command=self.remove)

        # Resize widgets (workaround to sizing bug)
        self.r_spin.config(width=4)
        self.g_spin.config(width=4)
        self.b_spin.config(width=4)
        self.hex_spin.config(width=8)

        # Set the cursor to the name box when initializing a tint frame
        self.colour_tint_name.focus_set()

        self.colour_tint_name.pack(fill="both", side="left", expand=True)
        self.r_spin.pack(fill="both", side="left")
        self.g_spin.pack(fill="both", side="left")
        self.b_spin.pack(fill="both", side="left")
        self.hex_spin.pack(fill="both", side="left")
        self.colour_spin.pack(fill="both", side="left")
        self.remove.pack(fill="both", side="left")
        # TODO: Create box with colour next to hex value (to prevent text becoming unreadable)

        # Bind both tab and left click to
        self.r_spin.bind("<Tab>", self.focus_change)
        self.g_spin.bind("<Tab>", self.focus_change)
        self.b_spin.bind("<Tab>", self.focus_change)

        self.r_spin.bind("<Button-1>", self.focus_change)
        self.g_spin.bind("<Button-1>", self.focus_change)
        self.b_spin.bind("<Button-1>", self.focus_change)

    # Get hex value and update colour
    def hex_conversion(self):
        # Try to convert the values
        try:
            r_nonlin = float(self.r_spin.get())
            g_nonlin = float(self.g_spin.get())
            b_nonlin = float(self.b_spin.get())
            rgb_nonlin = (r_nonlin, g_nonlin, b_nonlin)
            rgb_linear = nonlinearsrgbtolinear(rgb_nonlin)
            hexvals = webcolors.rgb_to_hex(rgb_linear)
            self.hex_entry_var.set(hexvals.upper())
            # self.hex_spin.config({"background": self.hex_spin.get()}) Adds colour to main box
            self.colour_spin.config({"background": self.hex_spin.get()})  # Adds colour to side box
        except ValueError:
            # print("One box still empty?")
            pass

    def focus_change(self, *args):
        self.hex_conversion()

    # Remove current instance from list and visualisation
    def remove(self):
        RemovableTint.instances.remove(self)
        self.destroy()
        # print(self.instances)

    # Remove bottom most instance
    def delete_last(self):
        self.destroy()
        RemovableTint.instances.remove(self)


# Add frame instance (dynamic addition of widgets)
def add_frame():
    RemovableTint(home_frame).pack(fill=tk.X)
    # print(RemovableTint.instances)


def filewrite():
    file1 = open(f"{config.get('main', 'SaveLocation')}" + "/Text" + "_Colors.txt", "w+")
    item_name = "Item_Name"
    file1.write(item_name + "\n\n")
    colour_area = "Colours for the\n\n"

    print(f"From config in file write {config.get('main', 'SaveLocation')}")

    # TODO: figure out how to make it print the colour area when it changes, not every single time (it will be an entry column soon)
    for i in RemovableTint.instances:
        file1.write(colour_area.capitalize())
        file1.write(f"{i.colour_tint_name.get().capitalize()}\n")
        file1.write(f" R = {float(i.r_spin.get())}\n")

        file1.write(f" B = {float(i.g_spin.get())}\n")
        file1.write(f" G = {float(i.b_spin.get())}\n")
        file1.write(f"  {i.hex_spin.get()}\n")

    item_name = ""

    # L = [item_name+"\n", "R = 0.1\n", "G = 0.1\n", "B = 0.1\n", "#FFFFFF"]
    # file1.writelines(L)
    file1.close()
    webbrowser.open(f"{config.get('main', 'SaveLocation')}/Text_Colors.txt")


# Setting up global key binds
def on_key_press(event):
    # Enter key
    if event.keycode == 13:
        add_frame()
        RemovableTint.hex_conversion(RemovableTint.instances[-1])
    # Escape key
    if event.keycode == 27:
        # Delete last tint frame instance
        RemovableTint.instances[-1].delete_last()
        print(RemovableTint.instances)
    # Print keypress for debugging
    # print(f"Key Press - char:{event.keycode}, readable: {event.char}")


# TODO: Choose output file

# TODO: Add Column names
def main():
    Settings(settings_frame)
    About(about_frame)
    Home(home_frame)
    root.mainloop()


if __name__ == "__main__":
    main()
