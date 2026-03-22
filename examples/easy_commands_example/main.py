"""
Example bot using Easy Commands auto-loading system.

This example demonstrates how to use the auto-loading feature
to automatically discover and load commands, events, and plugins.
"""

import hikari
import arc
from arc.ext import EasyAll

# Create bot instance
bot = hikari.GatewayBot(token="YOUR_TOKEN_HERE")

# Create arc client
client = arc.GatewayClient(bot)

# Auto-load all commands and events from ./commands and ./events directories
loaded = EasyAll(client)

print(f"Loaded {len(loaded)} modules:")
for module in loaded:
    print(f"  - {module}")

# Run the bot
if __name__ == "__main__":
    bot.run()
