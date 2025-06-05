from app.utils.functions import printf
from cli.models.task import Task

import os

class MakePluginTask(Task):
    """Create a new server plugin"""
    
    def __init__(self):
        super().__init__(
            namespace="make",
            name="plugin",
            description="Create a new server plugin"
        )
    
    def usage(self) -> str:
        return "[bright_yellow]Usage:[/] python pulse.py [green3]make:plugin[/] --name [bright_magenta]<name *>[/] --description [bright_magenta]<description *>[/] --author [bright_magenta]<author *>[/] --color [bright_magenta]<color *>[/] --version [bright_magenta]<version>[/]"
    
    def handle(self, *args: str) -> None:
        if not args:
            raise ValueError("Arguments are required")
        
        # Parse arguments
        name = None
        description = None
        version = "1.0.0"
        author = None
        color = None
        
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
            elif arg == "--version" and i + 1 < len(args):
                version = args[i + 1]
                i += 2
            elif arg == "--author" and i + 1 < len(args):
                author = args[i + 1]
                i += 2
            elif arg == "--color" and i + 1 < len(args):
                color = args[i + 1]
                i += 2
            else:
                i += 1
        
        # Safety checks
        if name is None or name.strip() == "":
            raise ValueError("--name argument is required and cannot be empty")
        if description is None or description.strip() == "":
            raise ValueError("--description argument is required and cannot be empty")
        if author is None or author.strip() == "":
            raise ValueError("--author argument is required and cannot be empty")
        if color is None or color.strip() == "":
            raise ValueError("--color argument is required and cannot be empty")
        if version.strip() == "":
            raise ValueError("Version cannot be empty")
        
        # Load stub file
        with open("app/templates/plugin.stub", "r") as file:
            template = file.read()

        replacements = {
            "{{ $name }}": name,
            "{{ $name.uppercase }}": ''.join(word.capitalize() for word in name.split()),
            "{{ $description }}": description,
            "{{ $version }}": version,
            "{{ $author }}": author,
            "{{ $color }}": color,
        }

        for key, value in replacements.items():
            template = template.replace(key, value)

        # Define file name, e.g example_plugin.py
        filename = f"{name.lower().replace(' ', '_')}.py"

        # If the plugin already exists, raise an error
        if os.path.exists(os.path.join("app/plugins", filename)):
            raise FileExistsError(f"Plugin '{name}' already exists.")

        filepath = os.path.join("app/plugins", filename)

        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Write the generated plugin
        with open(filepath, "w") as file:
            file.write(template)

        printf(f"[green3]✅ Plugin created at {filepath}[/]")
