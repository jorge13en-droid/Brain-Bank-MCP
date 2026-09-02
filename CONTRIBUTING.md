# Como contribuir

## Ambiente

```bash
git clone https://github.com/jorge13en-droid/Brain-Bank-MCP.git
cd Brain-Bank-MCP

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -e ".[dev]"
cp .env.example .env
```

## Antes de abrir um PR

```bash
ruff check .
ruff format --check .
pytest
```

O CI roda exatamente esses tres comandos em Python 3.10, 3.11 e 3.12.

## Padroes

- Toda logica nova em `src/brain_bank/storage.py`, com teste em `tests/`.
- Commits curtos e no imperativo: `Adiciona busca por conteudo`.
- Nao inclua `.env` nem arquivos de `data/` no commit.

## Reportando um problema

Abra uma [issue](https://github.com/jorge13en-droid/Brain-Bank-MCP/issues)
com o passo a passo para reproduzir, o que voce esperava e o que aconteceu.
