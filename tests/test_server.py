"""Testes da camada MCP: garante que as ferramentas continuam registradas."""

from __future__ import annotations

import asyncio

from brain_bank import server

FERRAMENTAS_ESPERADAS = {
    "listar_pastas",
    "listar_memorias",
    "buscar_memoria",
    "salvar_memoria",
    "procurar",
    "apagar_memoria",
}


def _nomes_das_ferramentas() -> set[str]:
    return {tool.name for tool in asyncio.run(server.mcp.list_tools())}


def test_todas_as_ferramentas_estao_registradas():
    assert _nomes_das_ferramentas() == FERRAMENTAS_ESPERADAS


def test_toda_ferramenta_tem_descricao():
    for tool in asyncio.run(server.mcp.list_tools()):
        assert tool.description, f"{tool.name} esta sem docstring"


def test_listar_pastas_descreve_cada_pasta():
    saida = server.listar_pastas()
    for pasta in ("projetos", "pessoas", "instrucoes"):
        assert pasta in saida


def test_erro_de_pasta_invalida_vira_texto_amigavel():
    saida = server.buscar_memoria("financeiro", "qualquer")
    assert "Pasta invalida" in saida


def test_servidor_entrega_instrucoes_ao_modelo():
    """Sem isso a IA so usa a memoria quando mandam explicitamente."""
    instrucoes = server.mcp.instructions
    assert instrucoes, "o servidor precisa expor instructions"
    for trecho in ("procurar", "salvar_memoria", "substitui o conteudo"):
        assert trecho in instrucoes


def test_instrucoes_citam_so_ferramentas_que_existem():
    citadas = {nome for nome in FERRAMENTAS_ESPERADAS if f"`{nome}`" in server.mcp.instructions}
    assert citadas, "as instrucoes deveriam citar ferramentas pelo nome"
    assert citadas <= FERRAMENTAS_ESPERADAS
