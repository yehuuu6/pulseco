from typing import Callable, Any

class Command:
    """
    Class that represents a command that can be executed in the pulse console.
    """
    def __init__(self, name: str, description: str, usage: str, function: Callable[..., None]) -> None:
        self.name = name
        self.description = description
        self.usage = usage
        self.function = function
    
    def __repr__(self) -> str:
        return f'Command(name={self.name}, description={self.description}, usage={self.usage})'

    def execute(self, *args: Any, **kwargs: Any) -> None:
        try:
            self.function(*args, **kwargs)
        except TypeError:
            print(self.usage)