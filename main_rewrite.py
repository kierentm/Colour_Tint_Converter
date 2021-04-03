import pathlib
import tkinter as tk
import webbrowser
from configparser import ConfigParser
from tkinter import filedialog
from tkinter import ttk
import time

import webcolors
from PIL import ImageGrab, ImageTk

from convert import *

root = tk.Tk()
root.geometry("450x500")

# Load Config and generate main if required
config = ConfigParser()
config.read('config.ini')

if not config.has_section('main'):
    config.add_section('main')
    config.set('main', 'SaveLocation', f'{pathlib.Path().absolute()}')
    config.set('main', 'OnTop', '0')
    with open('config.ini', 'w') as file:
        config.write(file)


def main():
    # Initialise Tab Parent Notebook
    tab_parent = ttk.Notebook(root)

    # Initialise home frame
    home = Home(root)
    settings = Settings(root)
    hotkeys = Hotkeys(root)
    about = About(root)

    # Add frames to tabs then pack
    tab_parent.add(home, text="Home")
    tab_parent.add(hotkeys, text="Hotkeys")
    tab_parent.add(about, text="About")
    tab_parent.add(settings, text="Settings")

    tab_parent.pack(expand=1, fill="both")

    # Tk main loop
    root.mainloop()


class Home(tk.Frame):
    # ---- Style Setup ---- #
    btn_clr = "#393a40"  # button colour
    btn_clr_act = "#57a337"  # button colour when clicked
    btn_fg = "#ffffff"  # button font colour
    btn_font = "Calibri", "16"
    bg_clr = "#2f3136"  # background colour

    plus_ico = tk.PhotoImage(file="UI_Images/Plus_Solo_1.png")
    pipette_ico = tk.PhotoImage(file="UI_Images/Pipette_Solo.png")
    export_ico = tk.PhotoImage(file="UI_Images/Txt_Solo.png")

    def __init__(self, parent, *args, **kwargs):

        root.bind('<KeyPress>', self.on_key_press)

        # --- Main frames --- #
        tk.Frame.__init__(self, parent, *args, **kwargs)
        control_frame = tk.Frame(self)

        # --- Controls --- #
        add_button = tk.Button(control_frame, text="Add", command=lambda: Home.RemovableEntry(self))
        remove_button = tk.Button(control_frame, text="Remove", command=lambda: self.remove_entry())
        picker = tk.Button(control_frame, text="Colour Pick", command=lambda: self.screenshot())

        # --- Pack Controls --- #
        add_button.pack(side="left")
        remove_button.pack(side="left")
        picker.pack(side="right")

        # --- Export --- #
        self.export_frame = tk.Frame(self.master)
        self.export_btn = tk.Button(self.export_frame, text="Export .txt",
                                    compound="left", command=self.file_write)
        self.export_name = self.EntryWithPlaceholder(self.export_frame, "Item Name")

        # --- Pack Export --- #
        self.export_frame.pack(side="bottom", fill=tk.X)
        self.export_btn.pack(side="right")
        self.export_name.pack(fill="both", side="left", expand=True)

        # --- Pack frames --- #
        control_frame.pack(side="top", fill=tk.X, pady=(0, 5))
        self.pack(side="top", fill="both", expand=True)

        # --- Declare screenshot variables --- #
        self.image = None
        self.tracer_win = None

    def screenshot(self):
        root.withdraw()
        time.sleep(0.2)
        self.image = ImageGrab.grab()  # Takes screenshot of whole screen

        img = ImageTk.PhotoImage(self.image)

        self.tracer_win = tk.Toplevel(self.master, cursor="cross")  # To make top level
        self.tracer_win.attributes("-fullscreen", True)  # Full screen
        self.tracer_win.overrideredirect(1)
        self.tracer_win.attributes('-alpha', 1)  # Sets transparency
        self.tracer_win.attributes('-topmost', True)  # Keeps on top
        tracer_frame = tk.Frame(self.tracer_win)
        self.tracer_win.bind("<Button-1>", self.capture)  # Binds left click to run capture
        screenshot_bg = tk.Label(self.tracer_win, image=img)
        screenshot_bg.photo = img  # Anchors the image to the object
        screenshot_bg.pack(fill="both", expand=True)

        tracer_frame.pack()

    def capture(self, event):  # Auto pass in event details (clicking)
        x, y = event.x, event.y
        self.tracer_win.destroy()  # Destroys grey window
        self.image = self.image.crop((x - 1, y - 1, x + 1, y + 1))  # Crops image to 2 x 2 box
        self.image = self.image.convert('RGB')  # Converts to RGB8
        # self.image.save("screenshot.png")
        rgb_tuple = self.image.getpixel((1, 1))  # Gets SRGB8 of centre pixel
        rounded = [round(num, 3) for num in rgb_tuple]  # Round Tuple
        red = rounded[0]
        green = rounded[1]
        blue = rounded[2]

        self.RemovableEntry(self, convert_type="sRGB8 [0,255]", r=red, g=green, b=blue,
                            is_screenshot=True)  # Sends RBG values to add_frame
        root.deiconify()

    def remove_entry(self):
        if not len(self.RemovableEntry.instances) == 0:
            Home.RemovableEntry.instances[-1].delete_last()

    # Setting up global key binds
    def on_key_press(self, event):
        # Enter key
        if event.keycode == 13:
            self.RemovableEntry(self)
        # Escape key
        if event.keycode == 27:
            # Delete last tint frame instance
            Home.RemovableEntry.instances[-1].delete_last()
            print(Home.RemovableEntry.instances)

    # ----------------------------- File write Start ----------------------------- #
    def file_write(self):
        file1 = open(f"{config.get('main', 'SaveLocation')}/{self.export_name.get()}_colours_info.txt", "w+")
        item_name = "Item_Name"
        file1.write(item_name + "\n\n")
        # colour_area = "Colours for the\n\n"

        for i in Home.RemovableEntry.instances:
            # file1.write(colour_area.capitalize())
            file1.write(f"{i.entry_name.get().capitalize()}\n")
            file1.write(f"Type: {i.convert_type}\n")
            file1.write(f" R = {ifgreaterthan1(float(i.r_entry.get()))}\n")
            file1.write(f" B = {ifgreaterthan1(float(i.g_entry.get()))}\n")
            file1.write(f" G = {ifgreaterthan1(float(i.b_entry.get()))}\n")
            file1.write(f"  {i.hex_box.get()}\n")

        file1.close()
        webbrowser.open(f"{config.get('main', 'SaveLocation')}/{self.export_name.get()}_colours_info.txt")

    # ----- Class to create and track entries ---- #
    class RemovableEntry(tk.Frame):
        instances = []

        def __init__(self, parent, convert_type="sRGB [0,1]", r=0, g=0, b=0, is_screenshot=False, *args, **kwargs):
            self.convert_type = convert_type

            # ---- Setup ---- #
            tk.Frame.__init__(self, parent, *args, **kwargs)
            Home.RemovableEntry.instances.append(self)

            # ---- Each entry set up here ---- #
            convert_types = [
                "sRGB8 [0,255]",
                "sRGB' [0,1]",
                "sRGB [0,1]"
            ]

            self.type_drop_value = tk.StringVar(self)
            self.type_drop_value.set(self.convert_type)

            type_dropdown = tk.OptionMenu(self, self.type_drop_value, *convert_types)
            type_dropdown.config(width=10)

            self.entry_name = Home.EntryWithPlaceholder(self, width=20, placeholder="Colour Name")

            self.r_value = tk.StringVar()
            self.g_value = tk.StringVar()
            self.b_value = tk.StringVar()
            self.hex_box_value = tk.StringVar()

            self.r_entry = Home.EntryWithPlaceholder(self, width=4, textvariable=self.r_value)
            self.g_entry = Home.EntryWithPlaceholder(self, width=4, textvariable=self.g_value)
            self.b_entry = Home.EntryWithPlaceholder(self, width=4, textvariable=self.b_value)

            self.hex_box = tk.Entry(self, width=10, textvariable=self.hex_box_value)

            self.colour_preview = tk.Entry(self, width=4)

            self.remove_button = tk.Button(self, text="X", command=lambda: self.remove())

            # ---- Remove placeholder functionality if it's a screenshot ---- #
            if is_screenshot:
                self.r_entry.config(fg="black")
                self.g_entry.config(fg="black")
                self.b_entry.config(fg="black")

                self.r_value.set(r)
                self.g_value.set(g)
                self.b_value.set(b)

            # ---- Pack ---- #
            type_dropdown.pack(side="left", fill=tk.Y)
            self.entry_name.pack(side="left", fill=tk.Y)

            self.r_entry.pack(side="left", fill=tk.Y)
            self.g_entry.pack(side="left", fill=tk.Y)
            self.b_entry.pack(side="left", fill=tk.Y)

            self.remove_button.pack(side="right")
            self.colour_preview.pack(side="right", fill=tk.Y)
            self.hex_box.pack(side="right", fill=tk.Y)

            self.pack(side="top", fill=tk.X)

            # ---- Trace Value Change to Update Hex ---- #
            self.r_value.trace('w', self.value_change)
            self.g_value.trace('w', self.value_change)
            self.b_value.trace('w', self.value_change)
            self.type_drop_value.trace('w', self.value_change)

            # ---- Trace Value Change to Update Hex ---- #
            self.entry_name.focus_set()

            # --- Update hex on creation --- #
            self.hex_convert()

        def value_change(self, *args):
            self.hex_convert()

        def hex_convert(self):
            # ---- Fetch values ---- #
            conversion_type = self.type_drop_value.get()
            # entries = [self.r_entry, self.g_entry, self.b_entry]
            get_entries = [self.r_entry.get(), self.g_entry.get(), self.b_entry.get()]

            # for e in entries:
            #     if KierensStupidTest(e.get()):
            #         e.config(background="white")
            #     else:
            #         e.config(background="red")

            # If there is no empty box...
            if '' not in get_entries:

                # Use conversion type...
                # Conversion type sRGB [0,1]
                if conversion_type == "sRGB [0,1]":
                    rgb_nonlin = tuple(map(float, get_entries))
                    rgb_linear = LSRGBtoSRGB8(rgb_nonlin)
                    hexvals = webcolors.rgb_to_hex(rgb_linear)
                    self.hex_box_value.set(hexvals.upper())
                    self.colour_preview.config({"background": self.hex_box.get()})  # Adds colour to side box

                # Conversion type sRGB [0,1]
                if conversion_type == "sRGB8 [0,255]":
                    r_nonlin = int(self.r_entry.get())
                    g_nonlin = int(self.g_entry.get())
                    b_nonlin = int(self.b_entry.get())
                    rgb_nonlin = (r_nonlin, g_nonlin, b_nonlin)

                    hexvals = webcolors.rgb_to_hex(rgb_nonlin)
                    self.hex_box_value.set(hexvals.upper())
                    self.colour_preview.config({"background": self.hex_box.get()})  # Adds colour to side box

                # TODO: add final conversion type
                if conversion_type == "sRGB' [0,1]":
                    print("hello")
                    rgb_nonlin = tuple(map(float, get_entries))
                    yeet = NLSRGBtoSRGB8(rgb_nonlin)
                    hexvals = webcolors.rgb_to_hex(yeet)
                    self.hex_box_value.set(hexvals.upper())
                    self.colour_preview.config({"background": self.hex_box.get()})  # Adds colour to side box

        def delete_last(self):
            Home.RemovableEntry.instances.remove(self)
            self.destroy()

        def remove(self):
            self.destroy()
            Home.RemovableEntry.instances.remove(self)

    # ----- Class to create entries with placeholder text ----- #
    class EntryWithPlaceholder(tk.Entry):
        def __init__(self, master=None, placeholder="0", color='grey', font="Calibri", *args, **kwargs):
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
            if self['fg'] == self.placeholder_color:
                self.delete('0', 'end')
                self['fg'] = self.default_fg_color

        def foc_out(self, *args):
            if not self.get():
                self.put_placeholder()


