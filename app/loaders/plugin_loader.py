from typing import List
from app.models.plugin import Plugin
from app.utils.functions import printf  # Importing the printf function for console output

import os
import sys
import importlib
import inspect

class PluginLoaderSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.plugins: List[Plugin] = []
            self._initialized = True

    def _get_config(self):
        from app.server import room
        return room.cfg_loader.config

    def load_plugins(self) -> None:
        config = self._get_config()
        DEBUG_MODE = config.debug
        
        if DEBUG_MODE:
            file_extension = ".py"
            plugins_folder = "app/plugins"
        else:
            file_extension = ".so"
            plugins_folder = "build/plugins"
        
        # Check if the folder exists
        if not os.path.exists(plugins_folder):
            printf(f"[red]Plugins folder {plugins_folder} does not exist[/]")
            return

        sys.path.append(os.path.abspath(plugins_folder))

        for filename in os.listdir(plugins_folder):
            if filename.endswith(file_extension) and not filename.startswith("__"):
                module_name = filename[:-len(file_extension)]  # Remove the correct extension length
                try:
                    module = importlib.import_module(module_name)

                    for _name, obj in inspect.getmembers(module, inspect.isclass):
                        if issubclass(obj, Plugin) and obj is not Plugin:
                            plugin_instance = obj()  # type: ignore
                            self.plugins.append(plugin_instance)
                            plugin_instance.on_load()
                            break
                    else:
                        printf(f"[orange1]No valid Plugin subclass found in {module_name}[/]")

                except Exception as e:
                    printf(f"[red]Error loading plugin {module_name}: {e}[/]")

    def get_plugins(self) -> List[Plugin]:
        return self.plugins
