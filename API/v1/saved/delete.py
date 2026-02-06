from fastapi import Depends

from .router import router
from API.schemas.users import UserSchema
from API.dependencies.users.user import UserHandling
from API.services.cart import CartService, get_cart_service


@router.delete("/remove/{id}")
async def remove_from_saved(id: int, user: UserSchema = Depends(UserHandling().user), service: CartService = Depends(get_cart_service)):
    return await service.remove_saved(user_id=user.id, product_id=id)
