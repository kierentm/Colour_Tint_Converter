import tkinter as tk
from PIL import ImageGrab


class Screenshot:
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.window.attributes('-alpha', 0.1)
        self.fullScreenState = True
        self.window.bind("<Button-1>", self.picked)
        self.window.bind("<Escape>", self.quit_picker)

        self.window.mainloop()

    def picked(self, event):
        print(event)
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)
        self.window.destroy()
        x, y = event.x, event.y
        image = ImageGrab.grab()
        image = image.crop((x, y, x + 2, y + 2))
        image = image.convert('RGB')
        self.r, self.g, self.b = image.getpixel((1, 1))

    def quit_picker(self, event):
        print(event)
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)
        self.window.destroy()


if __name__ == '__main__':
    app = Screenshot()
    print(app.r, app.g, app.b)
