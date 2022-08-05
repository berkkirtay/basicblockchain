from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
import threading
import numpy as np
from datetime import datetime
import time
import matplotlib.pyplot as plt
from hashlib import sha256


from Blockchain import *
#from p2pserver import *

block1 = None  # block1
wallets1 = []

# Database will save and load after every transaction or mining operation.
newDatabase = database()


def load():
    global block1, wallets1, newDatabase
    newDatabase.loadDatabase("")
    block1 = newDatabase.blockchain
    wallets1 = newDatabase.wallets


try:
    load()
except:
    print("New blockchain is created.")
    block1 = blockchain(4, 0.2)


#block1 = None
# address = socket.gethostbyname(socket.gethostname()) # '127.0.0.1'
#newNetwork = p2p(block1, address, 8000)

#block1 = newNetwork.blockchain
# def refreshNetwork():
    #global block1
    # while True:
    # newNetwork.refreshBlockchain(block1)
    # time.sleep(2)

#p2pThread = threading.Thread(target=refreshNetwork)
# p2pThread.start()


root = Tk()
root.title("Coin GUI")
root.geometry("480x360")

tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab_control.add(tab1, text='My Wallet')


tab_control.pack(expand=1, fill='both')

# Welcoming Screen
welcomingLabel = Label(tab1, text="Coin GUI Wallet")
welcomingLabel.place(x=180, y=10)

# Credentials
publicNameLabel = Label(tab1, text="Public Key: ")
publicNameLabel.place(x=20, y=60)
publicName = Entry(tab1, width=40)
publicName.place(x=120, y=60)

privateKeyLabel = Label(tab1, text="Private Key: ")
privateKeyLabel.place(x=20, y=110)
privateKey = Entry(tab1, width=40)
privateKey.place(x=120, y=110)

# New wallet


def onCreateWallet():
    subwindow = Toplevel(root)
    subwindow.title("New Wallet")
    subwindow.geometry("240x140")

    registerLabel = Label(
        subwindow, text="Plase enter a random nickname\n for your wallet.")
    registerLabel.place(x=10, y=0)

    publicNameRegister = Entry(subwindow, width=20)
    publicNameRegister.place(x=40, y=50)
    publicNameRegister.focus()

    def getPublicName():
        if publicNameRegister.get() == "":
            messagebox.showerror("Error!", "Public name register error!")
        try:
            return publicNameRegister.get()
        except:
            messagebox.showerror("Error!", "Public name register error!")

    def createNewWallet():
        newpublicName = getPublicName()
        # Handle public address here later!!
        newWallet = wallet(newpublicName, newpublicName)
        newWallet.updateTransactions(block1)
        wallets1.append(newWallet)  # hash(getPublicName())
        publicName.insert(0, newpublicName)
        privateKey.insert(0, newWallet.privateAddress)
        messagebox.showinfo(
            "Success!", f"Wallet is created! Please don't forget your public and private keys!\nPublic key = {newWallet.publicAddress}\nPrivate key = {newWallet.privateAddress}", command=subwindow.destroy())
        # Force transaction
        #block1.forceTransaction(transaction("null", newpublicName, 100))
        newDatabase.saveDatabase(block1, wallets1, "")
    registerButton = Button(subwindow, text="Enter", command=createNewWallet)
    registerButton.place(x=90, y=90)


createWalletButton = Button(
    tab1, text="Create a new wallet", command=onCreateWallet)
createWalletButton.place(x=300, y=200)

# Transactions
getBalance = StringVar()

availableCoinsLabel = Label(tab2, textvariable=getBalance)
availableCoinsLabel.place(x=10, y=10)

transactionLabel1 = Label(tab2, text="Public Address: ")
transactionLabel1.place(x=10, y=70)
transactionEntry1 = Entry(tab2, width=35)
transactionEntry1.place(x=120, y=70)

transactionLabel2 = Label(tab2, text="Coin Amount: ")
transactionLabel2.place(x=10, y=100)
transactionEntry2 = Entry(tab2, width=35)
transactionEntry2.place(x=120, y=100)

transactionLabel3 = Label(tab2, text="Transaction History:")
transactionLabel3.place(x=6, y=150)


