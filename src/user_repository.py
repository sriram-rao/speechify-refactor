import json
from typing import Any, cast

from src.lru_cache import LRUCache


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


class CachedUserRepository:
    def __init__(self) -> None:
        self.repo: UserRepository = UserRepository()
        self.cache: LRUCache = LRUCache(100_000)

    async def cached_get_result(self, key: str, func) -> Any:
        if self.cache.has(key):
            return self.cache.get(key)
        result = func(key)
        self.cache.set(key, result)
        return result

    async def get_all(self) -> list[object]:
        return await self.cached_get_result("all", self.repo.get_all)

    async def get_by_email(self, email: str) -> object:
        return await self.cached_get_result(email, self.repo.get_by_email)

    async def get_by_id(self, id: str) -> object:
        return await self.cached_get_result(id, self.repo.get_by_email)

    async def add(self, user: object):
        self.cache.set(user["id"], user)
        self.repo.add(user)
