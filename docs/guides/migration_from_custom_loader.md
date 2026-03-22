# Migração de Loaders Customizados

Se você estava usando um loader customizado (como o código ofuscado mostrado abaixo), este guia mostra como migrar para o sistema oficial de auto-loading do arc.

## Código Antigo (Ofuscado)

```python
_0 = __import__("pathlib").Path(__file__).parent.parent / "commands"
_0e = __import__("pathlib").Path(__file__).parent.parent / "events"
_1 = []

def _2(_3):
    for _4 in _0.iterdir():
        if not _4.is_dir() or _4.name.startswith("_"):
            continue
        for _5 in _4.glob("*.py"):
            if _5.name.startswith("_"):
                continue
            _6 = f"{_0.parent.name}.commands.{_4.name}.{_5.stem}"
            with __import__("contextlib").suppress(Exception):
                _7 = __import__("importlib").import_module(_6)
                for _8, _9 in __import__("inspect").getmembers(_7):
                    if isinstance(_9, __import__("arc").SlashCommand):
                        _10 = __import__("arc").GatewayPlugin(_8)
                        _10.include(_9)
                        _3.add_plugin(_10)
                        _1.append(_6)

def _2e(_3):
    if not _0e.exists():
        return
    for _4 in _0e.glob("*.py"):
        if _4.name.startswith("_"):
            continue
        _6 = f"{_0e.parent.name}.events.{_4.stem}"
        try:
            _7 = __import__("importlib").import_module(_6)
            for _8, _9 in __import__("inspect").getmembers(
                _7, __import__("inspect").iscoroutinefunction
            ):
                _3.bot.listen()(_9)
                _1.append(_6)
                print(f"[LOADER] Evento carregado: {_6} -> {_8}")
        except Exception as e:
            print(f"[LOADER] Erro ao carregar {_6}: {e}")

def Cmds(_3):
    _2(_3)
    _2e(_3)
    return _1
```

## Código Novo (arc.ext)

```python
from arc.ext import EasyAll

# Isso substitui todo o código acima!
loaded = EasyAll(client)
```

## Migração Passo a Passo

### 1. Remova o Loader Antigo

Remova todo o código do loader customizado do seu projeto.

### 2. Atualize o Main File

**Antes:**
```python
import hikari
import arc
from seu_loader import Cmds

bot = hikari.GatewayBot(token="...")
client = arc.GatewayClient(bot)

# Loader customizado
Cmds(client)

bot.run()
```

**Depois:**
```python
import hikari
import arc
from arc.ext import EasyAll

bot = hikari.GatewayBot(token="...")
client = arc.GatewayClient(bot)

# Loader oficial do arc
EasyAll(client)

bot.run()
```

### 3. Estrutura de Diretórios

A estrutura permanece a mesma:

```
seu_bot/
├── main.py
├── commands/
│   ├── general/
│   │   └── ping.py
│   └── moderation/
│       └── ban.py
└── events/
    └── ready.py
```

### 4. Formato dos Comandos

**Antes:**
```python
# commands/general/ping.py
from arc import *
from hikari import *

@slash_command("ping", "Check latency")
async def ping(ctx: GatewayContext):
    await ctx.respond("Pong!")
```

**Depois (recomendado):**
```python
# commands/general/ping.py
from arc import slash_command, GatewayContext

@slash_command("ping", "Check latency")
async def ping(ctx: GatewayContext):
    await ctx.respond("Pong!")
```

Nota: Evite `from arc import *` - importe apenas o que você precisa.

### 5. Formato dos Eventos

**Antes:**
```python
# events/ready.py
async def on_ready(event):
    print("Bot ready!")
```

**Depois (adicione type hints):**
```python
# events/ready.py
import hikari

async def on_ready(event: hikari.StartedEvent):
    print("Bot ready!")
```

## Vantagens da Migração

1. **Código Oficial**: Mantido pela equipe do arc
2. **Mais Legível**: Sem ofuscação
3. **Melhor Suporte**: Documentação e exemplos
4. **Type Safety**: Type hints adequados
5. **Error Handling**: Mensagens de erro claras
6. **Flexibilidade**: Múltiplas opções de loading

## Opções Avançadas

### Carregar Apenas Comandos

```python
from arc.ext import load_commands

load_commands(client)
```

### Carregar Apenas Eventos

```python
from arc.ext import load_events

load_events(client)
```

### Caminhos Customizados

```python
from pathlib import Path
from arc.ext import load_commands, load_events

load_commands(client, Path("./src/commands"))
load_events(client, Path("./src/events"))
```

### Carregar Plugins Também

```python
from arc.ext import EasyAll, load_plugins

# Carrega comandos e eventos
EasyAll(client)

# Carrega plugins adicionais
load_plugins(client, "./plugins")
```

## Diferenças Importantes

### 1. Criação Automática de Plugins

**Loader Antigo**: Criava um plugin para cada comando
```python
_10 = __import__("arc").GatewayPlugin(_8)
_10.include(_9)
_3.add_plugin(_10)
```

**Loader Novo**: Faz o mesmo automaticamente
```python
plugin = arc.GatewayPlugin(name)
plugin.include(obj)
client.add_plugin(plugin)
```

### 2. Error Handling

**Loader Antigo**: Suprimia todos os erros
```python
with __import__("contextlib").suppress(Exception):
    # ...
```

**Loader Novo**: Mostra erros com mensagens claras
```python
try:
    # ...
except Exception as e:
    print(f"[EASY_COMMANDS] Error loading {module_name}: {e}")
```

### 3. Logging

**Loader Antigo**: Logging apenas para eventos
```python
print(f"[LOADER] Evento carregado: {_6} -> {_8}")
```

**Loader Novo**: Logging para tudo (opcional)
```python
print(f"[EASY_COMMANDS] Event loaded: {module_name} -> {name}")
```

## Troubleshooting

### Comandos não estão sendo carregados

Verifique:
1. Estrutura de diretórios está correta
2. Arquivos não começam com `_`
3. Comandos usam `@slash_command`
4. Imports estão corretos

### Eventos não estão sendo carregados

Verifique:
1. Funções são `async`
2. Funções têm type hints corretos
3. Arquivos estão em `./events`

### Erros de Import

Se você tinha:
```python
from arc import *
```

Mude para:
```python
from arc import slash_command, GatewayContext, Option
```

## Conclusão

A migração é simples e traz muitos benefícios. O novo sistema é mais limpo, mais fácil de manter e totalmente suportado pela equipe do arc.
