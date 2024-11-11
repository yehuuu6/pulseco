"""
Provides built-in commands for the Pulse command line tool.
"""

from pulseco.console.classes import Command
from pulseco.console.command_registry import command_registry
from pulseco.loaders.custom_cmd_loader import load_commands
import pulseco.console.functions as funcs


def init_module():
    """
    Initializes the commands module by loading all the custom commands.
    """
    commands = load_commands()
    for command_name, command_module in commands.items():
        command = getattr(command_module, command_name)
        command_registry.register(command)


# Create commands
help = Command(
    name="help",
    description="Prints the help message for the pulseco command line tool.",
    usage="Usage: python pulse.py help",
    function=funcs.help_function,
)
command_registry.register(help)

clear_logs = Command(
    name="clear_logs",
    description="Clears the given log file.",
    usage="Usage: python pulse.py clear_logs <log_file_name>",
    function=funcs.clear_logs_function,
)
command_registry.register(clear_logs)

reset_config = Command(
    name="reset_config",
    description="Resets the config file to the default settings.",
    usage="Usage: python pulse.py reset_config",
    function=funcs.reset_config_function,
)
command_registry.register(reset_config)

test_command = Command(
    name="test_command",
    description="This is a test command.",
    usage="Usage: python pulse.py test_command <arg1> <arg2>",
    function=funcs.test_command_function,
)
command_registry.register(test_command)

make = Command(
    name="make",
    description="Creates the given component like a new command for the Pulse command line tool.",
    usage="Usage: python pulse.py make <component> <name>",
    function=funcs.make_function,
)
command_registry.register(make)
