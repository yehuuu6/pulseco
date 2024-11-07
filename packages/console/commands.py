from packages.console.classes import Command
from packages.console.command_registery import command_registry
import packages.console.functions as funcs

# Create commands
help = Command(name= 'help',
                description='Prints the help message for the pulseco command line tool.',
                function=funcs.help_function)
command_registry.register(help)

clear_logs = Command(name='clear_logs',
                    description='Clears a log file.',
                    function=funcs.clear_logs_function)
command_registry.register(clear_logs)