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

class Users(Base):
    __tablename__ = "users"
    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(default=0)
    time_registration: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

