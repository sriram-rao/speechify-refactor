import json
from typing import cast


class UserRepository:
    def __init__(self) -> None:
        with open("db.json", 'r') as f:
            self.db: dict[str, list[object]] = json.load(f)

    async def get_all(self) -> list[object]:
        return self.db.get("users", [])

    async def get_by_email(self, email: str) -> object:
        return next(u for u in self.db.get("users", []) if cast(dict[str, str], u)["email"] == email)

    async def get_by_id(self, id: str) -> object:
        return next(u for u in self.db.get("users", []) if cast(dict[str, str], u)["id"] == id)

    async def add(self, user: object):
        self.db["users"].append(user)
        with open("db.json", 'w') as file:
            json.dump(self.db, file, indent=2, default=str)

