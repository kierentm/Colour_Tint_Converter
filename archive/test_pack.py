from tkinter import *

window = Tk()
window.title("List")
window.geometry("700x450")
window.configure(bg="orange red")

# center this label
lbl1 = Label(window, text="List", bg="orange red", fg="white", font="none 24 bold")
lbl1.config(anchor=CENTER)
lbl1.pack()

lbl2 = Label(window, text="Enter something here:", bg="orange red", fg="white", font="none 12 bold")
lbl2.config(anchor=CENTER)
lbl2.pack()

window.mainloop()