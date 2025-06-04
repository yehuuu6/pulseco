from app.utils.functions import printf, is_space
from prompt_toolkit import PromptSession, ANSI
from typing import Any
from time import sleep
from app.models.user import User
from app.models.package import Package, send_package, get_package

import socket as sck
import threading
import asyncio
import random
import string

COMPUTER = sck.gethostname() # This is the computer name, used for the package source.

input_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()  # Create a new event loop for handling input

client_sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

def generate_random_string(length: int) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_random_username() -> str:
    # Generate a random username with a length of 10 characters, only alphabets, no digits.
    characters = string.ascii_letters
    return ''.join(random.choice(characters) for _ in range(10))

user_id = generate_random_string(10)
user_name = generate_random_username()

#IP = input("Server IP: ")
#PORT = int(input("Server Port: "))

IP = "127.0.0.1"
PORT = 7030

def handle_package(package: Package) -> None:
    if not package.is_valid_package():
        printf(f"Invalid package received, something is wrong!")

    if package.type == "handshake" and package.content == "nickname":
        user_package = Package(type = "handshake", content = user.get_json())
        send_package(user_package, client_sock)

    elif package.type == "message":
        printf(f"{package.content}")

async def handle_admin_input() -> None:
    prompt_text = f"{user_name}@{COMPUTER}" + r"\~ "
    session: PromptSession[Any] = PromptSession(ANSI(prompt_text), erase_when_done=True)

    while True:  
        try:
            cin: str = await session.prompt_async()
            if is_space(cin):
                continue
        except (EOFError, KeyboardInterrupt):
            exit(0)
            break
        msg = f"{cin}"
        if msg.startswith("/"):
            package =Package(type = "command", content = msg.replace("/", "", 1))
        else:
            package = Package(type = "message", content = msg)
        send_package(package, client_sock)

def listen() -> None:
    while True:
        try:
            package = get_package(client_sock)
            if package is not None:
                handle_package(package)
        except sck.error:
            printf("An error occured!")
            client_sock.close()
            break

def connect_to_room() -> None:
    global user
    try:
        client_sock.connect((IP, PORT))
        user = User(id = user_id, name = user_name, sock = client_sock)
    except ConnectionRefusedError:
        printf("Connection refused by the room.")
        sleep(3)
        exit(1)
    
    listen_thread = threading.Thread(target=listen, daemon=True)
    listen_thread.start()

def main() -> None:
    printf(f"Welcome {user_name}! Connecting to the room...")
    connect_to_room()
    try:
        asyncio.set_event_loop(input_loop)
        input_loop.run_until_complete(handle_admin_input())
    except KeyboardInterrupt:
        printf("[orange1]Server shutdown initiated by user.[/]")
    finally:
        input_loop.close()
        printf("Goodbye!")
        exit(0)

if __name__ == "__main__":
    main()