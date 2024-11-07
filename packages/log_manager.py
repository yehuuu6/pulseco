from os import mkdir, path
from typing import List
from logging import getLogger, Logger, basicConfig, INFO

"""
Provides logging functionality for the pulseco app.
"""

# Create the main logger
main_logger: Logger = getLogger('pulseco') # Create the main logger
basicConfig(filename='logs/server.log', level=INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# If logs directory does not exist, create it
if not path.exists('logs'):
    main_logger.info('Creating logs directory...')
    mkdir('logs')
    main_logger.info('Logs directory created.')

# List of log files
log_files: List[str] = ['chat.log', 'commands.log', 'server.log']

# Create log files if they don't exist
for log_file in log_files:
    if not path.exists(f'logs/{log_file}'):
        main_logger.info(f'Creating {log_file}...')
        with open(f'logs/{log_file}', 'w') as f:
            f.write('')
        main_logger.info(f'{log_file} created.')