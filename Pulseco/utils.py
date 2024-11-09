"""
Provides utility functions for the pulseco app.
"""

from pulseco.log_manager import main_logger

def printb(text: str, log: bool = False) -> None:
    """
    Prints a message to the console and logs it if specified.
    Its name is shorthand for 'print better.'
    """
    if log:
        main_logger.info(text)
    print(text)