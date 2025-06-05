from app.utils.functions import printf
from cli.models.task import Task

class ListPluginsTask(Task):
    """List all available server plugins"""
    
    def __init__(self):
        super().__init__(
            namespace="list",
            name="plugins",
            description="List all available server plugins"
        )
    
    def usage(self) -> str:
        return "[bright_yellow]Usage:[/] python pulse.py [green3]list:plugins[/] - Lists all server plugins"
    
    def handle(self, *args: str) -> None:
        import os
        
        config_path = "config/server_options.json"
        if not os.path.exists(config_path):
            printf("[red3]Error:[/] Configuration file not found! Run the server for once to generate it.")
            return
        
        import json

        # Load configuration
        with open(config_path, "r") as file:
            cfg = json.load(file)
        
        plugins_folder = "app/plugins" if cfg.get("debug", True) else "build/plugins"
        file_extension = ".py" if cfg.get("debug", True) else ".so"
        if not os.path.exists(plugins_folder):
            printf("[red3]Error:[/] Plugins folder not found! Did you try to build plugins using [green3]build:plugins[/]?")
            return
        
        printf("[bright_yellow]Available Server Plugins:[/]")
        
        for filename in os.listdir(plugins_folder):
            if filename.endswith(file_extension) and not filename.startswith("__"):
                plugin_name = filename[:-3].replace("_", " ").title()
                printf(f"• [green3]{plugin_name}[/] ({filename})")
        
        # If no plugins found
        if not any(filename.endswith(file_extension) and not filename.startswith("__") for filename in os.listdir(plugins_folder)):
            printf("[red3]No plugins found![/] You can create a new plugin using [green3]make:plugin[/].")
