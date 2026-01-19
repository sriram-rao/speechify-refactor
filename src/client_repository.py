import json

from src.lru_cache import LRUCache
from .client import Client


class ClientRepository:

    def __init__(self) -> None:
        self.cache = LRUCache(100_000)

    async def get_by_id(self, id: str) -> Client | None:
        if (self.cache.has(id)):
            return self.cache.get(id)

        with open("db.json", 'r') as f:
            db = json.load(f)
        
        clients: dict[str, object] = db.get("clients")
        client = None
        for c in db.get("clients", []):
            if c["id"] == id:
                client = c
                break
        
        if not client:
            return None
        new_client = Client(
            id=client["id"],
            name=client["name"]
        )
        self.cache.set(id, new_client)
        return new_client

    async def get_all(self) -> list[Client]:
        with open("db.json", 'r') as f:
            db = json.load(f)
        clients = db.get("clients", [])
        for c in clients:
            self.cache.set(c["id"], Client(id=c["id"], name=c["name"]))
        return db.get("clients", []) 

