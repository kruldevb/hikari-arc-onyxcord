"""Ban command."""

import hikari
from arc import slash_command, GatewayContext, Option, UserParams


@slash_command("ban", "Ban a user from the server")
async def ban(
    ctx: GatewayContext,
    user: Option[hikari.User, UserParams("The user to ban")],
    reason: Option[str, "Reason for the ban"] = "No reason provided"
):
    """Ban a user from the server."""
    await ctx.respond(f"🔨 Banned {user.mention} for: {reason}")
