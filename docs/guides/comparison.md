# Comparação de Abordagens

Este guia compara as diferentes formas de organizar seu bot com hikari-arc.

## Visão Geral

| Abordagem | Boilerplate | Controle | Organização | Melhor Para |
|-----------|-------------|----------|-------------|-------------|
| Easy Commands | ⭐⭐⭐⭐⭐ Mínimo | ⭐⭐ Baixo | 📁 Arquivos | Bots simples |
| Easy Plugins | ⭐⭐⭐⭐ Baixo | ⭐⭐⭐ Médio | 📁 Arquivos | Features interativas |
| Traditional Plugins | ⭐⭐ Alto | ⭐⭐⭐⭐⭐ Total | 🎯 Lógico | Bots complexos |

## Exemplo Lado a Lado

### Comando Simples

#### Easy Commands
```python
# commands/general/ping.py
from arc import slash_command, GatewayContext

@slash_command("ping", "Check latency")
async def ping(ctx: GatewayContext):
    await ctx.respond("Pong!")
```

```python
# main.py
from arc.ext import EasyAll
EasyAll(client)
```

**Linhas de código:** ~10

#### Traditional Plugin
```python
# plugins/general.py
import arc

general = arc.GatewayPlugin("General")

@general.include
@arc.slash_command("ping", "Check latency")
async def ping(ctx: arc.GatewayContext):
    await ctx.respond("Pong!")
```

```python
# main.py
from plugins.general import general
client.add_plugin(general)
```

**Linhas de código:** ~15

### Feature Interativa

#### Easy Plugin
```python
# plugins/panel.py
from arc.ext import EasyPlugin

panel = EasyPlugin("Panel")

@panel.slash_command(name="panel", description="Panel")
async def panel_cmd(ctx):
    row = ctx.client.rest.build_message_action_row()
    row.add_interactive_button(hikari.ButtonStyle.PRIMARY, "info", label="Info")
    await ctx.respond("Panel", components=[row])

@panel.button("info")
async def info_btn(ctx):
    await ctx.send("Info!", ephemeral=True)
```

```python
# main.py
from arc.ext import load_plugins, EasyInteraction
bot.listen(hikari.InteractionCreateEvent)(EasyInteraction)
load_plugins(client)
```

**Linhas de código:** ~20

#### Traditional Plugin
```python
# plugins/panel.py
import arc
import hikari

panel = arc.GatewayPlugin("Panel")

@panel.include
@arc.slash_command("panel", "Panel")
async def panel_cmd(ctx: arc.GatewayContext):
    row = ctx.client.rest.build_message_action_row()
    row.add_interactive_button(hikari.ButtonStyle.PRIMARY, "info", label="Info")
    await ctx.respond("Panel", components=[row])

@panel.set_error_handler
async def error_handler(ctx, error):
    await ctx.respond(f"Error: {error}")

# Você precisaria de um sistema customizado para lidar com interações
```

```python
# main.py
from plugins.panel import panel
client.add_plugin(panel)

# + Sistema customizado de interações
```

**Linhas de código:** ~30+

## Casos de Uso

### 1. Bot Simples (Poucos Comandos)

**Recomendação:** Easy Commands

```python
# main.py
import hikari
import arc
from arc.ext import EasyAll

bot = hikari.GatewayBot(token="...")
client = arc.GatewayClient(bot)
EasyAll(client)
bot.run()
```

**Por quê?**
- Mínimo boilerplate
- Fácil de começar
- Rápido para prototipar

### 2. Bot com Painéis Interativos

**Recomendação:** Easy Plugins

```python
# main.py
import hikari
import arc
from arc.ext import load_plugins, EasyInteraction

bot = hikari.GatewayBot(token="...")
client = arc.GatewayClient(bot)

bot.listen(hikari.InteractionCreateEvent)(EasyInteraction)
load_plugins(client)

bot.run()
```

**Por quê?**
- Suporte nativo a botões/selects
- Auto-loading conveniente
- Context simplificado

### 3. Bot Complexo (Muitas Features)

