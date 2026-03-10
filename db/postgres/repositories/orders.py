from sqlalchemy import select, and_, or_
from sqlalchemy.orm import joinedload, selectinload

from db.postgres.repositories import AsyncRepository
from db.schemas import (
    orders
)


class AsyncProductRepository(AsyncRepository):
    table = orders
