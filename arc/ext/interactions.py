"""Interaction system for arc - Disnake-style decorators for buttons, modals, and selects

This module provides a simplified interaction handling system similar to disnake,
allowing you to use decorators for buttons, modals, and select menus.

Example:
    ```python
    import hikari
    import arc
    from arc.ext import EasyPlugin, EasyInteraction
    
    bot = hikari.GatewayBot("TOKEN")
    client = arc.GatewayClient(bot)
    
    # Register the interaction handler
    bot.listen(hikari.InteractionCreateEvent)(EasyInteraction)
    
    plugin = EasyPlugin("MyPlugin")
    
    @plugin.slash_command(name="panel", description="Open panel")
    async def panel(ctx: arc.GatewayContext):
        await ctx.respond(
            "Click a button:",
            components=[
                ctx.client.rest.build_message_action_row()
                .add_interactive_button(hikari.ButtonStyle.PRIMARY, "config", label="Config")
            ]
        )
    
    @plugin.button("config")
    async def config_button(ctx):
        await ctx.send("Config opened!", ephemeral=True)
    ```
"""

from __future__ import annotations

import logging
import re
import typing as t
from dataclasses import dataclass, field

import hikari

if t.TYPE_CHECKING:
    from collections.abc import Callable, Sequence

__all__ = (
    "InteractionContext",
    "InteractionRouter",
    "button",
    "select_menu",
    "modal",
    "EasyInteraction",
)

_logger = logging.getLogger("arc.ext.interactions")

# Global variable to store miru_client reference
# Set by user code: import arc.ext.interactions as interactions_module
#                   interactions_module._global_miru_client = miru_client
_global_miru_client = None


def _sanitize_response_params(
    content: str | hikari.UndefinedType = hikari.UNDEFINED,
    embed: hikari.Embed | None = None,
    embeds: Sequence[hikari.Embed] | None = None,
    components: Sequence[hikari.api.ComponentBuilder] | None = None,
) -> tuple[str | hikari.UndefinedType | None, hikari.UndefinedType | Sequence[hikari.Embed] | None, hikari.UndefinedType | Sequence[hikari.api.ComponentBuilder] | None]:
    """Sanitize response parameters to avoid sending empty/unwanted values.
    
    When parameters are not explicitly passed (UNDEFINED), they are converted to None
    to clear previous values instead of keeping them.
    
    Args:
        content: Message content
        embed: Single embed
        embeds: Multiple embeds
        components: Message components
        
    Returns:
        Tuple of (sanitized_content, sanitized_embeds, sanitized_components)
    """
    # Sanitize content - convert UNDEFINED/empty strings to None (to clear)
    if content is hikari.UNDEFINED or (isinstance(content, str) and not content):
        final_content = None
    else:
        final_content = content
    
    # Sanitize embeds - convert UNDEFINED/empty lists/None to None
    final_embeds = None
    if embeds is not None and len(embeds) > 0:
        final_embeds = embeds
    elif embed is not None:
        final_embeds = [embed]
    
    # Sanitize components - convert UNDEFINED/empty lists/None to None
    final_components = None
    if components is not None and len(components) > 0:
        final_components = components
    
    return final_content, final_embeds, final_components


class ModalValues:
    """Container for modal values with attribute access.
    
    Example:
        ```python
        # Instead of: ctx.get_modal_value("name")
        # Use: ctx.values.name
        name = ctx.values.name
        age = ctx.values.age
        ```
    """
    
    def __init__(self, components: Sequence[hikari.ModalActionRowComponent] | None):
        self._data: dict[str, str] = {}
        if components:
            for row in components:
                for component in row.components:
                    self._data[component.custom_id] = component.value
    
    def __getattr__(self, name: str) -> str | None:
        return self._data.get(name)
    
    def __getitem__(self, key: str) -> str | None:
        return self._data.get(key)
    
    def get(self, key: str, default: t.Any = None) -> str | t.Any:
        """Get a value with a default fallback."""
        return self._data.get(key, default)
    
    def __repr__(self) -> str:
        return f"ModalValues({self._data})"


