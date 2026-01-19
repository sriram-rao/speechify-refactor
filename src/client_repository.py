import json
from typing import List, Optional
from .client import Client


class ClientRepository:
    async def get_by_id(self, id: str) -> Optional[Client]:
        with open("db.json", 'r') as f:
            db = json.load(f)
        
        clients = db.get("clients", [])
        c = None
        for i in range(len(clients)):
            if clients[i]["id"] == id:
                c = clients[i]
                break
        
        if not c:
            return None
        
        return Client(
            id=c["id"],
            name=c["name"]
        )

    async def get_all(self) -> List[Client]:
        with open("db.json", 'r') as f:
            db = json.load(f)
        
        clients = db.get("clients", [])
        return clients 