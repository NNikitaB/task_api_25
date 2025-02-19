from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel,Field
from fastapi.responses import JSONResponse
from uuid import UUID
from typing import List,Literal
from internal.schema.Response import (
    BaseResponse, 
    BaseBadRequestResponse, 
    BaseNotEnoughFundsResponse, 
    BaseNotFoundResponse,
    WalletResponse,
    WalletOperation
)
from internal.database.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from internal.services.transaction import Transaction,TransactionService,NotEnoughFunds
from internal.schema.WalletSchema import WalletGetSchema,WalletUpdateSchema
from internal.repository.WalletRepository import WalletRepository,WalletNotCreatedExeption

wallet_router = APIRouter(prefix="/api/v1/wallets", tags=["Wallets"])


# Эндпоинт для выполнения операции с кошельком
@wallet_router.post("/{uuid}/operation", response_model=WalletResponse)
async def operation(uuid: UUID,operation: WalletOperation,db_session: AsyncSession = Depends(get_async_session) ):
    try:
        servise = TransactionService(WalletRepository(db_session))
        updated_wallet = await servise.operationWallet(uuid,operation)
    except NotEnoughFunds:
        return JSONResponse(status_code=BaseNotEnoughFundsResponse.status, content=NotEnoughFunds.detail)
    except WalletNotCreatedExeption:
        return JSONResponse(status_code=BaseNotFoundResponse.status, content=WalletNotCreatedExeption.detail)
    except ValueError:
        return JSONResponse(status_code=BaseBadRequestResponse.status, content="Value error")
    except Exception:
        return JSONResponse(status_code=BaseBadRequestResponse.status, content="Bad request")
    return WalletResponse(uuid=uuid, balance=updated_wallet.amount)

# Эндпоинт для получения кошелька
@wallet_router.post("/{uuid}", response_model=WalletResponse)
async def get_wallet(uuid: UUID, db_session: AsyncSession = Depends(get_async_session)):
    try:
        wallet = WalletRepository(db_session)
        wallet = await wallet.get_wallet(uuid)
    except WalletNotCreatedExeption:
        return JSONResponse(status_code=BaseNotFoundResponse.status, content=WalletNotCreatedExeption.detail)
    except ValueError:
        return JSONResponse(status_code=BaseBadRequestResponse.status, content="Value error")
    except Exception:
        return JSONResponse(status_code=BaseBadRequestResponse.status, content="Bad request")
    return WalletResponse(uuid=wallet.uuid, balance=wallet.amount)

