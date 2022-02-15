import pathlib
from src.Blockchain.Blockchain import Blockchain, Block
from src.Transaction.Transaction import Transaction

import json


class DataConverter:
    def dumpBlochcainDataAsStr(self, blockchain) -> str:
        data = self.dumpBlockchainData(blockchain)
        return json.dumps(data)

    def dumpBlockchainData(self, blockchain) -> list:
        blocks = []
        blockCounter = 0

        for block in blockchain.blockchain:
            newBlock = {
                "blockNumber": blockCounter,
                "previousHash": block.previousBlockHash,
                "blockHash": block.blockHash,
                "blockNonce": block.blockNonce,
                "hashDifficulty": block.hashDifficulty,
                "validationTime": block.validationTime
            }

            transactions = []
            for blockTransaction in block.blockTransactions:
                newTransaction = {
                    "source":  blockTransaction.source,
                    "destination": blockTransaction.destination,
                    "balance": blockTransaction.balance,
                    "transactionMessage": blockTransaction.transactionMessage,
                    "transactionHash": blockTransaction.transactionHash,
                    "transactionSignature": blockTransaction.transactionSignature,
                    "validationTime": blockTransaction.validationTime
                }
                transactions.append(newTransaction)

            blockCounter += 1
            blocks.append({
                "block": newBlock,
                "blockTransactions": transactions.copy()})

        jsonData = {
            "HashDifficulty": blockchain.hashDifficulty,
            "MiningReward": blockchain.miningReward,
            "Blocks": blocks.copy()
        }

        return jsonData

    def loadBlockchainData(self, blockchainData) -> Blockchain:
        blockchainData = json.loads(blockchainData)

        hashDifficulty = blockchainData["HashDifficulty"]
        miningReward = blockchainData["MiningReward"]

        loadedBlockchain = Blockchain(hashDifficulty, miningReward)
        loadedBlockchain.transactions = []
        loadedBlockchain.blockchain = []

        for block in blockchainData["Blocks"]:
            tempBlock = Block(block["block"]["previousHash"],
                              0, {})
            tempBlock.hashDifficulty = block["block"]["hashDifficulty"]
            tempBlock.blockHash = block["block"]["blockHash"]
            tempBlock.blockNonce = block["block"]["blockNonce"]
            tempBlock.validationTime = block["block"]["validationTime"]
            tempBlock.blockTransactions = []
            for transaction in block["blockTransactions"]:
                tempTransaction = Transaction.initializeTransaction(
                    transaction["source"],
                    transaction["destination"],
                    transaction["balance"],
                    transaction["transactionMessage"],
                    transaction["transactionHash"],
                    transaction["transactionSignature"],
                    transaction["validationTime"]
                )

                tempBlock.blockTransactions.append(tempTransaction)

            loadedBlockchain.blockchain.append(tempBlock)

        return loadedBlockchain


class BlockDataIO():
    folderName = './blockchain_data/'

    def __init__(self):
        pathlib.Path(self.folderName).mkdir(exist_ok=True)

    def readDataAndImport(self, path) -> Blockchain:
        with open(self.folderName + path, 'r') as f:
            return self.importDataGenerateBlockchain(f.read())

    def importDataGenerateBlockchain(self, blockchainData) -> Blockchain:
        return DataConverter().loadBlockchainData(blockchainData)

    def exportData(self, blockchain, path):
        jsonData = DataConverter().dumpBlockchainData(blockchain)
        with open(self.folderName + path, 'w', encoding='utf-8') as f:
            json.dump(jsonData, f, ensure_ascii=False, indent=4)
