from typing import Callable, Any

class Command:
    """
    Class that represents a command that can be executed in the pulse console.
    """
    def __init__(self, name: str, description: str, function: Callable[..., None]) -> None:
        self.name = name
        self.description = description
        self.function = function

    def execute(self, *args: Any, **kwargs: Any) -> None:
        self.function(*args, **kwargs)