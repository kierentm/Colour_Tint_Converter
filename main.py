import tkinter as tk
from tkinter import ttk, Toplevel
from tkinter import filedialog
from convert import *
from PIL import ImageGrab
import webcolors
import webbrowser
from configparser import ConfigParser
import pathlib

root = tk.Tk()

p1 = tk.PhotoImage(file='Design Images/CTC.png')
root.iconphoto(False, p1)

root.title("Colour Tint Master")
root.geometry('450x500')

# Initialise Tab Parent Notebook
tab_parent = ttk.Notebook(root)

# Colour Variables
# btn_clr = "#393a40"
# btn_clr_active = "#212124"
# bg_clr = "#f4f4f4"
btn_clr = "#393a40"         #button colour
btn_clr_act = "#57a337"     #button colour when clicked
btn_fg = "#ffffff"          #button font colour
btn_font = "Calibri", "16"

bg_clr = "#2f3136"          #background colour



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

# Load Config and generate main if required
config = ConfigParser()

config.read('config.ini')

if not config.has_section('main'):
    config.add_section('main')
    config.set('main', 'SaveLocation', f'{pathlib.Path().absolute()}')
    config.set('main', 'OnTop', '0')
    with open('config.ini', 'w') as f:
        config.write(f)

# TODO: Toggle Dark mode

# TODO: Add hotkeys (update all colours, toggle keep on top .etc)

# TODO: Add Comments
# TODO: Add program icon
# TODO: Make text white when all three numbers are below 0.1 (practically black)

plus_ico = tk.PhotoImage(file="UI_Images\Plus_Solo_1.png")
pipette_ico = tk.PhotoImage(file="UI_Images\Pipette_Solo.png")
export_ico = tk.PhotoImage(file="UI_Images\Txt_Solo.png")


