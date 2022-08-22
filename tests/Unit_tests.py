# ----------------------------------------
# Functional unit tests for blockchain
# Copyright (c) 2022 Berk Kırtay
# ----------------------------------------

from src.DataConverter.DataConverter import BlockDataIO
from src.Wallet.Wallet import Wallet
from src.Transaction.Transaction import Transaction
from src.Transaction.TransactionSignature import TransactionSignature
from src.Blockchain.Blockchain import Blockchain
from src.BlockchainExceptionHandler.BlockchainExceptionHandler import *
import random
import pytest


class BlockchainFactory:
    def __init__(self):
        pass

    def getBlockchain(self, hashDifficulty, gasPrice) -> Blockchain:
        return Blockchain(hashDifficulty, gasPrice)

    def getBlockchainWithFundedWallet(self, hashDifficulty, gasPrice, publicKey, amount):
        blockchain = Blockchain(hashDifficulty, gasPrice)
        blockchain.forceTransaction(publicKey, amount)
        blockchain.handleTransactions("null")
        return blockchain


blockchainFactory = BlockchainFactory()


def test_blockchainsShouldBeUnique():
    blockchain1 = blockchainFactory.getBlockchain(2, 1)
    blockchain2 = blockchainFactory.getBlockchain(2, 1)
    assert blockchain1.getCurrentBlock(
    ).blockHash != blockchain2.getCurrentBlock().blockHash


def test_shouldCreateTwoDifferentWalletsWithSameName():
    wallet1 = Wallet("person")
    wallet2 = Wallet("person")
    assert wallet1.privateKey != wallet2.privateKey


def test_importedWalletShouldBeWorking():
    wallet1 = Wallet("test")
    blockchain = blockchainFactory.getBlockchainWithFundedWallet(
        1, 10, wallet1.publicKey, 10000)
    wallet2 = Wallet.importWallet("test")

    assert 10000 == wallet2.getBalance(blockchain)
    assert wallet1.privateKey == wallet2.privateKey


def test_shouldSendExpectedAmounts():
    wallet1 = Wallet("person1")
    wallet2 = Wallet("person2")
    blockchain = blockchainFactory.getBlockchainWithFundedWallet(
        1, 1, wallet1.publicKey, 630)

    tempTransaction = Transaction(
        wallet1.publicKey, wallet2.publicKey, 599, wallet1.privateKey)

    blockchain.addTransaction(tempTransaction)
    blockchain.handleTransactions("null")

    blockchain.addTransaction(Transaction(
        wallet2.publicKey, "null", 99, wallet2.privateKey))
    blockchain.handleTransactions(wallet2.publicKey)

    assert 500 == wallet2.getBalance(blockchain)
    assert wallet1.getBalance(blockchain) == 630 - \
        tempTransaction.balance - tempTransaction.fee


def test_shouldReveiceExpectedBlockRewards():
    wallet1 = Wallet("person1")
    wallet2 = Wallet("person2")
    blockchain = blockchainFactory.getBlockchainWithFundedWallet(
        0, 1, wallet1.publicKey, 10000)

    totalBlockRewards = 0
    for i in range(5):
        blockchain.addTransaction(Transaction(
            wallet1.publicKey, "null", 10, wallet1.privateKey))
        blockchain.handleTransactions(wallet2.publicKey)
        totalBlockRewards += blockchain.blockchain[-1].blockFee

    # wallet2 has built 5 blocks, so it will
    # receive 5 block rewards totally.
    assert totalBlockRewards == wallet2.getBalance(blockchain)


def test_shoulNotSendNegativeAmount():
    wallet1 = Wallet("person")
    blockchain = blockchainFactory.getBlockchainWithFundedWallet(
        0, 10, wallet1.publicKey, 10000)

    with pytest.raises(BalanceError) as err:

        blockchain.addTransaction(Transaction(
            wallet1.publicKey, "null", -100, wallet1.privateKey))

        blockchain.handleTransactions(wallet1.publicKey)

    assert "Transaction amount can't be zero or a negative value!" in str(
        err.value)


def test_shouldNotSendIfInsufficientFundInWallet():
    wallet1 = Wallet("person")
    blockchain = blockchainFactory.getBlockchainWithFundedWallet(
        0, 10, wallet1.publicKey, 100)

    with pytest.raises(BalanceError) as err:

        blockchain.addTransaction(Transaction(
            wallet1.publicKey, "null", 90, wallet1.privateKey))
        blockchain.addTransaction(Transaction(
            wallet1.publicKey, "null", 90, wallet1.privateKey))

    assert "Insufficient balance in the source!" in str(err.value)


def test_shouldCheckPendingTransactionBalances():
    blockchain = blockchainFactory.getBlockchain(2, 10)
    wallet1 = Wallet("person")

    with pytest.raises(BalanceError) as err:

        blockchain.addTransaction(Transaction(
            wallet1.publicKey, "null", 10, wallet1.privateKey))

        blockchain.handleTransactions(wallet1.publicKey)

    assert "Insufficient balance in the source!" in str(err.value)


