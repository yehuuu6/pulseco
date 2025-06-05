from app.models.package import Package
from app.models.user import User
from app.utils.functions import printf
from typing import List
from abc import ABC, abstractmethod

class Plugin(ABC):
    def __init__(self, name: str, description: str, version: str, author: str, color: str):
        self.name = name
        self.description = description
        self.author = author
        self.version = version
        self.color = color
        self.prefix = f"[{self.color}]{self.name.strip()}[/]"
        self.room = None  # This will be set by the plugin loader
    
    def __str__(self) -> str:
        return f"{self.prefix}: {self.description} | v{self.version}"
    
    # Events

    @abstractmethod
    def on_load(self) -> None:
        """
        Called when the plugin is loaded.
        """
        from app.server import room
        self.room = room
        printf(f"Plugin {self.prefix} loaded successfully.")

    @abstractmethod
    def on_package_received(self, package: Package) -> None:
        """
        Called when a package is received.
        """
        printf(f"{self.prefix}: received package: {package.type}")

    @abstractmethod
    def on_command_received(self, command: str, args: List[str], executer: User) -> None:
        """
        Called when a command is received.
        """
        printf(f"{self.prefix}: Received command: <{command}> with args: <{args}> from <{executer.name}>")

    @abstractmethod
    def on_user_joined(self, user: User) -> None:
        """
        Called when a user joins.
        """
        printf(f"{self.prefix}: User joined: {user.name}")

    @abstractmethod
    def on_user_left(self, user: User) -> None:
        """
        Called when a user leaves.
        """
        printf(f"{self.prefix}: User left: {user.name}")