"""Simple ping command."""

from arc import slash_command, GatewayContext


@slash_command("ping", "Check bot latency")
async def ping(ctx: GatewayContext):
    """Respond with pong and latency."""
    latency = ctx.client.bot.heartbeat_latency * 1000
    await ctx.respond(f"🏓 Pong! Latency: {latency:.0f}ms")
