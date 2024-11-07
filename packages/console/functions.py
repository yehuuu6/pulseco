"""
Provides functions for the console package.
"""
from packages.utils import printb
from packages.console.command_registery import command_registry

def help_function() -> None:
    print('Usage: python pulse.py <command> [args]')
    print('Commands:')
    for command in command_registry.get_commands():
        print(f'{command.name}: {command.description}')

def clear_logs_function(file_name: str) -> None:
    try:
        printb(f'Clearing {file_name}...', log=True)
        # Check if the file exists
        open(f'logs/{file_name}', 'r').close()
        with open(f'logs/{file_name}', 'w') as f:
            f.write('')
        printb(f'{file_name} cleared successfully.', log=True)
    except Exception as e:
        printb(f'Failed to clear {file_name}: {e}', log=True)