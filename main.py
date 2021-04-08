from pathlib import Path
import tkinter as tk
import webbrowser
from configparser import ConfigParser
from tkinter import filedialog
from tkinter import ttk
from time import sleep
from sys import executable, argv
from os import execl
from webcolors import rgb_to_hex
from PIL import ImageGrab, ImageTk
from utility_functions import *

# ---- Version 1.0 ----- #

# FIXME: when restarting to change settings, when you use colour picker it crashes
#  (not happening when I created exe)

# TODO: Comment

# Group Bonding Moment Stuff

# TODO: Create readme and video
# TODO: Could create manual file

# TODO: Remove sus comments
# TODO: Refactor some names (eg. spin)
# TODO: Remove redundant self. tags (High Risk)
# TODO: Add Comments
# TODO: Optimise imports (High Risk)
# TODO: Pack into exe binary files and use installer (High Risk)

# TODO: Github 1.0 release
# TODO: Github about page

# ---- Version 1.1 ----- #
# TODO: Save session (json?) (High Risk)
# TODO: Add group column and reorganize output file (High Risk)
# TODO: Custom hotkeys (High Risk)
# TODO: Live preview box for colour picker (High Risk)
# TODO: Scroll bar (High Risk)
# TODO: Change default placeholder to 0.0 (High Risk)


root = tk.Tk()
root.geometry("450x500")
p1 = tk.PhotoImage(file='UI_Images/CTC_Logo.png')
root.iconphoto(False, p1)
root.title("Colour Tint Converter")
root.configure(bg="#000000")

# Load Config and generate main if required
config = ConfigParser()
config.read('config.ini')

if not config.has_section('main'):
    # Adds main config section
    config.add_section('main')
    config.set('main', 'SaveLocation', f'{Path().absolute()}')
    config.set('main', 'OnTop', '0')
    config.set('main', 'Convert_Type', 'sRGB [0,1]')
    config.set('main', 'Colour_Mode', 'dark_mode')

    # Adds dark mode config section
    config.add_section('dark_mode')
    config.set('dark_mode', 'btn_clr', '#393a40')
    config.set('dark_mode', 'btn_clr_act', '#BCBCBC')
    config.set('dark_mode', 'btn_fg', '#ffffff')
    config.set('dark_mode', 'btn_font_type', 'Calibri')
    config.set('dark_mode', 'btn_font_size', '16')
    config.set('dark_mode', 'bg_clr', '#2f3136')
    config.set('dark_mode', 'tab_bg_clr', '#45484f')
    config.set('dark_mode', 'tab_bg_clr_act', '#45484f')
    config.set('dark_mode', 'entry_bg', '#212426')

    config.set('dark_mode', 'plus_ico', 'UI_Images/Plus_Ico_Dark_Mode.png')
    config.set('dark_mode', 'minus_ico', 'UI_Images/Minus_Ico_Dark_Mode.png')
    config.set('dark_mode', 'pipette_ico', 'UI_Images/Pipette_Ico_Dark_Mode.png')
    config.set('dark_mode', 'export_ico', 'UI_Images/Txt_Ico_Dark_Mode.png')
    config.set('dark_mode', 'git_ico', 'UI_Images/Github_Ico_Dark_Mode.png')
    config.set('dark_mode', 'twitter_ico', 'UI_Images/Twitter_Ico_Dark_Mode.png')

    config.set('dark_mode', 'option_menu_mode', 'Dark Mode')

    # Adds light mode config section
    config.add_section('light_mode')
    config.set('light_mode', 'btn_clr', '#f0f0f0')
    config.set('light_mode', 'btn_clr_act', '#ffffff')
    config.set('light_mode', 'btn_fg', '#0d0d0d')
    config.set('light_mode', 'btn_font_type', 'Calibri')
    config.set('light_mode', 'btn_font_size', '16')
    config.set('light_mode', 'bg_clr', '#f0f0f0')
    config.set('light_mode', 'tab_bg_clr', '#f0f0f0')
    config.set('light_mode', 'tab_bg_clr_act', '#ffffff')
    config.set('light_mode', 'entry_bg', '#f5f5f5')

    config.set('light_mode', 'plus_ico', 'UI_Images/Plus_Ico_Light_Mode.png')
    config.set('light_mode', 'minus_ico', 'UI_Images/Minus_Ico_Light_Mode.png')
    config.set('light_mode', 'pipette_ico', 'UI_Images/Pipette_Ico_Light_Mode.png')
    config.set('light_mode', 'export_ico', 'UI_Images/Txt_Ico_Light_Mode.png')
    config.set('light_mode', 'git_ico', 'UI_Images/Github_Ico_Light_Mode.png')
    config.set('light_mode', 'twitter_ico', 'UI_Images/Twitter_Ico_Light_Mode.png')

    config.set('light_mode', 'option_menu_mode', 'Light Mode')

    with open('config.ini', 'w') as file:
        config.write(file)

