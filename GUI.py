import tkinter as tk
import Signatures
import time

def keyGen():
    pass

def send(f):
    popup = tk.Tk()
    how_much = float(f['amt'].get())
    whom_to = f['recipient'].get()
    A=tk.Label(popup, text = "Sending " + str(how_much) + " to ")
    A.grid(row=0,column=0)
    B=tk.Label(popup, wraplength=350, text = str(whom_to))
    B.grid(row=1,column=0)
    C=tk.Label(popup, text="...")
    C.grid(row=2,column=0)
    popup.update()
    print("Waiting")
    time.sleep(2)
    print("Done waiting")
    A.destroy()
    B.destroy()
    C.destroy()
    tk.Label(popup,text = "Done!").grid(row=1,column=0)
    
root = tk.Tk()

w=tk.Label(root,text="EasyCoin GUI")
w.pack()

frame = tk.Frame(root)
frame.pack()

pr1,pu1 = Signatures.generate_keys()
tk.Label(frame, text="My Address: ").grid(row=2,column=1)
tk.Label(frame, wraplength=350, text=str(Signatures.public_key_to_ssl(pu1))).grid(row=2,column=2)
tk.Label(frame, text="Balance:    " + str(1.234)).grid(row=3, column=1)

tk.Label(frame, text="Send  ").grid(row=4, column=1)
amt = tk.Entry(frame)
amt.grid(row=4, column=2)
print(type(amt))
tk.Label(frame, text="   to   ").grid(row=4, column=3)
recipient = tk.Entry(frame, width=25)
recipient.grid(row=4, column=4)
tk.Button(frame, text="Send", fg='green', command=(lambda d={'amt':amt,'recipient':recipient}: send(d))).grid(row=4, column=5)


tk.Button(frame, text="Generate new keys", fg="blue",
                           command=keyGen).grid(row=8,column=1)

tk.Button(frame, text="QUIT", fg="gray", command=quit).grid(row=8, column=3)


root.mainloop()
