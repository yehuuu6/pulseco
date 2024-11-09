from typing import List
from Pulseco.Console.commands import Command

class CommandRegistry:
    """
    Singleton class that holds all the commands that can be executed in the pulse console.
    """
    _instance = None
    _commands: List[Command] = []

    # Singleton pattern
    # This class will only have one instance.
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommandRegistry, cls).__new__(cls)
        return cls._instance

    def register(self, command: Command):
        self._commands.append(command)

    def get_commands(self) -> List[Command]:
        return self._commands

# Create a singleton instance
command_registry = CommandRegistry()