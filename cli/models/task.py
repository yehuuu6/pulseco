from abc import ABC, abstractmethod

import os
import sys

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class Task(ABC):
    """Base class for Pulse CLI tasks"""
    
    def __init__(self, namespace: str, name: str, description: str):
        self.namespace = namespace
        self.name = name
        self.description = description
    
    @abstractmethod
    def usage(self) -> str:
        """Return usage instructions for this task"""
        pass
    
    @abstractmethod
    def handle(self, *args: str) -> None:
        """Handle the task execution"""
        pass