@dataclass
class InteractionContext:
    """Simplified context for component interactions.
    
    Similar to disnake's interaction context, provides easy methods
    for responding to button clicks, select menus, and modals.
    
    Attributes:
        interaction: The underlying Hikari interaction object.
        app: The Hikari application instance.
        user: The user who triggered the interaction.
        guild_id: The guild ID where the interaction occurred (None for DMs).
        channel_id: The channel ID where the interaction occurred.
        custom_id: The custom_id of the component that was interacted with.
        values: Selected values (for select menus) or modal values.
        match: Regex match object (if custom_id matched a regex pattern).
    """
    
    interaction: hikari.ComponentInteraction | hikari.ModalInteraction
    app: hikari.RESTAware
    match: re.Match[str] | None = None
    _responded: bool = field(default=False, init=False)
    
    @property
    def user(self) -> hikari.User:
        """The user who triggered the interaction."""
        return self.interaction.user
    
    @property
    def guild_id(self) -> int | None:
        """The guild ID where the interaction occurred."""
        return self.interaction.guild_id
    
    @property
    def channel_id(self) -> int:
        """The channel ID where the interaction occurred."""
        return self.interaction.channel_id
    
    @property
    def custom_id(self) -> str:
        """The custom_id of the component."""
        return self.interaction.custom_id
    
    @property
    def values(self) -> Sequence[str] | ModalValues:
        """Selected values (for select menus) or modal values."""
        if isinstance(self.interaction, hikari.ComponentInteraction):
            return self.interaction.values
        elif isinstance(self.interaction, hikari.ModalInteraction):
            return ModalValues(self.interaction.components)
        return []
    
    @property
    def value(self) -> str | None:
        """First selected value (for single-select menus)."""
        vals = self.values
        if isinstance(vals, list) and vals:
            return vals[0]
        return None
    
    @property
    def responded(self) -> bool:
        """Whether the interaction has been responded to."""
        return self._responded
    
    def get_modal_value(self, custom_id: str, default: t.Any = None) -> str | t.Any:
        """Get a value from a modal by custom_id.
        
        Args:
            custom_id: The custom_id of the text input component.
            default: Default value if not found.
        
        Returns:
            The value entered by the user, or default if not found.
        """
        if isinstance(self.values, ModalValues):
            return self.values.get(custom_id, default)
        return default
    
    async def respond(
        self,
        content: str | hikari.UndefinedType = hikari.UNDEFINED,
        *,
        ephemeral: bool = False,
        embed: hikari.Embed | None = None,
        embeds: Sequence[hikari.Embed] | None = None,
        components: Sequence[hikari.api.ComponentBuilder] | None = None,
        flags: hikari.MessageFlag | int | None = None,
    ) -> None:
        """Respond to the interaction.
        
        Args:
            content: The message content.
            ephemeral: Whether the message should be ephemeral (only visible to user).
            embed: A single embed to send.
            embeds: Multiple embeds to send.
            components: Message components (buttons, selects, etc).
            flatualeze no github e restale ssage flags.
        """
        if ephemeral and flags is None:
            flags = hikari.MessageFlag.EPHEMERAL
        
        # Sanitize parameters to avoid sending empty/unwanted values
        final_content, final_embeds, final_components = _sanitize_response_params(
            content, embed, embeds, components
        )
        
        await self.interaction.create_initial_response(
            hikari.ResponseType.MESSAGE_CREATE,
            content=final_content,
            embeds=final_embeds,
            components=final_components,
            flags=flags,
        )
        self._responded = True
    
    async def send(
        self,
        content: str | hikari.UndefinedType = hikari.UNDEFINED,
        *,
        ephemeral: bool = False,
        embed: hikari.Embed | None = None,
        embeds: Sequence[hikari.Embed] | None = None,
        components: Sequence[hikari.api.ComponentBuilder] | None = None,
        flags: hikari.MessageFlag | int | None = None,
    ) -> None:
        """Alias for respond() - more intuitive for Disnake users.
        
        Args:
            content: The message content.
            ephemeral: Whether the message should be ephemeral.
            embed: A single embed to send.
            embeds: Multiple embeds to send.
            components: Message components.
            flags: Message flags.
        """
        await self.respond(content, ephemeral=ephemeral, embed=embed, embeds=embeds, components=components, flags=flags)
    
    async def defer(self, *, ephemeral: bool = False, edit_original: bool = True) -> None:
        """Defer the interaction response.
        
        Args:
            ephemeral: Whether the deferred message should be ephemeral.
            edit_original: If True, edits the original message (for buttons/selects).
                          If False, creates a new message (for slash commands).
        """
        flags = hikari.MessageFlag.EPHEMERAL if ephemeral else hikari.UNDEFINED
        
        # For component interactions (buttons/selects), use MESSAGE_UPDATE to edit the original message
        # For command interactions, use MESSAGE_CREATE to create a new message
        response_type = (
            hikari.ResponseType.DEFERRED_MESSAGE_UPDATE if edit_original
            else hikari.ResponseType.DEFERRED_MESSAGE_CREATE
        )
        
        await self.interaction.create_initial_response(
            response_type,
            flags=flags,
        )
        self._responded = True
    
    async def edit(
        self,
        content: str | hikari.UndefinedType = hikari.UNDEFINED,
        *,
        embed: hikari.Embed | None = None,
        embeds: Sequence[hikari.Embed] | None = None,
        components: Sequence[hikari.api.ComponentBuilder] | None = None,
    ) -> None:
        """Edit the original message.
        
        Automatically detects if the interaction was already acknowledged (e.g., via defer())
        and uses the appropriate method (create_initial_response or edit_initial_response).
        
        Args:
            content: The new message content.
            embed: A single embed.
            embeds: Multiple embeds.
            components: New message components.
        """
        # Sanitize parameters to avoid sending empty/unwanted values
        final_content, final_embeds, final_components = _sanitize_response_params(
            content, embed, embeds, components
        )
        
        # If already responded (e.g., via defer()), use edit_initial_response
        if self._responded:
            await self.interaction.edit_initial_response(
                content=final_content,
                embeds=final_embeds,
                components=final_components,
            )
        else:
            # First response - use create_initial_response with MESSAGE_UPDATE
            await self.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_UPDATE,
                content=final_content,
                embeds=final_embeds,
                components=final_components,
            )
            self._responded = True
    
    async def edit_response(
        self,
        content: str | hikari.UndefinedType = hikari.UNDEFINED,
        *,
        embed: hikari.Embed | None = None,
        embeds: Sequence[hikari.Embed] | None = None,
        components: Sequence[hikari.api.ComponentBuilder] | None = None,
    ) -> None:
        """Edit the deferred response.
        
        Args:
            content: The new message content.
            embed: A single embed.
            embeds: Multiple embeds.
            components: New message components.
        """
        # Sanitize parameters to avoid sending empty/unwanted values
        final_content, final_embeds, final_components = _sanitize_response_params(
            content, embed, embeds, components
        )
        
        if self._responded:
            # If already responded with defer, edit the initial response
            await self.interaction.edit_initial_response(
                content=final_content,
                embeds=final_embeds,
                components=final_components,
            )
        else:
            # If not responded yet, use MESSAGE_UPDATE
            await self.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_UPDATE,
                content=final_content,
                embeds=final_embeds,
                components=final_components,
            )
            self._responded = True
    
    async def respond_with_modal(self, modal) -> None:
        """Respond with a modal (Miru modal).
        
        Args:
            modal: A Miru modal instance to send.
        """
        # Register the modal with Miru client so it can handle the callback
        global _global_miru_client
        
        if _global_miru_client:
            # Start the modal with Miru client to register it for callback handling
            _global_miru_client.start_modal(modal)
        
        # Send the modal response
        await self.interaction.create_modal_response(
            title=modal.title,
            custom_id=modal.custom_id,
            components=modal.build()
        )
        self._responded = True
    
    @property
    def bot(self):
        """Alias for app - for compatibility."""
        return self.app
    
    @property
    def guild(self):
        """Get the guild object if available."""
        if self.guild_id:
            return self.app.cache.get_guild(self.guild_id)
        return None
    
    def get_guild(self):
        """Get the guild object if available (method version for compatibility)."""
        if self.guild_id:
            return self.app.cache.get_guild(self.guild_id)
        return None


