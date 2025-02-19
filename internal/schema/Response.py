from pydantic import BaseModel, Field
from starlette.status import HTTP_200_OK, HTTP_201_CREATED,HTTP_400_BAD_REQUEST,HTTP_422_UNPROCESSABLE_ENTITY,HTTP_404_NOT_FOUND
from typing import Literal, Optional,Sequence
from uuid import UUID
from internal.schema.WalletSchema import WalletGetSchema

class BaseResponse(BaseModel):
    status: int = HTTP_200_OK
    error: bool = False
    content: str = ""


class BaseCreateResponse(BaseModel):
    status: int = HTTP_201_CREATED
    error: bool = False


class BaseNotEnoughFundsResponse(BaseModel):
    status: int = 425
    error: bool = True


class BaseBadRequestResponse(BaseModel):
    status: int = HTTP_400_BAD_REQUEST
    error: bool = True


class BaseNotFoundResponse(BaseModel):
    status: int = HTTP_404_NOT_FOUND
    error: bool = True


# Модель для операции с кошельком
class WalletOperation(BaseModel):
    operationType: Literal['DEPOSIT','WITHDRAW']
    amount: int = Field(ge=0)

# Модель для успешного ответа
class WalletResponse(BaseResponse):
    uuid: Optional[UUID] = Field(default=None)
    balance: Optional[int]  = Field(default=None)


class WalletsResponse(BaseResponse):
    seq: Sequence[WalletGetSchema] = Field(default=[])

