from fastapi import APIRouter
from internal.endpoints.wallets import wallet_router
from internal.endpoints.crud import crud_router

routers = APIRouter()

routers.include_router(wallet_router)
routers.include_router(crud_router)

