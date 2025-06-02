from app.models.room import RoomSingleton
from prompt_toolkit import PromptSession, ANSI
from typing import Any, List
from pydantic import StrictStr
from app.utils.functions import printf  # Importing the printf function for console output

import asyncio
import rich.traceback

rich.traceback.install() # Better error reporting
    
server = RoomSingleton()
server.cfg_loader.load_config()  # Load the server configuration
server.cmd_loader.load_commands()  # Load the commands

if server.cfg_loader.config.debug:
    printf("[orange1]Warning:[/] Debug mode is enabled. This is not recommended for production use.")

def set_console_title(titleObj: dict[StrictStr, Any], online_users: int = 0) -> None:
    # Set the console title
    import sys
    title: str = f"\033]0;{titleObj['name']} - {online_users}/{titleObj['max_users']} online\007"
    sys.stdout.write(title)
    sys.stdout.flush()

async def handle_admin_input() -> None:
    consoleTitle: dict[StrictStr, Any] = {
        "name": server.cfg_loader.config.name,
        "max_users": server.cfg_loader.config.max_users,
    }

    set_console_title(titleObj = consoleTitle, online_users = 0)  # Set the console title with the server name

    prompt_text = f"console@{server.cfg_loader.config.id}" + r"\~ "
    session: PromptSession[Any] = PromptSession(ANSI(prompt_text), erase_when_done=True)

    while True:  
        try:
            cin: str = await session.prompt_async()
            if cin == "":
                continue
        except (EOFError, KeyboardInterrupt):
            exit(0)
            break

        input_list = cin.strip().split(' ')
        command: str = input_list[0]
        args: List[str] = input_list[1:]

        if server.cmd_loader.get_command_by_name(command) is not None:
            cmd = server.cmd_loader.get_command_by_name(command)
            try:
                cmd.run(*args)  # type: ignore
            except Exception as e:
                printf(f"[red]Error executing command '{command}': {e}[/]")
        else:
            printf(f"[red]Unknown command:[/] {command}. Type 'help' for a list of commands.")

def run_server() -> None:
    try:
        asyncio.set_event_loop(server.input_loop)
        server.input_loop.run_until_complete(handle_admin_input())
    except KeyboardInterrupt:
        printf("[orange1]Server shutdown initiated by user.[/]")
    finally:
        server.input_loop.close()
        printf("Server has been shut down.")
        exit(0)