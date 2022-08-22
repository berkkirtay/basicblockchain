# --------------------------------------
# A data converter module that
# provides blockchain IO between peers.
# Copyright (c) 2022 Berk Kırtay
# --------------------------------------

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
            transactions = []
            for blockTransaction in block.blockTransactions:
                newTransaction = {
                    "source":  blockTransaction.source,
                    "destination": blockTransaction.destination,
                    "balance": blockTransaction.balance,
                    "gas": blockTransaction.gas,
                    "fee": blockTransaction.fee,
                    "transactionMessage": blockTransaction.transactionMessage,
                    "transactionHash": blockTransaction.transactionHash,
                    "transactionSignature": blockTransaction.transactionSignature,
                    "validationTime": blockTransaction.validationTime
                }
                transactions.append(newTransaction)

            newBlock = {
                "blockNumber": blockCounter,
                "previousHash": block.previousBlockHash,
                "blockHash": block.blockHash,
                "blockNonce": block.blockNonce,
                "hashDifficulty": block.hashDifficulty,
                "blockBalance": block.blockBalance,
                "blockFee": block.blockFee,
                "validationTime": block.validationTime,
                "numberOFTransactions": len(transactions),
                "blockTransactions": transactions.copy()
            }
            blockCounter += 1
            blocks.append({
                "block": newBlock})

        jsonData = {
            "HashDifficulty": blockchain.hashDifficulty,
            "GasPrice": blockchain.gasPrice,
            "ChainSize": blockchain.chainSize,
            "Blocks": blocks.copy()
        }

        return jsonData

    def loadBlockchainData(self, blockchainData) -> Blockchain:
        blockchainData = json.loads(blockchainData)

        hashDifficulty = blockchainData["HashDifficulty"]
        gasPrice = blockchainData["GasPrice"]

        loadedBlockchain = Blockchain(hashDifficulty, gasPrice)
        loadedBlockchain.transactions = []
        loadedBlockchain.blockchain = []

        for block in blockchainData["Blocks"]:
            tempBlock = Block(block["block"]["previousHash"],
                              0, {})
            tempBlock.hashDifficulty = block["block"]["hashDifficulty"]
            tempBlock.blockHash = block["block"]["blockHash"]
            tempBlock.blockNonce = block["block"]["blockNonce"]
            tempBlock.blockBalance = block["block"]["blockBalance"]
            tempBlock.blockFee = block["block"]["blockFee"]
            tempBlock.validationTime = block["block"]["validationTime"]
            tempBlock.blockTransactions = []

            for transaction in block["block"]["blockTransactions"]:
                tempTransaction = Transaction.initializeTransaction(
                    transaction["source"],
                    transaction["destination"],
                    transaction["balance"],
                    transaction["gas"],
                    transaction["fee"],
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

    def importData(self, path) -> Blockchain:
        with open(self.folderName + path, 'r') as f:
            return self.importDataGenerateBlockchain(f.read())

    def importDataGenerateBlockchain(self, blockchainData) -> Blockchain:
        return DataConverter().loadBlockchainData(blockchainData)

    def exportData(self, blockchain, path):
        jsonData = DataConverter().dumpBlockchainData(blockchain)
        with open(self.folderName + path, 'w', encoding='utf-8') as f:
            json.dump(jsonData, f, ensure_ascii=False, indent=4)
