"""
Provides functions for the console package.
"""
from Pulseco.utils import printb
from Pulseco.Console.command_registery import command_registry
from typing import Any

def help_function() -> None:
    print('Usage: python pulse.py <command> [args]')
    print('Commands:')
    for command in command_registry.get_commands():
        print(f'{command.name}: {command.description}')

def clear_logs_function(file_name: str) -> None:
    try:
        printb(f'Clearing "{file_name}"...', log=True)
        # Check if the file exists
        open(f'logs/{file_name}', 'r').close()
        with open(f'logs/{file_name}', 'w') as f:
            f.write('')
        printb(f'{file_name} cleared successfully.', log=True)
    except Exception as e:
        printb(f'Failed to clear given log file: {e}', log=True)

def test_command_function(arg1: Any, arg2: Any) -> None:
    args = [arg1, arg2]
    print(f'Test command executed with args: {args}')