def test_shouldValidateTransactionCorrectly():
    wallet1 = Wallet("person")
    blockchain = blockchainFactory.getBlockchainWithFundedWallet(
        0, 10, wallet1.publicKey, 10000)

    transaction = Transaction(
        wallet1.publicKey, "someone", 10, wallet1.privateKey)

    blockchain.addTransaction(transaction)
    blockchain.handleTransactions(wallet1.publicKey)

    validator = TransactionSignature()
    signature = validator.decodeKeyPairs(transaction.transactionSignature)
    assert validator.validateTransaction(
        transaction.transactionHashByte, signature, transaction.source) == True


def test_shouldNotAddFraudTransactionToBlockchain():
    wallet1 = Wallet("person")
    wallet2 = Wallet("person")
    blockchain = blockchainFactory.getBlockchainWithFundedWallet(
        0, 10, wallet1.publicKey, 10000)

    # Let's assume wallet2 is a fraud wallet and tries to
    # attempt receiving a transaction to itself from wallet1
    # with its own private key:
    transaction = Transaction(
        wallet1.publicKey, wallet2.publicKey, 10, wallet2.privateKey)
    blockchain.addTransaction(transaction)
    blockchain.handleTransactions("null")

    assert wallet2.getBalance(blockchain) == 0


def test_blockchainShouldBeValid():
    wallet1 = Wallet("person")
    blockchain = blockchainFactory.getBlockchainWithFundedWallet(
        0, 10, wallet1.publicKey, 1000000)

    for i in range(5):
        blockchain.addTransaction(Transaction(
            wallet1.publicKey, "someone", random.randint(1, 900), wallet1.privateKey))
        blockchain.handleTransactions(wallet1.publicKey)

    assert blockchain.validationFlag == True


def test_shouldBeInvalidWhenAttemptIllegalChange():
    wallet1 = Wallet("person")
    blockchain = blockchainFactory.getBlockchainWithFundedWallet(
        0, 10, wallet1.publicKey, 100000)

    for i in range(5):
        blockchain.addTransaction(Transaction(
            wallet1.publicKey, "someone", random.randint(1, 900), wallet1.privateKey))
        blockchain.handleTransactions(wallet1.publicKey)

    # Illegal change:
    # Create a hacker wallet with 0 coins:
    wallet2 = Wallet("hacker")
    blockchain.blockchain[3].blockTransactions.append(Transaction(
        wallet2.publicKey, wallet1.publicKey, 1000, wallet2.privateKey))

    # Now try to attempt a normal transaction:
    with pytest.raises(IllegalAccessError) as err:
        blockchain.addTransaction(Transaction(
            wallet1.publicKey, "someone", 10000, wallet1.privateKey))
        blockchain.handleTransactions(wallet1.publicKey)

    assert "Changed block properties found! The corresponding block is corrupted!" in str(
        err.value)


def test_shouldRaiseErrWhenAttemptToUseDifferentDataType():
    wallet1 = Wallet("person")
    blockchain = blockchainFactory.getBlockchainWithFundedWallet(
        0, 10, wallet1.publicKey, 1000000)

    with pytest.raises(TransactionDataConflictError) as err:
        blockchain.addTransaction(Transaction(
            wallet1.publicKey, "null", "test message", wallet1.privateKey))

    assert TransactionDataConflictError().err_str in str(
        err.value)


def test_integration_blockchainDataIO():
    blockchain = Blockchain(3, 0)

# Creating random wallets
    numberofWallets = 5

    wallets = []
    for i in range(numberofWallets):
        newWallet = Wallet("person")
        wallets.append(newWallet)
        blockchain.forceTransaction(newWallet.publicKey, 10000)

    for i in range(1, 5):
        randomWallet1 = wallets[random.randint(0, numberofWallets - 1)]
        randomWallet2 = wallets[random.randint(0, numberofWallets - 1)]
        blockchain.addTransaction(Transaction(
            randomWallet1.publicKey, randomWallet2.publicKey, random.randint(1, 1000), randomWallet1.privateKey))

    blockchain.handleTransactions(wallets[0].publicKey)


# Blockchain data export and import
    usersBalanceBeforeExport = 0
    usersBalanceAfterExport = 0

    for i in range(numberofWallets):
        usersBalanceBeforeExport += wallets[i].getBalance(blockchain)

    BlockDataIO().exportData(blockchain, "blockchainData.json")
    newBlockchain = BlockDataIO().importData("blockchainData.json")

    for i in range(numberofWallets):
        assert wallets[i].getBalance(
            blockchain) == wallets[i].getBalance(newBlockchain)
        usersBalanceAfterExport += wallets[i].getBalance(newBlockchain)

    assert usersBalanceBeforeExport == usersBalanceAfterExport
