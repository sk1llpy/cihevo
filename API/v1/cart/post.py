from fastapi import Depends, Body

from .router import router
from API.dependencies.users.user import UserHandling
from API.services.cart import CartService, get_cart_service
from API.schemas.cart import AddCartSchema
from API.schemas.users import UserSchema


@router.post("/add")
async def add_to_cart(user: UserSchema = Depends(UserHandling().user), data: AddCartSchema = Body(), service: CartService = Depends(get_cart_service)):
    data = await service.add_to_cart(user_id=user.id, product_id=data.product_id, size=data.size)
    
    return data
