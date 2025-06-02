from typing import Any
from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __repr__(self) -> str:
        """
        Return a string representation of the command.
        This method should be implemented by subclasses to provide a meaningful representation.
        """
        return f"Command(name={self.name}, description={self.description})"
    
    def __str__(self) -> str:
        return f"[bright_cyan]{self.name}[/]: {self.description}"
    
    @abstractmethod
    def usage(self) -> str:
        """
        Return a string that describes how to use the command.
        This method should be implemented by subclasses to provide usage instructions.
        """
        return f"Usage: You should give the command {self.name} with the following arguments: ..."

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> None:
        """
        Run the command with the given arguments.
        This method should be implemented by subclasses to define the command's behavior.
        """
        pass