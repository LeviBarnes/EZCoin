import tkinter as tk
import Signatures
import time
import pickle
from BlockChain import TxBlock
import FileIO
from EZCoinSocket import sendMessage, recvNewObject
from EZCoinSocket import newClientSocket, newServerSocket
from Transactions import Tx

txfee = 0.01

def keyGen():
    pass

def send(f):
    popup = tk.Tk()
    how_much = float(f['amt'].get())
    whom_to = f['recipient'].get()
    private = f['pr']
    public = f['pu']
    A=tk.Label(popup, text = "Sending " + str(how_much) + " to ")
    A.grid(row=0,column=0)
    B=tk.Label(popup, wraplength=350, text = str(whom_to))
    B.grid(row=1,column=0)
    C=tk.Label(popup, text="...")
    C.grid(row=2,column=0)
    popup.update()
    newTx = Tx()
    newTx.add_output(whom_to, how_much)
    newTx.add_input(public, how_much*(1+txfee))
    newTx.sign(private)

    cSock = newClientSocket()
    sendMessage(newTx, cSock)
    
    A.destroy()
    B.destroy()
    C.destroy()
    tk.Label(popup,text = "Done!").grid(row=1,column=0)

def LoadBlockChain(filename):
    try:
        return FileIO.loadBC(filename)
    except:
        print("Failed to load block chain. Generating new one.")
        return TxBlock(None)

def LoadKeys(filename):
    try:
        return FileIO.loadKeys(filename)
    except:
        print("Failed to load keys. Generating.")
        return Signatures.generate_keys()

def startGUI(pr,pu,headBlock):
    root = tk.Tk()

    w=tk.Label(root,text="EasyCoin GUI")
    w.pack()

    frame = tk.Frame(root)
    frame.pack()

    tk.Label(frame, text="My Address: ").grid(row=2,column=1)
    tk.Label(frame, wraplength=350, text=str(Signatures.public_key_to_ssl(pu))).grid(row=2,column=2)
    tk.Label(frame, text="Balance:    " + str(headBlock.getBalance(pu))).grid(row=3, column=1)

    tk.Label(frame, text="Send  ").grid(row=4, column=1)
    amt = tk.Entry(frame)
    amt.grid(row=4, column=2)
    tk.Label(frame, text="   to   ").grid(row=4, column=3)
    recipient = tk.Entry(frame, width=25)
    recipient.grid(row=4, column=4)
    tk.Button(frame, text="Send", fg='green', command=
                 (lambda d={'amt':amt,'recipient':recipient, 'pu':pu, 'pr':pr}: send(d))).grid(row=4, column=5)


    #tk.Button(frame, text="Generate new keys", fg="blue",
    #                       command=keyGen).grid(row=8,column=1)

    tk.Button(frame, text="QUIT", fg="gray", command=quit).grid(row=8, column=3)


    root.mainloop()

head = LoadBlockChain("BlockChain.dat")
pr,pu = LoadKeys("prkey3.dat")
startGUI(pr,pu,head)

