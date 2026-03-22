"""Arc extensions for simplified command creation."""

from arc.ext.easy import EasyPlugin, easy_plugin
from arc.ext.interactions import (
    InteractionContext,
    InteractionRouter,
    EasyInteraction,
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
)
