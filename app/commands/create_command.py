from app.models.command import Command
from app.utils.functions import printf  # Importing the printf function for console output
# from app.server import server # Used to access to the server (room) singleton.

import os

class CreateCommandCommand(Command):
    def __init__(self):
        super().__init__(name="create_command", description="Creates a new command for your server")
    
    def usage(self) -> str:
        return "Usage: create_command <name*> <description*> - Creates a new command with the specified name and description."

    def run(self, name: str, *description_parts: str) -> None:
        if name.strip() == "":
            raise ValueError("Command name cannot be empty")
        
        description = " ".join(description_parts)
        if description.strip() == "":
            raise ValueError("Command description cannot be empty")

        # Load stub file
        with open("app/templates/command.stub", "r") as file:
            template = file.read()

        # Replace placeholders
        replacements = {
            "{{ $name }}": name.lower(),
            "{{ $name.uppercase }}": name.capitalize(),  # or name.upper()
            "{{ $description }}": description,
        }

        for key, value in replacements.items():
            template = template.replace(key, value)

        # Define output file path
        filename = f"{name.lower()}.py"

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