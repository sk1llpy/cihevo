from sqlalchemy import select
from sqlalchemy.orm import Session

from db.repository import BaseRepository
from db.schemas.users import UsersTable

class UsersTableRepository(BaseRepository):
    table = UsersTable

    async def create_user(self, data: dict, session: Session):
        is_exist = self.is_exist("phone_number", data.get("phone_number"), session)

        if not is_exist:
            obj = self.create(data, session)

            return obj
        else:
            return {"error": "USER_ALREADY_EXISTS"}
        
    async def get_user_by_phone_number(self, phone_number: str, session: Session):
        with session:
            user = session.execute(
                select(UsersTable).where(UsersTable.phone_number == phone_number)
            ).scalar_one_or_none()

        return user

