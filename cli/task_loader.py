"""
CLI Task Loader - Automatically loads CLI tasks from the cli/tasks directory
"""

from typing import Dict, Type, Optional
from cli.models.task import Task
from app.utils.functions import printf

import os
import sys
import importlib
import importlib.util
import inspect

class TaskLoaderSingleton:
    """Singleton class for loading CLI tasks automatically"""
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.tasks: Dict[str, Dict[str, Type[Task]]] = {}
            self._initialized = True

    def load_tasks(self) -> None:
        """Load all CLI tasks from the cli/tasks directory"""
        tasks_folder = "cli/tasks"
        
        # Check if the folder exists
        if not os.path.exists(tasks_folder):
            printf(f"[red]CLI tasks folder {tasks_folder} does not exist[/]")
            return

        # Add the tasks folder to sys.path for importing
        tasks_abs_path = os.path.abspath(tasks_folder)
        if tasks_abs_path not in sys.path:
            sys.path.append(tasks_abs_path)

        for filename in os.listdir(tasks_folder):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]  # Remove .py extension
                try:
                    # Import the module using importlib with full path
                    spec = importlib.util.spec_from_file_location(
                        module_name, 
                        os.path.join(tasks_folder, filename)
                    )
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        # Find all Task subclasses in the module
                        for _name, obj in inspect.getmembers(module, inspect.isclass):
                            if issubclass(obj, Task) and obj is not Task:
                                # Create an instance to get task info
                                task_instance = obj() # type: ignore
                                
                                # Register the task
                                self.register_task(task_instance.namespace, task_instance.name, obj)
                                break
                        else:
                            printf(f"[orange1]No valid Task subclass found in {module_name}[/]")

                except Exception as e:
                    printf(f"[red]Error loading CLI task {module_name}: {e}[/]")

    def register_task(self, namespace: str, task_name: str, task_class: Type[Task]):
        """Register a task under a specific namespace"""
        if namespace not in self.tasks:
            self.tasks[namespace] = {}
        self.tasks[namespace][task_name] = task_class

    def get_task(self, namespace: str, task_name: str) -> Optional[Type[Task]]:
        """Get a task class by namespace and name"""
        if namespace in self.tasks and task_name in self.tasks[namespace]:
            return self.tasks[namespace][task_name]
        return None

    def get_all_tasks(self) -> Dict[str, Dict[str, Type[Task]]]:
        """Get all registered tasks"""
        return self.tasks
