from typing import List
from app.models.command import Command
from app.utils.functions import printf  # Importing the printf function for console output

import os
import sys
import importlib
import inspect

class CommandLoaderSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.commands: List[Command] = []
            self._initialized = True

    def _get_config(self):
        from app.server import room
        return room.cfg_loader.config

    def load_commands(self) -> None:
        config = self._get_config()
        DEBUG_MODE = config.debug
        
        if DEBUG_MODE:
            file_extension = ".py"
            commands_folder = "app/commands"
        else:
            file_extension = ".so"
            commands_folder = "build/commands"
        
        # Check if the folder exists
        if not os.path.exists(commands_folder):
            printf(f"[red]Commands folder {commands_folder} does not exist[/]")
            return

        sys.path.append(os.path.abspath(commands_folder))

        for filename in os.listdir(commands_folder):
            if filename.endswith(file_extension) and not filename.startswith("__"):
                module_name = filename[:-len(file_extension)]  # Remove the correct extension length
                try:
                    module = importlib.import_module(module_name)

                    for _name, obj in inspect.getmembers(module, inspect.isclass):
                        if issubclass(obj, Command) and obj is not Command:
                            command_instance = obj()  # type: ignore
                            self.commands.append(command_instance)
                            break
                    else:
                        printf(f"[orange1]No valid Command subclass found in {module_name}[/]")

                except Exception as e:
                    printf(f"[red]Error loading command {module_name}: {e}[/]")

    def get_commands(self) -> List[Command]:
        return self.commands

    def get_command_by_name(self, name: str) -> Command | None:
        for command in self.commands:
            if command.name == name:
                return command
        return None
