# Complete Example - All Features Combined

This example demonstrates how to use all hikari-arc features together in one bot.

## Features Demonstrated

1. **Easy Commands** - Auto-loaded commands from `./commands`
2. **Easy Plugins** - Auto-loaded plugins from `./plugins`
3. **Easy Interactions** - Buttons, selects, and modals
4. **Traditional Plugins** - Manual plugin registration
5. **Events** - Auto-loaded event handlers

## Structure

```
complete_example/
├── main.py                    # Main bot file
├── commands/                  # Easy Commands (auto-loaded)
│   └── utility/
│       └── ping.py
├── plugins/                   # Easy Plugins (auto-loaded)
│   └── interactive.py         # With buttons & selects
├── manual_plugins/            # Traditional plugins (manual)
│   └── admin.py
└── events/                    # Events (auto-loaded)
    └── ready.py
```

## How It Works

### 1. Easy Commands (Auto-loaded)

```python
# commands/utility/ping.py
from arc import slash_command, GatewayContext

@slash_command("ping", "Check bot latency")
async def ping(ctx: GatewayContext):
    await ctx.respond("Pong!")
```

Loaded automatically by `EasyAll(client)` in main.py.

### 2. Easy Plugins (Auto-loaded)

```python
# plugins/interactive.py
from arc.ext import EasyPlugin

interactive = EasyPlugin("Interactive")

@interactive.slash_command(name="panel", description="Panel")
async def panel(ctx):
    # ...

@interactive.button("info")
async def info_button(ctx):
    # ...
```

Loaded automatically by `load_plugins(client)` in main.py.

### 3. Traditional Plugins (Manual)

```python
# manual_plugins/admin.py
import arc

admin_plugin = arc.GatewayPlugin("Admin")

@admin_plugin.include
@arc.slash_command("announce", "Send announcement")
async def announce(ctx):
    # ...
```

Loaded manually with `client.add_plugin(admin_plugin)` in main.py.

### 4. Events (Auto-loaded)

```python
# events/ready.py
import hikari

async def on_ready(event: hikari.StartedEvent):
    print("Bot ready!")
```

Loaded automatically by `EasyAll(client)` in main.py.

## Running

1. Replace `YOUR_TOKEN_HERE` in `main.py`
2. Run: `python main.py`

## When to Use Each Approach

### Easy Commands
- ✅ Simple, independent commands
- ✅ Quick prototyping
- ✅ Minimal boilerplate

### Easy Plugins
- ✅ Commands with shared state
- ✅ Interactive features (buttons, selects)
- ✅ Auto-loading with organization

### Traditional Plugins
- ✅ Complex features
- ✅ Fine-grained control
- ✅ Conditional loading
- ✅ Shared dependencies

## Mixing Approaches

You can use all three approaches in the same bot! This example shows how:

```python
# main.py
from arc.ext import EasyAll, load_plugins

# Auto-load simple commands
EasyAll(client)

# Auto-load interactive plugins
load_plugins(client)

# Manually add complex plugins
from manual_plugins.admin import admin_plugin
client.add_plugin(admin_plugin)
```

## Best Practices

1. Use Easy Commands for simple utilities
2. Use Easy Plugins for interactive features
3. Use Traditional Plugins for complex systems
4. Keep related commands together
5. Use meaningful directory names
6. Add docstrings to all commands

## Available Commands

After running this example, you'll have:

- `/ping` - Check bot latency (Easy Command)
- `/panel` - Interactive panel with buttons (Easy Plugin)
- `/select` - Select menu example (Easy Plugin)
- `/announce` - Send announcement (Traditional Plugin)
- `/clear` - Clear messages (Traditional Plugin)

Try them all to see the different approaches in action!
