"""Ready event handler."""

import hikari


async def on_ready(event: hikari.StartedEvent):
    """Called when the bot is ready."""
    print(f"✅ Bot is ready! Logged in as {event.my_user.username}")
