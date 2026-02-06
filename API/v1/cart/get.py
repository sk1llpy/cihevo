from fastapi import Depends

from .router import router
from API.schemas.users import UserSchema
from API.dependencies.users.user import UserHandling
from API.services.cart import CartService, get_cart_service


@router.get("/")
async def get_cart(user: UserSchema = Depends(UserHandling().user), service: CartService = Depends(get_cart_service)):
    return await service.get_cart(user_id=user.id)

@router.get("/count")
async def get_cart_products_count(user: UserSchema = Depends(UserHandling().user), service: CartService = Depends(get_cart_service)):
    return len(user.basket)