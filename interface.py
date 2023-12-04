from Tkinter import *
#import project

root = Tk()

root.title("BNV Driver")

def sync():
    None

Label(root, text="Commands").grid(column=0, row=0)
Button(root, text="Sync", command=sync).grid(column=0, row=1)
Button(root, text="Poll", command=sync).grid(column=0, row=2)
Button(root, text="Set inhibits", command=sync).grid(column=0, row=3)
Button(root, text="Enable", command=sync).grid(column=0, row=4)
Button(root, text="Set up request", command=sync).grid(column=0, row=5)
Entry(root,width=30).grid(column=0, row=6)


root.geometry("300x300")
root.mainloop()