class InteractionRouter:
    """Router for handling component interactions.
    
    Manages registration and dispatching of button, select menu,
    and modal handlers with support for regex patterns and auto-defer.
    """
    
    def __init__(self, *, auto_defer: bool = False, debug: bool = False) -> None:
        """Initialize the router.
        
        Args:
            auto_defer: Whether to automatically defer interactions if not responded within 2s.
            debug: Whether to log debug information about interactions.
        """
        self._handlers: dict[str, Callable[[InteractionContext], t.Awaitable[None]]] = {}
        self._regex_handlers: list[tuple[re.Pattern[str], Callable]] = []
        self._auto_defer = auto_defer
        self._debug = debug
    
    def register(
        self,
        custom_id: str | re.Pattern[str],
        handler: Callable,
        namespace: str | None = None,
    ) -> None:
        """Register an interaction handler.
        
        Args:
            custom_id: The custom_id to match (string or regex pattern).
            handler: The async function to call when the interaction is triggered.
            namespace: Optional namespace to prefix the custom_id.
        """
        # Apply namespace if provided
        if namespace and isinstance(custom_id, str):
            custom_id = f"{namespace}:{custom_id}"
        
        if isinstance(custom_id, re.Pattern):
            self._regex_handlers.append((custom_id, handler))
        else:
            self._handlers[custom_id] = handler
        
        if self._debug:
            _logger.debug(f"Registered handler for: {custom_id}")
    
    async def dispatch(self, interaction: hikari.ComponentInteraction | hikari.ModalInteraction, app: hikari.RESTAware) -> bool:
        """Dispatch an interaction to the appropriate handler.
        
        Args:
            interaction: The interaction to dispatch.
            app: The application instance.
        
        Returns:
            True if a handler was found and executed, False otherwise.
        """
        custom_id = interaction.custom_id
        ctx = InteractionContext(interaction, app)
        
        # Skip modal interactions - let Miru handle them
        if isinstance(interaction, hikari.ModalInteraction):
            if self._debug:
                _logger.debug(f"[MODAL] custom_id={custom_id} - Skipping (handled by Miru)")
            return False
        
        if self._debug:
            interaction_type = "BUTTON" if isinstance(interaction, hikari.ComponentInteraction) else "MODAL"
            _logger.debug(f"[{interaction_type}] custom_id={custom_id} user={interaction.user.id}")
        
        # Auto-defer if enabled and not responded
        if self._auto_defer and not ctx.responded:
            try:
                await ctx.defer()
            except:
                pass  # Already responded
        
        # Try exact match first
        if custom_id in self._handlers:
            try:
                await self._handlers[custom_id](ctx)
                return True
            except hikari.NotFoundError as e:
                # Interação expirada - tentar continuar com REST API
                if "Unknown interaction" in str(e):
                    # Não mostrar warning se o handler conseguiu completar via REST API
                    # O warning só aparece se realmente falhar
                    if self._debug:
                        _logger.debug(f"Interaction token expired for {custom_id}, but handler may have used REST API fallback")
                else:
                    _logger.error(f"NotFoundError in handler for {custom_id}: {e}", exc_info=True)
                return True
            except Exception as e:
                _logger.error(f"Error in handler for {custom_id}: {e}", exc_info=True)
                if not ctx.responded:
                    try:
                        await ctx.send("❌ An error occurred while processing your interaction.", ephemeral=True)
                    except:
                        pass
                return True
        
        # Try regex patterns
        for pattern, handler in self._regex_handlers:
            match = pattern.match(custom_id)
            if match:
                ctx.match = match
                try:
                    # Extract groups and pass as arguments
                    groups = match.groups()
                    if groups:
                        await handler(ctx, *groups)
                    else:
                        await handler(ctx)
                    return True
                except hikari.NotFoundError as e:
                    # Interação expirada - tentar continuar com REST API
                    if "Unknown interaction" in str(e):
                        # Não mostrar warning se o handler conseguiu completar via REST API
                        if self._debug:
                            _logger.debug(f"Interaction token expired for {custom_id}, but handler may have used REST API fallback")
                    else:
                        _logger.error(f"NotFoundError in regex handler for {custom_id}: {e}", exc_info=True)
                    return True
                except Exception as e:
                    _logger.error(f"Error in regex handler for {custom_id}: {e}", exc_info=True)
                    if not ctx.responded:
                        try:
                            await ctx.send("❌ An error occurred while processing your interaction.", ephemeral=True)
                        except:
                            pass
                    return True
        
        if self._debug:
            _logger.warning(f"No handler found for custom_id: {custom_id}")
        
        return False


