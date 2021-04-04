import tkinter as tk
import sys
import os

# --- classes ---


class App:

    def __init__(self, master):
        self.master = master

        question_label = tk.Label(master, text="There's a troll in the dungeon")
        question_label.pack(side="top", fill='x')

        button_bonus = tk.Button(master, text="Restart", command=self.restart_window)
        button_bonus.pack(fill='x')

        button_close = tk.Button(master, text="Close", command=master.destroy)
        button_close.pack(fill='x')

    def restart_window(self):
        window = tk.Toplevel()

        question_label = tk.Label(window, text="Saving requires a program restart \n Would you like to restart now?")
        question_label.pack(side="top", fill='x')

        button_bonus = tk.Button(window, text="Yes", command=self.restart_program)
        button_bonus.pack(fill='x')

        button_close = tk.Button(window, text="No", command=window.destroy)
        button_close.pack(fill='x')

    @staticmethod
    def restart_program():
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, *sys.argv)

# --- main ---


root = tk.Tk()
app = App(root)
root.mainloop()
