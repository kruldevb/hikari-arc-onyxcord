"""Easy command syntax for arc - similar to disnake.ext.commands

This module provides a simplified, decorator-based syntax for creating
slash commands in arc, similar to disnake's command system.

Example:
    ```python
    import hikari
    import arc
    from arc.ext import EasyPlugin
    
    bot = hikari.GatewayBot("TOKEN")
    client = arc.GatewayClient(bot)
    
    # Create a plugin (similar to disnake Cog)
    plugin = EasyPlugin("General")
    
    @plugin.slash_command(name="ping", description="Shows bot latency")
    async def ping(ctx: arc.GatewayContext):
        await ctx.respond(f"Pong! {ctx.client.app.heartbeat_latency * 1000:.0f}ms")
    
    # Load the plugin
    client.add_plugin(plugin)
    
    bot.run()
    ```
"""

from __future__ import annotations

import re
import typing as t

from arc.plugin import GatewayPluginBase
from arc.command import slash_command
from arc.client import GatewayContext
from arc.context import AutodeferMode

if t.TYPE_CHECKING:
    import hikari
from arc.abc.option import CommandOptionBase
from arc.context import AutodeferMode
from arc.ext.interactions import get_router

if t.TYPE_CHECKING:
    import hikari
    from collections.abc import Callable, Sequence

    from arc.abc.command import CallableCommandProto
    from arc.command.slash import SlashCommand, SlashSubCommand

__all__ = ("EasyPlugin", "easy_plugin")


class EasyPlugin(GatewayPluginBase):
    """A simplified plugin class with decorator-based command registration.
    
    Similar to disnake.ext.commands.Cog, but for arc.
    
    Example:
        ```python
        plugin = EasyPlugin("MyCommands")
        
        @plugin.slash_command(name="hello", description="Say hello")
        async def hello(ctx: GatewayContext):
            await ctx.respond("Hello!")
        
        client.add_plugin(plugin)
        ```
    """

    def slash_command(
        self,
        name: str | None = None,
        description: str | None = None,
        *,
        guilds: Sequence[int] | int | None = None,
        is_dm_enabled: bool = True,
        is_nsfw: bool = False,
        autodefer: bool | AutodeferMode = True,
        default_permissions: hikari.Permissions | None = None,
        name_localizations: dict[hikari.Locale, str] | None = None,
        description_localizations: dict[hikari.Locale, str] | None = None,
    ) -> Callable[[CallableCommandProto[GatewayContext]], SlashCommand[GatewayContext]]:
        """Decorator to register a slash command to this plugin.
        
        Args:
            name: The name of the command. If None, uses function name.
            description: The description of the command. If None, uses function docstring.
            guilds: Guild IDs where this command should be registered. None for global.
            is_dm_enabled: Whether the command can be used in DMs.
            is_nsfw: Whether the command is age-restricted.
            autodefer: Whether to automatically defer the response.
            default_permissions: Default permissions required to use this command.
            name_localizations: Localized names for the command.
            description_localizations: Localized descriptions for the command.
        
        Example:
            ```python
            @plugin.slash_command(name="ping", description="Check bot latency")
            async def ping(ctx: GatewayContext):
                await ctx.respond("Pong!")
            ```
        """
        def decorator(func: CallableCommandProto[GatewayContext]) -> SlashCommand[GatewayContext]:
            # Use function name if name not provided
            cmd_name = name or func.__name__
            
            # Use docstring if description not provided
            cmd_description = description
            if cmd_description is None and func.__doc__:
                # Get first line of docstring
                cmd_description = func.__doc__.strip().split('\n')[0]
            if not cmd_description:
                cmd_description = "No description provided"
            
            # Create the slash command
            command = slash_command(
                name=cmd_name,
                description=cmd_description,
                guilds=guilds,
                is_dm_enabled=is_dm_enabled,
                is_nsfw=is_nsfw,
                autodefer=autodefer,
                default_permissions=default_permissions,
                name_localizations=name_localizations,
                description_localizations=description_localizations,
            )(func)
            
            # Add to plugin
            self.include_slash_command(command)
            
            return command
        
        return decorator
    
    def button(self, custom_id: str | re.Pattern[str], *, use_namespace: bool = True) -> Callable[[Callable], Callable]:
        """Decorator to register a button handler in this plugin.
        
        Args:
            custom_id: The custom_id of the button (string or regex pattern).
            use_namespace: Whether to prefix with plugin name (default: True).
        
        Example:
            ```python
            @plugin.button("config")
            async def config_handler(ctx: InteractionContext):
                await ctx.send("Config opened!")
            ```
        """
        def decorator(func: Callable) -> Callable:
            func.__interaction_type__ = "button"
            func.__custom_id__ = custom_id
            namespace = self.name if use_namespace and isinstance(custom_id, str) else None
            get_router().register(custom_id, func, namespace)
            return func
        return decorator
    
    def select_menu(self, custom_id: str | re.Pattern[str], *, use_namespace: bool = True) -> Callable[[Callable], Callable]:
        """Decorator to register a select menu handler in this plugin.
        
        Args:
            custom_id: The custom_id of the select menu (string or regex pattern).
            use_namespace: Whether to prefix with plugin name (default: True).
        
        Example:
            ```python
            @plugin.select_menu("role_select")
            async def role_handler(ctx: InteractionContext):
                selected = ctx.value
                await ctx.send(f"Selected: {selected}")
            ```
        """
        def decorator(func: Callable) -> Callable:
            func.__interaction_type__ = "select"
            func.__custom_id__ = custom_id
            namespace = self.name if use_namespace and isinstance(custom_id, str) else None
            get_router().register(custom_id, func, namespace)
            return func
        return decorator
    
    def modal(self, custom_id: str | re.Pattern[str], *, use_namespace: bool = True) -> Callable[[Callable], Callable]:
        """Decorator to register a modal handler in this plugin.
        
        Args:
            custom_id: The custom_id of the modal (string or regex pattern).
            use_namespace: Whether to prefix with plugin name (default: True).
        
        Example:
            ```python
            @plugin.modal("registration")
            async def registration_handler(ctx: InteractionContext):
                name = ctx.values.name
                age = ctx.values.age
                await ctx.send(f"Registered: {name}, {age}")
            ```
        """
        def decorator(func: Callable) -> Callable:
            func.__interaction_type__ = "modal"
            func.__custom_id__ = custom_id
            namespace = self.name if use_namespace and isinstance(custom_id, str) else None
            get_router().register(custom_id, func, namespace)
            return func
        return decorator


def easy_plugin(name: str | None = None) -> EasyPlugin:
    """Create an EasyPlugin instance.
    
    Args:
        name: The name of the plugin. If None, a default name will be used.
    
    Returns:
        A new EasyPlugin instance.
    
    Example:
        ```python
        plugin = easy_plugin("MyCommands")
        
        @plugin.slash_command(name="test", description="Test command")
        async def test(ctx: arc.GatewayContext):
            await ctx.respond("Test!")
        ```
    """
    return EasyPlugin(name or "EasyPlugin")
