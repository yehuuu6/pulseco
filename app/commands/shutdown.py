from app.models.command import Command
from app.utils.functions import printf
from app.server import room # Used to access to the server (room) singleton.

class ShutdownCommand(Command):
    def __init__(self):
        super().__init__(name="shutdown", description="Shut down the server with the given message.")
    
    def usage(self) -> str:
        return f"Usage: shutdown <reason> - You should give a reason for shutting down the server. It will be broadcasted to all users."

    def run(self, *msg_parts: str) -> None:
        msg = " ".join(msg_parts)
        if msg.strip() == "":
            msg = "No reason provided."
        printf(f"Shutting down server: {msg}")
        room.sock.close()  # Close the server socket to stop accepting new connections.
        exit(0)