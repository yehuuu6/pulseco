from app.loaders.config_loader import ConfigLoaderSingleton
from app.loaders.command_loader import CommandLoaderSingleton
from app.loaders.plugin_loader import PluginLoaderSingleton
from app.models.package import Package, send_package
from app.utils.functions import printf
from typing import List
# from rich.markup import escape
from app.models.user import User

import socket as sck
import asyncio

class RoomSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
            self.users_list: List[User] = []
            self.cfg_loader: ConfigLoaderSingleton = ConfigLoaderSingleton()
            self.cmd_loader: CommandLoaderSingleton = CommandLoaderSingleton()
            self.plugin_loader: PluginLoaderSingleton = PluginLoaderSingleton()
            self.input_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
            self._initialized = True

    def get_user_by_socket(self, sock: sck.socket) -> User | None:
        for user in self.users_list:
            if user.sock == sock:
                return user
        return None
    
    def broadcast(self, message: str, user: User | None = None, exclude: User | None = None, render_on_console: bool = True) -> None:
        if user is None:
            final_message = message
        else:
            final_message: str = f"[cyan]{user.name}[/]: {message}"
        package = Package(type="message", content=final_message)
        if render_on_console:
                printf(final_message)
        for user in self.users_list:
            send_package(package, user.sock)
            if user == exclude:
                continue
                