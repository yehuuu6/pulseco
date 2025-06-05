from app.models.room import RoomSingleton
from prompt_toolkit import PromptSession, ANSI
from typing import Any, List
from pydantic import StrictStr
from app.utils.functions import printf, is_space, set_window_title
from app.models.package import Package, send_package, get_package
from app.models.user import User
# from rich.markup import escape

import threading
import socket as sck
import json
import asyncio
import rich.traceback

rich.traceback.install() # Better error reporting

room = RoomSingleton()
room.cfg_loader.load_config()  # Load the server configuration
room.cmd_loader.load_commands()  # Load the commands
room.users_list = []  # Initialize the users list

cfg = room.cfg_loader.config  # Get the configuration object

if cfg.enable_plugins:
    room.plugin_loader.load_plugins()  # Load the plugins
else:
    printf("[orange1]Warning:[/] Plugins are disabled in the configuration. No plugins will be loaded.")

if cfg.debug:
    printf("[orange1]Warning:[/] Debug mode is enabled. This is not recommended for production use.")

room.sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  # Create a socket for the server
room.sock.bind((str(cfg.ip), cfg.port))  # Bind the socket to the host and port

consoleTitle: dict[StrictStr, Any] = {
    "name": cfg.name,
    "max_users": cfg.max_users,
}

set_window_title(titleObj = consoleTitle, online_users_count = len(room.users_list))

def refresh_title() -> None:
    set_window_title(titleObj = consoleTitle, online_users_count = len(room.users_list))

async def handle_admin_input() -> None:
    prompt_text = f"console@{cfg.id}" + r"\~ "
    session: PromptSession[Any] = PromptSession(ANSI(prompt_text), erase_when_done=True)

    while True:  
        try:
            cin: str = await session.prompt_async()
            if is_space(cin):
                continue
        except (EOFError, KeyboardInterrupt):
            room.sock.close()
            exit(0)

        input_list = cin.strip().split(' ')
        command: str = input_list[0]
        args: List[str] = input_list[1:]

        if room.cmd_loader.get_command_by_name(command) is not None:
            cmd = room.cmd_loader.get_command_by_name(command)
            try:
                cmd.run(*args)  # type: ignore
            except Exception as e:
                printf(f"[red]Error executing command '{command}': {e}[/]")
        else:
            printf(f"[red]Unknown command:[/] {command}. Type 'help' for a list of commands.")

def handle_package(package: Package, sender: sck.socket) -> None:
    """
    Handles received packages.
    """
    if not package.is_valid_package():
        printf(f"[red]Error:[/red] Invalid package received, something is wrong!")
        _package = Package(type = "message", content = "You have send an invalid package. Connection will be closed.")
        send_package(_package, sender)
        sender.close()

    if package.type == "handshake":
        user_data: dict[str, Any] = json.loads(package.content)
        user_id = user_data["id"]
        user_name = user_data["name"]

        user = User(id = user_id, name = user_name, sock = sender)

        room.users_list.append(user)

        refresh_title()

        room.broadcast(message=f"[cyan]{user.name}[/] has joined the room.")

    elif package.type == "message":
        user = room.get_user_by_socket(sock = sender)
        # Content is already a dict, no need to parse JSON
        if user is None or is_space(package.content):
            return
    
        room.broadcast(user=user, message=package.content)

def client_handler(client: sck.socket, address: tuple[str, int]) -> None:
    try:
        while True:
            package = get_package(client)
            if package is not None:
                handle_package(package, client)
            else:
                printf(f"Connection from {address} has been lost.")
                user = room.get_user_by_socket(client)
                if user is not None:
                    room.users_list.remove(user)
                    room.broadcast(message=f"[cyan]{user.name}[/] has left the room.")
                    refresh_title()
                break
    except sck.error:
        # Handle socket errors (disconnections, etc.)
        printf(f"Connection from {address} has been lost unexpectedly.")
        user = room.get_user_by_socket(client)
        if user is not None:
            room.users_list.remove(user)
            room.broadcast(message=f"[cyan]{user.name}[/] has left the room unexpectedly.")
            refresh_title()
    finally:
        try:
            client.close()
        except:
            pass

def connection_handler() -> None:
    while True:
        try:
            client_socket, address = room.sock.accept()

            # Check if we've reached the maximum number of users
            if len(room.users_list) >= cfg.max_users:
                printf(f"Connection from {address} rejected - server is full.")
                error_package = Package(type="message", content="[red3]Server is full. Please try again later.[/]")
                send_package(error_package, client_socket)
                client_socket.close()
                continue

            printf(f"Connection from {address} has been established.")

            client_handler_thread = threading.Thread(target=client_handler, args=(client_socket, address), daemon=True)
            client_handler_thread.start()

            package = Package(type = "handshake", content = "nickname")
            send_package(package, client_socket)

        except sck.error as e:
            print(f"[red]Error:[/red] Failed to accept connection: {e}")
        except KeyboardInterrupt:
            room.cmd_loader.get_command_by_name("shutdown").run()  # type: ignore
            room.sock.close()
            break

def run_server() -> None:
    printf(f"Starting server on [green3]{cfg.ip}:{cfg.port}[/]")
    room.sock.listen(10)
    printf(f"Server is [green3]running[/]!")
    connection_handler_thread = threading.Thread(target=connection_handler, daemon=True)
    connection_handler_thread.start()
    try:
        asyncio.set_event_loop(room.input_loop)
        room.input_loop.run_until_complete(handle_admin_input())
    except KeyboardInterrupt:
        printf("[orange1]Server shutdown initiated by user.[/]")
    finally:
        room.input_loop.close()
        printf("Server has been shut down.")
        room.sock.close()
        exit(0)