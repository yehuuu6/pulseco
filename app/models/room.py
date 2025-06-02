from app.loaders.config_loader import ConfigLoaderSingleton
from app.loaders.command_loader import CommandLoaderSingleton
import asyncio

class RoomSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.cfg_loader: ConfigLoaderSingleton = ConfigLoaderSingleton()
            self.cmd_loader: CommandLoaderSingleton = CommandLoaderSingleton()
            self.input_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
            self._initialized = True