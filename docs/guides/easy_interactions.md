# Easy Interactions - Disnake-style Components

Arc's `EasyPlugin` and `EasyInteraction` system provides a simplified, decorator-based approach to handling buttons, select menus, and modals - similar to disnake.ext.commands.

## Quick Start

```python
import hikari
import arc
from arc.ext import EasyPlugin, EasyInteraction

bot = hikari.GatewayBot("TOKEN")
client = arc.GatewayClient(bot)

# Register the interaction handler
bot.listen(hikari.InteractionCreateEvent)(EasyInteraction)

# Create a plugin
plugin = EasyPlugin("MyPlugin")

@plugin.slash_command(name="panel", description="Open control panel")
async def panel(ctx: arc.GatewayContext):
    row = ctx.client.rest.build_message_action_row()
    row.add_interactive_button(hikari.ButtonStyle.PRIMARY, "config", label="⚙️ Config")
    await ctx.respond("Control Panel", components=[row])

@plugin.button("config")
async def config_button(ctx):
    await ctx.send("Config opened!", ephemeral=True)

client.add_plugin(plugin)
bot.run()
```

## Features

### 🎯 Decorator-based Handlers

Register handlers for buttons, select menus, and modals using simple decorators:

```python
@plugin.button("custom_id")
async def button_handler(ctx):
    await ctx.send("Button clicked!")

@plugin.select_menu("menu_id")
async def select_handler(ctx):
    await ctx.send(f"Selected: {ctx.value}")

@plugin.modal("modal_id")
async def modal_handler(ctx):
    await ctx.send(f"Name: {ctx.values.name}")
```

### 🔥 Intuitive Context

The `InteractionContext` provides a clean API similar to disnake:

```python
@plugin.button("example")
async def handler(ctx):
    # Send a response
    await ctx.send("Hello!", ephemeral=True)
    
    # Access user info
    user = ctx.user
    guild_id = ctx.guild_id
    
    # For select menus
    selected = ctx.value  # Single select
    all_values = ctx.values  # All selected values
    
    # For modals
    name = ctx.values.name_input  # Attribute access
    age = ctx.get_modal_value("age_input", "Unknown")  # With default
```

### 🧩 Regex Support for Dynamic IDs

Handle dynamic custom_ids using regex patterns:

```python
import re

@plugin.button(re.compile(r"user:(\d+)"))
async def user_profile(ctx, user_id: str):
    # user_id is automatically extracted from the regex group!
    await ctx.send(f"Viewing profile for user {user_id}")

@plugin.button(re.compile(r"shop:(\w+):(\d+)"))
async def shop_item(ctx, category: str, item_id: str):
    await ctx.send(f"Category: {category}, Item: {item_id}")
```

### 🏷️ Automatic Namespacing

Plugins automatically namespace their custom_ids to prevent conflicts:

```python
admin_plugin = EasyPlugin("Admin")
user_plugin = EasyPlugin("User")

@admin_plugin.button("config")  # Becomes "Admin:config"
async def admin_config(ctx):
    await ctx.send("Admin config")

@user_plugin.button("config")  # Becomes "User:config"
async def user_config(ctx):
    await ctx.send("User config")

# Disable namespacing if needed
@admin_plugin.button("global_button", use_namespace=False)
async def global_handler(ctx):
    await ctx.send("Global button")
```

## Button Handlers

### Basic Button

```python
@plugin.slash_command(name="menu", description="Show menu")
async def menu(ctx: arc.GatewayContext):
    row = ctx.client.rest.build_message_action_row()
    row.add_interactive_button(hikari.ButtonStyle.PRIMARY, "option1", label="Option 1")
    row.add_interactive_button(hikari.ButtonStyle.SUCCESS, "option2", label="Option 2")
    await ctx.respond("Choose an option:", components=[row])

@plugin.button("option1")
async def option1_handler(ctx):
    await ctx.send("You chose option 1!", ephemeral=True)

@plugin.button("option2")
async def option2_handler(ctx):
    await ctx.edit(content="You chose option 2!", components=[])
```

