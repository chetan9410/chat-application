from tkinter import *
from turtle import title

root = Tk()
root.title("test")

scrollbar = Scrollbar(root)
scrollbar.pack( side = RIGHT, fill = Y )

mylist = Listbox(root, xscrollcommand = scrollbar.set )
for line in range(20):
   mylist.insert(END, "This is line number " + str(line))

mylist.pack( side = LEFT, fill = BOTH )
scrollbar.config( command = mylist.yview )

mainloop()