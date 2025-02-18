from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class WalletGetSchema(BaseModel):
    uuid: UUID
    amount: int


class WalletDeleteSchema(BaseModel):
    uuid: UUID


class WalletUpdateSchema(BaseModel):
    uuid: UUID
    amount: int


class WalletSchema(BaseModel):
    '''
    Wallet schema
    '''
    uuid: UUID
    amount: int
    time_registration: datetime

    class ConfigDict:
        from_attributes = True
        schema_extra = {
            "example": {
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "amount": 100,
                "time_registration": "2021-01-01T00:00:00.000000"
            }
        }