logIndex = 1
logs = scrolledtext.ScrolledText(tab2, width=57, height=9)
logs.place(x=6, y=170)

# There are bugs on transactions!!


def onTransaction():
    ########################################
    load()
    global index, logIndex
    if block1.addTransaction(transaction(wallets1[index].publicAddress, transactionEntry1.get(), int(transactionEntry2.get()))) == False:
        logs.insert(INSERT, f'{logIndex}. {block1.lastBlockLog}\n')
    else:
        logs.insert(
            INSERT, f'{logIndex}. Transaction is pending: from {wallets1[index].publicAddress} to {transactionEntry1.get()}, amount={int(transactionEntry2.get())}\n')
    logIndex += 1
    global getBalance
    getBalance.set(wallets1[index].updateTransactions(block1))
    newDatabase.saveDatabase(block1, wallets1, "")
    ########################################


transactionButton = Button(tab2, text="Send", command=onTransaction)
transactionButton.place(x=350, y=130)

# Login
index = -1


def onLogin():
    global index
    for i in range(len(wallets1)):
        if publicName.get() == wallets1[i].publicAddress:
            index = i
            break

    if index == -1 or wallets1[index].privateAddress != privateKey.get():
        messagebox.showerror("Error!", "Wallet Credentials error!")
        return -1

    publicNameLabel2 = Label(tab1, text=publicName.get())
    publicName.destroy()
    publicNameLabel2.place(x=120, y=60)
    privateKey.destroy()
    loginButton.destroy()
    privateKeyLabel.destroy()
    createWalletButton.destroy()
    tab_control.add(tab2, text='Transactions')
    tab_control.add(tab3, text='Coin Mining')

    global getBalance
    getBalance.set(wallets1[index].updateTransactions(block1))
    balanceLabel = Label(tab1, textvariable=getBalance)
    balanceLabel.place(x=20, y=110)

    balanceLabel = Label(tab3, textvariable=getBalance)
    balanceLabel.place(x=10, y=110)

    def setBalance():
        global index
        while True:
            getBalance.set(wallets1[index].updateTransactions(block1))
            time.sleep(2)

    balanceThread = threading.Thread(target=setBalance)
    balanceThread.start()

    def onMining():
        miningProgress = ttk.Progressbar(
            tab3, orient=HORIZONTAL, length=250, mode="determinate")
        miningProgress.place(x=20, y=150)
        process = IntVar()

        def miningLoop():
            ########################################
            load()
            global index
            for i in range(int(int(miningAmount.get()) / block1.miningReward) + 1):
                # Mining reward + 0.2 / wallets[index].publicAddress
                block1.handleTransaction(str(miningAddress.get()))
                getBalance.set(wallets1[index].updateTransactions(block1))
                process.set(
                    int((i + 1) / (int(miningAmount.get()) / block1.miningReward) * 100))
                miningProgress['value'] = int(
                    (i + 1) / (int(miningAmount.get()) / block1.miningReward) * 100)
                miningProgress.update_idletasks()

            miningCompletedLabel.configure(text="Completed!")
            miningLabel.destroy()
            miningCompletedLabel.destroy()
            newDatabase.saveDatabase(block1, wallets1, "")
            ########################################

        thread = threading.Thread(target=miningLoop)
        thread.daemon = True
        thread.start()

        miningCompletedLabel = Label(tab3, text="%")
        miningCompletedLabel.place(x=295, y=150)
        miningLabel = Label(tab3, textvariable=process)
        miningLabel.place(x=275, y=150)

    miningLabel1 = Label(tab3, text="Enter the public address for rewards: ")
    miningLabel1.place(x=10, y=10)
    miningAddress = Entry(tab3, width=15)
    miningAddress.place(x=310, y=10)

    miningLabel2 = Label(
        tab3, text="Enter the amount of coins you want to farm: ")
    miningLabel2.place(x=10, y=40)
    miningAmount = Entry(tab3, width=15)
    miningAmount.place(x=310, y=40)

    miningButton = Button(tab3, text="Start Mining!", command=onMining)
    miningButton.place(x=350, y=90)


loginButton = Button(tab1, text="Login", command=onLogin)
loginButton.place(x=400, y=150)


root.mainloop()
