from typing import Any, Coroutine, Sequence
from uuid import UUID
from internal.repository.SQLAlchemyRepository import SQLAlchemyRepository
from internal.models.Wallets import Wallets
from internal.schema.WalletSchema import WalletSchema,WalletGetSchema,WalletDeleteSchema,WalletUpdateSchema


class WalletRepository(SQLAlchemyRepository):
    def __init__(self, session) -> None:
        super().__init__(model=Wallets,session=session)
    
    async def create_wallet(self) -> UUID | None:
        wallet_dict = WalletSchema().model_dump()
        return await self.add_one(**wallet_dict)

    async def get_wallet(self, uuid: UUID) -> WalletGetSchema | None:
        wallet = await self.get_one(uuid=uuid)
        if wallet is None:
            return None
        wallet = WalletSchema.model_validate(wallet.to_read_model())
        return WalletGetSchema(uuid=wallet.uuid,amount=wallet.amount)
    
    async def update_wallet(self, wallet: WalletUpdateSchema) -> WalletUpdateSchema | None:
        updated_wallet = await self.update_one(wallet.uuid, amount=wallet.amount)
        if updated_wallet is None:
            return None
        updated_wallet = WalletSchema.model_validate(updated_wallet.to_read_model())
        return WalletUpdateSchema(uuid=updated_wallet.uuid,amount=updated_wallet.amount)
    
    async def delete_wallet(self, uuid: UUID) -> None:
        await self.delete_one(uuid=uuid)

    async def get_all_wallets(self) -> Sequence[WalletGetSchema]:
        wallets = await self.get_all()
        return [WalletGetSchema.model_validate(wallet.to_read_get_model()) for wallet in wallets]
        