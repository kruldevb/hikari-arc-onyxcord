"""Admin plugin - Traditional manual plugin style."""

import hikari
import arc

# Create traditional plugin
admin_plugin = arc.GatewayPlugin("Admin")


@admin_plugin.include
@arc.slash_command("announce", "Send an announcement")
async def announce(
    ctx: arc.GatewayContext,
    message: arc.Option[str, "The announcement message"],
    channel: arc.Option[hikari.TextableGuildChannel | None, "Target channel"] = None
):
    """Send an announcement to a channel."""
    target = channel or ctx.channel_id
    
    embed = hikari.Embed(
        title="📢 Announcement",
        description=message,
        color=0xFF0000
    )
    
    await ctx.client.bot.rest.create_message(target, embed=embed)
    await ctx.respond("✅ Announcement sent!", flags=hikari.MessageFlag.EPHEMERAL)


@admin_plugin.include
@arc.slash_command("clear", "Clear messages")
async def clear(
    ctx: arc.GatewayContext,
    amount: arc.Option[int, "Number of messages to clear"] = 10
):
    """Clear messages from the channel."""
    await ctx.respond(f"🗑️ Clearing {amount} messages...", flags=hikari.MessageFlag.EPHEMERAL)
    # Implementation would go here
