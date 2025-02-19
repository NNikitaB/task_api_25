from internal.schema.WalletSchema import WalletGetSchema,WalletUpdateSchema
from internal.schema.Response import WalletOperation
from internal.repository.SQLAlchemyRepository import SQLAlchemyRepository,AbstractRepository
from internal.repository.WalletRepository import WalletRepository
from uuid import UUID


class NotEnoughFunds(Exception):
    detail:str = "Not enough funds"
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


class TransactionService:
    def __init__(self,sqla_repo: WalletRepository):
        self.sqla_repo:WalletRepository = sqla_repo

    async def operationWallet(self, uuid:UUID, operation: WalletOperation):
        get_answer:WalletGetSchema = await self.sqla_repo.get_wallet(uuid=uuid)
        t = Transaction(get_answer)
        res = None
        if operation.operationType == 'DEPOSIT':
            res = t.deposit(operation.amount)
        elif operation.operationType == 'WITHDRAW':
            res = t.withdraw(operation.amount)
        else:
            raise Exception("Invalid operation type")
        wallet_update:WalletUpdateSchema = res
        return await self.sqla_repo.update_wallet(wallet_update)