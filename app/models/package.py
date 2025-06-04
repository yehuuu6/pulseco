from typing import List, Any
from app.utils.functions import printf  # Importing the printf function for console output

import json
import socket as sck

class Package:
    VALID_TYPES: List[str] = [
        "handshake",
        "command",
        "message",
    ]

    def __init__(self, type: str, content: Any) -> None:
        self.type: str = type
        self.content: Any = content

    def is_valid_package(self)-> bool:
        return self.type in self.VALID_TYPES
    
HEADER_SIZE: int = 10

def receive_all(sender: sck.socket) -> str:
    """
    Receives all the data from the sender and returns it as str.
    """
    full_data = ""
    new_data = True
    data_len = 0
    while True:
        try:
            data = sender.recv(4096)
            if not data:  # Client disconnected
                raise sck.error("Client disconnected")
            
            if new_data:
                header = data[:HEADER_SIZE].decode("utf-8")
                if not header.strip():  # Empty header indicates disconnection
                    raise sck.error("Empty header received")
                data_len = int(header)
                new_data = False

            full_data += data.decode("utf-8")

            if len(full_data) - HEADER_SIZE == data_len:
                break
        except (ValueError, UnicodeDecodeError) as e:
            # Handle invalid data or encoding errors
            raise sck.error(f"Invalid data received: {e}")

    return full_data[HEADER_SIZE:]

def send_all(package: Package, target: sck.socket) -> None:
    data: str = json.dumps({
        "type": package.type,
        "content": package.content,
    })

    data = f"{len(data):<{HEADER_SIZE}}" + data

    try:
        target.sendall(data.encode('utf-8'))
    except sck.error as e:
        printf(f"[red]Error:[/] sending data: {e}")

def get_package(sender: sck.socket)-> Package | None:
    try:
        response = receive_all(sender)
    except sck.error:
        return None
    try:
        data = json.loads(response)
    except json.decoder.JSONDecodeError:
        # If client sends a long message, returns none, this will cause
        # the client to disconnect by force.
        return None

    package = Package(data["type"], data["content"])

    return package

def send_package(package: Package, target: sck.socket) -> None:
    """
    Sends the package to the target as bytes.
    Known bug: If the package is being sent to a client just before the client's connection
    is closed by the server, the client will not receive the package. Because they will be
    disconnected before the package is received.
    """
    data: str = json.dumps({
        "type": package.type,
        "content": package.content
    })

    data = f"{len(data):<{HEADER_SIZE}}" + data

    try:
        target.send(bytes(data, "utf-8"))
    except sck.error:
        pass