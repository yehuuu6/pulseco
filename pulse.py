"""
The command line tool named 'pulse' to manage your pulseco chat server.
"""

from sys import argv
from packages.console.commands import help, clear_logs

def main() -> None:
    """
    The main function of the pulseco command line tool.
    """
    if len(argv) == 1:
        print('Usage: pulse.py <command> [args]')
        print('Use "python pulse.py help" for help.')
        return
    command = argv[1]
    
    if command == 'help':
        help.execute()
    elif command == 'clear_logs':
        if len(argv) == 3:
            clear_logs.execute(argv[2])
        else:
            print('Usage: python pulse.py clear_logs <log_file_name>')
    else:
        print(f'Unknown command: {command}')
        print('Use "python pulse.py help" for help.')

if __name__ == "__main__":
    main()