### Dynamic Buttons with Regex

```python
@plugin.slash_command(name="users", description="List users")
async def users(ctx: arc.GatewayContext):
    row = ctx.client.rest.build_message_action_row()
    for user_id in [123, 456, 789]:
        row.add_interactive_button(
            hikari.ButtonStyle.PRIMARY,
            f"user:{user_id}",
            label=f"User {user_id}"
        )
    await ctx.respond("Select a user:", components=[row])

@plugin.button(re.compile(r"user:(\d+)"))
async def view_user(ctx, user_id: str):
    await ctx.send(f"Viewing user {user_id}", ephemeral=True)
```

## Select Menu Handlers

```python
@plugin.slash_command(name="roles", description="Select your roles")
async def roles(ctx: arc.GatewayContext):
    row = ctx.client.rest.build_message_action_row()
    menu = row.add_text_menu("role_select")
    menu.add_option("Developer", "dev").set_emoji("💻")
    menu.add_option("Designer", "design").set_emoji("🎨")
    menu.add_option("Moderator", "mod").set_emoji("🛡️")
    await ctx.respond("Select your role:", components=[row])

@plugin.select_menu("role_select")
async def role_handler(ctx):
    # Use ctx.value for single select
    selected = ctx.value
    
    # Or ctx.values for multi-select
    all_selected = ctx.values
    
    await ctx.send(f"You selected: {selected}", ephemeral=True)
```

## Modal Handlers

### Creating and Handling Modals

```python
@plugin.slash_command(name="register", description="Register in the system")
async def register(ctx: arc.GatewayContext):
    await ctx.interaction.create_modal_response(
        title="Registration Form",
        custom_id="registration_modal",
        components=[
            ctx.client.rest.build_modal_action_row().add_text_input(
                "name_input",
                "Name",
                placeholder="Enter your name",
                required=True,
                max_length=50
            ),
            ctx.client.rest.build_modal_action_row().add_text_input(
                "age_input",
                "Age",
                placeholder="Enter your age",
                required=True,
                max_length=3
            ),
            ctx.client.rest.build_modal_action_row().add_text_input(
                "bio_input",
                "Bio",
                style=hikari.TextInputStyle.PARAGRAPH,
                placeholder="Tell us about yourself",
                required=False,
                max_length=500
            ),
        ]
    )

@plugin.modal("registration_modal")
async def registration_handler(ctx):
    # Method 1: Attribute access (cleanest)
    name = ctx.values.name_input
    age = ctx.values.age_input
    bio = ctx.values.bio_input or "Not provided"
    
    # Method 2: Get with default
    # name = ctx.get_modal_value("name_input", "Anonymous")
    
    embed = hikari.Embed(
        title="✅ Registration Complete",
        description=f"**Name:** {name}\n**Age:** {age}\n**Bio:** {bio}",
        color=0x00FF00
    )
    
    await ctx.send(embed=embed, ephemeral=True)
```

## Advanced Configuration

### Router Configuration

Configure the global router with advanced options:

```python
from arc.ext import configure_router, EasyInteraction

# Enable auto-defer and debug logging
configure_router(auto_defer=True, debug=True)

bot.listen(hikari.InteractionCreateEvent)(EasyInteraction)
```

**Options:**
- `auto_defer`: Automatically defer interactions if not responded to (prevents "Interaction Failed" errors)
- `debug`: Enable debug logging to see interaction events in console

### Error Handling

The router automatically handles errors and provides user feedback:

```python
@plugin.button("error_test")
async def error_handler(ctx):
    raise ValueError("Something went wrong!")
    # User will see: "❌ An error occurred while processing your interaction."
    # Error is logged with full traceback
```

## Context Methods

### InteractionContext API

