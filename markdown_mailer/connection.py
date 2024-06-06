from dataclasses import dataclass
from typing import Any


@dataclass
class Connection:
    id: str
    server: str
    port: int
    user: str
    password: str


def parse_connection(_id: str, connection: dict[str, Any]) -> Connection:
    return Connection(
        id=_id,
        server=connection['smtp_server'],
        port=connection['smtp_port'],
        user=connection['smtp_user'],
        password=connection['smtp_password'],
    )
