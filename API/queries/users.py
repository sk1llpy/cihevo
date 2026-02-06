from db import repository as repo
from sqlalchemy.orm import Session
from bot.decorators import create_session

class UserQuery(repo.UsersTableRepository):
    def __init__(self, user=None) -> None:
        self.user_data: repo.UsersTableRepository.table = user

    @create_session
    async def user(self, user_id: int, session: Session):
        user = self.get(
            attribute = "id",
            value = user_id,
            session = session,
        )
        
        return user if user else None