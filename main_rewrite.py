import pathlib
import tkinter as tk
import webbrowser
from configparser import ConfigParser
from tkinter import filedialog
from tkinter import ttk
import time
import sys
import os

import webcolors
from PIL import ImageGrab, ImageTk

from convert import *

root = tk.Tk()
root.geometry("450x500")
p1 = tk.PhotoImage(file='Design Images/Logo2.png')
root.iconphoto(False, p1)
root.title("Colour Tint Converter")

# Load Config and generate main if required
config = ConfigParser()
config.read('config.ini')

if not config.has_section('main'):
    config.add_section('main')
    config.set('main', 'SaveLocation', f'{pathlib.Path().absolute()}')
    config.set('main', 'OnTop', '0')
    config.set('main', 'Convert_Type', 'sRGB [0,1]')
    config.set('main', 'Colour_Mode', 'Dark Mode')
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
    tab_parent.add(settings, text="Settings")
    tab_parent.add(hotkeys, text="Hotkeys")
    tab_parent.add(about, text="About")

    tab_parent.pack(expand=1, fill="both")

    # Tk main loop
    root.mainloop()


class Home(tk.Frame):
    # ---- Style Setup ---- #
    colour_scheme = colour_mode(f"{config.get('main', 'Colour_Mode')}")

    btn_clr = colour_scheme[0]  # button colour
    btn_clr_act = colour_scheme[1]  # button colour when clicked
    btn_fg = colour_scheme[2]  # button font colour
    btn_font = colour_scheme[3]
    bg_clr = colour_scheme[4]  # background colour
    tab_bg_clr = colour_scheme[5]
    entry_bg = colour_scheme[6]

    plus_ico = tk.PhotoImage(file="UI_Images/Plus_Solo_1.png")
    pipette_ico = tk.PhotoImage(file="UI_Images/Pipette_Solo.png")
    export_ico = tk.PhotoImage(file="UI_Images/Txt_Solo.png")
    git_ico = tk.PhotoImage(file="UI_Images/Github_Solo.png")
    twitter_ico = tk.PhotoImage(file="UI_Images/Twitter_Solo.png")

    def __init__(self, parent, *args, **kwargs):

        root.bind('<Return>', lambda event: self.RemovableEntry(self))
        root.bind('<Escape>', lambda event: self.remove_entry())
        root.bind('<Control-Return>', lambda event: self.screenshot())

        # --- Main frames --- #
        tk.Frame.__init__(self, parent, *args, **kwargs, bg=Home.bg_clr)
        control_frame = tk.Frame(self, bg=Home.tab_bg_clr)

        # --- Controls --- #
        add_button = tk.Button(control_frame, image=Home.plus_ico, text="Add", bg=Home.btn_clr, fg=Home.btn_fg,
                               activebackground=Home.btn_clr_act, command=lambda: Home.RemovableEntry(self),
                               bd="3", height="22", compound="left", font=Home.btn_font)
        remove_button = tk.Button(control_frame, image=Home.plus_ico, text="Remove", bg=Home.btn_clr, fg=Home.btn_fg,
                                  activebackground=Home.btn_clr_act, command=self.remove_entry,
                                  bd="3", height="22", compound="left", font=Home.btn_font)
        picker = tk.Button(control_frame, image=Home.pipette_ico, text="Colour Pick", bg=Home.btn_clr, fg=Home.btn_fg,
                           activebackground=Home.btn_clr_act, command=self.screenshot,
                           bd="3", height="22", compound="left", font=Home.btn_font)

        # --- Pack Controls --- #
        add_button.pack(side="left")
        remove_button.pack(side="left")
        picker.pack(side="right")

        # --- Export --- #
        self.export_frame = tk.Frame(self, bg=Home.bg_clr)
        self.export_btn = tk.Button(self.export_frame, image=Home.export_ico, text="Export .txt", bg=Home.btn_clr,
                                    fg=Home.btn_fg,
                                    activebackground=Home.btn_clr_act, command=self.file_write,
                                    bd="3", relief="raised", height="22", compound="left", font=Home.btn_font)
        self.export_name = self.EntryWithPlaceholder(self.export_frame, "Item Name", bg=Home.tab_bg_clr, fg=Home.btn_fg,
                                                     bd="3", relief="raised")

        # --- Pack Export --- #
        self.export_frame.pack(side="bottom", fill=tk.X)
        self.export_btn.pack(side="right")
        self.export_name.pack(fill=tk.BOTH, side="left", expand=True)

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
        # rounded = [round(num, 3) for num in rgb_tuple]  # Round Tuple
        # red = rounded[0]
        # green = rounded[1]
        # blue = rounded[2]

        conversion_type = config.get('main', 'Convert_Type')
        if conversion_type == "sRGB [0,1]":
            rgb_tuple = RGB8toLSRGB(rgb_tuple)
            print(rgb_tuple)

        if conversion_type == "sRGB' [0,1]":
            rgb_tuple = RGB8toNLSRGB(rgb_tuple)
            print(rgb_tuple)

        if conversion_type == "sRGB8 [0,255]":
            pass

        rounded = [round(num, 2) for num in rgb_tuple]  # Round Tuple
        red = rounded[0]
        green = rounded[1]
        blue = rounded[2]
        self.RemovableEntry(self, r=red, g=green, b=blue,
                            is_screenshot=True)  # Sends RBG values to add_frame
        root.deiconify()

    def remove_entry(self):
        if not len(self.RemovableEntry.instances) == 0:
            Home.RemovableEntry.instances[-1].delete_last()

    # ----------------------------- File write Start ----------------------------- #
    def file_write(self):
        file1 = open(f"{config.get('main', 'SaveLocation')}/{self.export_name.get()}_colours_info.txt", "w+")
        # item_name = "Item_Name"
        # file1.write(item_name + "\n\n")
        # colour_area = "Colours for the\n\n"

        conversion_type = config.get('main', 'Convert_Type')

        for i in Home.RemovableEntry.instances:
            # file1.write(colour_area.capitalize())
            file1.write(f"{i.entry_name.get().capitalize()}\n")
            file1.write(f"Type: {i.convert_type}\n")
            file1.write(f" R  = {ifgreaterthan1(float(i.r_entry.get()), conversion_type)}\n")
            file1.write(f" B  = {ifgreaterthan1(float(i.g_entry.get()), conversion_type)}\n")
            file1.write(f" G  = {ifgreaterthan1(float(i.b_entry.get()), conversion_type)}\n")
            file1.write(f"Hex = {i.hex_box.get()}\n\n")

        file1.close()
        webbrowser.open(f"{config.get('main', 'SaveLocation')}/{self.export_name.get()}_colours_info.txt")

    # ----- Class to create and track entries ---- #
    class RemovableEntry(tk.Frame):
        instances = []

        def __init__(self, parent, r=0, g=0, b=0, is_screenshot=False, *args, **kwargs):
            self.convert_type = config.get('main', 'Convert_Type')

            # ---- Setup ---- #
            tk.Frame.__init__(self, parent, *args, **kwargs, bg=Home.bg_clr)
            Home.RemovableEntry.instances.append(self)

            # # ---- Each entry set up here ---- #
            # convert_types = [
            #     "sRGB8 [0,255]",
            #     "sRGB' [0,1]",
            #     "sRGB [0,1]"
            # ]
            #
            # self.type_drop_value = tk.StringVar(self)
            # self.type_drop_value.set(self.convert_type)
            #
            # type_dropdown = tk.OptionMenu(self, self.type_drop_value, *convert_types)
            # type_dropdown.config(width=10)

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
            # type_dropdown.pack(side="left", fill=tk.Y)
            self.entry_name.pack(side="left", fill=tk.BOTH, expand=True)

            self.r_entry.pack(side="left", fill=tk.Y)
            self.g_entry.pack(side="left", fill=tk.Y)
            self.b_entry.pack(side="left", fill=tk.Y)

            self.colour_preview.pack(side="left", fill=tk.Y)
            self.hex_box.pack(side="left", fill=tk.Y)
            self.remove_button.pack(side="left")

            self.pack(side="top", fill=tk.X)

            # ---- Trace Value Change to Update Hex ---- #
            self.r_value.trace('w', self.value_change)
            self.g_value.trace('w', self.value_change)
            self.b_value.trace('w', self.value_change)
            # self.type_drop_value.trace('w', self.value_change)

            # ---- Trace Value Change to Update Hex ---- #
            self.entry_name.focus_set()

            # --- Update hex on creation --- #
            self.hex_convert()

        def value_change(self, *args):
            self.hex_convert()

        def hex_convert(self):
            # ---- Fetch values ---- #
            conversion_type = config.get('main', 'Convert_Type')
            entries = [self.r_entry, self.g_entry, self.b_entry]
            get_entries = [self.r_entry.get(), self.g_entry.get(), self.b_entry.get()]

            for e in entries:
                if KierensStupidTest(e.get(), conversion_type):
                    e.config(background="white")
                else:
                    e.config(background="red")

            # If there is no empty box...
            if '' not in get_entries:

                # Use conversion type...
                # Conversion type sRGB [0,1]
                if conversion_type == "sRGB [0,1]":
                    try:
                        rgb_nonlin = tuple(map(float, get_entries))
                    except ValueError:
                        rgb_nonlin = (0, 0, 0)
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

                if conversion_type == "sRGB' [0,1]":
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

            self.bind("<FocusIn>", lambda event: self.foc_in())
            self.bind("<FocusOut>", lambda event: self.foc_out())
            self.put_placeholder()

        def put_placeholder(self):
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

        def foc_in(self):
            if self['fg'] == self.placeholder_color:
                self.delete('0', 'end')
                self['fg'] = self.default_fg_color

        def foc_out(self):
            if not self.get():
                self.put_placeholder()


