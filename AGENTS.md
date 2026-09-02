# Instrucoes para agentes de IA

Contexto rapido para qualquer agente (Claude Code, Cowork, Codex, Copilot)
que for editar este repositorio.

## O que e este projeto

Servidor MCP em Python que guarda memorias em markdown dentro de `data/`.
Nao ha frontend neste repositorio.

## Estrutura

- `src/brain_bank/config.py` - pastas padrao e configuracao via ambiente.
- `src/brain_bank/storage.py` - toda a logica de disco. **Sem dependencia de MCP.**
- `src/brain_bank/server.py` - apenas a camada MCP (as ferramentas `@mcp.tool()`).
- `tests/` - pytest, sem tocar em disco real (usa `tmp_path`).
- `server.py` na raiz - atalho de compatibilidade, nao coloque logica ali.

## Regras

1. Logica nova vai em `storage.py` e precisa de teste. `server.py` so traduz
   chamadas MCP em chamadas de `MemoryStore`.
2. Nomes de arquivo passam sempre por `slugify()`. Nunca monte um caminho
   concatenando entrada do usuario direto.
3. Erros previsiveis usam `BrainBankError`; a camada MCP converte em texto.
4. Nunca versione `.env` nem o conteudo de `data/` - sao dados pessoais.
5. Antes de commitar: `ruff check . && ruff format --check . && pytest`.
6. As ferramentas MCP tem nomes em portugues por decisao de produto. Mantenha.
