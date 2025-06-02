from io import StringIO
from rich.console import Console
# from rich.markup import escape
from prompt_toolkit import ANSI, print_formatted_text

import time

output_buffer = StringIO()
console = Console(file=output_buffer, color_system="truecolor")

def clear_console() -> None:
    """
    Clears the server console.
    """
    print("\033[H\033[J", end='')  # ANSI escape sequence to clear the console

def get_current_time() -> str:
    """
    Returns the current time in HH:MM format.
    """
    return time.strftime("%H:%M:%S", time.localtime(time.time()))

def printf(msg: str) -> None:
    """
    Prints output to the server console.
    """
    output_buffer.seek(0)  # Reset the buffer to the beginning
    output_buffer.truncate(0)  # Clear the buffer content
    console.print(f"[white]{get_current_time()}[/white] {msg}")
    print_formatted_text(ANSI(output_buffer.getvalue()), end='')