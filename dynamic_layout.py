# File to test the dynamic addition of widgets
import tkinter as tk
import webcolors

root = tk.Tk()
root.title("Colour Tint Converter")
root.geometry('450x400')


class RemovableTask(tk.Frame):
    instances = []

    def __init__(self, master):
        self.__class__.instances.append(self)
        tk.Frame.__init__(self, master, borderwidth=10, relief="groove")

        self.hex_colour = "#ffffff"

        self.colour_tint_name = tk.Entry(self, width=18, bg="gray40", fg="white", font="Calibri")
        self.r_spin = tk.Entry(self, width=4, bg="gray40", fg="white", font="Calibri")
        self.g_spin = tk.Entry(self, width=4, bg="gray40", fg="white", font="Calibri")
        self.b_spin = tk.Entry(self, width=4, bg="gray40", fg="white", font="Calibri")
        self.hex_spin = tk.Entry(self, width=10, bg="gray40", fg="white", font="Calibri", textvariable=self.hex_colour)
        self.update = tk.Button(self, text="Update", bg="gray40", fg="white", font="Calibri",
                                command=self.hex_conversion)
        self.remove = tk.Button(self, width=1, bg="gray40", fg="white", font="Calibri",
                                text="X", command=self.destroy)

        self.colour_tint_name.grid(column=1, row=2)
        self.r_spin.grid(column=2, row=2)
        self.g_spin.grid(column=3, row=2)
        self.b_spin.grid(column=4, row=2)
        self.hex_spin.grid(column=5, row=2)
        self.update.grid(column=6, row=2)
        self.remove.grid(column=7, row=2)

    def hex_conversion(self):
        r_value = self.r_spin.get()
        g_value = self.g_spin.get()
        b_value = self.b_spin.get()
        try:

            r_value = int(255 * float(r_value))
            g_value = int(255 * float(g_value))
            b_value = int(255 * float(b_value))

            hex_value = webcolors.rgb_to_hex((r_value, g_value, b_value))
            print(hex_value)
        except ValueError:
            # print(ValueError)
            pass

        print(r_value, g_value, b_value)

    def test_command(self):
        print(self.r_spin.get())

    @classmethod
    def print_instances(cls):
        for instance in cls.instances:
            print(instance)


def add_tint():
    RemovableTask(root).pack()
    print("running add_tint")
    RemovableTask.print_instances()


add_btn = tk.Button(text="add tint", command=add_tint)
add_btn.pack()

root.mainloop()
