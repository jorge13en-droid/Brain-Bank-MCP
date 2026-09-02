"""Testes da camada de armazenamento do Brain Bank."""

from __future__ import annotations

import pytest

from brain_bank.config import Settings
from brain_bank.storage import BrainBankError, MemoryStore, slugify


@pytest.fixture()
def store(tmp_path):
    settings = Settings(data_dir=tmp_path / "data", max_memory_bytes=4096)
    store = MemoryStore(settings)
    store.ensure_structure()
    return store


def test_ensure_structure_cria_todas_as_pastas(store):
    assert store.folders() == [
        "aprendizado",
        "contexto",
        "fonte",
        "ideias",
        "instrucoes",
        "pessoas",
        "projetos",
    ]


def test_ensure_structure_e_idempotente(store):
    assert store.ensure_structure() == []


@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("Reuniao com a Ana!", "reuniao-com-a-ana"),
        ("  Plano 2026  ", "plano-2026"),
        ("Ideia/Nova", "ideia-nova"),
        ("acentuacao ficticia", "acentuacao-ficticia"),
    ],
)
def test_slugify(entrada, esperado):
    assert slugify(entrada) == esperado


def test_write_e_read(store):
    info = store.write("projetos", "Brain Bank", "# Notas\nPrimeira memoria.")
    assert info.name == "brain-bank"
    assert store.read("projetos", "Brain Bank") == "# Notas\nPrimeira memoria."


def test_write_sobrescreve(store):
    store.write("ideias", "teste", "v1")
    store.write("ideias", "teste", "v2")
    assert store.read("ideias", "teste") == "v2"
    assert len(store.list_memories("ideias")) == 1


def test_read_de_memoria_inexistente(store):
    with pytest.raises(BrainBankError, match="nao encontrada"):
        store.read("projetos", "fantasma")


def test_pasta_invalida_e_recusada(store):
    with pytest.raises(BrainBankError, match="Pasta invalida"):
        store.write("financeiro", "x", "y")


def test_path_traversal_no_nome_do_arquivo(store):
    """O nome vira slug, entao '../..' nunca escapa da pasta de dados."""
    info = store.write("projetos", "../../segredo", "conteudo")
    assert info.name == "segredo"
    assert (store.root / "projetos" / "segredo.md").exists()
    assert not (store.root.parent / "segredo.md").exists()


def test_nome_vazio_e_recusado(store):
    with pytest.raises(BrainBankError, match="invalido"):
        store.write("projetos", "///", "conteudo")


def test_limite_de_tamanho(store):
    with pytest.raises(BrainBankError, match="grande demais"):
        store.write("fonte", "gigante", "x" * 5000)


def test_delete(store):
    store.write("contexto", "hoje", "reuniao as 10h")
    store.delete("contexto", "hoje")
    assert store.list_memories("contexto") == []


def test_delete_de_memoria_inexistente(store):
    with pytest.raises(BrainBankError, match="nao encontrada"):
        store.delete("contexto", "fantasma")


def test_search_encontra_por_conteudo(store):
    store.write("projetos", "alpha", "o cliente pediu um dashboard")
    store.write("projetos", "beta", "nada a ver")

    resultados = store.search("dashboard")
    assert len(resultados) == 1
    info, trecho = resultados[0]
    assert info.name == "alpha"
    assert "dashboard" in trecho


def test_search_encontra_por_nome(store):
    store.write("pessoas", "ana-souza", "contato do time")
    assert len(store.search("ana")) == 1


def test_search_limitada_a_uma_pasta(store):
    store.write("projetos", "alpha", "prazo curto")
    store.write("ideias", "beta", "prazo curto")

    assert len(store.search("prazo")) == 2
    assert len(store.search("prazo", folder="ideias")) == 1


def test_search_com_termo_vazio(store):
    with pytest.raises(BrainBankError, match="termo de busca"):
        store.search("   ")
