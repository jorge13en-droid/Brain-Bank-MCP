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
- O repositorio E o plugin: `.mcp.json`, `skills/` e `plugin.json` ficam na
  raiz. O catalogo do Grok (xai-org/plugin-marketplace) so aceita fonte `url`
  apontando para a raiz do repo, sem subpasta - por isso nao usamos
  `plugins/<nome>/`. Nao mova esses arquivos para uma subpasta.
- O `.mcp.json` roda o servidor via `uvx brain-bank-mcp`: o plugin depende do
  pacote publicado no PyPI, nao do codigo desta pasta.
- `.claude-plugin/plugin.json` e o manifesto do Claude Code; `plugin.json` na
  raiz e o formato nativo do Grok. Mantenha os dois em sincronia.

## Regras

1. Logica nova vai em `storage.py` e precisa de teste. `server.py` so traduz
   chamadas MCP em chamadas de `MemoryStore`.
2. Nomes de arquivo passam sempre por `slugify()`. Nunca monte um caminho
   concatenando entrada do usuario direto.
3. Erros previsiveis usam `BrainBankError`; a camada MCP converte em texto.
4. Nunca versione `.env` nem memorias. O padrao de gravacao e `~/BrainBank`,
   fora do repositorio - nao mude isso para um caminho relativo ao codigo,
   porque some no cache do uvx a cada atualizacao.
5. Antes de commitar: `ruff check . && ruff format --check . && pytest`.
6. As ferramentas MCP tem nomes em portugues por decisao de produto. Mantenha.
   O mesmo vale para `INSTRUCTIONS` em server.py: e o texto que o modelo
   recebe ao conectar, e o que faz a IA usar a memoria sozinha. Ao mexer
   nele, so cite ferramentas que existem - ha teste checando isso.
7. Ao mexer na versao, edite so `src/brain_bank/__init__.py`: o `pyproject.toml`
   le dali. Mantenha em sincronia com `plugins/brain-bank/plugin.json`.
