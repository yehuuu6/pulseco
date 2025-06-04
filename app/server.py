from app.models.room import RoomSingleton
from prompt_toolkit import PromptSession, ANSI
from typing import Any, List
from pydantic import StrictStr
from app.utils.functions import printf, is_space, set_window_title
from app.models.package import Package, send_package, get_package
from app.models.user import User
from rich.markup import escape

import threading
import socket as sck
import json
import asyncio
import rich.traceback

rich.traceback.install() # Better error reporting

server = RoomSingleton()
server.cfg_loader.load_config()  # Load the server configuration
server.cmd_loader.load_commands()  # Load the commands
server.users_list = []  # Initialize the users list

cfg = server.cfg_loader.config  # Get the configuration object

if cfg.debug:
    printf("[orange1]Warning:[/] Debug mode is enabled. This is not recommended for production use.")

server.sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  # Create a socket for the server
server.sock.bind((str(cfg.ip), cfg.port))  # Bind the socket to the host and port

consoleTitle: dict[StrictStr, Any] = {
    "name": cfg.name,
    "max_users": cfg.max_users,
}

set_window_title(titleObj = consoleTitle, online_users_count = len(server.users_list))

def refresh_title() -> None:
    set_window_title(titleObj = consoleTitle, online_users_count = len(server.users_list))

async def handle_admin_input() -> None:
    prompt_text = f"console@{cfg.id}" + r"\~ "
    session: PromptSession[Any] = PromptSession(ANSI(prompt_text), erase_when_done=True)

    while True:  
        try:
            cin: str = await session.prompt_async()
            if is_space(cin):
                continue
        except (EOFError, KeyboardInterrupt):
            server.sock.close()
            exit(0)

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
        printf(f"[green]Handshake received from {sender.getpeername()}[/green]")
        user_data: dict[str, Any] = json.loads(package.content)
        user_id = user_data["id"]
        user_name = user_data["name"]

        user = User(id = user_id, name = user_name, sock = sender)

        if user.is_banned:
            banned_inform_package = Package(type = "message", content = "You are banned from this room!")
            send_package(banned_inform_package, sender)
            user.disconnect()
            printf(f"[cyan]{user.name}[/cyan] tried to join the room, but they are banned.")
            return

        server.users_list.append(user)

        refresh_title()

        server.broadcast(f"[cyan]{user.name}[/cyan] has joined the room.")

    elif package.type == "message":
        user = server.get_user_by_socket(sock = sender)
        if user is None:
            return
        if package.content == "":
            return
        # If package content has only spaces, ignore it.
        if is_space(package.content):
            return

        server.broadcast(f"<{user.name}> {escape(package.content)}")

def client_handler(client: sck.socket, address: tuple[str, int]) -> None:
    try:
        while True:
            package = get_package(client)
            if package is not None:
                handle_package(package, client)
            else:
                printf(f"Connection from {address} has been lost.")
                user = server.get_user_by_socket(client)
                if user is not None:
                    server.users_list.remove(user)
                    printf(f"[cyan]{user.name}[/cyan] has left the room.")
                    refresh_title()
                break
    except sck.error:
        # Handle socket errors (disconnections, etc.)
        printf(f"Connection from {address} has been lost unexpectedly.")
        user = server.get_user_by_socket(client)
        if user is not None:
            server.users_list.remove(user)
            printf(f"[cyan]{user.name}[/cyan] has left the room.")
            refresh_title()
    finally:
        try:
            client.close()
        except:
            pass

def connection_handler() -> None:
    while True:
        try:
            client_socket, address = server.sock.accept()
            printf(f"Connection from {address} has been established.")

            client_handler_thread = threading.Thread(target=client_handler, args=(client_socket, address), daemon=True)
            client_handler_thread.start()

            package = Package(type = "handshake", content = "nickname")
            send_package(package, client_socket)

        except sck.error as e:
            print(f"[red]Error:[/red] Failed to accept connection: {e}")
        except KeyboardInterrupt:
            server.cmd_loader.get_command_by_name("shutdown").run()  # type: ignore
            break

def run_server() -> None:
    printf(f"[green]Starting server on {cfg.ip}:{cfg.port}...[/]")
    server.sock.listen(cfg.max_users)  # Start listening for incoming connections
    printf(f"[green]Server is running![/]")
    connection_handler_thread = threading.Thread(target=connection_handler, daemon=True)
    connection_handler_thread.start()
    try:
        asyncio.set_event_loop(server.input_loop)
        server.input_loop.run_until_complete(handle_admin_input())
    except KeyboardInterrupt:
        printf("[orange1]Server shutdown initiated by user.[/]")
    finally:
        server.input_loop.close()
        printf("Server has been shut down.")
        exit(0)