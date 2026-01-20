import json
from typing import cast

from src.lru_cache import LRUCache
from .client import Client
from src import client


class ClientRepository:

    def __init__(self) -> None:
        with open("db.json", 'r') as f:
            self.db = json.load(f)
        self.cache = LRUCache(100_000)

    async def get_by_id(self, id: str) -> Client | None:
        client: dict[str, str] | None = next((c for c in self.db.get("clients", []) if cast(dict[str, str], c)["id"] == id), None)
        if not client:
            return None
        new_client = Client(client["id"], client["name"])
        self.cache.set(id, new_client)
        return new_client

    async def get_all(self) -> list[Client]:
        return [client.from_dict(c) for c in self.db.get("clients", [])]