class Home:
    tracer_win: Toplevel

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, bg=bg_clr, relief="ridge", bd="500")

        # Create Entry and Colour Frame
        self.entry_frame = tk.Frame(self.master, bg=bg_clr)

        self.entry_btn = tk.Button(self.entry_frame, image=plus_ico, bg=btn_clr, activebackground=btn_clr_act,
                                   fg=btn_fg, bd="3", height="22", text="New Entry", compound="left", command=add_frame,
                                   font=btn_font)
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

        root.bind('<KeyPress>', on_key_press)

    def my_function(self):
        pass

    def file_write(self):
        file1 = open(f"{config.get('main', 'SaveLocation')}/{self.export_name.get()}_colours_info.txt", "w+")
        item_name = "Item_Name"
        file1.write(item_name + "\n\n")
        #colour_area = "Colours for the\n\n"

        # TODO: figure out how to make it print the colour area when it changes
        #  , not every single time (it will be an entry column soon)

        for i in RemovableTint.instances:
            #file1.write(colour_area.capitalize())
            file1.write(f"{i.colour_tint_name.get().capitalize()}\n")
            file1.write(f" R = {ifgreaterthan1(float(i.r_spin.get()))}\n")
            file1.write(f" B = {ifgreaterthan1(float(i.g_spin.get()))}\n")
            file1.write(f" G = {ifgreaterthan1(float(i.b_spin.get()))}\n")
            file1.write(f"  {i.hex_spin.get()}\n")

        file1.close()
        webbrowser.open(f"{config.get('main', 'SaveLocation')}/{self.export_name.get()}_colours_info.txt")

    # ----------------------------- Screenshot Start ----------------------------- #
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
        self.image.save("screenshot.png")
        rgb_tuple = self.image.getpixel((1, 1))  # Gets SRGB8 of centre pixel
        lsrgb_tuple = RGBtoNLSRGB(rgb_tuple) # Convert RBG8 to SRGB [0,1]
        add_frame(lsrgb_tuple[0], lsrgb_tuple[1], lsrgb_tuple[2], True)  # Sends RBG values to add_frame

    # ------------------------------- Screenshot End ------------------------------- #


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
    on_top_var = tk.IntVar(value=config.get('main', 'OnTop'))
    dark_mode = tk.IntVar()
    dummy1 = tk.IntVar()
    dummy2 = tk.IntVar()

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

        # Create setting for File Location
        self.directory_button = tk.Button(self.master, text="Select Save Location", command=self.getFilepast)
        self.folder_location = tk.StringVar(self.master, f"{config.get('main', 'SaveLocation')}")
        self.directory_display = tk.Entry(self.master, width=36, font="Calibri", textvariable=self.folder_location
                                          , state="disabled")

        # .label_frame.grid(column=0, row=0, sticky='w')
        self.label_frame.grid(column=0, row=0, sticky='w', pady=5)
        self.hotkey_frame.grid(column=0, row=1, sticky='w', pady=5)
        self.on_top.grid(column=0, row=1, sticky='w')
        self.dark_mode.grid(column=0, row=2, sticky='w')
        self.hotkey1.grid(column=0, row=1, sticky='w')
        self.hotkey2.grid(column=0, row=2, sticky='w')
        self.directory_button.grid(column=0, row=3, sticky='w')
        self.directory_display.grid(column=1, row=3, sticky='w')
        self.save_button.grid(column=0, row=10, sticky='w')

        # Check config to apply settings
        root.attributes('-topmost', config.get('main', 'OnTop'))

    def update_settings(self):
        config.set('main', 'OnTop', f"{Settings.on_top_var.get()}")
        with open('config.ini', 'w') as f:
            config.write(f)
        root.attributes('-topmost', config.get('main', 'OnTop'))

    # Initialise windows directory selection and save within config
    def getFilepast(self):
        # Open dialog box to select file and saves location to config
        self.pathpast = filedialog.askdirectory(initialdir="/", title="Select Directory")
        config.set('main', 'SaveLocation', self.pathpast)
        with open('config.ini', 'w') as f:
            config.write(f)

        # Updates file location box
        self.folder_location = tk.StringVar(self.master, f"{config.get('main', 'SaveLocation')}")
        self.directory_display.config(text=self.folder_location)
        self.directory_display.grid(column=1, row=3, sticky='w')


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
    # Passed in is screenshot from add_frame
    def __init__(self, parent_frame, r=0, g=0, b=0, is_screenshot=False):
        # Adds instance to list of instances
        RemovableTint.instances.append(self)

        # Create variables for r, g and b entry boxes
        self.r_contents = tk.StringVar()
        self.r_contents.set("0")
        self.g_contents = tk.StringVar()
        self.g_contents.set("0")
        self.b_contents = tk.StringVar()
        self.b_contents.set("0")

        # TODO: Remove redundant self. tags
        # Initialise all entry boxes and buttons
        tk.Frame.__init__(self, parent_frame, height=5, pady=1)
        self.hex_entry_var = tk.StringVar()
        self.colour_tint_name = EntryWithPlaceholder(self, "Colour Name")

        # Create r, g and b entry boxes with grey 0 placeholder
        self.r_spin = EntryWithPlaceholder(self, "0")
        self.g_spin = EntryWithPlaceholder(self, "0")
        self.b_spin = EntryWithPlaceholder(self, "0")
        self.hex_spin = tk.Entry(self, width=8, font="Calibri", textvariable=self.hex_entry_var, state="disabled")
        self.colour_spin = tk.Label(self, width=4, background="black", relief="ridge")
        self.remove = tk.Button(self, font="Calibri", text="X", command=self.remove)

        # Add textvaribles to the r, g and b entry boxes
        self.r_spin.config(textvariable=self.r_contents)
        self.g_spin.config(textvariable=self.g_contents)
        self.b_spin.config(textvariable=self.b_contents)

        # Resize widgets (workaround to sizing bug)
        self.r_spin.config(width=5)
        self.g_spin.config(width=5)
        self.b_spin.config(width=5)
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

        # Trace r,g, b entry box variables, running value_change when they change
        self.r_contents.trace('w', self.value_change)
        self.g_contents.trace('w', self.value_change)
        self.b_contents.trace('w', self.value_change)

        # If screenshot is true then use screenshot values
        if is_screenshot:
            print("screenshot")
            self.r_contents.set(str(r))
            self.g_contents.set(str(g))
            self.b_contents.set(str(b))
            self.hex_conversion()

    # Get hex value and update colour
    def hex_conversion(self):
        # Tests if incorrect entry and highlights red
        if KierensStupidTest(self.r_spin.get()):
            self.r_spin.config(background="white")
        else:
            self.r_spin.config(background="red")

        if KierensStupidTest(self.g_spin.get()):
            self.g_spin.config(background="white")
        else:
            self.g_spin.config(background="red")

        if KierensStupidTest(self.b_spin.get()):
            self.b_spin.config(background="white")
        else:
            self.b_spin.config(background="red")

        # Try to convert the values
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

    def value_change(self, *args):
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
# If add frame called from anywhere but screenshot does not provide Bool
def add_frame(r=0, g=0, b=0, is_screenshot=False):
    RemovableTint(home_frame, r, g, b, is_screenshot).pack(fill=tk.X)
    RemovableTint.hex_conversion(RemovableTint.instances[-1])
    # print(RemovableTint.instances)


# Setting up global key binds
def on_key_press(event):
    # Enter key
    if event.keycode == 13:
        add_frame()
    # Escape key
    if event.keycode == 27:
        # Delete last tint frame instance
        RemovableTint.instances[-1].delete_last()
        print(RemovableTint.instances)
    # Print keypress for debugging
    # print(f"Key Press - char:{event.keycode}, readable: {event.char}")


# TODO: Choose output file

def main():
    Settings(settings_frame)
    About(about_frame)
    Home(home_frame)
    root.mainloop()


if __name__ == "__main__":
    main()