# ---- Style Setup ---- #
colour_scheme = f'{config.get("main", "Colour_Mode")}'

btn_clr = f'{config.get(f"{colour_scheme}", "btn_clr")}'  # button colour
btn_clr_act = f'{config.get(f"{colour_scheme}", "btn_clr_act")}'  # button colour when clicked
btn_fg = f'{config.get(f"{colour_scheme}", "btn_fg")}'  # button font colour
btn_font = (f'{config.get(f"{colour_scheme}", "btn_font_type")}', f'{config.get(colour_scheme, "btn_font_size")}')
bg_clr = f'{config.get(f"{colour_scheme}", "bg_clr")}'  # background colour
tab_bg_clr = f'{config.get(f"{colour_scheme}", "tab_bg_clr")}'
tab_bg_clr_act = f'{config.get(f"{colour_scheme}", "tab_bg_clr_act")}'
entry_bg = f'{config.get(f"{colour_scheme}", "entry_bg")}'

plus_ico = tk.PhotoImage(file=f'{config.get(f"{colour_scheme}", "plus_ico")}')
minus_ico = tk.PhotoImage(file=f'{config.get(f"{colour_scheme}", "minus_ico")}')
pipette_ico = tk.PhotoImage(file=f'{config.get(f"{colour_scheme}", "pipette_ico")}')
export_ico = tk.PhotoImage(file=f'{config.get(f"{colour_scheme}", "export_ico")}')
git_ico = tk.PhotoImage(file=f'{config.get(f"{colour_scheme}", "git_ico")}')
twitter_ico = tk.PhotoImage(file=f'{config.get(f"{colour_scheme}", "twitter_ico")}')


