from typing import Any

import json
import socket as sck

class User:
    BANS_PATH = "config/bans.json"
    MUTES_PATH = "config/mutes.json"
    OPS_PATH = "config/ops.json"
    ROLES_PATH = "config/roles.json"

    def __init__(self, id: str, name: str, sock: sck.socket):
        self.id = id
        self.name = name

        self.sock = sock
        self.addr = sock.getpeername()

    def disconnect(self):
        self.sock.close()

    def get_json(self) -> str:
        data: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "addr": self.addr,
        }
        return json.dumps(data)