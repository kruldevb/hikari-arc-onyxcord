"""
Example bot using Easy Plugins auto-loading system.

This example demonstrates how to automatically load plugins
without manual registration.
"""

import hikari
import arc
from arc.ext import load_plugins

# Create bot instance
bot = hikari.GatewayBot(token="YOUR_TOKEN_HERE")

# Create arc client
client = arc.GatewayClient(bot)

# Auto-load all plugins from ./plugins directory
loaded = load_plugins(client)

print(f"Loaded {len(loaded)} plugins:")
for module in loaded:
    print(f"  - {module}")

# Run the bot
if __name__ == "__main__":
    bot.run()
