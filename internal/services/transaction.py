from internal.schema.WalletSchema import WalletGetSchema,WalletUpdateSchema


class NotEnoughFunds(Exception):
    pass
class AmountError(Exception):
    pass


class Transaction:
    def __init__(self, wallet:WalletGetSchema):
        self.wallet = wallet


    def deposit(self, amount: int):
        if amount < 0:
            raise AmountError("Amount must be positive")
        return WalletUpdateSchema(uuid=self.wallet.uuid,amount=self.wallet.amount + amount)


    def withdraw(self, amount: int):
        if self.wallet.amount < amount:
            raise NotEnoughFunds("Not enough funds")
        self.wallet.amount -= amount
        return WalletUpdateSchema(uuid=self.wallet.uuid,amount=self.wallet.amount)