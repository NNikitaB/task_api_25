from internal.database.db import Base
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    DateTime,
    Text,
    func,
)
import datetime
from uuid import UUID
from typing import Optional
from internal.schema.WalletSchema import WalletSchema


class Wallets(Base):
    '''
    Wallets table
    '''
    __tablename__ = "wallets"
    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(default=0)
    time_registration: Mapped[datetime.datetime] = mapped_column(server_default=func.now())


    def to_read_model(self) -> WalletSchema:
        '''Converting model to schema'''
        return WalletSchema(
            uuid=self.uuid,
            amount=self.amount,
            time_registration=self.time_registration,
        )

