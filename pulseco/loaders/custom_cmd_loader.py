# Load command classes from the commands folder

from pathlib import Path
from importlib import import_module
from typing import Dict, Any
from pulseco.utils import printb
import os


def load_commands() -> Dict[str, Any]:
    """
    Load command classes from the commands folder.
    """

    os.makedirs("app/commands", exist_ok=True)

    commands: Dict[str, Any] = {}
    commands_path = Path("app/commands")
    for file in commands_path.glob("*.py"):
        if not file.stem.startswith("__"):
            module_name = file.stem
            try:
                module = import_module(f"app.commands.{module_name}")
                commands[module_name] = module
            except Exception as e:
                printb(f"Failed to import module {module_name}: {e}", log=True)
    return commands
