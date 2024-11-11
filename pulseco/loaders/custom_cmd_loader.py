# Load command classes from the commands folder

from pathlib import Path
from importlib import import_module
from typing import Dict, Any
from pulseco.log_manager import main_logger
import os


def load_commands() -> Dict[str, Any]:
    """
    Load command classes from the commands folder.
    """

    os.makedirs("commands", exist_ok=True)

    commands: Dict[str, Any] = {}
    commands_path = Path("commands")
    for file in commands_path.glob("*.py"):
        if not file.stem.startswith("__"):
            module_name = file.stem
            try:
                module = import_module(f"commands.{module_name}")
                commands[module_name] = module
            except Exception as e:
                main_logger.error(f"Failed to import module {module_name}: {e}")
    return commands
