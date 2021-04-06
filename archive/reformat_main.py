# ---- Imports ---- #
import tkinter as tk
from tkinter import ttk
# from tkinter import filedialog
from convert import *
from PIL import ImageGrab
import webcolors
import webbrowser
from configparser import ConfigParser
import pathlib

# ---- Software-wide variables ---- #
root = tk.Tk()

# Colour Variables
btn_clr = "#393a40"  # button colour
btn_clr_act = "#57a337"  # button colour when clicked
btn_fg = "#ffffff"  # button font colour
btn_font = "Calibri", "16"
bg_clr = "#2f3136"  # background colour

plus_ico = tk.PhotoImage(file="../UI_Images/Plus_Ico_Dark_Mode.png")
pipette_ico = tk.PhotoImage(file="../UI_Images/Pipette_Ico_Dark_Mode.png")
export_ico = tk.PhotoImage(file="../UI_Images/Txt_Ico_Dark_Mode.png")


# ---- Main Loop ---- #
def main():

    p1 = tk.PhotoImage(file='../Design Images/CTC.png')
    root.iconphoto(False, p1)

    root.title("Colour Tint Master")
    root.geometry('450x500')

    # Initialise Tab Parent Notebook
    tab_parent = ttk.Notebook(root)

    # Define Tabs - MAIN TABS TO REFERENCE
    home_frame = ttk.Frame(tab_parent, borderwidth=5, relief="groove")
    settings_frame = ttk.Frame(tab_parent, borderwidth=5, relief="groove")
    hotkeys_frame = ttk.Frame(tab_parent, borderwidth=5, relief="groove")
    about_frame = ttk.Frame(tab_parent, borderwidth=5, relief="groove")

    # Add Tabs to Tab Parent
    tab_parent.add(home_frame, text="Home")
    tab_parent.add(settings_frame, text="Settings")
    tab_parent.add(hotkeys_frame, text="Hotkeys")
    tab_parent.add(about_frame, text="About")

    # Pack Tabs into Layout
    tab_parent.pack(expand=1, fill="both")

    # Load Config and generate main if required
    config = ConfigParser()

    config.read('config.ini')

    if not config.has_section('main'):
        config.add_section('main')
        config.set('main', 'SaveLocation', f'{pathlib.Path().absolute()}')
        with open('../config.ini', 'w') as f:
            config.write(f)

    Settings(settings_frame)
    About(about_frame)
    Home(home_frame)
    root.mainloop()


# -------------------- Home Tab -------------------- #
class Home:

    # ---- Basic Layout ---- #
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.image = None
        self.tracer_win = None

        # Create Entry and Colour Frame
        self.entry_frame = tk.Frame(self.master, bg=bg_clr)

        self.entry_btn = tk.Button(self.entry_frame, image=plus_ico, bg=btn_clr, activebackground=btn_clr_act,
                                   fg=btn_fg, bd="3", height="22", text="New Entry", compound="left",
                                   command=self.add_frame, font=btn_font)
        self.divider = tk.Label(self.entry_frame, bg=bg_clr, width="0", padx="1")
        self.colour_btn = tk.Button(self.entry_frame, image=pipette_ico, bg=btn_clr, activebackground=btn_clr_act,
                                    fg=btn_fg, height="22", text="New Colour", compound="left", command=self.screenshot,
                                    font=btn_font)
        # Create Export Frame
        self.export_frame = tk.Frame(self.master, bg=bg_clr)
        self.export_btn = tk.Button(self.export_frame, image=export_ico, bg=btn_clr,
                                    activebackground=btn_clr_act, bd="3", height="24", text="Export .txt",
                                    compound="left", command=self.file_write, fg=btn_fg)
        self.export_name = EntryWithPlaceholder(self.export_frame, "Item Name")

        # Pack the stuff
        self.entry_frame.pack(side="top", fill=tk.X, pady=(0, 5))
        self.entry_btn.pack(side="left", fill=tk.X, expand=True)
        self.divider.pack(side="left")
        self.colour_btn.pack(side="left", fill=tk.X, expand=True)
        self.export_frame.pack(side="bottom", fill=tk.X)
        self.export_btn.pack(side="right")
        self.export_name.pack(fill="both", side="left", expand=True)

    # ---- Main Functions ---- #
    def add_frame(self, rgb=None, is_screenshot=False):

        RemovableTint(self.master, rgb, is_screenshot).pack(fill=tk.X)
        RemovableTint.hex_conversion(RemovableTint.instances[-1])
        pass

    # ---- File Saving ---- #
    def file_write(self):
        pass

    # ---- Screenshot ---- #
    def screenshot(self):
        self.image = ImageGrab.grab()  # Takes screenshot of whole screen
        self.tracer_win = tk.Toplevel(self.master)  # To make top level
        self.tracer_win.attributes("-fullscreen", True)  # Full screen
        self.tracer_win.overrideredirect(1)
        self.tracer_win.attributes('-alpha', 0.3)  # Sets transparency
        self.tracer_win.attributes('-topmost', True)  # Keeps on top
        self.tracer_win.bind("<Button-1>", self.capture)  # Binds left click to run capture

    def capture(self, event):  # Auto pass in event details (clicking)
        print(event)
        x, y = event.x, event.y
        self.tracer_win.destroy()  # Destroys grey window

        self.image = self.image.crop((x - 1, y - 1, x + 1, y + 1))  # Crops image to 2 x 2 box
        self.image = self.image.convert('RGB')  # Converts to RGB8
        # self.image.save("screenshot.png")
        rgb_tuple = self.image.getpixel((1, 1))  # Gets SRGB8 of centre pixel
        lsrgb_tuple = RGB8toLSRGB(rgb_tuple)  # Convert RBG8 to SRGB [0,1]
        lsrgb_tuple = [round(num, 3) for num in lsrgb_tuple]  # Round Tuple
        self.add_frame(lsrgb_tuple, True)  # Sends RBG values to add_frame


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="_", color='grey', font="Calibri", *args, **kwargs):
        super().__init__(master, *args, **kwargs)

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
        print(args)
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        print(args)
        if not self.get():
            self.put_placeholder()


