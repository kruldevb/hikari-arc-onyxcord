# Easy Commands & Auto-Loading

The `arc.ext.easy_commands` and `arc.ext.easy_plugins` extensions provide automatic loading of commands, events, and plugins without manual registration.

## Overview

There are two main approaches to organizing your bot:

1. **Plugins** - Manual grouping of related commands (traditional arc approach)
2. **Easy Commands** - Automatic discovery and loading of commands from directories

## Plugins vs Easy Commands

### Traditional Plugins

Plugins are manually created containers that group related commands together:

```python
# plugins/moderation.py
import arc
import hikari

moderation = arc.GatewayPlugin("Moderation")

@moderation.include
@arc.slash_command("ban", "Ban a user")
async def ban(ctx: arc.GatewayContext, user: hikari.User):
    await ctx.respond(f"Banned {user.mention}")

@moderation.include
@arc.slash_command("kick", "Kick a user")
async def kick(ctx: arc.GatewayContext, user: hikari.User):
    await ctx.respond(f"Kicked {user.mention}")
```

```python
# main.py
import arc
from plugins.moderation import moderation

client = arc.GatewayClient(...)
client.add_plugin(moderation)
bot.run()
```

**Pros:**
- Explicit control over what gets loaded
- Easy to enable/disable entire feature sets
- Clear organization of related commands

**Cons:**
- Requires manual plugin creation and registration
- More boilerplate code

### Easy Commands

Easy Commands automatically discovers and loads commands without manual plugin creation:

```python
# commands/moderation/ban.py
from arc import slash_command, GatewayContext
import hikari

@slash_command("ban", "Ban a user")
async def ban(ctx: GatewayContext, user: hikari.User):
    await ctx.respond(f"Banned {user.mention}")
```

```python
# commands/moderation/kick.py
from arc import slash_command, GatewayContext
import hikari

@slash_command("kick", "Kick a user")
async def kick(ctx: GatewayContext, user: hikari.User):
    await ctx.respond(f"Kicked {user.mention}")
```

```python
# main.py
import arc
from arc.ext.easy_commands import load_all

client = arc.GatewayClient(...)
load_all(client)
bot.run()
```

**Pros:**
- Zero boilerplate - just write commands
- Automatic discovery and loading
- File-based organization

**Cons:**
- Less explicit control
- All commands in directory are loaded

## Auto-Loading Commands

### Directory Structure

```
your_bot/
├── main.py
├── commands/
│   ├── general/
│   │   ├── ping.py
│   │   └── info.py
│   ├── moderation/
│   │   ├── ban.py
│   │   └── kick.py
│   └── fun/
│       └── meme.py
└── events/
    ├── ready.py
    └── message.py
```

### Loading Commands

```python
# main.py
import hikari
import arc
from arc.ext.easy_commands import load_commands

bot = hikari.GatewayBot(token="...")
client = arc.GatewayClient(bot)

# Load all commands from ./commands directory
load_commands(client)

bot.run()
```

### Command File Example

```python
# commands/general/ping.py
from arc import slash_command, GatewayContext

@slash_command("ping", "Check bot latency")
async def ping(ctx: GatewayContext):
    latency = ctx.client.bot.heartbeat_latency * 1000
    await ctx.respond(f"Pong! Latency: {latency:.0f}ms")
```

## Auto-Loading Events

### Event File Example

```python
# events/ready.py
import hikari

async def on_ready(event: hikari.StartedEvent):
    print(f"Bot started as {event.my_user.username}")
```

### Loading Events

```python
# main.py
from arc.ext.easy_commands import load_events

# Load all events from ./events directory
load_events(client)
```

## Auto-Loading Plugins

If you prefer the plugin approach but want automatic loading:

```python
# plugins/moderation.py
import arc
import hikari

moderation_plugin = arc.GatewayPlugin("Moderation")

@moderation_plugin.include
@arc.slash_command("ban", "Ban a user")
async def ban(ctx: arc.GatewayContext, user: hikari.User):
    await ctx.respond(f"Banned {user.mention}")
```

```python
# main.py
from arc.ext.easy_plugins import load_plugins

# Load all plugins from ./plugins directory
load_plugins(client)
```

## Load Everything

Use `EasyAll()` (or `load_all()`) to load both commands and events:

```python
# main.py
import hikari
import arc
from arc.ext import EasyAll

bot = hikari.GatewayBot(token="...")
client = arc.GatewayClient(bot)

# Load all commands and events
EasyAll(client)

bot.run()
```

Note: `EasyAll()` is an alias for `load_all()` - both work the same way.

## Custom Paths

You can specify custom paths for your commands, events, or plugins:

```python
from pathlib import Path
from arc.ext.easy_commands import load_commands, load_events
from arc.ext.easy_plugins import load_plugins

# Custom paths
load_commands(client, Path("./src/commands"))
load_events(client, Path("./src/events"))
load_plugins(client, Path("./src/plugins"))
```

## Which Approach Should I Use?

### Use Easy Commands when:
- Building a simple bot with many independent commands
- You want minimal boilerplate
- File-based organization is sufficient
- You're prototyping or learning

### Use Plugins when:
- You need fine-grained control over loading
- Commands have shared state or dependencies
- You want to enable/disable feature sets dynamically
- Building a complex bot with many integrations

### Use Both:
You can mix both approaches! Use plugins for complex features and easy commands for simple utilities:

```python
import arc
from arc.ext.easy_commands import load_all
from arc.ext.easy_plugins import load_plugins

client = arc.GatewayClient(...)

# Load manual plugins
load_plugins(client, "./plugins")

# Load easy commands
EasyAll(client)

bot.run()
```

## Notes

- Files starting with `_` are ignored (e.g., `_utils.py`)
- Commands must use the `@slash_command` decorator
- Events must be async functions
- Plugins must be instances of `GatewayPlugin` or `RESTPlugin`
