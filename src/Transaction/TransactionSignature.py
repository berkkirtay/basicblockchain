# --------------------------------------------------------------------
# We need digital signatures to validate our transactions.
# We can use any asymetric encryption algorithm. For my
# implementation, I used RSA algorithm.
# For each transaction, we will encrypt the transaction
# hash with the source's private key and send it to the handler.
# Handler will validate transaction by decrypting the hash with
# the source's public key and compare it with the original transaction
# hash. If they are same, then validation will be successful.
# Copyright (c) 2022 Berk Kırtay
# --------------------------------------------------------------------

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as signer
from src.BlockchainExceptionHandler.BlockchainExceptionHandler import SignatureError
import base64


class TransactionSignature:
    def __init__(self):
        pass

    def signTransaction(self, transactionHash: str, privateKey: str) -> bytes:
        privateKey = self.decodeKeyPairs(privateKey)
        signature = signer.new(RSA.importKey(privateKey)).sign(transactionHash)
        return signature

    def validateTransaction(self, transactionHash,
                            signedTransactionHash: bytes, publicKey: str) -> bool:
        publicKey = self.decodePublicKey(publicKey)
        try:
            validator = signer.new(RSA.importKey(publicKey)).verify(
                transactionHash, signedTransactionHash)
            return validator
        except:
            raise SignatureError()

    def decodeKeyPairs(self, key: str) -> bytes:
        return base64.b64decode(key)

    # Here we add the trivial parts back to the public key.
    def decodePublicKey(self, key: str) -> bytes:
        key = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlHZk1BMEdDU3FHU0liM0RRRUJBUVVBQTRHTkFEQ0JpUUtCZ1F" + \
            key + "SURBUUFCCi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ=="
        return base64.b64decode(key)


def generateGenesisSignerKeyPair() -> list:
    randomGenerator = Random.new().read
    keyPair = RSA.generate(1024, randomGenerator)
    privateKey = keyPair.exportKey('PEM')
    privateKey = base64.b64encode(privateKey).decode("ascii")

    publicKey = keyPair.publickey().exportKey('PEM')
    publicKey = base64.b64encode(publicKey).decode("ascii")[87:-44]

    return [publicKey, privateKey]
