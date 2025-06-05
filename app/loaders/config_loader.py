from pydantic import BaseModel, Field, IPvAnyAddress, StrictInt, StrictBool, StrictStr
from typing import Optional
from ipaddress import IPv4Address

import os

# Create the config directory in the root directory if it doesn't exist
if not os.path.exists("config"):
    os.makedirs("config")

CONFIG_PATH = "config/server_options.json"

class ServerConfig(BaseModel):
    id: StrictStr = Field(..., description="Unique identifier for the server")
    name: StrictStr = Field(..., description="The name of the server")
    ip: IPvAnyAddress = Field(..., description="The IP address of the server")
    port: StrictInt = Field(7030, description="Port number")
    description: StrictStr = Field(..., description="A short description of the server")
    password: Optional[StrictStr] = Field(None, description="Optional password")
    debug: StrictBool = Field(False, description="Whether to enable debug mode")
    private: StrictBool = Field(False, description="Whether the server is private")
    max_users: StrictInt = Field(5, description="Maximum number of users allowed on the server")
    enable_plugins: StrictBool = Field(False, description="Whether to enable plugins")
    show_muted_messages: StrictBool = Field(True, description="Whether to show muted messages")
    show_executed_commands: StrictBool = Field(True, description="Whether to show executed commands")

DEFAULT_CONFIG = ServerConfig(
    id="pulseco",
    name="Pulseco Chat Server",
    ip=IPv4Address("127.0.0.1"),
    port=7030,
    description="A chat server for Pulseco",
    password=None,
    debug=False,
    private=False,
    max_users=10,
    enable_plugins=False,
    show_muted_messages=True,
    show_executed_commands=True
)

class ConfigLoaderSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.config: ServerConfig = DEFAULT_CONFIG
            self._initialized = True

    def load_config(self)-> None:
        """
        Load the server configuration from a file or return the default configuration.
        """
        # If the json does not exist, create it with the default configuration
        if not os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "w") as f:
                f.write(DEFAULT_CONFIG.model_dump_json(indent=4))

        BANS_PATH = "config/bans.json"
        MUTES_PATH = "config/mutes.json"
        OPS_PATH = "config/ops.json"
        ROLES_PATH = "config/roles.json"

        # Create the necessary directories and files if they do not exist
        for path in [BANS_PATH, MUTES_PATH, OPS_PATH, ROLES_PATH]:
            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write("[]")  # Initialize with an empty JSON array
        
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                loaded_config = ServerConfig.model_validate_json(f.read())
                self.config = loaded_config