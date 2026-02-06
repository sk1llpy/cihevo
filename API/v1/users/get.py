from fastapi import Depends

from .router import router
from API.dependencies.users.user import UserHandling
from API.schemas.users import UserSchema
from API.services.users import UserService, get_user_service


@router.get("/me")
async def get_me(user: UserSchema = Depends(UserHandling().user), service: UserService = Depends(get_user_service)):
    data = await service.get_user(user_id=user.id)
    
    return data