class About(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # --- Main frames --- #
        tk.Frame.__init__(self, parent, *args, **kwargs, bg=Home.bg_clr, bd="10")
        # Add content to about frame
        self.AboutBigText = tk.Label(self, text="Colour Tint Converter\n", font="bold, 20", bg=Home.bg_clr,
                                     fg=Home.btn_fg)
        self.AboutContent = tk.Label(self, text="Tool developed by Kieren Townley-Moss, Jake Broughton "
                                                "and Alex Todd\n\n Version 1.0.23 \n\n Copyright©2021 \n\n"

                                     , bg=Home.bg_clr, fg=Home.btn_fg)
        self.github = tk.Label(self, text="Github", cursor="hand2", image=Home.git_ico, bg=Home.bg_clr)
        self.twitter = tk.Label(self, text="Github", cursor="hand2", image=Home.twitter_ico, bg=Home.bg_clr)
        self.donationMessage = tk.Label(self, text="Colour Tint Converter is 100% free.\n"
                                                   "You can use the app however you wish\n"
                                                   "If you like the app, please donate :)", bg=Home.bg_clr,
                                        fg=Home.btn_fg)
        self.donationLink = tk.Label(self, text="Donate", fg="#538cc2", cursor="hand2", bg=Home.bg_clr)

        # self.AboutBigText.grid(column=0, row=0, sticky='w')
        # self.AboutContent.grid(column=0, row=1, sticky='w')
        # self.github.grid(column=0, row=2, sticky='w')
        # self.twitter.grid(column=1, row=2, sticky='w')
        # self.donationMessage.grid(column=0, row=3)
        # self.donationLink.grid(column=1, row=5, sticky="e")

        self.github.bind("<Button-1>", lambda e: self.github_click("https://github.com/kierentm/Colour_Tint_Converter"))
        self.twitter.bind("<Button-1>", lambda e: self.github_click("https://twitter.com/JakDevelopment"))
        self.donationLink.bind("<Button-1>", lambda e: self.github_click(
            "https://streamelements.com/beardo1557/tip"))

        self.AboutBigText.pack(side="top")
        self.AboutContent.pack(side="top")
        self.github.pack(side="top")
        self.donationMessage.pack(side="top")
        self.twitter.pack(side="top")
        self.donationLink.pack(side="top")

    @staticmethod
    def github_click(url):
        webbrowser.open_new(url)


class Hotkeys(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # --- Main frames --- #
        tk.Frame.__init__(self, parent, *args, **kwargs, bg=Home.bg_clr)

        # Add content to about frame
        tk.Label(self, text="Enter", fg=Home.btn_fg, bg=Home.bg_clr).grid(column=0, row=0, sticky='w')
        tk.Label(self, text="-", fg=Home.btn_fg, bg=Home.bg_clr).grid(column=1, row=0, sticky='w')
        tk.Label(self, text="Insert new colour", fg=Home.btn_fg, bg=Home.bg_clr).grid(column=2, row=0, sticky='w')

        tk.Label(self, text="Escape", fg=Home.btn_fg, bg=Home.bg_clr).grid(column=0, row=1, sticky='w')
        tk.Label(self, text="-", fg=Home.btn_fg, bg=Home.bg_clr).grid(column=1, row=1, sticky='w')
        tk.Label(self, text="Delete last colour", fg=Home.btn_fg, bg=Home.bg_clr).grid(column=2, row=1, sticky='w')

        tk.Label(self, text="Control + Enter", fg=Home.btn_fg, bg=Home.bg_clr).grid(column=0, row=2, sticky='w')
        tk.Label(self, text="-", fg=Home.btn_fg, bg=Home.bg_clr).grid(column=1, row=2, sticky='w')
        tk.Label(self, text="Colour Picker", fg=Home.btn_fg, bg=Home.bg_clr).grid(column=2, row=2, sticky='w')

    @staticmethod
    def github_click(url):
        webbrowser.open_new(url)


class Settings(tk.Frame):
    on_top_var = tk.IntVar(value=config.get('main', 'OnTop'))
    dark_mode = tk.IntVar()
    dummy1 = tk.IntVar()
    dummy2 = tk.IntVar()

    convert_types = [
        "sRGB8 [0,255]",
        "sRGB' [0,1]",
        "sRGB [0,1]"
    ]
    convert_var = tk.StringVar(value=config.get('main', 'Convert_Type'))

    colour_modes = [
        "Light Mode",
        "Dark Mode"
    ]
    colour_var = tk.StringVar(value=config.get('main', 'Colour_Mode'))

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs, bg=Home.bg_clr)

        self.restart_popup = None

        # Check config to apply settings
        root.attributes('-topmost', config.get('main', 'OnTop'))

        # Create frame for main settings (not save button) and options
        self.main_settings_frame = tk.Frame(self, bg=Home.bg_clr)
        self.on_top = tk.Checkbutton(self.main_settings_frame, text="Keep window on top", variable=Settings.on_top_var)
        self.on_top_var.trace('w', self.update_settings_main)

        # Create convert default type option
        self.convert_frame = tk.Frame(self, bg=Home.bg_clr)
        self.convert_options = tk.OptionMenu(self.convert_frame, Settings.convert_var, *Settings.convert_types)
        self.save_button = tk.Button(self.convert_frame, text="Save", width=10, command=self.restart_window)

        # Create colour scheme drop down
        self.colour_scheme = tk.OptionMenu(self.convert_frame, Settings.colour_var, *Settings.colour_modes)

        # Create setting for File Location and Frame
        self.save_location_frame = tk.Frame(self, bg=Home.bg_clr)
        self.directory_button = tk.Button(self.save_location_frame, text="Select Save Location",
                                          command=self.get_file_past)
        self.folder_location = tk.StringVar(self.save_location_frame, f"{config.get('main', 'SaveLocation')}")
        self.directory_display = tk.Entry(self.save_location_frame, width=42, font="Calibri",
                                          textvariable=self.folder_location, state="disabled")

        # Packs frames
        self.main_settings_frame.pack(side="top", anchor="nw", fill=tk.X, pady=(0, 15))
        self.on_top.grid(column=0, row=0, sticky='w')

        self.convert_frame.pack(side="top", anchor="nw", fill=tk.X, pady=(0, 15))
        self.convert_options.grid(column=0, row=0, sticky='w')
        self.save_button.grid(column=1, row=0, sticky='w')
        self.colour_scheme.grid(column=0, row=1, sticky='w')

        self.save_location_frame.pack(side="top", anchor="nw", fill=tk.X)
        self.directory_button.pack(side="left")
        self.directory_display.pack(fill="both", side="left", expand=True)

        # Declare Settings Path Variable
        self.path_past = ""

    @staticmethod
    def update_settings_main(*args):
        root.attributes('-topmost', Settings.on_top_var.get())
        config.set('main', 'OnTop', f"{Settings.on_top_var.get()}")
        with open('config.ini', 'w') as conf:
            config.write(conf)

    def restart_window(self):
        self.restart_popup = tk.Toplevel()
        self.restart_popup.attributes('-topmost', True)

        self.restart_popup.title("Warning")

        question_label = tk.Label(self.restart_popup, fg="red",
                                  text="----------------------- Warning -----------------------\n"
                                       "Saving requires a program restart,\n"
                                       "Please ensure you have exported required colour information,\n"
                                       "Would you like to restart now?")
        question_label.pack(side="top", fill='x')

        button_bonus = tk.Button(self.restart_popup, text="Yes", command=self.update_convert_type_yes)
        button_bonus.pack(fill='x')

        button_close = tk.Button(self.restart_popup, text="No", command=self.update_convert_type_no)
        button_close.pack(fill='x')

    @staticmethod
    def update_convert_type_yes():
        config.set('main', 'Convert_Type', f"{Settings.convert_var.get()}")
        config.set('main', 'Colour_Mode', f"{Settings.colour_var.get()}")
        with open('config.ini', 'w') as f:
            config.write(f)
        root.attributes('-topmost', config.get('main', 'OnTop'))
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def update_convert_type_no(self):
        self.convert_var.set(config.get('main', 'Convert_Type'))
        self.colour_var.set(config.get('main', 'Colour_Mode'))
        self.restart_popup.destroy()

    # Initialise windows directory selection and save within config
    def get_file_past(self):
        # Open dialog box to select file and saves location to config
        self.path_past = filedialog.askdirectory(initialdir="/", title="Select Directory")
        if self.path_past:
            config.set('main', 'SaveLocation', self.path_past)
            with open('config.ini', 'w') as past_file:
                config.write(past_file)

        # Updates file location box
        self.folder_location.set(f"{config.get('main', 'SaveLocation')}")


if __name__ == '__main__':
    main()
