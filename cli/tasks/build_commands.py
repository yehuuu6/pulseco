from app.utils.functions import printf
from cli.models.task import Task

import subprocess

class BuildCommandsTask(Task):
    """Build server commands for production"""
    
    def __init__(self):
        super().__init__(
            namespace="build",
            name="commands",
            description="Build server commands for production"
        )
    
    def usage(self) -> str:
        return "[orange1]Usage:[/] python pulse.py build:commands - Builds the server commands for production. This will run the build script located at app/scripts/build_commands.sh."
    
    def handle(self, *args: str) -> None:
        try:
            subprocess.run(["bash", "app/scripts/build_commands.sh"], check=True)
        except subprocess.CalledProcessError as e:
            printf(f"[red]❌ Build failed: {e}[/]")
        else:
            printf("[green3]✅ Build completed successfully![/]")