class RemovableTint(tk.Frame):
    instances = []

    # TODO: Refactor some names (eg. spin)
    # Passed in is screenshot from add_frame
    def __init__(self, master, rgb=None, hex_code=None, is_screenshot=False, **kw):
        master.bind('<Enter>', self.key_binds)
        # Adds instance to list of instances
        super().__init__(self, master, height=5, pady=1, **kw)
        RemovableTint.instances.append(self)
        self.hex_code = hex_code
        self.is_screenshot = is_screenshot
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]

        # Create variables for r, g and b entry boxes
        self.r_contents = tk.StringVar()
        self.g_contents = tk.StringVar()
        self.b_contents = tk.StringVar()

        self.hex_entry_var = tk.StringVar()
        self.colour_tint_name = EntryWithPlaceholder(self, "Colour Name")

        self.r_spin = EntryWithPlaceholder(self, str(self.r), width=5, color='grey', textvariable=self.r_contents)
        self.g_spin = EntryWithPlaceholder(self, str(self.g), width=5, color='grey', textvariable=self.g_contents)
        self.b_spin = EntryWithPlaceholder(self, str(self.b), width=5, color='grey', textvariable=self.b_contents)

        self.hex_spin = tk.Entry(self, width=8, font="Calibri", textvariable=self.hex_entry_var, state="disabled")
        self.hex_spin.bind('<1>', lambda event: self.hex_spin.focus_set())
        self.colour_spin = tk.Label(self, width=4, background="black", relief="ridge")
        self.remove = tk.Button(self, font="Calibri", text="X", command=self.remove)

        # Set the cursor to the name box when initializing a tint frame
        self.colour_tint_name.focus_set()

        # Pack buttons into frame
        self.colour_tint_name.pack(fill="both", side="left", expand=True)
        self.r_spin.pack(fill="both", side="left")
        self.g_spin.pack(fill="both", side="left")
        self.b_spin.pack(fill="both", side="left")
        self.hex_spin.pack(fill="both", side="left")
        self.colour_spin.pack(fill="both", side="left")
        self.remove.pack(fill="both", side="left")

        # Trace r,g, b entry box variables, running value_change when they change
        self.r_contents.trace('w', self.value_change)
        self.g_contents.trace('w', self.value_change)
        self.b_contents.trace('w', self.value_change)

    def value_change(self, *args):
        print(args)
        self.hex_conversion()

    def hex_conversion(self):
        try:
            r_nonlin = float(self.r_spin.get())
            g_nonlin = float(self.g_spin.get())
            b_nonlin = float(self.b_spin.get())
            rgb_nonlin = (r_nonlin, g_nonlin, b_nonlin)
            rgb_linear = LSRGBtoSRGB8(rgb_nonlin)
            hexvals = webcolors.rgb_to_hex(rgb_linear)
            self.hex_entry_var.set(hexvals.upper())
            # self.hex_spin.config({"background": self.hex_spin.get()}) Adds colour to main box
            self.colour_spin.config({"background": self.hex_spin.get()})  # Adds colour to side box
        except ValueError:
            # print("One box still empty?")
            pass

    @staticmethod
    def key_binds(self, event):
        if event.keycode == 13:
            self.add_frame()
        # Escape key
        if event.keycode == 27:
            # Delete last tint frame instance
            RemovableTint.instances[-1].delete_last()
            print(RemovableTint.instances)


# -------------------- Settings Tab -------------------- #
class Settings:
    def __init__(self, master):
        self.master = master


# -------------------- Hotkeys Tab -------------------- #
class Hotkeys:
    def __init__(self, master):
        self.master = master


# -------------------- About Tab -------------------- #
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

    @staticmethod
    def github_click(url):
        webbrowser.open_new(url)


# ---- Main Loop ---- #
if __name__ == '__main__':
    main()
