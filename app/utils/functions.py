from io import StringIO
from rich.console import Console
from pydantic import StrictStr
from typing import Any
from prompt_toolkit import ANSI, print_formatted_text

import time

output_buffer = StringIO()
console = Console(file=output_buffer, color_system="truecolor")

def set_window_title(titleObj: dict[StrictStr, Any], online_users_count: int) -> None:
    # Set the console title
    import sys
    title: str = f"\033]0;{titleObj['name']} - {online_users_count}/{titleObj['max_users']} online\007"
    sys.stdout.write(title)
    sys.stdout.flush()

def is_space(s: str) -> bool:
    """
    Checks if the given string is empty or contains only whitespace characters.
    """
    return not s or s.isspace()

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