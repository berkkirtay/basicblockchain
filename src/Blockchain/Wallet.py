from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import json
import pathlib
from Blockchain import Blockchain


# A general purpose wallet for blockchain.

class Wallet():
    ownerName = ''
    publicKey = ''  # aka source
    privateKey = ''
    coins = 0
    creationTime = None
    keySize = 1024

    def __init__(self, ownerName: str):
        self.ownerName = ownerName
        self.createNewWallet()

    def createNewWallet(self):
        self.creationTime = datetime.now().strftime("%H:%M:%S")
        self.generateKeyPair()
        self.exportKeyPair()
        self.done()

    def generateKeyPair(self):
        randomGenerator = Random.new().read
        keyPair = RSA.generate(self.keySize, randomGenerator)
        privateKey = keyPair.exportKey('PEM')
        self.privateKey = base64.b64encode(privateKey).decode("ascii")

        publicKey = keyPair.publickey().exportKey('PEM')
        self.publicKey = base64.b64encode(publicKey).decode("ascii")

        # Here we shorten public key by removing the trivial parts.
        self.publicKey = self.publicKey[87:-44]

    def exportKeyPair(self):
        keypair = {
            "wallet_user_name": self.ownerName,
            "private_key": self.privateKey
        }
        pathlib.Path('./key_pair_exports').mkdir(exist_ok=True)
        with open('./key_pair_exports/' + self.ownerName + '_key_pair.json', 'w', encoding='utf-8') as f:
            json.dump(keypair, f, ensure_ascii=False, indent=4)

    @classmethod
    def importWallet(self, ownerName):
        keypair = dict()
        pathlib.Path('./key_pair_exports').mkdir(exist_ok=True)
        with open('./key_pair_exports/' + ownerName + '_key_pair.json', 'r', encoding='utf-8') as f:
            keypair = json.load(f)

        keyPair = RSA.import_key(base64.b64decode(keypair["private_key"]))
        private_key = keyPair.export_key('PEM')
        public_key = keyPair.publickey().exportKey('PEM')

        wallet = Wallet(ownerName)

        wallet.privateKey = base64.b64encode(private_key).decode("ascii")
        wallet.publicKey = base64.b64encode(public_key).decode("ascii")
        wallet.publicKey = wallet.publicKey[87:-44]

        print(f"Wallet {ownerName} is imported.")
        return wallet

    def done(self):
        print(
            f'A new public and private key pair is generated for : {self.ownerName}.')
        print(
            'Please back up your key pair in order to keep an access to your transactions and wallet.')
        print(f'Your key pair is exported as a json file.\n')

    # Updating the Wallet's owner balance.

    def updateTransactions(self, blockchain: Blockchain):
        self.coins = blockchain.getBalance(self.publicKey)
        return f'Coins in the Wallet: {self.coins}'

    def getBalance(self, blockchain) -> int:
        self.updateTransactions(blockchain)
        return self.coins


class WalletChecker():
    Wallets = []

    def __init__(self, Wallets: list):
        self.Wallets = Wallets

    def addWallet(self, newWallet: Wallet):
        for Wallet in self.Wallets:
            if Wallet.publicAddress == newWallet.publicAddress:
                print("You can't use an existed Wallet name!")
                return

        self.Wallets.append(newWallet)
