"""Configuracao do Brain Bank, lida do ambiente com padroes seguros."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# Pastas padrao do Brain Bank e o proposito de cada uma.
# A descricao e usada nas respostas das ferramentas MCP para que a IA
# saiba onde procurar (e onde salvar) cada tipo de memoria.
FOLDERS: dict[str, str] = {
    "projetos": "Trabalhos e tarefas em andamento",
    "pessoas": "Contatos, times e relacionamentos",
    "aprendizado": "Licoes, artigos e conhecimento adquirido",
    "ideias": "Brainstorms e pensamentos criativos",
    "contexto": "Memoria de curto prazo: o que esta acontecendo agora",
    "instrucoes": "Regras, preferencias, tom de voz e estilo",
    "fonte": "Documentos brutos e material de referencia",
}

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DEFAULT_MAX_MEMORY_KB = 512


@dataclass(frozen=True)
class Settings:
    """Ajustes de execucao do servidor."""

    data_dir: Path
    max_memory_bytes: int

    @classmethod
    def from_env(cls) -> Settings:
        raw_dir = os.getenv("BRAIN_BANK_DATA_DIR", "").strip()
        data_dir = Path(raw_dir).expanduser().resolve() if raw_dir else DEFAULT_DATA_DIR

        raw_kb = os.getenv("BRAIN_BANK_MAX_MEMORY_KB", "").strip()
        try:
            max_kb = int(raw_kb) if raw_kb else DEFAULT_MAX_MEMORY_KB
        except ValueError:
            max_kb = DEFAULT_MAX_MEMORY_KB
        max_kb = max(1, max_kb)

        return cls(data_dir=data_dir, max_memory_bytes=max_kb * 1024)
