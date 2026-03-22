"""
Complete Example - Combining All Features

This example demonstrates how to use:
- Easy Commands (auto-loading)
- Easy Plugins (auto-loading)
- Easy Interactions (buttons, selects, modals)
- Traditional plugins (manual)

All in the same bot!
"""

import hikari
import arc
from arc.ext import EasyAll, load_plugins, EasyInteraction

# Create bot instance
bot = hikari.GatewayBot(token="YOUR_TOKEN_HERE")

# Create arc client
client = arc.GatewayClient(bot)

# Register interaction handler for EasyPlugin features
bot.listen(hikari.InteractionCreateEvent)(EasyInteraction)

# Auto-load commands and events from ./commands and ./events
print("Loading commands and events...")
loaded_commands = EasyAll(client)

# Auto-load plugins from ./plugins
print("Loading plugins...")
loaded_plugins = load_plugins(client)

# You can also add manual plugins
from manual_plugins.admin import admin_plugin
client.add_plugin(admin_plugin)

print(f"\n✅ Bot ready!")
print(f"   - Loaded {len(loaded_commands)} command/event modules")
print(f"   - Loaded {len(loaded_plugins)} auto plugins")
print(f"   - Loaded 1 manual plugin")

# Run the bot
if __name__ == "__main__":
    bot.run()
