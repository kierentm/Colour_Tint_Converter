import tkinter as tk
from tkinter import ttk, Toplevel

from PIL import ImageGrab

from utility_functions import nonlinearsrgbtolinear
import webcolors
from configparser import ConfigParser
import pathlib

root = tk.Tk()

p1 = tk.PhotoImage(file='../Design Images/CTC.png')
root.iconphoto(False, p1)

root.title("Colour Tint Master")
root.geometry('450x500')

# Initialise Tab Parent Notebook
tab_parent = ttk.Notebook(root)

btn_clr = "#AA3F00"
btn_clr_active = "#212124"
bg_clr = "#f4f4f4"

# Define Tabs - MAIN TABS TO REFERENCE
home_frame = ttk.Frame(tab_parent, borderwidth=5, relief="groove")
btn_frame_left = ttk.Frame(home_frame, borderwidth=5, relief="groove")
btn_frame_right = ttk.Frame(home_frame, borderwidth=5, relief="groove")

# Add Tabs to Tab Parent
tab_parent.add(home_frame, text="Home")

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

# TODO: Toggle Dark mode

# TODO: Add hotkeys (update all colours, toggle keep on top .etc)

# TODO: Add Comments
# TODO: Add program icon
# TODO: Make text white when all three numbers are below 0.1 (practically black)
# TODO: Add colour picker tool
plus_ico = tk.PhotoImage(file="../UI_Images/Plus_Icon_Test4.png")
pipette_ico = tk.PhotoImage(file="../UI_Images/Pipette_Icon4.png")
export_ico = tk.PhotoImage(file="../UI_Images/Export_txt_2.png")


class Home:
    tracer_win: Toplevel

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        # Create Entry and Colour Frame
        self.entry_frame = tk.Frame(self.master)

        self.entry_btn = tk.Button(self.entry_frame, image=plus_ico, bg=btn_clr,
                                   activebackground=btn_clr_active, bd="3", height="22", command=add_frame)
        self.divider = tk.Label(self.entry_frame, bg=bg_clr, width="0", padx="1")
        self.colour_btn = tk.Button(self.entry_frame, image=pipette_ico, bg=btn_clr,
                                    activebackground=btn_clr_active, bd="3", height="22", command=self.screenshot)

        # Pack the stuff
        self.entry_frame.pack(side="top", fill=tk.X, pady=(0, 5))
        self.entry_btn.pack(side="left", fill=tk.X, expand=True)
        self.divider.pack(side="left")
        self.colour_btn.pack(side="left", fill=tk.X, expand=True)

        root.bind('<KeyPress>', on_key_press)

    # ----------------------------- Screenshot ----------------------------- #
    def screenshot(self):
        self.tracer_win = tk.Toplevel(self.master)
        self.tracer_win.attributes("-fullscreen", True)
        # self.tracer_win.overrideredirect(1)
        self.tracer_win.attributes('-alpha', 0.3)  # to make toplevel
        self.tracer_win.attributes('-topmost', True)
        self.tracer_win.bind("<Button-1>", self.capture)

    def capture(self, event):
        print(event)
        x, y = event.x, event.y
        self.tracer_win.destroy()
        image = ImageGrab.grab()
        image = image.crop((x, y, x + 2, y + 2))
        image = image.convert('RGB')
        image.save("screenshot.png")
        r, g, b = image.getpixel((1, 1))

        add_frame(r / 255, g / 255, b / 255, True)
        print(r, g, b)


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

    def __init__(self, parent_frame, r=0, g=0, b=0, is_screenshot=False):
        # Adds instance to list of instances
        RemovableTint.instances.append(self)

        # Create variables for r, g and b entry boxes
        self.r_contents = tk.StringVar()
        self.g_contents = tk.StringVar()
        self.b_contents = tk.StringVar()

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
        self.colour_spin = tk.Label(self, width=4, background="black")
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

        if is_screenshot:
            print("screenshot")
            self.r_contents.set(str(r))
            self.g_contents.set(str(g))
            self.b_contents.set(str(b))
            self.hex_conversion()

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
def add_frame(r=0, g=0, b=0, is_screenshot=False):
    RemovableTint(home_frame, r, g, b, True).pack(fill=tk.X)
    RemovableTint.hex_conversion(RemovableTint.instances[-1])
    # print(RemovableTint.instances)

def on_key_press(event):
    # Enter key
    if event.keycode == 13:
        add_frame()
    # Escape key
    if event.keycode == 27:
        # Delete last tint frame instance
        RemovableTint.instances[-1].delete_last()
        print(RemovableTint.instances)


def main():
    Home(home_frame)
    root.mainloop()


if __name__ == "__main__":
    main()
