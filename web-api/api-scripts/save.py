from blockchain import * 
from blockStart import *
import json

newDatabase = database()

def save(block, wallets):
    newDatabase.saveDatabase(block, wallets, "./public/")

    walletJSON = {"users": []}
    # NO DUPLICATE WALLETS!! USE ALLWALLETS IN BLOCKCHAIN.PY !!
    for user in wallets:
        newUser = {
            "name": user.publicAddress,
            "balance": block.getBalance(user.publicAddress),
            "hashValue": block.blockchain[0].blockHash
        }
        walletJSON["users"].append(newUser)
        
    with open('./public/walletData.json', 'w', encoding='utf-8') as f:
        json.dump(walletJSON, f, ensure_ascii=False, indent=4)

def loadBlock():
    try:
        newDatabase.loadDatabase("./public/")
        return newDatabase.blockchain
    except:
        initialize()
        return loadBlock()

def loadWallets():
    try:
        newDatabase.loadDatabase("./public/")
        return newDatabase.wallets
    except:
        initialize()
        return loadWallets()
