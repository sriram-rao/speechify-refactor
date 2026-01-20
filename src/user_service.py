from datetime import datetime, date
from typing import cast

from src.user_repository import UserRepository
from .user import User
from .client_repository import ClientRepository
from src import user


class UserService:
    async def AddUser(
        self,
        firstname: str,
        surname: str,
        email: str,
        date_of_birth: datetime,
        client_id: str
    ) -> bool:
        user_repo = UserRepository()

        if not firstname or not surname or not email \
            or await user_repo.get_by_email(email) or not await self.is_adult(date_of_birth):
            return False

        client_repository = ClientRepository()
        client = await client_repository.get_by_id(client_id)
        if not client:
            print("Client not found")
            return False

        user = User(None, firstname, surname, client, date_of_birth, email)
        await user_repo.add(user.to_dict())

        return True

    async def is_adult(self, date_of_birth: datetime):
        age = (date.today() - date_of_birth.date()).days / 365
        return age >= 21

    async def UpdateUser(self, user: User) -> bool:
        user_repo = UserRepository()
        user_from_id = await user_repo.get_by_id(user.id)
        if user_from_id is None:
            return False
        await user_repo.add(user.to_dict())
        return True

    async def GetAllUsers(self) -> list[User]:
        users_data = await UserRepository().get_all()
        
        users: list[User] = []
        for u in users_data:
            # Parse date string back to datetime
            u = cast(dict[str, str | object], u)
            users.append(user.from_dict(u))
        
        return users

    async def GetUserByEmail(self, email: str) -> User | None:
        user_dict = await UserRepository().get_by_email(email)
        return user.from_dict(user_dict) if user_dict else None