**Recomendação:** Traditional Plugins

```python
# main.py
import hikari
import arc

bot = hikari.GatewayBot(token="...")
client = arc.GatewayClient(bot)

# Controle fino sobre o que carregar
from plugins.moderation import moderation
from plugins.music import music
from plugins.economy import economy

if config.enable_moderation:
    client.add_plugin(moderation)

if config.enable_music:
    client.add_plugin(music)

if config.enable_economy:
    client.add_plugin(economy)

bot.run()
```

**Por quê?**
- Controle total sobre loading
- Carregamento condicional
- Melhor para features complexas

### 4. Bot Híbrido (Recomendado)

**Recomendação:** Misturar Abordagens

```python
# main.py
import hikari
import arc
from arc.ext import EasyAll, load_plugins, EasyInteraction

bot = hikari.GatewayBot(token="...")
client = arc.GatewayClient(bot)

# Interações
bot.listen(hikari.InteractionCreateEvent)(EasyInteraction)

# Comandos simples (auto)
EasyAll(client, "./commands")

# Features interativas (auto)
load_plugins(client, "./plugins")

# Features complexas (manual)
from manual_plugins.economy import economy
from manual_plugins.music import music

client.add_plugin(economy)
client.add_plugin(music)

bot.run()
```

**Por quê?**
- Melhor dos dois mundos
- Flexibilidade máxima
- Organização clara

## Métricas de Decisão

### Use Easy Commands quando:
- ✅ Comandos são independentes
- ✅ Não há estado compartilhado
- ✅ Quer começar rápido
- ✅ Bot tem < 20 comandos
- ✅ Não precisa de controle fino

### Use Easy Plugins quando:
- ✅ Precisa de botões/selects
- ✅ Comandos compartilham estado
- ✅ Quer auto-loading
- ✅ Features são modulares
- ✅ Quer organização por arquivo

### Use Traditional Plugins quando:
- ✅ Bot é complexo (> 50 comandos)
- ✅ Precisa de carregamento condicional
- ✅ Features têm dependências complexas
- ✅ Quer controle total
- ✅ Precisa de error handling customizado

## Performance

Todas as abordagens têm performance similar:

| Abordagem | Tempo de Loading | Uso de Memória | Runtime Performance |
|-----------|------------------|----------------|---------------------|
| Easy Commands | ~50ms | Baixo | Idêntico |
| Easy Plugins | ~50ms | Baixo | Idêntico |
| Traditional | ~50ms | Baixo | Idêntico |

A diferença está na **Developer Experience**, não na performance.

## Migração Entre Abordagens

### Easy Commands → Traditional Plugin

**Antes:**
```python
# commands/moderation/ban.py
from arc import slash_command, GatewayContext

@slash_command("ban", "Ban user")
async def ban(ctx: GatewayContext):
    pass
```

**Depois:**
```python
# plugins/moderation.py
import arc

moderation = arc.GatewayPlugin("Moderation")

@moderation.include
@arc.slash_command("ban", "Ban user")
async def ban(ctx: arc.GatewayContext):
    pass
```

### Traditional Plugin → Easy Plugin

**Antes:**
```python
# plugins/panel.py
import arc

panel = arc.GatewayPlugin("Panel")

@panel.include
@arc.slash_command("panel", "Panel")
async def panel_cmd(ctx):
    pass
```

**Depois:**
```python
# plugins/panel.py
from arc.ext import EasyPlugin

panel = EasyPlugin("Panel")

@panel.slash_command(name="panel", description="Panel")
async def panel_cmd(ctx):
    pass

@panel.button("info")
async def info_btn(ctx):
    pass
```

## Conclusão

Não existe uma abordagem "melhor" - depende do seu caso de uso:

- **Começando?** Use Easy Commands
- **Precisa de interações?** Use Easy Plugins
- **Bot complexo?** Use Traditional Plugins
- **Não sabe?** Use todas! (Híbrido)

A beleza do hikari-arc é que você pode misturar e combinar conforme necessário.
