from app.utils.functions import printf
from cli.models.task import Task

import subprocess

class BuildPluginsTask(Task):
    """Build server plugins for production"""
    
    def __init__(self):
        super().__init__(
            namespace="build",
            name="plugins",
            description="Build server plugins for production"
        )
    
    def usage(self) -> str:
        return "[orange1]Usage:[/] python pulse.py build:plugins - Builds the server plugins for production. This will run the build script located at app/scripts/build_plugins.sh."
    
    def handle(self, *args: str) -> None:
        try:
            subprocess.run(["bash", "app/scripts/build_plugins.sh"], check=True)
        except subprocess.CalledProcessError as e:
            printf(f"[red]❌ Build failed: {e}[/]")
        else:
            printf("[green3]✅ Build completed successfully![/]")
