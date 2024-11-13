import socket as sck
from pydantic import BaseModel, Field, PositiveInt
from typing import Dict, List, Any
from pulseco.network.user_registry import user_registry


class Room(BaseModel):
    """
    Pulseco chat room class.
    """

    host: str = Field(..., title="Host IP address")
    port: PositiveInt = Field(..., title="Host port")
    id: str = Field(..., title="Room ID")
    name: str = Field(..., title="Room name")
    description: str = Field(..., title="Room description")
    max_users: PositiveInt = Field(1, title="Maximum number of users")
    public: bool = Field(True, title="Public room")
    logging: str = Field("none", title="Logging level")
    enable_plugins: bool = Field(False, title="Enable plugins")
    render_muted_messages: bool = Field(False, title="Render muted messages")
    render_executed_commands: bool = Field(False, title="Render executed commands")
    lang: str = Field("en", title="Language")
    dev: Dict[str, str | bool] = Field({"debug": False}, title="Developer options")
    sock: sck.socket = Field(None, title="Socket object")
    users: List[Any] = Field(user_registry.get_users(), title="Users list")
