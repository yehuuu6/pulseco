from app.models.command import Command
from app.utils.functions import printf  # Importing the printf function for console output
from app.server import server # Used to access to the server (room) singleton.

class HelpCommand(Command):
    def __init__(self):
        super().__init__(name="help", description="Display the available commands and their descriptions.")

    def usage(self) -> str:
        return f"Usage: help <command_name> for detailed information about a specific command."

    def run(self, command_name: str = "") -> None:
        if command_name != "":
            command = server.cmd_loader.get_command_by_name(command_name)
            if command:
                printf(command.usage())
            else:
                printf(f"❌ Command '{command_name}' not found.")
        else:
            printf("Available commands:")
            for cmd in server.cmd_loader.get_commands():
                printf(cmd) # type: ignore