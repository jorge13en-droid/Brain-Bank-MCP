"""Servidor MCP do Brain Bank.

Expoe as memorias em `data/` como ferramentas MCP, para que qualquer
cliente compativel (Claude Desktop, Cowork, agentes proprios) consiga
ler e gravar contexto persistente.
"""

from __future__ import annotations

try:  # mcp >= 2.0: FastMCP virou MCPServer
    from mcp.server.mcpserver import MCPServer as _Server
except ImportError:  # mcp < 2.0
    from mcp.server.fastmcp import FastMCP as _Server

from .config import FOLDERS
from .storage import BrainBankError, MemoryStore, slugify

# Instrucoes entregues ao modelo no momento em que ele conecta. E isso que
# faz a IA usar a memoria por conta propria, em vez de so quando mandam.
INSTRUCTIONS = """\
Este servidor e a memoria de longo prazo do usuario: arquivos markdown que
persistem entre conversas. Ele existe para que o usuario nao precise
reexplicar as mesmas coisas toda vez.

RECUPERAR. Antes de dizer que nao sabe algo sobre o usuario, use `procurar`.
Quando ele se referir a algo que contou antes ("aquele cliente", "o projeto
que te falei"), procure primeiro. Use a memoria para melhorar a resposta, sem
anunciar a cada frase que consultou.

CAPTURAR. Ao longo da conversa, identifique informacoes duraveis sobre o
usuario - decisoes, preferencias, restricoes, fatos estaveis, licoes - e
salve com `salvar_memoria` sem interromper o assunto. Nao pergunte a cada
frase se deve salvar. Agrupe por assunto em vez de criar memorias soltas.

NAO SALVE assuntos passageiros, rascunhos, dados que mudam em dias, o que ja
esta no Brain Bank, nem senhas, chaves de API ou numeros de cartao. Se nao
houver nada duravel, nao salve nada.

CUIDADOS. `salvar_memoria` substitui o conteudo anterior: para acrescentar,
leia com `buscar_memoria`, junte e salve o texto completo. Escreva memorias
autossuficientes - quem ler daqui a seis meses, sem esta conversa, tem que
entender. Nunca invente memorias: so afirme o que veio de uma ferramenta.
`apagar_memoria` e definitivo, confirme antes.
"""

mcp = _Server("brain-bank", instructions=INSTRUCTIONS)
store = MemoryStore()
store.ensure_structure()


@mcp.tool()
def listar_pastas() -> str:
    """Lista as pastas de memoria do Brain Bank e para que serve cada uma.

    Use esta ferramenta primeiro, quando nao souber onde procurar ou salvar.
    """
    linhas = [f"- {nome}: {descricao}" for nome, descricao in FOLDERS.items()]
    return "Pastas do Brain Bank:\n" + "\n".join(linhas)


@mcp.tool()
def listar_memorias(pasta: str) -> str:
    """Lista as memorias salvas em uma pasta, com data da ultima alteracao.

    Args:
        pasta: Nome da pasta (ex: projetos).
    """
    try:
        itens = store.list_memories(pasta)
    except BrainBankError as erro:
        return str(erro)

    if not itens:
        return f"A pasta '{pasta}' esta vazia."

    linhas = [
        f"- {item.name} ({item.size_bytes} bytes, alterado em {item.updated_label} UTC)"
        for item in itens
    ]
    return f"Memorias em '{pasta}':\n" + "\n".join(linhas)


@mcp.tool()
def buscar_memoria(pasta: str, arquivo: str) -> str:
    """Le o conteudo completo de uma memoria especifica.

    Args:
        pasta: Nome da pasta (ex: projetos).
        arquivo: Nome da memoria, sem a extensao .md.
    """
    try:
        return store.read(pasta, arquivo)
    except BrainBankError as erro:
        return str(erro)


@mcp.tool()
def salvar_memoria(pasta: str, arquivo: str, conteudo: str) -> str:
    """Cria ou atualiza uma memoria em markdown.

    Args:
        pasta: Nome da pasta (ex: projetos).
        arquivo: Nome da memoria, sem a extensao .md.
        conteudo: Texto completo da memoria. Substitui o conteudo anterior.
    """
    try:
        info = store.write(pasta, arquivo, conteudo)
    except BrainBankError as erro:
        return str(erro)
    return f"Memoria '{info.name}' salva em '{info.folder}' ({info.size_bytes} bytes)."


@mcp.tool()
def procurar(termo: str, pasta: str | None = None) -> str:
    """Procura um termo no nome e no conteudo das memorias.

    Args:
        termo: Palavra ou frase a procurar.
        pasta: Opcional. Limita a busca a uma unica pasta.
    """
    try:
        resultados = store.search(termo, folder=pasta)
    except BrainBankError as erro:
        return str(erro)

    if not resultados:
        escopo = f"na pasta '{pasta}'" if pasta else "no Brain Bank"
        return f"Nenhuma memoria com '{termo}' {escopo}."

    linhas = [
        f"- {info.folder}/{info.name} ({info.updated_label} UTC)\n  {trecho}"
        for info, trecho in resultados
    ]
    return f"{len(resultados)} resultado(s) para '{termo}':\n" + "\n".join(linhas)


@mcp.tool()
def apagar_memoria(pasta: str, arquivo: str) -> str:
    """Apaga uma memoria em definitivo. Use com cuidado.

    Args:
        pasta: Nome da pasta (ex: projetos).
        arquivo: Nome da memoria, sem a extensao .md.
    """
    try:
        store.delete(pasta, arquivo)
    except BrainBankError as erro:
        return str(erro)
    return f"Memoria '{slugify(arquivo)}' apagada de '{pasta}'."


def main() -> None:
    """Ponto de entrada do servidor (transporte stdio)."""
    mcp.run()


if __name__ == "__main__":
    main()
