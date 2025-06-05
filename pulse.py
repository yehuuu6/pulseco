"""
Pulse CLI - A command-line interface for managing Pulse server components
"""

from typing import List
from app.utils.functions import printf

import sys
import os

# Add the current directory to Python path so we can import from cli and app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.task_loader import TaskLoaderSingleton


class PulseCLI:
    """Main Pulse CLI application"""
    
    def __init__(self):
        self.task_loader = TaskLoaderSingleton()
        self.task_loader.load_tasks()
    
    def run(self, args: List[str]):
        """Run the CLI with provided arguments"""
        if len(args) < 2:
            self.show_available_tasks()
            return
        
        # Parse namespace:task format
        task_input = args[1]
        if ':' not in task_input:
            printf("[red3]Error:[/] Task must be in format [green3]namespace:task[/]")
            return
        
        namespace, task_name = task_input.split(':', 1)
        task_args = args[2:] if len(args) > 2 else []
        
        # Get and execute task
        task_class = self.task_loader.get_task(namespace, task_name)
        if task_class is None:
            printf(f"[red3]Error:[/] Task [green3]'{namespace}:{task_name}'[/] not found!")
            self.show_available_tasks()
            return
        
        try:
            # Create task instance and execute
            task_instance = task_class() # type: ignore
            task_instance.handle(*task_args)
        except Exception as e:
            printf(f"[red3]Error:[/] {str(e)}")
            # Create instance for usage info
            task_instance = task_class() # type: ignore
            printf(f"[white]{task_instance.usage()}[/]")
    
    def show_available_tasks(self):
        """Show all available tasks organized by namespace"""
        printf("[bright_yellow]Available Tasks:[/]")
        printf("")
        
        for namespace, tasks in self.task_loader.get_all_tasks().items():
            printf(f"● [bright_cyan]{namespace}[/]")
            for task_name, task_class in tasks.items():
                # Create instance to get description
                task_instance = task_class() # type: ignore
                printf(f"└──➤ [green3]{namespace}:{task_name}[/] - {task_instance.description}")
            printf("")


def main():
    """Main entry point"""
    cli = PulseCLI()
    cli.run(sys.argv)


if __name__ == "__main__":
    main()