# Easy Plugins Example

This example demonstrates the auto-loading feature for plugins in hikari-arc.

## Structure

```
easy_plugins_example/
├── main.py              # Main bot file
└── plugins/             # Plugins directory
    ├── moderation.py    # Moderation plugin
    └── fun.py           # Fun commands plugin
```

## How It Works

1. Each plugin file creates a `GatewayPlugin` instance
2. Commands are added to the plugin using `@plugin.include`
3. `load_plugins(client)` automatically discovers and loads all plugins

## Running

1. Replace `YOUR_TOKEN_HERE` in `main.py` with your bot token
2. Run: `python main.py`

## Adding New Plugins

Create a new `.py` file in the plugins directory:

```python
# plugins/utility.py
import arc

utility_plugin = arc.GatewayPlugin("Utility")

@utility_plugin.include
@arc.slash_command("ping", "Check bot latency")
async def ping(ctx: arc.GatewayContext):
    await ctx.respond("Pong!")
```

The plugin will be loaded automatically on next restart!

## When to Use Plugins vs Easy Commands

### Use Plugins When:
- Commands share state or dependencies
- You need fine-grained control over loading
- Commands are logically grouped (moderation, music, etc.)
- You want to enable/disable entire feature sets

### Use Easy Commands When:
- Commands are independent
- You want minimal boilerplate
- File-based organization is sufficient
- You're prototyping or learning

## Mixing Both Approaches

You can use both in the same bot:

```python
from arc.ext import load_plugins, load_commands

# Load plugins for complex features
load_plugins(client, "./plugins")

# Load simple commands
load_commands(client, "./commands")
```
