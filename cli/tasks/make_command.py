from app.utils.functions import printf
from cli.models.task import Task

import os

class MakeCommandTask(Task):
    """Create a new server command"""
    
    def __init__(self):
        super().__init__(
            namespace="make",
            name="command",
            description="Create a new server command"
        )
    
    def usage(self) -> str:
        return "[bright_yellow]Usage:[/] python pulse.py [green3]make:command[/] --name [bright_magenta]<name *>[/] --description [bright_magenta]<description *>[/]"
    
    def handle(self, *args: str) -> None:
        if not args:
            raise ValueError("Arguments are required")
        
        # Parse arguments
        name = None
        description = None
        
        i = 0
        while i < len(args):
            arg = args[i]
            if arg == "--name" and i + 1 < len(args):
                # Collect all words until next -- argument
                name_parts: list[str] = []
                i += 1
                while i < len(args) and not args[i].startswith("--"):
                    name_parts.append(args[i])
                    i += 1
                name = " ".join(name_parts)
            elif arg == "--description" and i + 1 < len(args):
                # Collect all words until next -- argument
                desc_parts: list[str] = []
                i += 1
                while i < len(args) and not args[i].startswith("--"):
                    desc_parts.append(args[i])
                    i += 1
                description = " ".join(desc_parts)
            else:
                i += 1
        
        # Safety checks
        if name is None or name.strip() == "":
            raise ValueError("--name argument is required and cannot be empty")
        if description is None or description.strip() == "":
            raise ValueError("--description argument is required and cannot be empty")
        
        # Load stub file
        with open("app/templates/command.stub", "r") as file:
            template = file.read()

        replacements = {
            "{{ $name }}": name,
            "{{ $name.uppercase }}": ''.join(word.capitalize() for word in name.split()),
            "{{ $description }}": description
        }

        for key, value in replacements.items():
            template = template.replace(key, value)

        # Define file name, e.g example_command.py
        filename = f"{name.lower().replace(' ', '_')}.py"

        # If the command already exists, raise an error
        if os.path.exists(os.path.join("app/commands", filename)):
            raise FileExistsError(f"Command '{name}' already exists.")

        filepath = os.path.join("app/commands", filename)

        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Write the generated command
        with open(filepath, "w") as file:
            file.write(template)

        printf(f"[green3]✅ Command created at {filepath}[/]")
