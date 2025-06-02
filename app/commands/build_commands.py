from app.models.command import Command
from app.utils.functions import printf
# from app.server import server # Used to access to the server (room) singleton.

import subprocess

class BuildCommandsCommand(Command):
    def __init__(self):
        super().__init__(name="build_commands", description="Builds commands for production")

    def usage(self) -> str:
        return "Usage: build_commands - Builds the commands for production. This will run the build script located at app/scripts/build_commands.sh."

    def run(self) -> None:
        try:
            subprocess.run(["bash", "app/scripts/build_commands.sh"], check=True)
        except subprocess.CalledProcessError as e:
            printf(f"[red]❌ Build failed: {e}[/]")
        else:
            printf("[green3]✅ Build completed successfully![/]")