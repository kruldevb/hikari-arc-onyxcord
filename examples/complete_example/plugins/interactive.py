"""Interactive plugin with buttons and selects - EasyPlugin style."""

import hikari
import arc
from arc.ext import EasyPlugin

# Create EasyPlugin for interactive features
interactive = EasyPlugin("Interactive")


@interactive.slash_command(name="panel", description="Open interactive panel")
async def panel(ctx: arc.GatewayContext):
    """Command with interactive buttons."""
    row = ctx.client.rest.build_message_action_row()
    row.add_interactive_button(hikari.ButtonStyle.PRIMARY, "info", label="ℹ️ Info")
    row.add_interactive_button(hikari.ButtonStyle.SUCCESS, "help", label="❓ Help")
    row.add_interactive_button(hikari.ButtonStyle.DANGER, "close", label="❌ Close")
    
    await ctx.respond("📋 Control Panel", components=[row])


@interactive.button("info")
async def info_button(ctx):
    """Handle info button click."""
    await ctx.send("ℹ️ This is an info message!", ephemeral=True)


@interactive.button("help")
async def help_button(ctx):
    """Handle help button click."""
    await ctx.send("❓ Need help? Check the docs!", ephemeral=True)


@interactive.button("close")
async def close_button(ctx):
    """Handle close button click."""
    await ctx.message.delete()
    await ctx.send("✅ Panel closed!", ephemeral=True)


@interactive.slash_command(name="select", description="Test select menu")
async def select_menu_cmd(ctx: arc.GatewayContext):
    """Command with select menu."""
    row = ctx.client.rest.build_message_action_row()
    
    select = row.add_select_menu("color_select")
    select.add_option("Red", "red").set_emoji("🔴")
    select.add_option("Green", "green").set_emoji("🟢")
    select.add_option("Blue", "blue").set_emoji("🔵")
    select.set_placeholder("Choose a color")
    
    await ctx.respond("🎨 Pick your favorite color:", components=[row])


@interactive.select_menu("color_select")
async def color_select_handler(ctx):
    """Handle color selection."""
    color = ctx.values[0]
    await ctx.send(f"You selected: {color}!", ephemeral=True)
