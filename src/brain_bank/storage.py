"""Camada de armazenamento do Brain Bank.

Toda a logica de disco vive aqui, sem nenhuma dependencia de MCP.
Isso mantem o modulo facil de testar e permite reaproveitar o Brain Bank
em outros contextos (CLI, API HTTP, scripts).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .config import FOLDERS, Settings

_SLUG_INVALID = re.compile(r"[^a-z0-9._-]+")
_SLUG_TRIM = re.compile(r"^[-._]+|[-._]+$")


class BrainBankError(Exception):
    """Erro previsivel de uso, com mensagem propria para o usuario final."""


@dataclass(frozen=True)
class MemoryInfo:
    """Metadados de uma memoria, sem carregar o conteudo."""

    folder: str
    name: str
    size_bytes: int
    updated_at: datetime

    @property
    def updated_label(self) -> str:
        return self.updated_at.strftime("%Y-%m-%d %H:%M")


def slugify(value: str) -> str:
    """Converte um titulo livre em um nome de arquivo seguro.

    'Reuniao com a Ana!' -> 'reuniao-com-a-ana'
    """
    normalized = unicodedata.normalize("NFKD", value)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    slug = _SLUG_INVALID.sub("-", ascii_only.strip().lower())
    slug = _SLUG_TRIM.sub("", slug)
    return slug


class MemoryStore:
    """Le e escreve memorias em markdown dentro de `data/<pasta>/`."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings.from_env()
        self.root = self.settings.data_dir

    # ----------------------------------------------------------------
    # Estrutura
    # ----------------------------------------------------------------
    def ensure_structure(self) -> list[str]:
        """Cria as pastas padrao que ainda nao existem. Idempotente."""
        created: list[str] = []
        for folder in FOLDERS:
            path = self.root / folder
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                (path / ".gitkeep").touch()
                created.append(folder)
        return created

    def folders(self) -> list[str]:
        if not self.root.exists():
            return []
        return sorted(p.name for p in self.root.iterdir() if p.is_dir())

    # ----------------------------------------------------------------
    # Validacao (defesa contra path traversal)
    # ----------------------------------------------------------------
    def _folder_path(self, folder: str) -> Path:
        if folder not in FOLDERS:
            valid = ", ".join(FOLDERS)
            raise BrainBankError(f"Pasta invalida: '{folder}'. Use uma de: {valid}.")
        return self.root / folder

    def _memory_path(self, folder: str, name: str) -> Path:
        base = self._folder_path(folder)
        slug = slugify(name)
        if not slug:
            raise BrainBankError(
                f"Nome de memoria invalido: '{name}'. Use letras, numeros ou hifens."
            )

        path = (base / f"{slug}.md").resolve()
        # Mesmo com o slug, confirmamos que o caminho final nao escapou da pasta.
        if base.resolve() not in path.parents:
            raise BrainBankError(f"Caminho recusado por seguranca: '{name}'.")
        return path

    # ----------------------------------------------------------------
    # Operacoes
    # ----------------------------------------------------------------
    def list_memories(self, folder: str) -> list[MemoryInfo]:
        base = self._folder_path(folder)
        if not base.exists():
            return []

        items: list[MemoryInfo] = []
        for path in sorted(base.glob("*.md")):
            stat = path.stat()
            items.append(
                MemoryInfo(
                    folder=folder,
                    name=path.stem,
                    size_bytes=stat.st_size,
                    updated_at=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
                )
            )
        return items

    def read(self, folder: str, name: str) -> str:
        path = self._memory_path(folder, name)
        if not path.exists():
            raise BrainBankError(f"Memoria '{slugify(name)}' nao encontrada em '{folder}'.")
        return path.read_text(encoding="utf-8")

    def write(self, folder: str, name: str, content: str) -> MemoryInfo:
        encoded = content.encode("utf-8")
        limit = self.settings.max_memory_bytes
        if len(encoded) > limit:
            raise BrainBankError(
                f"Memoria grande demais: {len(encoded) // 1024} KB (limite {limit // 1024} KB)."
            )

        path = self._memory_path(folder, name)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Escrita atomica: grava em um temporario e troca, para que uma
        # interrupcao nunca deixe a memoria pela metade.
        tmp = path.with_suffix(".md.tmp")
        tmp.write_text(content, encoding="utf-8")
        tmp.replace(path)

        stat = path.stat()
        return MemoryInfo(
            folder=folder,
            name=path.stem,
            size_bytes=stat.st_size,
            updated_at=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
        )

    def delete(self, folder: str, name: str) -> None:
        path = self._memory_path(folder, name)
        if not path.exists():
            raise BrainBankError(f"Memoria '{slugify(name)}' nao encontrada em '{folder}'.")
        path.unlink()

    def search(
        self, query: str, folder: str | None = None, limit: int = 20
    ) -> list[tuple[MemoryInfo, str]]:
        """Busca `query` no nome e no conteudo das memorias.

        Retorna pares (metadados, trecho) ordenados por data de alteracao.
        """
        term = query.strip().lower()
        if not term:
            raise BrainBankError("Informe um termo de busca.")

        folders = [folder] if folder else list(FOLDERS)
        results: list[tuple[MemoryInfo, str]] = []

        for name in folders:
            for info in self.list_memories(name):
                path = self._memory_path(name, info.name)
                try:
                    text = path.read_text(encoding="utf-8")
                except OSError:
                    continue

                haystack = f"{info.name}\n{text}".lower()
                if term not in haystack:
                    continue

                results.append((info, _excerpt(text, term)))

        results.sort(key=lambda pair: pair[0].updated_at, reverse=True)
        return results[:limit]


def _excerpt(text: str, term: str, width: int = 160) -> str:
    """Devolve um trecho curto ao redor da primeira ocorrencia do termo."""
    lowered = text.lower()
    pos = lowered.find(term)
    if pos == -1:
        return text.strip()[:width]

    start = max(0, pos - width // 2)
    end = min(len(text), pos + width // 2)
    snippet = text[start:end].replace("\n", " ").strip()
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(text) else ""
    return f"{prefix}{snippet}{suffix}"
