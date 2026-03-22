# Changelog - OnyxCord Modified Version

Todas as modificações feitas neste fork do hikari-arc.

## [Unreleased]

### Added - Auto-Loading System

#### Easy Commands (`arc.ext.easy_commands`)
- `load_commands()` - Carrega comandos automaticamente de diretórios
- `load_events()` - Carrega eventos automaticamente
- `load_all()` / `EasyAll()` - Carrega comandos e eventos de uma vez
- Suporte a estrutura de diretórios por categoria
- Zero boilerplate - apenas decore funções com `@slash_command`
- Ignora arquivos começando com `_`
- Error handling com mensagens claras

#### Easy Plugins (`arc.ext.easy_plugins`)
- `load_plugins()` - Carrega plugins automaticamente
- Descobre instâncias de `GatewayPlugin` e `RESTPlugin`
- Suporte a caminhos customizados
- Logging opcional de plugins carregados

#### Documentação
- Guia completo: `docs/guides/easy_commands.md`
- Comparação entre Plugins vs Easy Commands
- Exemplos práticos de uso
- Guia de migração de loaders customizados

#### Exemplos
- `examples/easy_commands_example/` - Exemplo completo de auto-loading de comandos
- `examples/easy_plugins_example/` - Exemplo completo de auto-loading de plugins
- READMEs explicativos em cada exemplo

#### README Updates
- Seção de Auto-Loading no README principal
- Tabela comparativa Plugins vs Easy Commands
- Links para guias e exemplos
- Tabela de resumo de features

### Previous Features

#### EasyPlugin & EasyInteraction
- Sistema de interações estilo disnake
- Decorators: `@button()`, `@select_menu()`, `@modal()`
- Context simplificado com `ctx.send()`
- Suporte a regex para IDs dinâmicos
- Auto-defer configurável
- Debug mode

#### Emoji Support
- Parsing automático de emojis customizados
- Suporte em botões e select menus

## Diferenças do Original

Este fork adiciona funcionalidades que não existem no hikari-arc original:

1. **Auto-Loading System** - Sistema completo de descoberta e carregamento automático
2. **Easy Commands** - Comandos sem necessidade de plugins manuais
3. **Easy Plugins** - Auto-loading de plugins
4. **EasyAll()** - Alias intuitivo para load_all()
5. **Documentação em Português** - Guias e exemplos em PT-BR
6. **Exemplos Práticos** - Exemplos completos e funcionais

## Compatibilidade

- Totalmente compatível com hikari-arc original
- Pode misturar abordagens (plugins manuais + auto-loading)
- Não quebra código existente
- Adiciona apenas novas funcionalidades opcionais

## Créditos

- **Fork por:** Gustavo S.
- **Base:** [hikari-arc](https://github.com/hypergonial/hikari-arc) por hypergonial
- **Propósito:** Facilitar desenvolvimento de bots Discord com hikari
