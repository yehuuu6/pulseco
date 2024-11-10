from typing import List
from pulseco.console.commands import Command
import inspect
import os


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
        if command in self._commands:
            return
        self._commands.append(command)

    def get_commands(self) -> List[Command]:
        return self._commands

    def reset_instance(self) -> None:
        """
        Reset the singleton instance of the CommandRegistry class.
        Created for unit testing.
        It isolates the tests from each other and the application itself.
        DO NOT USE IN PRODUCTION CODE.
        """

        # Check if the method is called from a unit test where the file name starts with "test_"
        if not os.path.basename(inspect.stack()[1].filename).startswith("test_"):
            raise RuntimeError(
                "This method is only allowed to be called from unit tests."
            )

        self._instance = None
        self._commands = []


# Create a singleton instance
command_registry = CommandRegistry()
