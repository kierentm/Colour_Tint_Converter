# --- Colour Tint Converter 2020 --- #
__author__ = "Kieren Townley-Moss, Jake Broughton, Alex Todd"
__credits__ = ["Kieren Townley-Moss", "Jake Broughton", "Alex Todd"]
__version__ = "1.0.0"
__maintainer__ = "Kieren Townley-Moss, Jake Broughton, Alex Todd"
__email__ = "kajdevelopmentofficial@gmail.comu"
__status__ = "Development"

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

root = tk.Tk()
root.geometry("450x500")
p1 = tk.PhotoImage(file='UI_Images/CTC_Logo.png')
root.iconphoto(False, p1)

root.configure(bg="#000000")

# Load Config and generate main if required
config = ConfigParser()
config.read('config.ini')
titleMode = config.get('main', 'Convert_Type')
root.title("Colour Tint Converter:  " + titleMode)

# Checks if ran before and sets default path location to install location
if not config.has_option('main', 'first_time_setup'):
    # Adds main config section
    config.set('main', 'SaveLocation', f'{Path().absolute()}')
    config.set('main', 'first_time_setup', '1')
    with open('config.ini', 'w') as file:
        config.write(file)

# ---- Style Setup from config for light/dark mode ---- #
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

    # Initialise all frames
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
        export_frame = tk.Frame(self, bg=bg_clr, padx=5, pady=5)
        export_btn = tk.Button(export_frame, image=export_ico, text="Export .txt", bg=btn_clr, fg=btn_fg,
                               activebackground=btn_clr_act, command=self.file_write,
                               bd="3", relief="raised", height="22", compound="left", font=btn_font)
        self.export_name = self.EntryWithPlaceholder(export_frame, "Item Name", bg=entry_bg, fg=btn_fg,
                                                     bd="3", relief="raised")

        # --- Pack Export --- #
        export_frame.pack(side="bottom", fill=tk.X)
        export_btn.pack(side="right")
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
            Home.RemovableEntry.instances[-1].remove()

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
        image = self.image.crop((x - 1, y - 1, x + 1, y + 1))  # Crops image to 2 x 2 box
        image = image.convert('RGB')  # Converts to RGB8
        rgb_tuple = image.getpixel((1, 1))  # Gets SRGB8 of centre pixel

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
        # Opens file in location specified by setting (from config) and using name from entry box
        file1 = open(f"{config.get('main', 'SaveLocation')}/{self.export_name.get()}_colours_info.txt", "w+")

        conversion_type = config.get('main', 'Convert_Type')

        # Writes values from removable entry list into file
        for i in Home.RemovableEntry.instances:
            file1.write(f"{i.entry_name.get().capitalize()}\n")
            file1.write(f"Type: {i.convert_type}\n")
            file1.write(f" R  = {export_clarity(float(i.r_entry.get()), conversion_type)}\n")
            file1.write(f" B  = {export_clarity(float(i.g_entry.get()), conversion_type)}\n")
            file1.write(f" G  = {export_clarity(float(i.b_entry.get()), conversion_type)}\n")
            file1.write(f"Hex = {i.hex_box.get()}\n\n")

        file1.close()

        # Opens txt after writing to file
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

            # --- Create variables to track/modify values --- #
            self.r_value = tk.StringVar()
            self.g_value = tk.StringVar()
            self.b_value = tk.StringVar()
            self.hex_box_value = tk.StringVar()

            # --- Create RGB entries with placeholder value --- #
            self.r_entry = Home.EntryWithPlaceholder(self, width=4, textvariable=self.r_value, bg=entry_bg, fg=btn_fg)
            self.g_entry = Home.EntryWithPlaceholder(self, width=4, textvariable=self.g_value, bg=entry_bg, fg=btn_fg)
            self.b_entry = Home.EntryWithPlaceholder(self, width=4, textvariable=self.b_value, bg=entry_bg, fg=btn_fg)

            # --- Create hex entry, colour preview and remove button --- #
            self.colour_preview = tk.Entry(self, width=4)
            self.hex_box = tk.Entry(self, width=10, textvariable=self.hex_box_value, bg=entry_bg, fg=btn_fg)
            self.remove_button = tk.Button(self, text="X", bg=entry_bg, fg=btn_fg, command=lambda: self.remove())

            # ---- Remove placeholder functionality if it's a screenshot by changing the foreground colour  ---- #
            if is_screenshot:
                # Change text colour of RGB entries
                self.r_entry.config(fg=btn_fg)
                self.g_entry.config(fg=btn_fg)
                self.b_entry.config(fg=btn_fg)

                # Set RGB values to those given by the screenshot function
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

        # --- Run hex conversion when RGB value changed --- #
        def value_change(self):
            self.hex_convert()

        # --- Function to convert RGB to hex value based on option in settings --- #
        def hex_convert(self):
            # ---- Fetch values ---- #
            conversion_type = config.get('main', 'Convert_Type')
            entries = [self.r_entry, self.g_entry, self.b_entry]
            get_entries = [self.r_entry.get(), self.g_entry.get(), self.b_entry.get()]

            # --- Check all RGB value validity --- #
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
                    self.hex_box_value.set(hexvals.upper())  # Sets hex box value
                    self.colour_preview.config({"background": self.hex_box.get()})  # Adds colour to side box

                # Conversion type sRGB [0,1]
                if conversion_type == "sRGB8 [0,255]":
                    rgb_nonlin = get_entries_convert(get_entries, conversion_type)
                    hexvals = rgb_to_hex(rgb_nonlin)
                    self.hex_box_value.set(hexvals.upper())  # Sets hex box value
                    self.colour_preview.config({"background": self.hex_box.get()})  # Adds colour to side box

                if conversion_type == "sRGB' [0,1]":
                    rgb_nonlin = get_entries_convert(get_entries, conversion_type)
                    yeet = NLSRGBtoSRGB8(rgb_nonlin)
                    hexvals = rgb_to_hex(yeet)
                    self.hex_box_value.set(hexvals.upper())  # Sets hex box value
                    self.colour_preview.config({"background": self.hex_box.get()})  # Adds colour to side box

        # --- Destroy instance and remove from instances list --- #
        def remove(self):
            Home.RemovableEntry.instances.remove(self)
            self.destroy()

        # def remove(self):
        #     self.destroy()
        #     Home.RemovableEntry.instances.remove(self)

    # ----- Class to create entries with placeholder text. Inherit from tk.Entry ----- #
    class EntryWithPlaceholder(tk.Entry):
        def __init__(self, master=None, placeholder="0", color='grey', font="Calibri", *args, **kwargs):
            # Create entry instance
            super().__init__(master, *args, **kwargs)

            # Grab arguments given
            self.placeholder = placeholder
            self.placeholder_color = color
            self.default_fg_color = self['fg']
            self.font = font

            # Bind focus in/out functions to event, i.e when clicking/tabbing in and out of entry
            self.bind("<FocusIn>", lambda event: self.foc_in())
            self.bind("<FocusOut>", lambda event: self.foc_out())
            self.put_placeholder()

        # Insert placeholder text into entry box
        def put_placeholder(self):
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

        # Remove text in entry when clicked/tabbed into if it's grey (fg colour)
        def foc_in(self):
            if self['fg'] == self.placeholder_color:
                self.delete('0', 'end')
                self['fg'] = self.default_fg_color

        # If the entry is not empty upon leaving the entry box, put the placeholder value back
        def foc_out(self):
            if not self.get():
                self.put_placeholder()


