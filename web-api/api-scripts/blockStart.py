from blockchain import * 
from datetime import datetime
#from save import save

def initialize():
    block1 = None
    wallets = []
    
    block1 = blockchain(2,0.2) # Mining Difficulty and reward

    block1.addTransaction(transaction("person1", "person2", 10))
    block1.handleTransaction("person1") # Mining reward + 0.2

    wallet1 = wallet("person1", "person1")
    wallet1.updateTransactions(block1)

    wallet2 = wallet("person2", "person2")
    wallet2.updateTransactions(block1)

    wallets = [wallet1, wallet2]
   # save(block1, wallets)
    newDatabase = database()
    newDatabase.saveDatabase(block1, wallets, "./public/")
    print("Blockchain is successfully initialized.") 

if __name__ == '__main__':
    initialize()
