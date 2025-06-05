from app.models.plugin import Plugin
from app.utils.functions import printf  # Importing the printf function for console output
from app.models.user import User
from app.models.package import Package
from typing import List

class AnnouncementsPlugin(Plugin):
    def __init__(self):
        super().__init__(
            name="Announcements",
            description="Sends announcement messages to the all users in the room",
            version="1.0.0",
            author="yehuuu6",
            color="green3",
        )

    def on_load(self) -> None:
        """
        Called when the plugin is loaded.
        """
        printf(f"Plugin {self.prefix} loaded successfully.")

    def on_package_received(self, package: Package) -> None:
        """
        Called when a package is received.
        """
        printf(f"{self.prefix}: received package: {package.type}")

    def on_command_received(self, command: str, args: List[str], executer: User) -> None:
        """
        Called when a command is received.
        """
        printf(f"{self.prefix}: Received command: <{command}> with args: <{args}> from <{executer.name}>")

    def on_user_joined(self, user: User) -> None:
        """
        Called when a user joins.
        """
        printf(f"{self.prefix}: User joined: {user.name}")

    def on_user_left(self, user: User) -> None:
        """
        Called when a user leaves.
        """
        printf(f"{self.prefix}: User left: {user.name}")