# --- Entry point and main class/function calls --- #
def main():
    style = ttk.Style()

    style.theme_create("Theme1", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": tab_bg_clr, "foreground": btn_fg, "focuscolor": tab_bg_clr},
            "map": {"background": [("selected", tab_bg_clr_act)], "expand": [("selected", [1, 1, 1, 0])]}}})

    style.theme_use("Theme1")

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

    def __init__(self, parent, *args, **kwargs):

        # --- Set up main key binds --- #
        root.bind('<Return>', lambda event: self.RemovableEntry(self))
        root.bind('<Escape>', lambda event: self.remove_entry())
        root.bind('<Control-Return>', lambda event: self.screenshot())

        # --- Main frames --- #
        tk.Frame.__init__(self, parent, *args, **kwargs, bg=bg_clr)
        control_frame = tk.Frame(self, bg=tab_bg_clr, padx=5, pady=5)

        # --- Controls --- #
        add_button = tk.Button(control_frame, image=plus_ico, text="Add", bg=btn_clr, fg=btn_fg,
                               activebackground=btn_clr_act, command=lambda: Home.RemovableEntry(self),
                               bd="3", height="22", compound="left", font=btn_font)
        remove_button = tk.Button(control_frame, image=minus_ico, text="Remove", bg=btn_clr, fg=btn_fg,
                                  activebackground=btn_clr_act, command=self.remove_entry,
                                  bd="3", height="22", compound="left", font=btn_font)
        picker = tk.Button(control_frame, image=pipette_ico, text="Colour Pick", bg=btn_clr, fg=btn_fg,
                           activebackground=btn_clr_act, command=self.screenshot,
                           bd="3", height="22", compound="left", font=btn_font)

        # --- Pack Controls --- #
        add_button.pack(fill="x", side="left", expand=1)
        remove_button.pack(fill="x", side="left", expand=1)
        picker.pack(fill="x", side="left", expand=1)

        # --- Export --- #
        self.export_frame = tk.Frame(self, bg=bg_clr, padx=5, pady=5)
        self.export_btn = tk.Button(self.export_frame, image=export_ico, text="Export .txt", bg=btn_clr,
                                    fg=btn_fg,
                                    activebackground=btn_clr_act, command=self.file_write,
                                    bd="3", relief="raised", height="22", compound="left", font=btn_font)
        self.export_name = self.EntryWithPlaceholder(self.export_frame, "Item Name", bg=entry_bg, fg=btn_fg,
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

    # --- Removes last entry in instances list --- #
    def remove_entry(self):
        # If there are instances in the list, remove the last one
        if not len(self.RemovableEntry.instances) == 0:
            Home.RemovableEntry.instances[-1].delete_last()

    # ----------------------------- Colour Picker Functionality ----------------------------- #
    # --- Initiates screenshot, overlay and key binds for screenshot --- #
    def screenshot(self):
        root.withdraw()  # Minimises
        sleep(0.2)

        self.image = ImageGrab.grab()  # Takes screenshot of whole screen
        img = ImageTk.PhotoImage(self.image)  # Creates tk image object to display on overlay

        self.tracer_win = tk.Toplevel(self.master, cursor="cross")  # To make top level
        self.tracer_win.attributes("-fullscreen", True)  # Full screen
        self.tracer_win.overrideredirect(1)
        self.tracer_win.attributes('-alpha', 1)  # Sets transparency
        self.tracer_win.attributes('-topmost', True)  # Keeps on top

        tracer_frame = tk.Frame(self.tracer_win)  # Adds frame to window in order to add label
        self.tracer_win.bind("<Button-1>", self.capture)  # Binds left click to run capture
        screenshot_bg = tk.Label(self.tracer_win, image=img)  # Creates label to bind image to
        screenshot_bg.photo = img  # Anchors the image to the object
        screenshot_bg.pack(fill="both", expand=True)  # Fills frame with label (image)
        tracer_frame.pack()  # Packs the frame to fill the window

    def capture(self, event):  # Auto pass in event details (clicking)
        x, y = event.x, event.y  # Mouse x and y coordinates
        self.tracer_win.destroy()  # Destroys grey window
        self.image = self.image.crop((x - 1, y - 1, x + 1, y + 1))  # Crops image to 2 x 2 box
        self.image = self.image.convert('RGB')  # Converts to RGB8
        rgb_tuple = self.image.getpixel((1, 1))  # Gets SRGB8 of centre pixel

        # --- Conversions depending on which setting is chosen --- #
        conversion_type = config.get('main', 'Convert_Type')
        if conversion_type == "sRGB [0,1]":
            rgb_tuple = RGB8toLSRGB(rgb_tuple)

        if conversion_type == "sRGB' [0,1]":
            rgb_tuple = RGB8toNLSRGB(rgb_tuple)

        if conversion_type == "sRGB8 [0,255]":
            pass

        # --- Rounds the RGB value ready for the UI --- #
        rounded = [round(num, 2) for num in rgb_tuple]  # Round Tuple
        red = rounded[0]
        green = rounded[1]
        blue = rounded[2]

        # --- Creates an entry based on the above RGB values --- #
        self.RemovableEntry(self, r=red, g=green, b=blue,
                            is_screenshot=True)  # Sends RBG values to add_frame

        root.deiconify()  # Restores the window

    # ----------------------------- File write Start ----------------------------- #
    def file_write(self):
        file1 = open(f"{config.get('main', 'SaveLocation')}/{self.export_name.get()}_colours_info.txt", "w+")

        conversion_type = config.get('main', 'Convert_Type')

        for i in Home.RemovableEntry.instances:
            # file1.write(colour_area.capitalize())
            file1.write(f"{i.entry_name.get().capitalize()}\n")
            file1.write(f"Type: {i.convert_type}\n")
            file1.write(f" R  = {export_clarity(float(i.r_entry.get()), conversion_type)}\n")
            file1.write(f" B  = {export_clarity(float(i.g_entry.get()), conversion_type)}\n")
            file1.write(f" G  = {export_clarity(float(i.b_entry.get()), conversion_type)}\n")
            file1.write(f"Hex = {i.hex_box.get()}\n\n")

        file1.close()
        webbrowser.open(f"{config.get('main', 'SaveLocation')}/{self.export_name.get()}_colours_info.txt")

    # ----- Class to create and track entries ---- #
    class RemovableEntry(tk.Frame):
        # List of object (entry) instances to keep track of them
        instances = []

        def __init__(self, parent, r=0, g=0, b=0, is_screenshot=False, *args, **kwargs):
            self.convert_type = config.get('main', 'Convert_Type')

            # ---- Setup ---- #
            tk.Frame.__init__(self, parent, *args, **kwargs, bg=bg_clr)
            Home.RemovableEntry.instances.append(self)

            self.entry_name = Home.EntryWithPlaceholder(self, width=20, placeholder="Colour Name", bg=entry_bg,
                                                        fg=btn_fg)

            self.r_value = tk.StringVar()
            self.g_value = tk.StringVar()
            self.b_value = tk.StringVar()
            self.hex_box_value = tk.StringVar()

            self.r_entry = Home.EntryWithPlaceholder(self, width=4, textvariable=self.r_value, bg=entry_bg, fg=btn_fg)
            self.g_entry = Home.EntryWithPlaceholder(self, width=4, textvariable=self.g_value, bg=entry_bg, fg=btn_fg)
            self.b_entry = Home.EntryWithPlaceholder(self, width=4, textvariable=self.b_value, bg=entry_bg, fg=btn_fg)

            self.colour_preview = tk.Entry(self, width=4)

            self.hex_box = tk.Entry(self, width=10, textvariable=self.hex_box_value, bg=entry_bg, fg=btn_fg)

            self.remove_button = tk.Button(self, text="X", bg=entry_bg, fg=btn_fg, command=lambda: self.remove())

            # ---- Remove placeholder functionality if it's a screenshot ---- #
            if is_screenshot:
                self.r_entry.config(fg=btn_fg)
                self.g_entry.config(fg=btn_fg)
                self.b_entry.config(fg=btn_fg)

                self.r_value.set(r)
                self.g_value.set(g)
                self.b_value.set(b)

            # ---- Pack ---- #
            self.entry_name.pack(side="left", fill=tk.BOTH, expand=True)

            self.r_entry.pack(side="left", fill=tk.Y)
            self.g_entry.pack(side="left", fill=tk.Y)
            self.b_entry.pack(side="left", fill=tk.Y)

            self.colour_preview.pack(side="left", fill=tk.Y)
            self.hex_box.pack(side="left", fill=tk.Y)
            self.remove_button.pack(side="left")

            self.pack(side="top", fill=tk.X)

            # ---- Trace Value Change to Update Hex ---- #
            self.r_value.trace('w', lambda event, f, _: self.value_change())
            self.g_value.trace('w', lambda event, f, _: self.value_change())
            self.b_value.trace('w', lambda event, f, _: self.value_change())
            # self.type_drop_value.trace('w', self.value_change)

            # ---- Trace Value Change to Update Hex ---- #
            self.entry_name.focus_set()

            # --- Update hex on creation --- #
            self.hex_convert()

            # --- Bind left click to update hex value --- #
            self.colour_preview.bind("<FocusIn>", self.skip_widget)
            self.hex_box.bind("<1>", lambda e: self.hex_convert())

        # --- skips to next widget in order of tabbing --- #
        @staticmethod
        def skip_widget(event):
            event.widget.tk_focusNext().focus()
            return "break"

        def value_change(self):
            self.hex_convert()

        def hex_convert(self):
            # ---- Fetch values ---- #
            conversion_type = config.get('main', 'Convert_Type')
            entries = [self.r_entry, self.g_entry, self.b_entry]
            get_entries = [self.r_entry.get(), self.g_entry.get(), self.b_entry.get()]

            for e in entries:
                if incorrect_entry_test(e.get(), conversion_type):
                    e.config(background=entry_bg)
                else:
                    e.config(background="red")

            # If there is no empty box...
            if '' not in get_entries:

                # Use conversion type...
                # Conversion type sRGB [0,1]
                if conversion_type == "sRGB [0,1]":
                    rgb_nonlin = get_entries_convert(get_entries, conversion_type)
                    rgb_linear = LSRGBtoSRGB8(rgb_nonlin)
                    hexvals = rgb_to_hex(rgb_linear)
                    self.hex_box_value.set(hexvals.upper())
                    self.colour_preview.config({"background": self.hex_box.get()})  # Adds colour to side box

                # Conversion type sRGB [0,1]
                if conversion_type == "sRGB8 [0,255]":
                    rgb_nonlin = get_entries_convert(get_entries, conversion_type)
                    hexvals = rgb_to_hex(rgb_nonlin)
                    self.hex_box_value.set(hexvals.upper())
                    self.colour_preview.config({"background": self.hex_box.get()})  # Adds colour to side box

                if conversion_type == "sRGB' [0,1]":
                    rgb_nonlin = get_entries_convert(get_entries, conversion_type)
                    yeet = NLSRGBtoSRGB8(rgb_nonlin)
                    hexvals = rgb_to_hex(yeet)
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
        tk.Frame.__init__(self, parent, *args, **kwargs, bg=bg_clr, bd="10")
        # Add content to about frame
        self.AboutBigText = tk.Label(self, text="Colour Tint Converter\n", font="bold, 20", bg=bg_clr,
                                     fg=btn_fg)
        self.AboutContent = tk.Label(self, text="Tool developed by Kieren Townley-Moss, Jake Broughton and "
                                                "Alex Todd\n\n Version 1.0.23 \n\n Copyright©2021 \n\n", bg=bg_clr,
                                     fg=btn_fg)
        self.aboutLinks = tk.Frame(self, bg=bg_clr)
        self.donationFrame = tk.Frame(self, bg=bg_clr)
        self.github = tk.Label(self.aboutLinks, text="Github", cursor="hand2", image=git_ico, bg=bg_clr)
        self.twitter = tk.Label(self.aboutLinks, text="Github", cursor="hand2", image=twitter_ico, bg=bg_clr)

        self.donationMessage = tk.Label(self.donationFrame, text="Colour Tint Converter is 100% free\n"
                                                                 "You can use the app however you wish\n"
                                                                 "If you like the app, please donate :)",
                                        bg=bg_clr, fg=btn_fg)

        self.donationLink = tk.Label(self.donationFrame, text="Donate", fg="#538cc2", cursor="hand2", bg=bg_clr)
        self.ContactUs = tk.Label(self, text="Contact us at : kajdevelopmentofficial@gmail.com", bg=bg_clr, fg=btn_fg)

        self.github.bind("<Button-1>", lambda e: self.github_click("https://github.com/kierentm/Colour_Tint_Converter"))
        self.twitter.bind("<Button-1>", lambda e: self.github_click("https://twitter.com/KajDevelopment"))
        self.donationLink.bind("<Button-1>", lambda e: self.github_click(
            "https://www.specialeffect.org.uk/get-involved/donate"))

        self.AboutBigText.pack(side="top")
        self.AboutContent.pack(side="top")
        self.aboutLinks.pack(side="bottom")
        self.github.pack(side="left", padx="10")
        self.twitter.pack(side="right")
        self.donationFrame.pack(side="bottom", pady="30")
        self.donationLink.pack(side="bottom")
        self.ContactUs.pack(side="bottom")
        self.donationMessage.pack(side="bottom", padx="10")

    @staticmethod
    def github_click(url):
        webbrowser.open_new(url)


class Hotkeys(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # --- Main frames --- #
        tk.Frame.__init__(self, parent, *args, **kwargs, bg=bg_clr, pady=5, padx=4)

        # Add content to about frame
        tk.Label(self, text="Enter", fg=btn_fg, bg=bg_clr).grid(column=0, row=0, sticky='w')
        tk.Label(self, text="-", fg=btn_fg, bg=bg_clr).grid(column=1, row=0, sticky='w')
        tk.Label(self, text="Insert new colour", fg=btn_fg, bg=bg_clr).grid(column=2, row=0, sticky='w')

        tk.Label(self, text="Escape", fg=btn_fg, bg=bg_clr).grid(column=0, row=1, sticky='w')
        tk.Label(self, text="-", fg=btn_fg, bg=bg_clr).grid(column=1, row=1, sticky='w')
        tk.Label(self, text="Delete last colour", fg=btn_fg, bg=bg_clr).grid(column=2, row=1, sticky='w')

        tk.Label(self, text="Control + Enter", fg=btn_fg, bg=bg_clr).grid(column=0, row=2, sticky='w')
        tk.Label(self, text="-", fg=btn_fg, bg=bg_clr).grid(column=1, row=2, sticky='w')
        tk.Label(self, text="Colour Picker", fg=btn_fg, bg=bg_clr).grid(column=2, row=2, sticky='w')

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
    colour_var = tk.StringVar(value=config.get(f"{config.get('main', 'Colour_Mode')}", "option_menu_mode"))

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs, bg=bg_clr)

        self.restart_popup = None
        self.restore_popup = None

        # Check config to apply settings
        root.attributes('-topmost', config.get('main', 'OnTop'))

        # Create frame for main settings (not save button) and options
        self.main_settings_frame = tk.Frame(self, bg=bg_clr)
        self.on_top = tk.Checkbutton(self.main_settings_frame, text="Keep window on top", variable=Settings.on_top_var,
                                     width="20", bg=bg_clr, fg=btn_fg, selectcolor=bg_clr, activebackground=bg_clr,
                                     activeforeground=btn_fg)
        self.on_top_var.trace('w', lambda func, subst, widget: self.update_settings_main())

        # Create convert default type option
        self.convert_frame = tk.Frame(self, bg=bg_clr)
        self.convert_options = tk.OptionMenu(self.convert_frame, Settings.convert_var, *Settings.convert_types)
        self.convert_options.config(bg=btn_clr, fg=btn_fg, activebackground=btn_clr_act, width="12",
                                    highlightthickness=0)
        self.convert_options["menu"].config(bg=btn_clr, fg=btn_fg)
        self.save_button = tk.Button(self.convert_frame, text="Save", width=10, command=self.restart_window,
                                     bg=bg_clr, fg=btn_fg)

        # Create colour scheme drop down
        self.colour_scheme = tk.OptionMenu(self.convert_frame, Settings.colour_var, *Settings.colour_modes)
        self.colour_scheme.config(bg=btn_clr, fg=btn_fg, activebackground=btn_clr_act, width="12", highlightthickness=0)
        self.colour_scheme["menu"].config(bg=btn_clr, fg=btn_fg)

        # Create setting for File Location and Frame
        self.save_location_frame = tk.Frame(self, bg=bg_clr)
        self.directory_button = tk.Button(self.save_location_frame, text="Select Save Location",
                                          command=self.get_file_past, bg=bg_clr, fg=btn_fg)
        self.folder_location = tk.StringVar(self.save_location_frame, f"{config.get('main', 'SaveLocation')}")
        self.directory_display = tk.Entry(self.save_location_frame, width=42, font="Calibri, 9",
                                          textvariable=self.folder_location, state="disabled",
                                          disabledbackground=entry_bg, disabledforeground=btn_fg)

        # Create a restore button
        self.restore_btn = tk.Button(self, text="Restore to Default Settings", command=self.restore_warning,
                                     bg=bg_clr, fg=btn_fg)

        # Packs frames left
        self.main_settings_frame.pack(side="top", anchor="nw", fill=tk.X, pady=(5, 15))
        self.on_top.pack(side="left")
        # self.on_top.place()

        self.convert_frame.pack(side="top", anchor="nw", fill=tk.X, pady=(0, 15), padx=6)
        self.convert_options.pack(side="left")
        self.colour_scheme.pack(side="left")
        self.save_button.pack(side="left")

        self.save_location_frame.pack(side="top", anchor="nw", fill=tk.X, pady=(0, 15), padx=6)
        self.directory_button.pack(side="left")
        self.directory_display.pack(fill="both", side="left", expand=True)

        self.restore_btn.pack(side="top", anchor="nw", padx=6)

        # Declare Settings Path Variable
        self.path_past = ""

    @staticmethod
    def update_settings_main():
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
        if f"{Settings.colour_var.get()}" == "Dark Mode":
            colour_config = "dark_mode"
        else:
            colour_config = "light_mode"
        config.set('main', 'Colour_Mode', colour_config)
        with open('config.ini', 'w') as f:
            config.write(f)
        python = executable
        execl(python, python, *argv)

    def update_convert_type_no(self):
        self.convert_var.set(config.get('main', 'Convert_Type'))
        self.colour_var.set(config.get(f"{config.get('main', 'Colour_Mode')}", "option_menu_mode"))
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

    def restore_warning(self):
        self.restore_popup = tk.Toplevel()
        self.restore_popup.attributes('-topmost', True)
        self.restore_popup.title("Warning")
        restore_label = tk.Label(self.restore_popup, fg="red",
                                 text="----------------------- Warning -----------------------\n"
                                      "Are you sure you want to restore to default settings?\n"
                                      "This will require a restart,"
                                      "Please ensure you have exported required colour information!")

        restore_label.pack(side="top", fill='x')

        button_bonus = tk.Button(self.restore_popup, text="Yes", command=self.restore)
        button_bonus.pack(fill='x')

        button_close = tk.Button(self.restore_popup, text="No", command=self.restore_popup.destroy)
        button_close.pack(fill='x')

    def restore(self):
        config.set('main', 'SaveLocation', f'{Path().absolute()}')
        config.set('main', 'OnTop', '0')
        config.set('main', 'Convert_Type', 'sRGB [0,1]')
        config.set('main', 'Colour_Mode', 'dark_mode')
        with open('config.ini', 'w') as restore_conf:
            config.write(restore_conf)

        self.folder_location.set(f"{config.get('main', 'SaveLocation')}")

        self.restore_popup.destroy()

        python = executable
        execl(python, python, *argv)


if __name__ == '__main__':
    main()
