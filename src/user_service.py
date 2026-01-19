import json
from datetime import datetime
from typing import List, Optional
import nanoid
from .client import Client
from .user import User
from .client_repository import ClientRepository


class UserService:
    async def AddUser(
        self,
        firstname: str,
        surname: str,
        email: str,
        date_of_birth: datetime,
        client_id: str
    ) -> bool:
        with open("db.json", 'r') as f:
            db = json.load(f)

        if not firstname or not surname:
            return False
        if not email:
            return False

        users = db.get("users", [])
        u = None
        for i in range(len(users)):
            if users[i]["email"] == email:
                u = users[i]
                break
        if u:
            return False

        now = datetime.now()
        age = now.year - date_of_birth.year

        if (
            now.month < date_of_birth.month or
            (now.month == date_of_birth.month and now.day < date_of_birth.day)
        ):
            age -= 1

        if age < 21:
            return False

        client_repository = ClientRepository()
        client = await client_repository.get_by_id(client_id)
        if not client:
            print("Client not found")
            return False
        
        user = {
            "id": nanoid.generate(),
            "client": {
                "id": client.id,
                "name": client.name
            },
            "date_of_birth": date_of_birth.isoformat(),
            "email": email,
            "firstname": firstname,
            "surname": surname,
        }

        if client.name == "VeryImportantClient":
            # Skip credit check
            user["has_credit_limit"] = False
        elif client.name == "ImportantClient":
            # Do credit check and double credit limit
            user["has_credit_limit"] = True
            user["credit_limit"] = 10000 * 2
        else:
            user["has_credit_limit"] = True
            user["credit_limit"] = 10000

        db["users"].append(user)
        with open("db.json", 'w') as f:
            json.dump(db, f, indent=2, default=str)

        return True

    async def UpdateUser(self, user: User) -> bool:
        if not user:
            return False
        
        with open("db.json", 'r') as f:
            db = json.load(f)
        
        users = db.get("users", [])
        u_idx = None
        for i in range(len(users)):
            if users[i]["id"] == user.id:
                u_idx = i
                break
        if u_idx is None:
            return False
        
        users[u_idx] = {
            "id": user.id,
            "client": {
                "id": user.client.id,
                "name": user.client.name
            },
            "date_of_birth": user.date_of_birth.isoformat(),
            "email": user.email,
            "firstname": user.firstname,
            "surname": user.surname,
            "has_credit_limit": user.has_credit_limit,
            "credit_limit": user.credit_limit
        }
        
        with open("db.json", 'w') as f:
            json.dump(db, f, indent=2, default=str)
        
        return True

    async def GetAllUsers(self) -> List[User]:
        with open("db.json", 'r') as f:
            db = json.load(f)
        
        users_data = db.get("users", [])
        
        users = []
        for user_data in users_data:
            # Parse date string back to datetime
            date_of_birth = datetime.fromisoformat(user_data["date_of_birth"].replace('Z', '+00:00'))
            
            user = User(
                id=user_data["id"],
                client=Client(
                    id=user_data["client"]["id"],
                    name=user_data["client"]["name"]
                ),
                date_of_birth=date_of_birth,
                email=user_data["email"],
                firstname=user_data["firstname"],
                surname=user_data["surname"],
                has_credit_limit=user_data["has_credit_limit"],
                credit_limit=user_data.get("credit_limit")
            )
            users.append(user)
        
        return users

    async def GetUserByEmail(self, email: str) -> Optional[User]:
        with open("db.json", 'r') as f:
            db = json.load(f)
        
        users = db.get("users", [])
        u = None
        for i in range(len(users)):
            if users[i]["email"] == email:
                u = users[i]
                break
        if not u:
            return None
        
        # Parse date string back to datetime
        date_of_birth = datetime.fromisoformat(u["date_of_birth"].replace('Z', '+00:00'))
        
        return User(
            id=u["id"],
            client=Client(
                id=u["client"]["id"],
                name=u["client"]["name"]
            ),
            date_of_birth=date_of_birth,
            email=u["email"],
            firstname=u["firstname"],
            surname=u["surname"],
            has_credit_limit=u["has_credit_limit"],
            credit_limit=u.get("credit_limit")
        ) 