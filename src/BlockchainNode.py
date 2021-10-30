from Blockchain import *
from Transaction import Transaction

import json


class DataConverter:

    def dumpBlockchainData(self, blockchain) -> list:
        blocks = []
        blockCounter = 0

        for block in blockchain.blockchain:
            newBlock = {
                "blockNumber": blockCounter,
                "previousHash": block.previousBlockHash,
                "blockHash": block.blockHash,
                "hashDifficulty": block.hashDifficulty,
                "validationTime": block.validationTime
            }

            transactions = []
            for blockTransaction in block.blockTransactions:
                newTransaction = {
                    "source":  blockTransaction.source,
                    "destination": blockTransaction.destination,
                    "balance": blockTransaction.coins,
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
            tempBlock.hashDifficulty = block["block"]
            ["hashDifficulty"]
            tempBlock.blockHash = block["block"]["blockHash"]
            tempBlock.validationTime = block["block"]["validationTime"]
            tempBlock.blockTransactions = []
            for transaction in block["blockTransactions"]:
                tempTransaction = Transaction.initializeTransaction(
                    transaction["source"],
                    transaction["destination"],
                    transaction["balance"],
                    transaction["transactionHash"],
                    transaction["transactionSignature"],
                    transaction["validationTime"]
                )

                tempBlock.blockTransactions.append(tempTransaction)

            loadedBlockchain.blockchain.append(tempBlock)

        return loadedBlockchain


class BlockDataIO():
    def readDataAndImport(self, path) -> Blockchain:
        with open(path, 'r') as f:
            return self.importDataGenerateBlockchain(f.read())

    def importDataGenerateBlockchain(self, blockchainData) -> Blockchain:
        return DataConverter().loadBlockchainData(blockchainData)

    def exportData(self, blockchain, path):
        jsonData = DataConverter().dumpBlockchainData(blockchain)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(jsonData, f, ensure_ascii=False, indent=4)


# TODO
class NodeNetwork:
    def __init__(self):
        pass

    def getBlockchainData(self) -> Blockchain:
        # some network stuff here
        receivedBlockchainData = []
        converter = DataConverter()
        return converter.loadBlockchainData(receivedBlockchainData)

    def sendBlockchainData(self, blockchain):
        converter = DataConverter()
        # send(converter.dumpBlockchainData(blockchain))

    def sendBlock(self):
        pass

    def receiveBlock(self):
        pass
