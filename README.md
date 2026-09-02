<div align="center">

# 🧠 Brain Bank MCP

**Nunca mais comece uma conversa com IA do zero.**

Memória persistente para qualquer modelo, via [Model Context Protocol](https://modelcontextprotocol.io).

[![CI](https://github.com/jorge13en-droid/Brain-Bank-MCP/actions/workflows/ci.yml/badge.svg)](https://github.com/jorge13en-droid/Brain-Bank-MCP/actions/workflows/ci.yml)
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
              data/*.md  (seus arquivos, no seu disco)
```

Sem banco de dados. Sem nuvem. Sem lock-in — é uma pasta de markdown.

---

## Instalação

```bash
git clone https://github.com/jorge13en-droid/Brain-Bank-MCP.git
cd Brain-Bank-MCP

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -e .
```

Requer **Python 3.10+**. Compatível com o SDK `mcp` 1.x (`FastMCP`) e 2.x (`MCPServer`).

### Conectando ao Claude Desktop

Abra `claude_desktop_config.json` e adicione:

```json
{
  "mcpServers": {
    "brain-bank": {
      "command": "C:/caminho/para/Brain-Bank-MCP/venv/Scripts/python.exe",
      "args": ["-m", "brain_bank"],
      "cwd": "C:/caminho/para/Brain-Bank-MCP"
    }
  }
}
```

O arquivo fica em:

| Sistema | Caminho |
| ------- | ------- |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS   | `~/Library/Application Support/Claude/claude_desktop_config.json` |

Em macOS ou Linux, troque `venv/Scripts/python.exe` por `venv/bin/python`.

Reinicie o Claude Desktop. O ícone de ferramentas deve mostrar `brain-bank`.

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
| `BRAIN_BANK_DATA_DIR` | `./data` | Onde as memórias são gravadas |
| `BRAIN_BANK_MAX_MEMORY_KB` | `512` | Tamanho máximo de uma memória |

---

## Privacidade

- **O conteúdo de `data/` não é versionado.** O `.gitignore` mantém só a
  estrutura de pastas — suas memórias nunca sobem para o GitHub por acidente.
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
├── data/                      # suas memórias (conteúdo ignorado pelo git)
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
