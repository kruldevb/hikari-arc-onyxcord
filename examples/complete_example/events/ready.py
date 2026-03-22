"""Ready event - Auto-loaded."""

import hikari


async def on_ready(event: hikari.StartedEvent):
    """Called when bot is ready."""
    print(f"✅ {event.my_user.username} is online!")
