from Pulseco.Console.classes import Command
from Pulseco.Console.command_registery import command_registry
import Pulseco.Console.functions as funcs

def init_module():
    """
    Only exists to prevent circular imports error.
    """
    pass

# Create commands
help = Command(name= 'help',
                description='Prints the help message for the pulseco command line tool.',
                usage="Usage: python pulse.py help",
                function=funcs.help_function)
command_registry.register(help)

clear_logs = Command(name='clear_logs',
                    description='Clears the given log file.',
                    usage='Usage: python pulse.py clear_logs <log_file_name>',
                    function=funcs.clear_logs_function)
command_registry.register(clear_logs)

test_command = Command(name='test_command',
                    description='This is a test command.',
                    usage='Usage: python pulse.py test_command <arg1> <arg2>',
                    function=funcs.test_command_function)
command_registry.register(test_command)