# Global router instance
_global_router = InteractionRouter(debug=False)


def get_router() -> InteractionRouter:
    """Get the global interaction router."""
    return _global_router


def configure_router(*, auto_defer: bool = False, debug: bool = False) -> None:
    """Configure the global router settings.
    
    Args:
        auto_defer: Whether to automatically defer interactions.
        debug: Whether to enable debug logging.
    """
    global _global_router
    _global_router = InteractionRouter(auto_defer=auto_defer, debug=debug)


def button(custom_id: str | re.Pattern[str], *, namespace: str | None = None) -> Callable[[Callable], Callable]:
    """Decorator to register a button handler.
    
    Args:
        custom_id: The custom_id of the button (string or regex pattern).
        namespace: Optional namespace to prefix the custom_id.
    
    Example:
        ```python
        @button("config")
        async def config_handler(ctx):
            await ctx.send("Config opened!")
        
        # With regex for dynamic IDs
        @button(re.compile(r"user:(\d+)"))
        async def user_handler(ctx, user_id: str):
            await ctx.send(f"User ID: {user_id}")
        
        # With namespace
        @button("settings", namespace="admin")
        async def admin_settings(ctx):
            await ctx.send("Admin settings")
        ```
    """
    def decorator(func: Callable) -> Callable:
        func.__interaction_type__ = "button"
        func.__custom_id__ = custom_id
        func.__namespace__ = namespace
        _global_router.register(custom_id, func, namespace)
        return func
    return decorator


