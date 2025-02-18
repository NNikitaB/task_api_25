from internal.schema.WalletSchema import WalletGetSchema,WalletUpdateSchema
from internal.services.transaction import Transaction,AmountError,NotEnoughFunds
from uuid import uuid4
import pytest

def test_transaction_add_amount():
    wallet = WalletGetSchema(uuid=uuid4(),amount=100)
    new_wallet:WalletUpdateSchema = Transaction(wallet).deposit(100)
    assert new_wallet.amount == 200

def test_transaction_sub_amount():
    wallet = WalletGetSchema(uuid=uuid4(),amount=100)
    new_wallet:WalletUpdateSchema = Transaction(wallet).withdraw(100)
    assert new_wallet.amount == 0

def test_amount_error():
    wallet = WalletGetSchema(uuid=uuid4(),amount=100)
    with pytest.raises(AmountError):
        Transaction(wallet).deposit(-1)

def test_not_enough_funds():
    wallet = WalletGetSchema(uuid=uuid4(),amount=100)
    with pytest.raises(NotEnoughFunds):
        Transaction(wallet).withdraw(200)

