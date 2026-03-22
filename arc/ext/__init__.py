"""Arc extensions for simplified command creation."""

from arc.ext.easy import EasyPlugin, easy_plugin
from arc.ext.easy_commands import EasyAll, load_all, load_commands, load_events
from arc.ext.easy_plugins import load_plugins
from arc.ext.interactions import (
    EasyInteraction,
    InteractionContext,
    InteractionRouter,
    button,
    configure_router,
    get_router,
    modal,
    select_menu,
)

__all__ = (
    "EasyPlugin",
    "easy_plugin",
    "InteractionContext",
    "InteractionRouter",
    "button",
    "select_menu",
    "modal",
    "get_router",
    "configure_router",
    "EasyInteraction",
    "load_commands",
    "load_events",
    "load_all",
    "EasyAll",
    "load_plugins",
)
