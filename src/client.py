from dataclasses import dataclass
import dataclasses


@dataclass
class Client:
    id: str
    name: str 

    def to_dict(self) -> dict[str, object]:
        return dataclasses.asdict(self)

def from_dict(client: dict[str, str]) -> Client:
    return Client(client["id"], client["name"])

