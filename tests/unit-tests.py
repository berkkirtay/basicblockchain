from blockchain import *
from blockchainChat import blockchainChat


def assertEquals(var1, var2):
    if var1 == var2:
        return True
    else:
        return False


def handleTransactionTestBase(blockchain):
    blockchain.handleTransaction("null")


def forceTransacitonTest1(blockchain):
    blockchain.forceTransaction(
        transaction("lsjy0p1q2kesd7j26e", "person1", 10000))
    handleTransactionTestBase(blockchain)
    return blockchain.getBalance("person1")  # returns 10000


def transactionTest1(blockchain):
    blockchain.addTransaction(
        transaction("null", "person1", 10000))
    handleTransactionTestBase(blockchain)
    return blockchain.getBalance("person1")  # returns 0


def transactionTest2(blockchain):
    blockchain.addTransaction(
        transaction("person1", "person2", -10000))
    handleTransactionTestBase(blockchain)
    return blockchain.getBalance("person2")  # returns 0


def transactionTest3(blockchain):
    blockchain.addTransaction(
        transaction("person2", "person1", 1000))
    handleTransactionTestBase(blockchain)
    return blockchain.getBalance("person1")  # returns 0


def transactionTest4(blockchain):
    blockchain.addTransaction(
        transaction("person1", "person2", 99999999999999))
    handleTransactionTestBase(blockchain)
    return blockchain.getBalance("person2")  # returns 0


def transactionTest5(blockchain):
    blockchain.addTransaction(
        transaction("person1", "person2", 10000))
    handleTransactionTestBase(blockchain)
    return blockchain.getBalance("person2")  # returns 10000


def transactionTest6(blockchain):
    blockchain.addTransaction(
        transaction("person1", "person1", 1000))
    handleTransactionTestBase(blockchain)


def textTransactionTest1(blockchain):
    blockchain.addText(
        transaction("person1", "person2", "hey"))


def textTransactionTest2(blockchain):
    blockchain.addText(
        transaction("person1", "person2", "1231321223"))


def textTransactionPrintTest(blockchain):
    blockchain.handleChat()
    blockchain.getText()
    for text in blockchain.texts:
        print(text)


def createWalletAndGetBalanceTest(blockchain):
    wallet1 = wallet("person1", "person1")
    wallet2 = wallet("person2", "person2")
    wallets = [wallet1, wallet2]

    printWalletInfoTest(blockchain, wallets)
    saveDatabasetest(blockchain, wallets)


def printWalletInfoTest(blockchain, wallets):
    for wallet in wallets:
        wallet.updateTransactions(blockchain)


def saveDatabasetest(blockchain, wallets):
    database1 = database()
    database1.saveDatabase(blockchain, wallets, '')
    database1.loadDatabase('')


def startTests(blockchain):

    # Coin transactions
    assertEquals(10000, forceTransacitonTest1(blockchain))

    assertEquals(0, transactionTest1(blockchain))
    assertEquals(0, transactionTest2(blockchain))
    assertEquals(0, transactionTest3(blockchain))
    assertEquals(0, transactionTest4(blockchain))
    assertEquals(10000, transactionTest5(blockchain))
    assertEquals(0, transactionTest6(blockchain))

    # Text block transactions

    textBlockchain = blockchainChat(1, 0)
    textTransactionTest1(textBlockchain)
    textTransactionTest2(textBlockchain)
    textTransactionPrintTest(textBlockchain)

    # Wallet tests
    createWalletAndGetBalanceTest(blockchain)


def differentBlockchainsTest():
    for i in range(1, 2):
        block1 = blockchain(i, 100)
        startTests(block1)


def miningTest():
    # Mining Difficulty and reward
    block1 = blockchain(3, 5)
    for i in range(100):
        block1.handleTransaction("person3")
    coins = block1.getBalance("person3")
    print(f"Total coin amount after mining: {coins}")


miningTest()
differentBlockchainsTest()
