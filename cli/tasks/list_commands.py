from app.utils.functions import printf
from cli.models.task import Task

class ListCommandsTask(Task):
    """List all available server commands"""
    
    def __init__(self):
        super().__init__(
            namespace="list",
            name="commands",
            description="List all available server commands"
        )
    
    def usage(self) -> str:
        return "[bright_yellow]Usage:[/] python pulse.py [green3]list:commands[/] - Lists all server commands"
    
    def handle(self, *args: str) -> None:
        import os
        import json
        
        config_path = "config/server_options.json"
        if not os.path.exists(config_path):
            printf("[red3]Error:[/] Configuration file not found! Run the server for once to generate it.")
            return
        
        # Load configuration
        with open(config_path, "r") as file:
            cfg = json.load(file)
        
        commands_folder = "app/commands" if cfg.get("debug", True) else "build/commands"
        file_extension = ".py" if cfg.get("debug", True) else ".so"
        if not os.path.exists(commands_folder):
            printf("[red3]Error:[/] Commands folder not found!")
            return
        
        printf("[bright_yellow]Available Server Commands:[/]")
        printf("")
        
        for filename in os.listdir(commands_folder):
            if filename.endswith(file_extension) and not filename.startswith("__"):
                command_name = filename[:-3].replace("_", " ").title()
                printf(f"• [green3]{command_name}[/] ({filename})")
        
        printf("")
        printf("[bright_cyan]Note:[/] These are server runtime commands, not CLI tasks.")
