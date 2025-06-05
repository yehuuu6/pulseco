from typing import List
from app.models.plugin import Plugin
from app.utils.functions import printf  # Importing the printf function for console output
from app.models.package import Package
from app.models.user import User

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
            # Event registries for quick lookup
            self._package_plugins: List[Plugin] = []
            self._command_plugins: List[Plugin] = []
            self._user_joined_plugins: List[Plugin] = []
            self._user_left_plugins: List[Plugin] = []
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
                            
                            # Auto-register events based on overridden methods
                            self._auto_register_events(plugin_instance)
                            
                            plugin_instance.on_load()
                            break
                    else:
                        printf(f"[orange1]No valid Plugin subclass found in {module_name}[/]")

                except Exception as e:
                    printf(f"[red]Error loading plugin {module_name}: {e}[/]")

    def _auto_register_events(self, plugin: Plugin) -> None:
        """Automatically register events based on overridden methods."""
        plugin_class = plugin.__class__
        base_class = Plugin
        
        # Check which methods are overridden
        if plugin_class.on_package_received != base_class.on_package_received:
            self._package_plugins.append(plugin)
            
        if plugin_class.on_command_received != base_class.on_command_received:
            self._command_plugins.append(plugin)
            
        if plugin_class.on_user_joined != base_class.on_user_joined:
            self._user_joined_plugins.append(plugin)
            
        if plugin_class.on_user_left != base_class.on_user_left:
            self._user_left_plugins.append(plugin)

    # Event trigger methods
    def trigger_package_received(self, package: Package) -> None:
        """Trigger package received event for registered plugins."""
        for plugin in self._package_plugins:
            try:
                plugin.on_package_received(package)
            except Exception as e:
                printf(f"[red]Error in plugin {plugin.name} on_package_received: {e}[/]")

    def trigger_command_received(self, command: str, args: List[str], executer: User) -> None:
        """Trigger command received event for registered plugins."""
        for plugin in self._command_plugins:
            try:
                plugin.on_command_received(command, args, executer)
            except Exception as e:
                printf(f"[red]Error in plugin {plugin.name} on_command_received: {e}[/]")

    def trigger_user_joined(self, user: User) -> None:
        """Trigger user joined event for registered plugins."""
        for plugin in self._user_joined_plugins:
            try:
                plugin.on_user_joined(user)
            except Exception as e:
                printf(f"[red]Error in plugin {plugin.name} on_user_joined: {e}[/]")

    def trigger_user_left(self, user: User) -> None:
        """Trigger user left event for registered plugins."""
        for plugin in self._user_left_plugins:
            try:
                plugin.on_user_left(user)
            except Exception as e:
                printf(f"[red]Error in plugin {plugin.name} on_user_left: {e}[/]")

    def get_plugins(self) -> List[Plugin]:
        return self.plugins
