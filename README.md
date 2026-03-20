# hikari-arc - OnyxCord Modified Version

> **Fork modificado por Gustavo S.**
> 
> Esta é uma versão modificada do [hikari-arc](https://github.com/hypergonial/hikari-arc) preparada para futuras modificações e suporte aos novos componentes de modais do Discord através do OnyxCord.

<div align="center">
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="./docs/assets/branding/composed-darkmode.svg">
        <source media="(prefers-color-scheme: light)" srcset="./docs/assets/branding/composed-lightmode.svg">
        <img alt="The arc logo" src="./docs/assets/branding/composed-lightmode.svg" width="30%">
    </picture>
</div>

---

<div align="center">

[![Original PyPI](https://img.shields.io/pypi/v/hikari-arc)](https://pypi.org/project/hikari-arc)
[![Original Repo](https://img.shields.io/badge/original-hypergonial/hikari--arc-blue)](https://github.com/hypergonial/hikari-arc)

</div>

A command handler for [hikari](https://github.com/hikari-py/hikari) with a focus on type-safety and correctness.

## Status do Fork

Este fork está atualmente sem modificações em relação ao original. Modificações serão adicionadas conforme necessário para suportar funcionalidades do OnyxCord. Atualizações futuras serão documentadas aqui.

## Instalação

### A partir do Git (Recomendado para OnyxCord)

```sh
pip install git+https://github.com/kruldevb/hikari-arc-onyxcord.git
```

### Desenvolvimento Local

```sh
pip install -e .
```

### Versão Original

Para instalar a versão original não modificada:

```sh
pip install -U hikari-arc
```

> [!NOTE]
> `hikari-arc` requer Python versão *no mínimo* 3.10.

## Basic Usage

```py
import hikari
import arc

bot = hikari.GatewayBot("TOKEN") # or hikari.RESTBot
client = arc.GatewayClient(bot) # or arc.RESTClient

@client.include
@arc.slash_command("hi", "Say hi!")
async def ping(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.User, arc.UserParams("The user to say hi to.")]
) -> None:
    await ctx.respond(f"Hey {user.mention}!")

bot.run()
```

To get started with `arc`, see the [documentation](https://arc.hypergonial.com), or the [examples](https://github.com/hypergonial/hikari-arc/tree/main/examples).

## Issues and support

For general usage help or questions, see the [hikari discord](https://discord.gg/hikari), if you have found a bug or have a feature request, feel free to [open an issue](https://github.com/hypergonial/hikari-arc/issues/new/choose)!

## Contributing

See [Contributing](./CONTRIBUTING.md).

## Acknowledgements

`arc` is in large part a combination of all the parts I like in other command handlers, with my own spin on it. The following projects have inspired me and aided me greatly in the design of this library:

- [`hikari-lightbulb`](https://github.com/tandemdude/hikari-lightbulb) - The library initially started as a reimagination of lightbulb, it inherits a similar project structure and terminology.
- [`Tanjun`](https://github.com/FasterSpeeding/Tanjun) - For the idea of using `typing.Annotated` and [dependency injection](https://arc.hypergonial.com/guides/dependency_injection/) in a command handler. `arc` also uses the same dependency injection library, [`Alluka`](https://github.com/FasterSpeeding/Alluka), under the hood.
- [`hikari-crescent`](https://github.com/hikari-crescent/hikari-crescent) The design of [hooks](https://arc.hypergonial.com/guides/hooks/) is largely inspired by `crescent`.
- [`FastAPI`](https://github.com/tiangolo/fastapi) - Some design ideas and most of the [documentation](https://arc.hypergonial.com/) [configuration](https://github.com/hypergonial/hikari-arc/blob/main/mkdocs.yml) derives from `FastAPI`.
- The `arc` logo was made by [@PythonTryHard](https://github.com/PythonTryHard).


## Links

- [**Repositório Original**](https://github.com/hypergonial/hikari-arc)
- [**Documentação Original**](https://arc.hypergonial.com)
- [**Examples**](https://github.com/hypergonial/hikari-arc/tree/main/examples)
- [**License**](https://github.com/hypergonial/hikari-arc/blob/main/LICENSE)

---

**Modificado por:** Gustavo S.  
**Versão Base:** hikari-arc (hypergonial)  
**Propósito:** Preparado para futuras modificações e suporte aos novos componentes de modais do Discord via OnyxCord
