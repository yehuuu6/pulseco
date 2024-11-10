from typing import Callable, Any
from pydantic import BaseModel, Field

class Command(BaseModel):
    """
    Class that represents a command that can be executed in the pulse console.
    """
    name: str = Field(
        title='Command name',
        description='Name of the command to display and use.')
    description: str = Field(
        title='Command description',
        description='Description of the command to display.')
    usage: str = Field(
        title='Command usage',
        description='Usage of the command to help users execute it.')
    function: Callable[..., None] = Field(
        title='Command function',
        description='Function that will be executed when the command is called.')
    
    def __repr__(self) -> str:
        return f'Command(name={self.name}, description={self.description}, usage={self.usage})'

    def execute(self, *args: Any, **kwargs: Any) -> None:
        try:
            self.function(*args, **kwargs)
        except TypeError:
            print(self.usage)