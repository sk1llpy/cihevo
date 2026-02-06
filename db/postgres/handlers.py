from db.postgres.factory import get_async_factory
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


async def create_async_session(factory = Depends(get_async_factory)):
    async with factory() as session:
        yield session


async def commit_async_session(session: AsyncSession):
    async with session:
        try:
            await session.commit()
        except Exception as ex:
            await session.rollback()
            raise ex
