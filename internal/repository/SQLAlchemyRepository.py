from internal.patterns.repository import AbstractRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert
from internal.models.Base import Base
from uuid import UUID
from typing import  Any, Never, Sequence


class SQLAlchemyRepository(AbstractRepository):
    '''CRUD operations for SQLAlchemy'''
    
    def __init__(self, model, session: AsyncSession) -> None:
        self.session = session
        self.model = model

    async def add_one(self, **data) -> UUID:
        smtp = insert(self.model).values(**data).returning(self.model.uuid)
        res = await self.session.execute(smtp)
        await self.session.commit()
        return res.scalar_one()

    async def get_one(self, **kwargs) -> Any | None:
        smtp = select(self.model).filter_by(**kwargs)
        res = await self.session.execute(smtp)
        return res.unique().scalar_one_or_none()

    async def update_one(self, uuid:UUID, **kwargs) -> Any | None:
        smtp = update(self.model).filter(self.model.uuid == uuid).values(**kwargs).returning(self.model)
        obj = await self.session.execute(smtp)
        await self.session.commit()
        return obj.scalar_one_or_none()

    async def delete_one(self, **kwargs: Any) -> Never:
        smtp = delete(self.model).filter_by(**kwargs)
        await self.session.execute(smtp)
        await self.session.commit()

    async def delete_all(self) -> Never:
        smtp = delete(self.model)
        await self.session.execute(smtp)

    async def get_all(self, **kwargs: Any) -> Sequence[Any]:
        smtp = select(self.model).filter_by(**kwargs)
        res = await self.session.execute(smtp)
        return res.scalars().all()
