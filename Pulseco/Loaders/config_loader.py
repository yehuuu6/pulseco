"""
Provides config loader and validation functionality for the pulseco app.
"""

from pulseco.utils import printb
from pulseco.loaders.classes import ServerConfig
from os import path, mkdir

DEFAULT_CONFIG: ServerConfig = ServerConfig(
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

def use_default_config() -> ServerConfig:
    """
    Saves the default config to settings.json and returns it.
    """
    if not path.exists("config"):
        try:
            mkdir("config")
        except Exception as e:
            printb(f"Failed to create config directory: {e}", log=True)
            printb("Using default config from memory instead...", log=True)
            return DEFAULT_CONFIG

    printb("Using default config...", log=True)
    with open("config/settings.json", "w") as f:
        f.write(DEFAULT_CONFIG.model_dump_json(indent=4))
    return DEFAULT_CONFIG

def load_config() -> ServerConfig:
    """
    Loads the config from settings.json and validates it.
    """
    try:
        printb("Loading config...", log=True)
        with open("config/settings.json", "r") as f:
            config = ServerConfig.model_validate_json(f.read(), strict=True)
        printb("Config loaded successfully.", log=True)
    except Exception as e:
        printb(f"Failed to load config: {e}", log=True)
        config = use_default_config()
    return config