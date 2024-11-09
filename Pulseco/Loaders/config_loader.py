"""
Provides config loader and validation functionality for the pulseco app.
"""

from pydantic import BaseModel, PositiveInt
from pulseco.utils import printb

class Config(BaseModel):
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

DEFAULT_CONFIG: Config = Config(
    host="127.0.0.1",
    port=7030,
    id="pulseco",
    max_users=10,
    name="Official Chat Room For Pulseco",
    description="This is the official chat room for Pulseco. Enjoy your stay!",
    public=True,
    logging="commands",
    enable_plugins=False,
    render_muted_messages=False,
    render_executed_commands=False,
    lang="en"
)

def load_config() -> Config:
    """
    Loads the config from settings.json and validates it.
    """
    try:
        printb("Loading config...", log=True)
        with open("config/settings.json", "r") as f:
            config = Config.model_validate_json(f.read(), strict=True)
        printb("Config loaded successfully.", log=True)
    except Exception as e:
        printb(f"Failed to load config: {e}", log=True)
        config = DEFAULT_CONFIG
        printb("Using default config instead...", log=True)
    return config