class About(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # --- Main frames --- #
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # Add content to about frame
        self.AboutContent = tk.Label(self, text="Tool developed by Kieren Townley-Moss,"
                                                " Jake Broughton and "
                                                "Alex Todd")
        self.github = tk.Label(self, text="Github", fg="blue", cursor="hand2")

        self.AboutContent.grid(column=0, row=0, sticky='w')
        self.github.grid(column=0, row=1, sticky='w')

        self.github.bind("<Button-1>", lambda e: self.github_click("https://github.com/kierentm/Colour_Tint_Converter"))

    @staticmethod
    def github_click(url):
        webbrowser.open_new(url)


class Hotkeys(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # --- Main frames --- #
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # Add content to about frame
        self.AboutContent = tk.Label(self, text="Enter   -   Insert new colour"
                                                "\n"
                                                "Esc     -   Delete last colour")

        self.AboutContent.grid(column=0, row=0, sticky='w')

    @staticmethod
    def github_click(url):
        webbrowser.open_new(url)


class Settings(tk.Frame):
    on_top_var = tk.IntVar(value=config.get('main', 'OnTop'))
    dark_mode = tk.IntVar()
    dummy1 = tk.IntVar()
    dummy2 = tk.IntVar()

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create frame for main settings (not save button) and options
        self.main_settings_frame = tk.Frame(self)

        self.save_button = tk.Button(self.main_settings_frame, text="Save", width=10, command=self.update_settings)
        self.on_top = tk.Checkbutton(self.main_settings_frame, text="Keep window on top", variable=Settings.on_top_var)

        # Create setting for File Location and Frame
        self.save_location_frame = tk.Frame(self)

        self.directory_button = tk.Button(self.save_location_frame, text="Select Save Location",
                                          command=self.get_file_past)
        self.folder_location = tk.StringVar(self.save_location_frame, f"{config.get('main', 'SaveLocation')}")
        self.directory_display = tk.Entry(self.save_location_frame, width=42, font="Calibri",
                                          textvariable=self.folder_location,
                                          state="disabled")

        self.main_settings_frame.pack(side="top", anchor="nw", fill=tk.X)
        self.on_top.grid(column=0, row=0, sticky='w')
        self.save_button.grid(column=0, row=1, sticky='w', pady=(0, 15))

        self.save_location_frame.pack(side="top", anchor="nw", fill=tk.X)
        self.directory_button.pack(side="left")
        self.directory_display.pack(fill="both", side="left", expand=True)

        # Declare Settings Path Variable
        self.path_past = ""

        # Check config to apply settings
        root.attributes('-topmost', config.get('main', 'OnTop'))

    @staticmethod
    def update_settings():
        config.set('main', 'OnTop', f"{Settings.on_top_var.get()}")
        with open('config.ini', 'w') as f:
            config.write(f)
        root.attributes('-topmost', config.get('main', 'OnTop'))

    # Initialise windows directory selection and save within config
    def get_file_past(self):
        # Open dialog box to select file and saves location to config
        self.path_past = filedialog.askdirectory(initialdir="/", title="Select Directory")
        config.set('main', 'SaveLocation', self.path_past)
        with open('config.ini', 'w') as past_file:
            config.write(past_file)

        # Updates file location box
        self.folder_location.set(f"{config.get('main', 'SaveLocation')}")


if __name__ == '__main__':
    main()
