# Guia Rápido - hikari-arc OnyxCord

Comece a usar hikari-arc em 5 minutos!

## Instalação

```bash
pip install git+https://github.com/kruldevb/hikari-arc-onyxcord.git
```

## Método 1: Easy Commands (Mais Simples)

### 1. Crie a estrutura

```
meu_bot/
├── main.py
└── commands/
    └── general/
        └── ping.py
```

### 2. Crie o comando

```python
# commands/general/ping.py
from arc import slash_command, GatewayContext

@slash_command("ping", "Check bot latency")
async def ping(ctx: GatewayContext):
    await ctx.respond("Pong!")
```

### 3. Crie o bot

```python
# main.py
import hikari
import arc
from arc.ext import EasyAll

bot = hikari.GatewayBot(token="SEU_TOKEN_AQUI")
client = arc.GatewayClient(bot)

EasyAll(client)  # Carrega tudo automaticamente!

bot.run()
```

### 4. Execute

```bash
python main.py
```

Pronto! Seu bot está rodando com comandos auto-carregados.

## Método 2: Com Botões e Interações

### 1. Crie a estrutura

```
meu_bot/
├── main.py
└── plugins/
    └── panel.py
```

### 2. Crie o plugin interativo

```python
# plugins/panel.py
import hikari
from arc.ext import EasyPlugin

panel = EasyPlugin("Panel")

@panel.slash_command(name="panel", description="Open panel")
async def panel_cmd(ctx):
    row = ctx.client.rest.build_message_action_row()
    row.add_interactive_button(hikari.ButtonStyle.PRIMARY, "info", label="ℹ️ Info")
    await ctx.respond("Control Panel", components=[row])

@panel.button("info")
async def info_button(ctx):
    await ctx.send("This is the info!", ephemeral=True)
```

### 3. Crie o bot

```python
# main.py
import hikari
import arc
from arc.ext import load_plugins, EasyInteraction

bot = hikari.GatewayBot(token="SEU_TOKEN_AQUI")
client = arc.GatewayClient(bot)

# Registrar handler de interações
bot.listen(hikari.InteractionCreateEvent)(EasyInteraction)

# Carregar plugins
load_plugins(client)

bot.run()
```

### 4. Execute

```bash
python main.py
```

Agora você tem um bot com botões interativos!

## Método 3: Tradicional (Mais Controle)

### 1. Crie o plugin

```python
# plugins/moderation.py
import arc
import hikari

moderation = arc.GatewayPlugin("Moderation")

@moderation.include
@arc.slash_command("ban", "Ban a user")
async def ban(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User, arc.UserParams("User to ban")]
):
    await ctx.respond(f"Banned {user.mention}")
```

### 2. Crie o bot

```python
# main.py
import hikari
import arc
from plugins.moderation import moderation

bot = hikari.GatewayBot(token="SEU_TOKEN_AQUI")
client = arc.GatewayClient(bot)

client.add_plugin(moderation)

bot.run()
```

## Próximos Passos

### Adicionar mais comandos

Crie novos arquivos em `commands/categoria/comando.py`:

```python
# commands/fun/roll.py
import random
from arc import slash_command, GatewayContext, Option

@slash_command("roll", "Roll a dice")
async def roll(ctx: GatewayContext, sides: Option[int, "Number of sides"] = 6):
    result = random.randint(1, sides)
    await ctx.respond(f"🎲 You rolled: {result}")
```

Não precisa registrar - será carregado automaticamente!

### Adicionar eventos

Crie arquivos em `events/`:

```python
# events/ready.py
import hikari

async def on_ready(event: hikari.StartedEvent):
    print(f"Bot {event.my_user.username} is ready!")
```

### Adicionar select menus

```python
# plugins/colors.py
from arc.ext import EasyPlugin

colors = EasyPlugin("Colors")

@colors.slash_command(name="colors", description="Pick a color")
async def colors_cmd(ctx):
    row = ctx.client.rest.build_message_action_row()
    select = row.add_select_menu("color_select")
    select.add_option("Red", "red").set_emoji("🔴")
    select.add_option("Blue", "blue").set_emoji("🔵")
    select.set_placeholder("Choose a color")
    await ctx.respond("Pick your color:", components=[row])

@colors.select_menu("color_select")
async def color_handler(ctx):
    await ctx.send(f"You picked: {ctx.values[0]}", ephemeral=True)
```

## Estrutura Recomendada

```
meu_bot/
├── main.py              # Arquivo principal
├── commands/            # Comandos simples (auto-load)
│   ├── general/
│   │   ├── ping.py
│   │   └── info.py
│   └── fun/
│       └── roll.py
├── plugins/             # Features interativas (auto-load)
│   ├── panel.py
│   └── colors.py
├── events/              # Event handlers (auto-load)
│   └── ready.py
└── manual_plugins/      # Plugins complexos (manual)
    └── economy.py
```

## Dicas

1. **Use Easy Commands** para comandos simples
2. **Use Easy Plugins** para features com botões/selects
3. **Use Traditional Plugins** para features complexas
4. **Misture abordagens** conforme necessário
5. Arquivos começando com `_` são ignorados
6. Use type hints para melhor autocomplete

## Recursos

- [Documentação Completa](./docs/guides/easy_commands.md)
- [Exemplos](./examples/)
- [Comparação de Métodos](./docs/guides/comparison.md)
- [Guia de Migração](./docs/guides/migration_from_custom_loader.md)

## Problemas Comuns

### Comandos não aparecem no Discord

1. Aguarde alguns minutos (pode demorar)
2. Verifique se o bot tem permissão `applications.commands`
3. Tente em um servidor de teste primeiro

### Botões não funcionam

Certifique-se de registrar o handler:

```python
bot.listen(hikari.InteractionCreateEvent)(EasyInteraction)
```

### Import errors

Verifique se instalou corretamente:

```bash
pip install git+https://github.com/kruldevb/hikari-arc-onyxcord.git
```

## Suporte

- [Discord do Hikari](https://discord.gg/hikari)
- [Issues no GitHub](https://github.com/kruldevb/hikari-arc-onyxcord/issues)

---

Pronto para começar? Escolha um método acima e comece a codar! 🚀
