from fastapi import Depends

from .router import router
from API.schemas.users import UserSchema
from API.dependencies.users.user import UserHandling
from API.services.cart import CartService, get_cart_service


@router.get("/")
async def get_saved_products(user: UserSchema = Depends(UserHandling().user), service: CartService = Depends(get_cart_service)):
    return await service.get_saved_products(user_id=user.id)
