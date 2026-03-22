"""
Easy Commands Extension for hikari-arc

This extension provides automatic command and event loading without manual plugin registration.
Simply decorate your functions with @slash_command and they'll be auto-discovered and loaded.
"""

import importlib
import inspect
from pathlib import Path
from typing import TYPE_CHECKING

import arc

if TYPE_CHECKING:
    from arc import GatewayClient, RESTClient

__all__ = ["load_commands", "load_events", "load_all", "EasyAll"]


def load_commands(
    client: "GatewayClient | RESTClient",
    commands_path: Path | str | None = None,
) -> list[str]:
    """
    Automatically load all slash commands from a directory structure.
    
    Args:
        client: The arc client instance
        commands_path: Path to commands directory. Defaults to './commands' relative to caller
        
    Returns:
        List of loaded module names
        
    Example:
        ```python
        # In your main file
        import arc
        from arc.ext.easy_commands import load_commands
        
        client = arc.GatewayClient(...)
        load_commands(client)
        ```
        
        ```python
        # In commands/general/ping.py
        from arc import slash_command, GatewayContext
        
        @slash_command("ping", "Check bot latency")
        async def ping(ctx: GatewayContext):
            await ctx.respond("Pong!")
        ```
    """
    if commands_path is None:
        # Get caller's directory
        frame = inspect.currentframe()
        if frame and frame.f_back:
            caller_file = frame.f_back.f_globals.get("__file__")
            if caller_file:
                commands_path = Path(caller_file).parent / "commands"
    
    commands_path = Path(commands_path) if isinstance(commands_path, str) else commands_path
    
    if not commands_path or not commands_path.exists():
        return []
    
    loaded_modules = []
    
    # Iterate through subdirectories (categories)
    for category_dir in commands_path.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith("_"):
            continue
            
        # Load all .py files in category
        for file_path in category_dir.glob("*.py"):
            if file_path.name.startswith("_"):
                continue
                
            module_name = f"{commands_path.parent.name}.commands.{category_dir.name}.{file_path.stem}"
            
            try:
                module = importlib.import_module(module_name)
                
                # Find all SlashCommand instances
                for name, obj in inspect.getmembers(module):
                    if isinstance(obj, arc.SlashCommand):
                        # Create a plugin for this command
                        plugin = arc.GatewayPlugin(name)
                        plugin.include(obj)
                        client.add_plugin(plugin)
                        loaded_modules.append(module_name)
                        
            except Exception as e:
                print(f"[EASY_COMMANDS] Error loading {module_name}: {e}")
    
    return loaded_modules


def load_events(
    client: "GatewayClient | RESTClient",
    events_path: Path | str | None = None,
) -> list[str]:
    """
    Automatically load all event listeners from a directory.
    
    Args:
        client: The arc client instance
        events_path: Path to events directory. Defaults to './events' relative to caller
        
    Returns:
        List of loaded module names
        
    Example:
        ```python
        # In your main file
        import arc
        from arc.ext.easy_commands import load_events
        
        client = arc.GatewayClient(...)
        load_events(client)
        ```
        
        ```python
        # In events/ready.py
        import hikari
        
        async def on_ready(event: hikari.StartedEvent):
            print("Bot is ready!")
        ```
    """
    if events_path is None:
        # Get caller's directory
        frame = inspect.currentframe()
        if frame and frame.f_back:
            caller_file = frame.f_back.f_globals.get("__file__")
            if caller_file:
                events_path = Path(caller_file).parent / "events"
    
    events_path = Path(events_path) if isinstance(events_path, str) else events_path
    
    if not events_path or not events_path.exists():
        return []
    
    loaded_modules = []
    
    # Load all .py files in events directory
    for file_path in events_path.glob("*.py"):
        if file_path.name.startswith("_"):
            continue
            
        module_name = f"{events_path.parent.name}.events.{file_path.stem}"
        
        try:
            module = importlib.import_module(module_name)
            
            # Find all coroutine functions (event handlers)
            for name, obj in inspect.getmembers(module, inspect.iscoroutinefunction):
                client.bot.listen()(obj)
                loaded_modules.append(module_name)
                print(f"[EASY_COMMANDS] Event loaded: {module_name} -> {name}")
                
        except Exception as e:
            print(f"[EASY_COMMANDS] Error loading {module_name}: {e}")
    
    return loaded_modules


def load_all(
    client: "GatewayClient | RESTClient",
    commands_path: Path | str | None = None,
    events_path: Path | str | None = None,
) -> list[str]:
    """
    Load both commands and events automatically.
    
    Args:
        client: The arc client instance
        commands_path: Path to commands directory
        events_path: Path to events directory
        
    Returns:
        List of all loaded module names
        
    Example:
        ```python
        import arc
        from arc.ext import load_all
        
        client = arc.GatewayClient(...)
        load_all(client)
        bot.run()
        ```
    """
    loaded = []
    loaded.extend(load_commands(client, commands_path))
    loaded.extend(load_events(client, events_path))
    return loaded


def EasyAll(
    client: "GatewayClient | RESTClient",
    commands_path: Path | str | None = None,
    events_path: Path | str | None = None,
) -> list[str]:
    """
    Load both commands and events automatically.
    Alias for load_all() with a more intuitive name.
    
    Args:
        client: The arc client instance
        commands_path: Path to commands directory
        events_path: Path to events directory
        
    Returns:
        List of all loaded module names
        
    Example:
        ```python
        import arc
        from arc.ext import EasyAll
        
        client = arc.GatewayClient(...)
        EasyAll(client)
        bot.run()
        ```
    """
    return load_all(client, commands_path, events_path)
