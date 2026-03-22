# Índice de Guias - hikari-arc OnyxCord

Documentação completa das features adicionadas neste fork.

## 🚀 Começando

- [**QUICKSTART**](../../QUICKSTART.md) - Comece em 5 minutos
- [**Installation Contexts**](./installation_contexts.md) - Instalação e configuração
- [**Hikari Fundamentals**](./hikari_fundamentals.md) - Fundamentos do Hikari

## 📦 Auto-Loading (Novo!)

### Easy Commands
- [**Easy Commands & Auto-Loading**](./easy_commands.md) - Sistema completo de auto-loading
  - `load_commands()` - Carrega comandos automaticamente
  - `load_events()` - Carrega eventos automaticamente
  - `load_all()` - Carrega tudo de uma vez
  - Estrutura de diretórios
  - Exemplos práticos

### Easy Plugins
- [**Easy Commands & Auto-Loading**](./easy_commands.md#auto-loading-plugins) - Auto-loading de plugins
  - `load_plugins()` - Carrega plugins automaticamente
  - Quando usar plugins vs comandos
  - Exemplos práticos

### Comparação
- [**Comparação de Abordagens**](./comparison.md) - Qual método usar e quando
  - Easy Commands vs Easy Plugins vs Traditional
  - Casos de uso
  - Métricas de decisão
  - Exemplos lado a lado

### Migração
- [**Migração de Loaders Customizados**](./migration_from_custom_loader.md) - Migrar código ofuscado
  - Passo a passo
  - Antes e depois
  - Troubleshooting

## 🎯 Interações (Novo!)

- [**Easy Interactions**](./easy_interactions.md) - Sistema estilo disnake
  - `EasyPlugin` - Plugin com suporte a interações
  - `@button()` - Decorator para botões
  - `@select_menu()` - Decorator para select menus
  - `@modal()` - Decorator para modals
  - Context simplificado
  - Regex para IDs dinâmicos
  - Auto-defer

## 📚 Comandos

- [**Options**](./options.md) - Parâmetros de comandos
- [**Command Groups**](./command_groups.md) - Grupos de comandos
- [**Context Menu**](./context_menu.md) - Comandos de contexto
- [**Typing**](./typing.md) - Type hints e validação

## 🔧 Features Avançadas

- [**Plugins & Extensions**](./plugins_extensions.md) - Sistema de plugins tradicional
- [**Dependency Injection**](./dependency_injection.md) - Injeção de dependências
- [**Error Handling**](./error_handling.md) - Tratamento de erros
- [**Hooks**](./hooks.md) - Lifecycle hooks
- [**Events**](./events.md) - Event handlers
- [**Loops**](./loops.md) - Tasks periódicas
- [**Concurrency Limiting**](./concurrency_limiting.md) - Controle de concorrência
- [**Startup & Shutdown**](./startup_shutdown.md) - Lifecycle do bot

## 📖 Exemplos

### Básicos
- [Easy Commands Example](../../examples/easy_commands_example/) - Auto-loading básico
- [Easy Plugins Example](../../examples/easy_plugins_example/) - Plugins com auto-loading

### Avançados
- [Complete Example](../../examples/complete_example/) - Todos os recursos combinados
- [Gateway Example](../../examples/gateway/) - Bot com gateway
- [REST Example](../../examples/rest/) - Bot REST-only

## 🆚 Comparações

| Você quer... | Use... | Guia |
|--------------|--------|------|
| Começar rápido | Easy Commands | [QUICKSTART](../../QUICKSTART.md) |
| Botões/Selects | Easy Plugins | [Easy Interactions](./easy_interactions.md) |
| Controle total | Traditional Plugins | [Plugins](./plugins_extensions.md) |
| Misturar tudo | Híbrido | [Complete Example](../../examples/complete_example/) |

## 🔄 Fluxo de Aprendizado Recomendado

1. **Iniciante**
   - [QUICKSTART](../../QUICKSTART.md)
   - [Easy Commands](./easy_commands.md)
   - [Easy Commands Example](../../examples/easy_commands_example/)

2. **Intermediário**
   - [Easy Interactions](./easy_interactions.md)
   - [Easy Plugins Example](../../examples/easy_plugins_example/)
   - [Comparison](./comparison.md)

3. **Avançado**
   - [Traditional Plugins](./plugins_extensions.md)
   - [Dependency Injection](./dependency_injection.md)
   - [Complete Example](../../examples/complete_example/)

4. **Expert**
   - [Hooks](./hooks.md)
   - [Concurrency Limiting](./concurrency_limiting.md)
   - [Custom Extensions](./plugins_extensions.md)

## 🆕 Features Exclusivas deste Fork

Estas features não existem no hikari-arc original:

- ✅ `load_commands()` - Auto-loading de comandos
- ✅ `load_events()` - Auto-loading de eventos
- ✅ `load_plugins()` - Auto-loading de plugins
- ✅ `load_all()` - Carrega tudo
- ✅ `EasyPlugin` - Sistema de interações simplificado
- ✅ `@button()` - Decorator para botões
- ✅ `@select_menu()` - Decorator para selects
- ✅ `@modal()` - Decorator para modals
- ✅ Documentação em Português
- ✅ Exemplos práticos completos

## 📝 Notas

- Todas as features são **opcionais** e **retrocompatíveis**
- Você pode misturar abordagens no mesmo bot
- O código original do hikari-arc continua funcionando
- Apenas adicionamos novas funcionalidades

## 🔗 Links Úteis

- [Repositório Original](https://github.com/hypergonial/hikari-arc)
- [Documentação Original](https://arc.hypergonial.com)
- [Discord do Hikari](https://discord.gg/hikari)
- [Hikari Docs](https://docs.hikari-py.dev/)

---

**Dica:** Comece pelo [QUICKSTART](../../QUICKSTART.md) e escolha o método que mais se adequa ao seu projeto!
