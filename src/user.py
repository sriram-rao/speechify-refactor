from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .client import Client


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