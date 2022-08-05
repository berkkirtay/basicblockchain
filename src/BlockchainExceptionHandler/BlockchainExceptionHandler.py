# Copyright (c) 2022 Berk Kırtay

class IllegalAccessError(Exception):
    def __call__(self, *args) -> Exception:
        return super().__call__(*(self.args + args))

    def __str__(self) -> str:
        return super().__str__()


class BlockchainSequenceError(Exception):
    def __call__(self, *args) -> Exception:
        return super().__call__(*(self.args + args))

    def __str__(self) -> str:
        return super().__str__()


class BalanceError(ValueError):
    def __call__(self, *args) -> ValueError:
        return super().__call__(*(self.args + args))

    def __str__(self) -> str:
        return super().__str__()


class SignatureError(Exception):
    def __call__(self, *args) -> Exception:
        return super().__call__(*(self.args + args))

    def __str__(self) -> str:
        return "Signature error, please debug the signature process."


class TransactionDataConflictError(Exception):
    err_str = "Blockchain transactions must be same data type!" + \
        "To resolve this error and not to lose any data, " + \
        "please remove the last block and start a new blockchain with the last block data."

    def __call__(self, *args) -> Exception:
        return super().__call__(*(self.args + args))

    def __str__(self) -> str:
        return self.err_str