class About(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # --- Main frames --- #
        tk.Frame.__init__(self, parent, *args, **kwargs, bg=bg_clr, bd="10")

        # Add content to about frame
        about_big_text = tk.Label(self, text="Colour Tint Converter\n", font="bold, 20", bg=bg_clr, fg=btn_fg)
        about_content = tk.Label(self, text="Tool developed by Kieren Townley-Moss, Jake Broughton and "
                                            "Alex Todd\n\n Version 1.0.23 \n\n Copyright©2021 \n\n", bg=bg_clr,
                                 fg=btn_fg)
        about_links = tk.Frame(self, bg=bg_clr)
        donation_frame = tk.Frame(self, bg=bg_clr)
        github = tk.Label(about_links, text="Github", cursor="hand2", image=git_ico, bg=bg_clr)
        twitter = tk.Label(about_links, text="Github", cursor="hand2", image=twitter_ico, bg=bg_clr)

        donation_message = tk.Label(donation_frame, text="Colour Tint Converter is 100% free\n"
                                                         "You can use the app however you wish\n"
                                                         "If you like the app, please donate :)",
                                    bg=bg_clr, fg=btn_fg)

        donation_link = tk.Label(donation_frame, text="Donate", fg="#538cc2", cursor="hand2", bg=bg_clr)
        contact_us = tk.Label(self, text="Contact us at : kajdevelopmentofficial@gmail.com", bg=bg_clr, fg=btn_fg)

        github.bind("<Button-1>", lambda e: self.github_click("https://github.com/kierentm/Colour_Tint_Converter"))
        twitter.bind("<Button-1>", lambda e: self.github_click("https://twitter.com/KajDevelopment"))
        donation_link.bind("<Button-1>", lambda e: self.github_click(
            "https://www.specialeffect.org.uk/get-involved/donate"))

        # Packs content to about frame
        about_big_text.pack(side="top")
        about_content.pack(side="top")
        about_links.pack(side="bottom")
        github.pack(side="left", padx="10")
        twitter.pack(side="right")
        donation_frame.pack(side="bottom", pady="30")
        donation_link.pack(side="bottom")
        contact_us.pack(side="bottom")
        donation_message.pack(side="bottom", padx="10")

    # --- Callback function to launch GitHub URL --- #
    @staticmethod
    def github_click(url):
        webbrowser.open_new(url)


class Hotkeys(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # --- Main frames --- #
        tk.Frame.__init__(self, parent, *args, **kwargs, bg=bg_clr, pady=5, padx=4)

        # Add content to about frame using to grid to align -
        tk.Label(self, text="Enter", fg=btn_fg, bg=bg_clr).grid(column=0, row=0, sticky='w')
        tk.Label(self, text="-", fg=btn_fg, bg=bg_clr).grid(column=1, row=0, sticky='w')
        tk.Label(self, text="Insert new colour", fg=btn_fg, bg=bg_clr).grid(column=2, row=0, sticky='w')

        tk.Label(self, text="Escape", fg=btn_fg, bg=bg_clr).grid(column=0, row=1, sticky='w')
        tk.Label(self, text="-", fg=btn_fg, bg=bg_clr).grid(column=1, row=1, sticky='w')
        tk.Label(self, text="Delete last colour", fg=btn_fg, bg=bg_clr).grid(column=2, row=1, sticky='w')

        tk.Label(self, text="Control + Enter", fg=btn_fg, bg=bg_clr).grid(column=0, row=2, sticky='w')
        tk.Label(self, text="-", fg=btn_fg, bg=bg_clr).grid(column=1, row=2, sticky='w')
        tk.Label(self, text="Colour Picker", fg=btn_fg, bg=bg_clr).grid(column=2, row=2, sticky='w')

    # --- Callback function to open GitHub link --- #
    @staticmethod
    def github_click(url):
        webbrowser.open_new(url)


# --- Settings Class --- #
class Settings(tk.Frame):
    # Create settings variables, setting values set to default to config value
    on_top_var = tk.IntVar(value=config.get('main', 'OnTop'))
    dark_mode = tk.IntVar()
    dummy1 = tk.IntVar()
    dummy2 = tk.IntVar()

    # Create convert type list and set initial value based on config
    convert_types = [
        "sRGB8 [0,255]",
        "sRGB' [0,1]",
        "sRGB [0,1]"
    ]
    convert_var = tk.StringVar(value=config.get('main', 'Convert_Type'))

    # Create colour mode list and set initial value based on config
    colour_modes = [
        "Light Mode",
        "Dark Mode"
    ]
    colour_var = tk.StringVar(value=config.get(f"{config.get('main', 'Colour_Mode')}", "option_menu_mode"))

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs, bg=bg_clr)

        # Generate variables for use in restart warning pop up windows
        self.restart_popup = None
        self.restore_popup = None

        # Check config to apply settings
        root.attributes('-topmost', config.get('main', 'OnTop'))

        # Create frame for main settings (not save button) and options
        main_settings_frame = tk.Frame(self, bg=bg_clr)
        on_top = tk.Checkbutton(main_settings_frame, text="Keep window on top", variable=Settings.on_top_var,
                                width="20", bg=bg_clr, fg=btn_fg, selectcolor=bg_clr, activebackground=bg_clr,
                                activeforeground=btn_fg)
        self.on_top_var.trace('w', lambda func, subst, widget: self.update_settings_main())

        # Create convert default type option
        convert_frame = tk.Frame(self, bg=bg_clr)
        convert_options = tk.OptionMenu(convert_frame, Settings.convert_var, *Settings.convert_types)
        convert_options.config(bg=btn_clr, fg=btn_fg, activebackground=btn_clr_act, width="12", highlightthickness=0)
        convert_options["menu"].config(bg=btn_clr, fg=btn_fg)
        save_button = tk.Button(convert_frame, text="Save", width=10, command=self.restart_window, bg=bg_clr, fg=btn_fg)

        # Create colour scheme drop down
        self.colour_scheme = tk.OptionMenu(convert_frame, Settings.colour_var, *Settings.colour_modes)
        self.colour_scheme.config(bg=btn_clr, fg=btn_fg, activebackground=btn_clr_act, width="12", highlightthickness=0)
        self.colour_scheme["menu"].config(bg=btn_clr, fg=btn_fg)

        # Create setting for File Location and Frame
        save_location_frame = tk.Frame(self, bg=bg_clr)
        directory_button = tk.Button(save_location_frame, text="Select Save Location",
                                     command=self.get_file_past, bg=bg_clr, fg=btn_fg)
        self.folder_location = tk.StringVar(save_location_frame, f"{config.get('main', 'SaveLocation')}")
        directory_display = tk.Entry(save_location_frame, width=42, font="Calibri, 9",
                                     textvariable=self.folder_location, state="disabled",
                                     disabledbackground=entry_bg, disabledforeground=btn_fg)

        # Create a restore button
        restore_btn = tk.Button(self, text="Restore to Default Settings", command=self.restore_warning,
                                bg=bg_clr, fg=btn_fg)

        # Packs frames left
        main_settings_frame.pack(side="top", anchor="nw", fill=tk.X, pady=(5, 15))
        on_top.pack(side="left")

        convert_frame.pack(side="top", anchor="nw", fill=tk.X, pady=(0, 15), padx=6)
        convert_options.pack(side="left")
        self.colour_scheme.pack(side="left")
        save_button.pack(side="left")

        save_location_frame.pack(side="top", anchor="nw", fill=tk.X, pady=(0, 15), padx=6)
        directory_button.pack(side="left")
        directory_display.pack(fill="both", side="left", expand=True)

        restore_btn.pack(side="top", anchor="nw", padx=6)

        # Declare Settings Path Variable
        self.path_past = ""

    @staticmethod
    def update_settings_main():
        # Updates config with new setting automatically from previous trace
        root.attributes('-topmost', Settings.on_top_var.get())
        config.set('main', 'OnTop', f"{Settings.on_top_var.get()}")
        with open('config.ini', 'w') as conf:
            config.write(conf)

    def restart_window(self):
        # Generates warning restart window when choosing to save update to colour mode and conversion type
        self.restart_popup = tk.Toplevel()
        self.restart_popup.attributes('-topmost', True)
        self.restart_popup.title("Warning")

        # Inputs warning and packs to top
        question_label = tk.Label(self.restart_popup, fg="red",
                                  text="----------------------- Warning -----------------------\n"
                                       "Saving requires a program restart,\n"
                                       "Please ensure you have exported required colour information,\n"
                                       "Would you like to restart now?")
        question_label.pack(side="top", fill='x')

        # Creates option buttons which either restart and update setting or return to previous window without update
        button_bonus = tk.Button(self.restart_popup, text="Yes", command=self.update_convert_type_yes)
        button_bonus.pack(fill='x')

        button_close = tk.Button(self.restart_popup, text="No", command=self.update_convert_type_no)
        button_close.pack(fill='x')

    # Update config file and restart program
    @staticmethod
    def update_convert_type_yes():
        # Update config to convert type and colour mode (if statement used as defined as dark/light_mode in config
        config.set('main', 'Convert_Type', f"{Settings.convert_var.get()}")
        if f"{Settings.colour_var.get()}" == "Dark Mode":
            colour_config = "dark_mode"
        else:
            colour_config = "light_mode"
        config.set('main', 'Colour_Mode', colour_config)
        with open('config.ini', 'w') as f:
            config.write(f)
        # Restarts program to allow update to take effect
        python = executable
        execl(python, python, *argv)

    # Restores lists to current value and closes warning window
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

    # Warning when selecting restore
    def restore_warning(self):
        # Generates window and title
        self.restore_popup = tk.Toplevel()
        self.restore_popup.attributes('-topmost', True)
        self.restore_popup.title("Warning")
        restore_label = tk.Label(self.restore_popup, fg="red",
                                 text="----------------------- Warning -----------------------\n"
                                      "Are you sure you want to restore to default settings?\n"
                                      "This will require a restart,"
                                      "Please ensure you have exported required colour information!")

        restore_label.pack(side="top", fill='x')

        # Creates option buttons to either restore to default and restart or close warning window
        button_bonus = tk.Button(self.restore_popup, text="Yes", command=self.restore)
        button_bonus.pack(fill='x')

        button_close = tk.Button(self.restore_popup, text="No", command=self.restore_popup.destroy)
        button_close.pack(fill='x')

    # Restores config to default and restarts window
    def restore(self):
        config.set('main', 'SaveLocation', f'{Path().absolute()}')
        config.set('main', 'OnTop', '0')
        config.set('main', 'Convert_Type', 'sRGB [0,1]')
        config.set('main', 'Colour_Mode', 'dark_mode')
        with open('config.ini', 'w') as restore_conf:
            config.write(restore_conf)

        self.folder_location.set(f"{config.get('main', 'SaveLocation')}")
        self.restore_popup.destroy()

        # Restarts program
        python = executable
        execl(python, python, *argv)


# --- Entry point --- #
if __name__ == '__main__':
    main()
