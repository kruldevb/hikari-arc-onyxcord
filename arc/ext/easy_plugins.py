"""
Easy Plugins Extension for hikari-arc

This extension provides automatic plugin loading from a directory.
"""

import importlib
import inspect
from pathlib import Path
from typing import TYPE_CHECKING

import arc

if TYPE_CHECKING:
    from arc import GatewayClient, RESTClient

__all__ = ["load_plugins"]


def load_plugins(
    client: "GatewayClient | RESTClient",
    plugins_path: Path | str | None = None,
) -> list[str]:
    """
    Automatically load all plugins from a directory.
    
    Args:
        client: The arc client instance
        plugins_path: Path to plugins directory. Defaults to './plugins' relative to caller
        
    Returns:
        List of loaded module names
        
    Example:
        ```python
        # In your main file
        import arc
        from arc.ext.easy_plugins import load_plugins
        
        client = arc.GatewayClient(...)
        load_plugins(client)
        bot.run()
        ```
        
        ```python
        # In plugins/moderation.py
        import arc
        
        moderation_plugin = arc.GatewayPlugin("Moderation")
        
        @moderation_plugin.include
        @arc.slash_command("ban", "Ban a user")
        async def ban(ctx: arc.GatewayContext, user: hikari.User):
            await ctx.respond(f"Banned {user.mention}")
        ```
    """
    if plugins_path is None:
        # Get caller's directory
        frame = inspect.currentframe()
        if frame and frame.f_back:
            caller_file = frame.f_back.f_globals.get("__file__")
            if caller_file:
                plugins_path = Path(caller_file).parent / "plugins"
    
    plugins_path = Path(plugins_path) if isinstance(plugins_path, str) else plugins_path
    
    if not plugins_path or not plugins_path.exists():
        return []
    
    loaded_modules = []
    
    # Load all .py files in plugins directory
    for file_path in plugins_path.glob("*.py"):
        if file_path.name.startswith("_"):
            continue
            
        module_name = f"{plugins_path.parent.name}.plugins.{file_path.stem}"
        
        try:
            module = importlib.import_module(module_name)
            
            # Find all GatewayPlugin or RESTPlugin instances
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, (arc.GatewayPlugin, arc.RESTPlugin)):
                    client.add_plugin(obj)
                    loaded_modules.append(module_name)
                    print(f"[EASY_PLUGINS] Plugin loaded: {module_name} -> {name}")
                    
        except Exception as e:
            print(f"[EASY_PLUGINS] Error loading {module_name}: {e}")
    
    return loaded_modules