def select_menu(custom_id: str | re.Pattern[str], *, namespace: str | None = None) -> Callable[[Callable], Callable]:
    """Decorator to register a select menu handler.
    
    Args:
        custom_id: The custom_id of the select menu (string or regex pattern).
        namespace: Optional namespace to prefix the custom_id.
    
    Example:
        ```python
        @select_menu("role_select")
        async def role_handler(ctx):
            selected = ctx.value  # or ctx.values[0]
            await ctx.send(f"Selected: {selected}")
        ```
    """
    def decorator(func: Callable) -> Callable:
        func.__interaction_type__ = "select"
        func.__custom_id__ = custom_id
        func.__namespace__ = namespace
        _global_router.register(custom_id, func, namespace)
        return func
    return decorator


def modal(custom_id: str | re.Pattern[str], *, namespace: str | None = None) -> Callable[[Callable], Callable]:
    """Decorator to register a modal handler.
    
    Args:
        custom_id: The custom_id of the modal (string or regex pattern).
        namespace: Optional namespace to prefix the custom_id.
    
    Example:
        ```python
        @modal("registration")
        async def registration_handler(ctx):
            name = ctx.values.name  # or ctx.get_modal_value("name")
            age = ctx.values.age
            await ctx.send(f"Registered: {name}, {age}")
        ```
    """
    def decorator(func: Callable) -> Callable:
        func.__interaction_type__ = "modal"
        func.__custom_id__ = custom_id
        func.__namespace__ = namespace
        _global_router.register(custom_id, func, namespace)
        return func
    return decorator


async def EasyInteraction(event: hikari.InteractionCreateEvent) -> None:
    """Easy interaction handler for component and modal interactions.
    
    Register this as a listener on your bot:
    
    ```python
    from arc.ext import EasyInteraction
    
    bot.listen(hikari.InteractionCreateEvent)(EasyInteraction)
    ```
    
    Or with configuration:
    
    ```python
    from arc.ext import configure_router, EasyInteraction
    
    configure_router(auto_defer=True, debug=True)
    bot.listen(hikari.InteractionCreateEvent)(EasyInteraction)
    ```
    """
    interaction = event.interaction
    
    if isinstance(interaction, (hikari.ComponentInteraction, hikari.ModalInteraction)):
        await _global_router.dispatch(interaction, event.app)
