"""Bot info command."""

import hikari
from arc import slash_command, GatewayContext


@slash_command("info", "Get bot information")
async def info(ctx: GatewayContext):
    """Display bot information."""
    bot_user = ctx.client.bot.get_me()
    
    embed = hikari.Embed(
        title=f"ℹ️ {bot_user.username}",
        description="A bot built with hikari-arc!",
        color=0x00FF00
    )
    
    embed.add_field("Servers", str(len(ctx.client.bot.cache.get_guilds_view())), inline=True)
    embed.add_field("Users", str(len(ctx.client.bot.cache.get_users_view())), inline=True)
    
    await ctx.respond(embed=embed)
