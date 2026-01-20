from dataclasses import dataclass
import dataclasses
from datetime import datetime
from typing import Optional

import nanoid
from .client import Client
from src import client


@dataclass
class User:
    id: str
    firstname: str
    surname: str
    client: Client
    date_of_birth: datetime
    email: str
    has_credit_limit: bool
    credit_limit: Optional[int] = None 

    def __init__(self, id: str | None, firstname: str, surname: str, client: Client, date_of_birth: datetime, email: str):
        self.id = id or nanoid.generate()
        self.firstname = firstname
        self.surname = surname
        self.client = client
        self.date_of_birth = date_of_birth
        self.email = email
        self.has_credit_limit = client.name == "VeryImportantClient"
        if self.has_credit_limit:
            self.credit_limit = 10_000 * 2 if client.name == "ImportantClient" else 10_000


    def to_dict(self) -> dict[str, object]:
        return dataclasses.asdict(self)

def from_dict(user_dict: dict[str, str | object]) -> User:
    date_of_birth = datetime.fromisoformat(user_dict["date_of_birth"].replace('Z', '+00:00'))
    return User(user_dict["id"], user_dict["firstname"], user_dict["surname"], 
                client.from_dict(user_dict["client"]), date_of_birth, user_dict["email"])