```python
# Send a response
await ctx.send("Message", ephemeral=True)
await ctx.respond("Message")  # Alias for send()

# Defer the response
await ctx.defer(ephemeral=True)

# Edit the original message
await ctx.edit(content="Updated!", components=[])

# Access properties
user = ctx.user
guild_id = ctx.guild_id
channel_id = ctx.channel_id
custom_id = ctx.custom_id

# Check if responded
if not ctx.responded:
    await ctx.send("Response")

# For select menus
value = ctx.value  # First selected value
values = ctx.values  # All selected values

# For modals
name = ctx.values.name_input  # Attribute access
age = ctx.get_modal_value("age_input", "Unknown")  # With default

# For regex matches
if ctx.match:
    groups = ctx.match.groups()
```

## Complete Example

```python
import hikari
import arc
import re
from arc.ext import EasyPlugin, EasyInteraction, configure_router

bot = hikari.GatewayBot("TOKEN")
client = arc.GatewayClient(bot)

# Configure router
configure_router(auto_defer=False, debug=True)
bot.listen(hikari.InteractionCreateEvent)(EasyInteraction)

# Create plugin
plugin = EasyPlugin("Dashboard")

@plugin.slash_command(name="dashboard", description="Open dashboard")
async def dashboard(ctx: arc.GatewayContext):
    row = ctx.client.rest.build_message_action_row()
    row.add_interactive_button(hikari.ButtonStyle.PRIMARY, "settings", label="⚙️ Settings")
    row.add_interactive_button(hikari.ButtonStyle.SUCCESS, "profile", label="👤 Profile")
    row.add_interactive_button(hikari.ButtonStyle.DANGER, "logout", label="🚪 Logout")
    
    await ctx.respond("**Dashboard**\nSelect an option:", components=[row])

@plugin.button("settings")
async def settings(ctx):
    await ctx.send("⚙️ Opening settings...", ephemeral=True)

@plugin.button("profile")
async def profile(ctx):
    embed = hikari.Embed(
        title="👤 Your Profile",
        description=f"User: {ctx.user.mention}\nID: {ctx.user.id}",
        color=0x00FF00
    )
    await ctx.send(embed=embed, ephemeral=True)

@plugin.button("logout")
async def logout(ctx):
    await ctx.edit(content="👋 Logged out!", components=[])

# Dynamic buttons with regex
@plugin.slash_command(name="items", description="Browse items")
async def items(ctx: arc.GatewayContext):
    row = ctx.client.rest.build_message_action_row()
    for item_id in range(1, 4):
        row.add_interactive_button(
            hikari.ButtonStyle.PRIMARY,
            f"item:{item_id}",
            label=f"Item {item_id}"
        )
    await ctx.respond("Select an item:", components=[row])

@plugin.button(re.compile(r"item:(\d+)"))
async def view_item(ctx, item_id: str):
    await ctx.send(f"Viewing item #{item_id}", ephemeral=True)

client.add_plugin(plugin)
bot.run()
```

## Migration from Standard Arc

### Before (Standard Arc)

```python
@bot.listen(hikari.InteractionCreateEvent)
async def on_interaction(event: hikari.InteractionCreateEvent):
    if isinstance(event.interaction, hikari.ComponentInteraction):
        if event.interaction.custom_id == "my_button":
            await event.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                content="Button clicked!",
                flags=hikari.MessageFlag.EPHEMERAL
            )
```

### After (EasyInteraction)

```python
from arc.ext import EasyPlugin, EasyInteraction

bot.listen(hikari.InteractionCreateEvent)(EasyInteraction)

plugin = EasyPlugin("MyPlugin")

@plugin.button("my_button")
async def button_handler(ctx):
    await ctx.send("Button clicked!", ephemeral=True)
```

## Best Practices

1. **Use namespacing** for large bots to avoid custom_id conflicts
2. **Enable debug mode** during development to see interaction logs
3. **Use regex patterns** for dynamic content (user profiles, shop items, etc.)
4. **Leverage ctx.values** for clean modal value access
5. **Use ctx.send()** instead of ctx.respond() for better readability
6. **Handle errors gracefully** - the router will catch them, but log appropriately

## See Also

- [Plugins & Extensions](plugins_extensions.md)
- [Error Handling](error_handling.md)
- [Hikari Fundamentals](hikari_fundamentals.md)
