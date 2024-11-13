from pydantic import BaseModel, PositiveInt
from typing import Dict


class ServerConfig(BaseModel):
    host: str
    port: PositiveInt
    id: str
    max_users: PositiveInt
    name: str
    description: str
    public: bool
    logging: str
    enable_plugins: bool
    render_muted_messages: bool
    render_executed_commands: bool
    lang: str
    dev: Dict[str, str | bool]
