"""
Provides functions for the console package.
"""
from pulseco.utils import printb
from pulseco.console.command_registry import command_registry
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
    
def reset_config_function() -> None:
    confirmation: str = input('Are you sure you want to reset the config? (y/n): ')
    if confirmation.lower() != 'y':
        printb('Config reset aborted.', log=True)
        return
    printb('Resetting config...', log=True)
    from pulseco.loaders.config_loader import use_default_config
    use_default_config()
    printb('Config reset successfully.', log=True)

def test_command_function(arg1: Any, arg2: Any) -> None:
    args = [arg1, arg2]
    print(f'Test command executed with args: {args}')