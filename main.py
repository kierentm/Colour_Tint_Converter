import tkinter as tk
from tkinter import ttk
from convert import nonlinearsrgbtolinear
import webcolors
import webbrowser

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

# Add content to about frame
AboutContent = tk.Label(about_frame, text="Tool developed by Kieren Townley-Moss, Jake Broughton and Alex Todd")
AboutContent.grid(column=0, row=0)


# TODO: Settings
# TODO: Keep window on top toggle
# TODO: Toggle Dark mode

# TODO: Add hotkeys (update all colours, toggle keep on top .etc)

# TODO: Output colours to txt file button

# TODO: Add Comments
# TODO: Add program icon
# TODO: Make text white when all three numbers are below 0.1 (practically black)
# TODO: Figure out if entry boxes can have grey text label when nothing is in the box
# TODO: Add colour picker tool

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
        # TODO: Need to check hex value as might be a rounding error when producing rgb8 values (and test generally)

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
    print(RemovableTint.instances)


def filewrite():
    file1 = open("Text" + "_Colors.txt", "w+")
    for i in RemovableTint.instances:
        file1.write(f"Colour Name = {i.colour_tint_name.get()}\n")
        file1.write(i.r_spin.get())
        file1.write(i.g_spin.get())
        file1.write(i.b_spin.get())
        file1.write(i.hex_spin.get())

    item_name = ""

    # L = [item_name+"\n", "R = 0.1\n", "G = 0.1\n", "B = 0.1\n", "#FFFFFF"]
    # file1.writelines(L)
    file1.close()
    webbrowser.open("Text_Colors.txt")

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
    print(f"Key Press - char:{event.keycode}, readable: {event.char}")


# TODO: Choose output file

# TODO: Add Column names


btn = tk.Button(home_frame, text="Add Entry", width=5, command=add_frame)
btn2 = tk.Button(home_frame, text="Export .txt", command=filewrite)
btn3 = tk.Button(home_frame, text="Fetch all")

btn.pack(side="bottom", fill=tk.X)
btn2.pack(side="bottom", fill=tk.X)
btn3.pack(side="bottom", fill=tk.BOTH)

root.bind('<KeyPress>', on_key_press)
home_frame.mainloop()
