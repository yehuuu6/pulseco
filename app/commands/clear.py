from app.models.command import Command
from app.utils.functions import clear_console  # Importing the printf function for console output
# from app.server import room # Used to access to the server (room) singleton.

class ClearCommand(Command):
    def __init__(self):
        super().__init__(name="clear", description="Clear the server's console.")
    
    def usage(self) -> str:
        """
        Return a string that describes how to use the command.
        This method should be implemented by subclasses to provide usage instructions.
        """
        return f"Usage: Just type '{self.name}' to clear the console."

    def run(self) -> None:
        clear_console()
