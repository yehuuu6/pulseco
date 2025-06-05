from app.models.package import Package
from app.models.user import User
from app.utils.functions import printf
from typing import List, Set
from abc import ABC

class Plugin(ABC):
    def __init__(self, name: str, description: str, version: str, author: str, color: str):
        self.name = name
        self.description = description
        self.author = author
        self.version = version
        self.color = color
        self.prefix = f"[{self.color}]{self.name.strip()}[/]"
        self.room = None  # This will be set by the plugin loader
        self._registered_events: Set[str] = set()
    
    def __str__(self) -> str:
        return f"{self.prefix}: {self.description} | v{self.version}"
    
    def register_event(self, event_name: str) -> None:
        """Register this plugin for a specific event."""
        self._registered_events.add(event_name)
    
    def is_registered_for_event(self, event_name: str) -> bool:
        """Check if this plugin is registered for a specific event."""
        return event_name in self._registered_events
    
    # Events - now optional, not abstract

    def on_load(self) -> None:
        """Called when the plugin is loaded."""
        printf(f"Plugin {self.prefix} loaded successfully.")

    def on_package_received(self, package: Package) -> None:
        """Called when a package is received."""
        pass

    def on_command_received(self, command: str, args: List[str], executer: User | None = None) -> None:
        """Called when a command is received."""
        pass

    def on_user_joined(self, user: User) -> None:
        """Called when a user joins."""
        pass

    def on_user_left(self, user: User) -> None:
        """Called when a user leaves."""
        pass