"""Moderation plugin with multiple related commands."""

import hikari
import arc

# Create the plugin
moderation_plugin = arc.GatewayPlugin("Moderation")


@moderation_plugin.include
@arc.slash_command("ban", "Ban a user from the server")
async def ban(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User, arc.UserParams("The user to ban")],
    reason: arc.Option[str, "Reason for the ban"] = "No reason provided"
):
    """Ban a user from the server."""
    await ctx.respond(f"🔨 Banned {user.mention} for: {reason}")


@moderation_plugin.include
@arc.slash_command("kick", "Kick a user from the server")
async def kick(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User, arc.UserParams("The user to kick")],
    reason: arc.Option[str, "Reason for the kick"] = "No reason provided"
):
    """Kick a user from the server."""
    await ctx.respond(f"👢 Kicked {user.mention} for: {reason}")


@moderation_plugin.include
@arc.slash_command("timeout", "Timeout a user")
async def timeout(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User, arc.UserParams("The user to timeout")],
    duration: arc.Option[int, "Duration in minutes"] = 10
):
    """Timeout a user for a specified duration."""
    await ctx.respond(f"⏰ Timed out {user.mention} for {duration} minutes")
