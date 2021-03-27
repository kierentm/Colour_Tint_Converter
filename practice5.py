from tkinter import *
root = Tk()
canvas = Canvas(root, width = 1200, height = 600)
canvas.pack()
img = PhotoImage(file="UI_Stuff/20i-resistance.png")
canvas.create_image(20,20, anchor=NW, image=img)
mainloop()