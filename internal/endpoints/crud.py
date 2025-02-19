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
    WalletOperation,
    WalletsResponse
)
from internal.database.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from internal.services.transaction import Transaction,TransactionService,NotEnoughFunds
from internal.schema.WalletSchema import WalletGetSchema,WalletUpdateSchema
from internal.repository.WalletRepository import WalletRepository,WalletNotCreatedExeption


crud_router = APIRouter(prefix="/api/v2/wallet", tags=["CRUDWallet"])


@crud_router.post("/create", response_model=WalletResponse)
async def create_wallet(db_session: AsyncSession = Depends(get_async_session)):
    try:
        wallet = WalletRepository(db_session)
        wallet_uuid = await wallet.create_wallet()
        if wallet_uuid is None:
            return WalletResponse(status=BaseNotFoundResponse.status, content=WalletNotCreatedExeption.detail)
    except Exception:
        return HTTPException(status_code=BaseBadRequestResponse.status, detail="Bad request")
    return WalletResponse(uuid=wallet_uuid, balance=0)

@crud_router.get("/{uuid}", response_model=WalletResponse)
async def get_wallet(uuid: UUID, db_session: AsyncSession = Depends(get_async_session)):
    try:
        wallet = WalletRepository(db_session)
        wallet = await wallet.get_wallet(uuid)
    except WalletNotCreatedExeption:
        return WalletResponse(uuid=uuid, balance=0,status=BaseNotFoundResponse.status, content=WalletNotCreatedExeption.detail)
    except ValueError:
        return WalletResponse(uuid=uuid, balance=0,status=BaseBadRequestResponse.status, content="Value error")
    except Exception:
        return WalletResponse(uuid=uuid, balance=0,status=BaseBadRequestResponse.status, content="Bad request")
    return WalletResponse(uuid=uuid, balance=wallet.amount)

@crud_router.post("/update/{uuid}", response_model=WalletResponse)
async def update_wallet(wallet: WalletUpdateSchema, db_session: AsyncSession = Depends(get_async_session)):
    try:
        rep = WalletRepository(db_session)
        wallet = await rep.update_wallet(wallet)
    except WalletNotCreatedExeption:
        return WalletResponse(status=BaseNotFoundResponse.status, content=WalletNotCreatedExeption.detail)
    except ValueError:
        return WalletResponse(status=BaseBadRequestResponse.status, content="Value error")
    except Exception:
        return WalletResponse(status=BaseBadRequestResponse.status, content="Bad request")
    return WalletResponse(uuid=wallet.uuid, balance=wallet.amount)

@crud_router.post("/delete/{uuid}", response_model=BaseResponse)
async def delete_wallet(uuid: UUID, db_session: AsyncSession = Depends(get_async_session)):
    try:
        rep = WalletRepository(db_session)
        await rep.delete_wallet(uuid)
    except Exception:
        return WalletResponse(status=BaseBadRequestResponse.status, content="Bad request")
    return BaseResponse()

@crud_router.post("/get_all_wallets", response_model=WalletsResponse)
async def get_all_wallets(db_session: AsyncSession = Depends(get_async_session)):
    try:
        rep = WalletRepository(db_session)
        wallets = await rep.get_all_wallets()
    except Exception:
        return WalletsResponse(status=BaseBadRequestResponse.status, content="Bad request")
    return WalletsResponse( seq=wallets)

