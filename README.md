<div align="center">

<img src="imagens/brain-bank-banner.jpg" alt="Brain Bank" width="620">

# Brain Bank MCP

**Nunca mais comece uma conversa com IA do zero.**

Memória persistente para qualquer modelo, via [Model Context Protocol](https://modelcontextprotocol.io).

[![CI](https://github.com/jorge13en-droid/Brain-Bank-MCP/actions/workflows/ci.yml/badge.svg)](https://github.com/jorge13en-droid/Brain-Bank-MCP/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/brain-bank-mcp.svg)](https://pypi.org/project/brain-bank-mcp/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-compatible-8A2BE2.svg)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

</div>

---

## O problema

Toda conversa nova com uma IA é uma página em branco. Você reexplica o mesmo
projeto, as mesmas preferências, as mesmas decisões — todo santo dia.

## A solução

O Brain Bank guarda esse contexto uma única vez, em arquivos markdown que você
controla, e o entrega para qualquer IA compatível com MCP. A IA lê e escreve
memórias sozinha, no meio da conversa.

```
Você  ──▶  Claude / Cowork / agente próprio
                      │  (MCP, stdio)
                      ▼
              Brain Bank MCP
                      │
                      ▼
        ~/BrainBank/*.md  (seus arquivos, no seu disco)
```

Sem banco de dados. Sem nuvem. Sem lock-in — é uma pasta de markdown.

### Prefere na nuvem?

Existe uma versão web do Brain Bank, com interface, busca e uma fila de
aprovação para revisar o que a IA quis guardar antes de entrar no cofre:
**[ai-brain-share.lovable.app](https://ai-brain-share.lovable.app)**.

Os dois são independentes — este repositório é a versão local, em que os
arquivos ficam na sua máquina e ninguém mais toca neles. Escolha pelo que
importa mais para você: controle total ou acesso de qualquer lugar.

---

## Instalação

Requer **Python 3.10+**. Compatível com o SDK `mcp` 1.x (`FastMCP`) e 2.x (`MCPServer`).

### Opção 1 — plugin (mais rápido)

No Claude Code:

```
/plugin marketplace add jorge13en-droid/Brain-Bank-MCP
/plugin install brain-bank@brain-bank
```

No Grok Build:

```bash
grok plugin marketplace add jorge13en-droid/Brain-Bank-MCP
grok plugin install brain-bank --trust
```

O plugin traz o servidor MCP e uma skill que ensina a IA a usar as memórias.
Requer o [uv](https://docs.astral.sh/uv/) instalado — é ele que baixa e roda o
servidor, sem clone e sem `pip install`.

### Opção 2 — Claude Desktop

Abra `claude_desktop_config.json` e adicione:

```json
{
  "mcpServers": {
    "brain-bank": {
      "command": "uvx",
      "args": ["brain-bank-mcp"]
    }
  }
}
```

O arquivo fica em:

| Sistema | Caminho |
| ------- | ------- |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS   | `~/Library/Application Support/Claude/claude_desktop_config.json` |

Reinicie o Claude Desktop. O ícone de ferramentas deve mostrar `brain-bank`.

Sem o `uv`? Use `pipx install brain-bank-mcp` e troque o comando por
`brain-bank-mcp`, sem `args`.

### Opção 3 — do código-fonte

```bash
git clone https://github.com/jorge13en-droid/Brain-Bank-MCP.git
cd Brain-Bank-MCP

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -e .
```

E aponte a configuração para o python do venv:

```json
{
  "mcpServers": {
    "brain-bank": {
      "command": "/caminho/para/Brain-Bank-MCP/venv/bin/python",
      "args": ["-m", "brain_bank"]
    }
  }
}
```

No Windows, `venv\Scripts\python.exe`.

---

## Onde ficam as memórias

Em **`~/BrainBank`** — na sua pasta de usuário, não junto do código. Assim elas
sobrevivem a atualizações, reinstalações e à troca de máquina, e você pode fazer
backup ou versionar essa pasta num repositório privado seu.

Para usar outro lugar, defina `BRAIN_BANK_DATA_DIR`.

---

## Ferramentas MCP

| Ferramenta | O que faz |
| ---------- | --------- |
| `listar_pastas` | Mostra as pastas de memória e o propósito de cada uma |
| `listar_memorias` | Lista o que existe em uma pasta, com data de alteração |
| `buscar_memoria` | Lê o conteúdo completo de uma memória |
| `salvar_memoria` | Cria ou atualiza uma memória (escrita atômica) |
| `procurar` | Busca um termo no nome **e** no conteúdo de todas as memórias |
| `apagar_memoria` | Remove uma memória em definitivo |

O servidor entrega ao modelo, na conexão, um conjunto de instruções sobre
**quando** usar cada ferramenta. É isso que faz a IA procurar antes de dizer
que não sabe, e guardar o que é durável por conta própria — em vez de só agir
quando você pede. Está em `INSTRUCTIONS`, em `src/brain_bank/server.py`.

### Na prática

> **Você:** salva no Brain Bank que o cliente Acme aprovou o escopo, prazo 15/03
>
> **IA:** *(chama `salvar_memoria("projetos", "acme", ...)`)* Memória 'acme' salva em 'projetos'.

Semanas depois, em outra conversa:

> **Você:** qual era o prazo da Acme mesmo?
>
> **IA:** *(chama `procurar("acme")`)* 15/03 — o escopo foi aprovado.

---

## Pastas de memória

| Pasta | Para que serve |
| ----- | -------------- |
| `projetos` | Trabalhos e tarefas em andamento |
| `pessoas` | Contatos, times e relacionamentos |
| `aprendizado` | Lições, artigos e conhecimento adquirido |
| `ideias` | Brainstorms e pensamentos criativos |
| `contexto` | Memória de curto prazo: o que está acontecendo agora |
| `instrucoes` | Regras, preferências, tom de voz e estilo |
| `fonte` | Documentos brutos e material de referência |

As pastas são criadas automaticamente na primeira execução.

---

## Configuração

Copie `.env.example` para `.env`. Todas as variáveis são opcionais.

| Variável | Padrão | Descrição |
| -------- | ------ | --------- |
| `BRAIN_BANK_DATA_DIR` | `~/BrainBank` | Onde as memórias são gravadas |
| `BRAIN_BANK_MAX_MEMORY_KB` | `512` | Tamanho máximo de uma memória |

---

## Privacidade

- **As memórias ficam fora do repositório**, em `~/BrainBank`. Não há como
  subirem para o GitHub por acidente, e o `.gitignore` ainda bloqueia `data/`
  como rede de segurança para quem apontar `BRAIN_BANK_DATA_DIR` para lá.
- **`.env` não é versionado.** Use `.env.example` como referência.
- Nomes de arquivo passam por `slugify()` antes de virarem caminho, então
  entrada como `../../etc/passwd` não escapa da pasta de dados. Há teste para isso.

---

## Estrutura do projeto

```
Brain-Bank-MCP/
├── .github/workflows/ci.yml   # lint + testes em 3.10, 3.11 e 3.12
├── src/brain_bank/
│   ├── config.py              # pastas padrão e configuração
│   ├── storage.py             # lógica de disco (sem dependência de MCP)
│   └── server.py              # camada MCP: as ferramentas
├── tests/                     # pytest
├── plugins/brain-bank/        # o plugin (Claude Code e Grok Build)
├── .claude-plugin/            # marketplace.json, para instalar do GitHub
├── server.py                  # atalho: python server.py
└── pyproject.toml
```

A separação entre `storage.py` e `server.py` é proposital: a lógica é testável
sem subir servidor nenhum, e pode ser reaproveitada em CLI ou API.

---

## Desenvolvimento

```bash
pip install -e ".[dev]"

ruff check .          # lint
ruff format .         # formatação
pytest                # testes
```

Veja [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Roadmap

- [ ] Busca semântica (embeddings) além da busca textual
- [ ] Tags e relações entre memórias
- [ ] Importação de PDFs e documentos para `fonte`
- [ ] Transporte HTTP/SSE, além de stdio

---

## Licença

[MIT](LICENSE) © Jorge
