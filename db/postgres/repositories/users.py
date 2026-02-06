from db.postgres.repositories import AsyncRepository
from db.schemas import UsersTable, BasketTable, SavedProductsTable
from sqlalchemy import select

class AsyncUserRepository(AsyncRepository):
    table = UsersTable

    async def get_user_by_tg_id(self, tg_id: str):
        query = select(UsersTable).where(UsersTable.tg_id == tg_id)

        user = await self.execute(query=query)
        
        return user.scalar_one_or_none()
    
    async def create_user(self, data: dict):
        user = await self.get_user_by_tg_id(tg_id=data.get('tg_id'))

        if not user:
            return await self.create(data)
        else:
            return {"error": "USER_ALREADY_EXISTS"}
    
    async def authenticate(self, tg_id: str):
        query = select(UsersTable).where(UsersTable.tg_id == str(tg_id))
        
        user = await self.session.execute(query)
        
        return user.scalar_one_or_none()

class AsyncBasketRepository(AsyncRepository):
    table = BasketTable
    
    async def add_product(self, user_id, product_id, size = None):
        obj = await self.create(params={
            "user_id": user_id,
            "product_id": product_id,
            "size": size
        })
        return obj
    
class AsyncSavedProductsRepository(AsyncRepository):
    table = SavedProductsTable
    
    async def add_product(self, user, product):
        is_exist = await self.exists(conditions={"user": user, "product": product})
        
        if not is_exist:
            obj = await self.create(params={
                "user": user,
                "product": product,
            })
            return obj
        return {"error": "Already in wishlist!"}

def get_async_user_repo() -> AsyncUserRepository:
    return AsyncUserRepository()

def get_async_basket_repo() -> AsyncBasketRepository:
    return AsyncBasketRepository()

def get_async_saved_product_repo() -> AsyncSavedProductsRepository:
    return AsyncSavedProductsRepository()