"""
The command line tool named 'Pulse' to manage your pulseco chat server.
"""

from sys import argv
import pulseco.console.commands as Pulse
from pulseco.console.command_registry import command_registry


def main() -> None:
    """
    The main function of the pulseco command line tool.
    """
    Pulse.init_module()

    if len(argv) == 1:
        print("Usage: pulse.py <command> [args]")
        print('Use "python pulse.py help" for help.')
        return

    command = argv[1]
    # Get all the commands from the command registry and store them in a dictionary.
    commands = {cmd.name: cmd for cmd in command_registry.get_commands()}

    if command in commands:
        commands[command].execute(*argv[2:])
    else:
        print(f"Unknown command: {command}")
        print('Use "python pulse.py help" for help.')


if __name__ == "__main__":
    main()
