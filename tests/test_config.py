"""Testes da configuracao lida do ambiente."""

from __future__ import annotations

from pathlib import Path

from brain_bank.config import DEFAULT_MAX_MEMORY_KB, Settings


def test_padrao_grava_na_pasta_do_usuario(monkeypatch):
    """O padrao nao pode ficar ao lado do codigo: some no cache do uvx."""
    monkeypatch.delenv("BRAIN_BANK_DATA_DIR", raising=False)
    monkeypatch.delenv("BRAIN_BANK_MAX_MEMORY_KB", raising=False)

    settings = Settings.from_env()
    assert settings.data_dir == Path.home() / "BrainBank"
    assert settings.max_memory_bytes == DEFAULT_MAX_MEMORY_KB * 1024


def test_data_dir_do_ambiente(monkeypatch, tmp_path):
    monkeypatch.setenv("BRAIN_BANK_DATA_DIR", str(tmp_path / "memorias"))
    assert Settings.from_env().data_dir == (tmp_path / "memorias").resolve()


def test_limite_do_ambiente(monkeypatch):
    monkeypatch.setenv("BRAIN_BANK_MAX_MEMORY_KB", "64")
    assert Settings.from_env().max_memory_bytes == 64 * 1024


def test_limite_invalido_cai_no_padrao(monkeypatch):
    monkeypatch.setenv("BRAIN_BANK_MAX_MEMORY_KB", "nao-e-numero")
    assert Settings.from_env().max_memory_bytes == DEFAULT_MAX_MEMORY_KB * 1024


def test_limite_zero_vira_um_kb(monkeypatch):
    monkeypatch.setenv("BRAIN_BANK_MAX_MEMORY_KB", "0")
    assert Settings.from_env().max_memory_bytes == 1024
