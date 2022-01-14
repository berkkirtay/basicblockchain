from sys import exc_info
import pytest

from Blockchain import Blockchain
from Transaction import TransactionSignature
from Wallet import Wallet
from Transaction import Transaction
from DataConverter import *


class BlockchainFactory:
    def __init__(self):
        pass

    def getBlockchain(self, hashDifficulty, miningReward) -> Blockchain:
        return Blockchain(hashDifficulty, miningReward)

    def getBlockchainWithFundedWallet(self, hashDifficulty, miningReward, publicKey, amount):
        blockchain = Blockchain(hashDifficulty, miningReward)
        blockchain.forceTransaction(publicKey, amount)
        blockchain.handleTransaction(publicKey)
        return blockchain

    def getRandWallet(self, walletName) -> Wallet:
        wallet = Wallet(walletName)
        wallet.createNewWallet()
        return wallet


blockchainFactory = BlockchainFactory()


def test_shouldCreateTwoDifferentWalletsWithSameName():
    wallet1 = blockchainFactory.getRandWallet("person")
    wallet2 = blockchainFactory.getRandWallet("person")
    assert wallet1.privateKey != wallet2.privateKey


def test_shouldSendExpectedAmounts():
    wallet1 = blockchainFactory.getRandWallet("person1")
    wallet2 = blockchainFactory.getRandWallet("person2")
    blockchain = blockchainFactory.getBlockchainWithFundedWallet(
        2, 10, wallet1.publicKey, 10000)

    blockchain.addTransaction(Transaction(
        wallet1.publicKey, wallet2.publicKey, 10, wallet1.privateKey))
    blockchain.addTransaction(Transaction(
        wallet1.publicKey, wallet2.publicKey, 123, wallet1.privateKey))

    blockchain.handleTransaction(wallet1.publicKey)

    blockchain.addTransaction(Transaction(
        wallet2.publicKey, wallet1.publicKey, 33, wallet2.privateKey))

    blockchain.handleTransaction(wallet1.publicKey)

    assert 100 == blockchain.getBalance(wallet2.publicKey)


def test_shouldReveiceExpectedBlockRewards():
    wallet1 = blockchainFactory.getRandWallet("person1")
    wallet2 = blockchainFactory.getRandWallet("person2")
    blockchain = blockchainFactory.getBlockchainWithFundedWallet(
        0, 10, wallet1.publicKey, 10000)

    for i in range(24):
        blockchain.addTransaction(Transaction(
            wallet1.publicKey, "null", 10, wallet1.privateKey))
        blockchain.handleTransaction(wallet2.publicKey)

    # wallet2 has built 24 blocks, so it will
    # receive 24 block rewards as total.
    assert 24 * 10 == wallet2.getBalance(blockchain)


def test_shouldNotSendIfInsufficientFundInWallet():
    wallet1 = blockchainFactory.getRandWallet("person")
    blockchain = blockchainFactory.getBlockchainWithFundedWallet(
        0, 10, wallet1.publicKey, 10000)

    with pytest.raises(ValueError) as err:

        blockchain.addTransaction(Transaction(
            wallet1.publicKey, "null", -100, wallet1.privateKey))

        blockchain.handleTransaction(wallet1.publicKey)

    assert "Transaction amount can't be zero or a negative value!" in str(
        err.value)


def test_shoulNotSendNegativeAmount():
    blockchain = blockchainFactory.getBlockchain(2, 10)
    wallet1 = blockchainFactory.getRandWallet("person")

    with pytest.raises(ValueError) as err:

        blockchain.addTransaction(Transaction(
            wallet1.publicKey, "null", 10, wallet1.privateKey))

        blockchain.handleTransaction(wallet1.publicKey)

    assert "Insufficient coins in the source!" in str(err.value)


def test_shouldValidateTransactionCorrectly():
    wallet1 = blockchainFactory.getRandWallet("person")
    blockchain = blockchainFactory.getBlockchainWithFundedWallet(
        0, 10, wallet1.publicKey, 10000)

    transaction = Transaction(
        wallet1.publicKey, "someone", 10, wallet1.privateKey)

    blockchain.addTransaction(transaction)
    blockchain.handleTransaction(wallet1.publicKey)

    validator = TransactionSignature()
    signature = validator.decodeKeyPairs(transaction.transactionSignature)
    assert validator.validateTransaction(
        transaction.transactionHashByte, signature, transaction.source) == True


def test_blockchainShouldBeValid():
    pass


def test_allTransactionSignaturesShouldBeValid():
    pass