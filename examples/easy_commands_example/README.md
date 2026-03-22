# Easy Commands Example

This example demonstrates the auto-loading feature of hikari-arc.

## Structure

```
easy_commands_example/
├── main.py              # Main bot file
├── commands/            # Commands directory
│   ├── general/         # General commands category
│   │   ├── ping.py
│   │   └── info.py
│   └── moderation/      # Moderation commands category
│       └── ban.py
└── events/              # Events directory
    └── ready.py
```

## How It Works

1. Commands are organized in subdirectories by category
2. Each command file contains a `@slash_command` decorated function
3. Events are async functions in the events directory
4. `EasyAll(client)` automatically discovers and loads everything

## Running

1. Replace `YOUR_TOKEN_HERE` in `main.py` with your bot token
2. Run: `python main.py`

## Adding New Commands

Just create a new `.py` file in any category folder:

```python
# commands/fun/joke.py
from arc import slash_command, GatewayContext

@slash_command("joke", "Tell a joke")
async def joke(ctx: GatewayContext):
    await ctx.respond("Why did the chicken cross the road? 🐔")
```

No need to register it - it will be loaded automatically!

## Adding New Events

Create a new `.py` file in the events directory:

```python
# events/message.py
import hikari

async def on_message(event: hikari.MessageCreateEvent):
    print(f"Message from {event.author.username}: {event.content}")
```

## Comparison with Traditional Plugins

### Traditional Way (More Control)

```python
# plugins/moderation.py
import arc

moderation = arc.GatewayPlugin("Moderation")

@moderation.include
@arc.slash_command("ban", "Ban a user")
async def ban(ctx: arc.GatewayContext):
    pass

# main.py
from plugins.moderation import moderation
client.add_plugin(moderation)
```

### Easy Commands Way (Less Boilerplate)

```python
# commands/moderation/ban.py
from arc import slash_command, GatewayContext

@slash_command("ban", "Ban a user")
async def ban(ctx: GatewayContext):
    pass

# main.py
from arc.ext import EasyAll
EasyAll(client)
```

Both approaches work and can be mixed in the same bot!
