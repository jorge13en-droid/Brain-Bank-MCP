import os
import json
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 1. ONDE FICAM AS MEMÓRIAS?
# Aqui dizemos ao código onde estão as pastas que você criou
DATA_DIR = Path(__file__).parent.parent / "data"

# Inicializa o servidor MCP
server = Server("brain-bank")

# ------------------------------------
# FERRAMENTA 1: Lembrar (Ler Contexto)
# ------------------------------------
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="buscar_memoria",
            description="Busca uma memória salva em uma pasta específica do Brain Bank",
            inputSchema={
                "type": "object",
                "properties": {
                    "pasta": {"type": "string", "description": "Nome da pasta (ex: projetos)"},
                    "arquivo": {"type": "string", "description": "Nome do arquivo sem extensão"}
                },
                "required": ["pasta", "arquivo"]
            }
        ),
        Tool(
            name="listar_pastas",
            description="Lista todas as pastas de memórias disponíveis",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

# ------------------------------------
# EXECUÇÃO DAS FERRAMENTAS
# ------------------------------------
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "listar_pastas":
        pastas = [p.name for p in DATA_DIR.iterdir() if p.is_dir()]
        return [TextContent(type="text", text=f"📂 Pastas disponíveis: {', '.join(pastas)}")]

    elif name == "buscar_memoria":
        pasta = arguments.get("pasta")
        arquivo = arguments.get("arquivo")
        
        # Garantindo que ninguém acesse pastas proibidas do sistema
        caminho = (DATA_DIR / pasta / f"{arquivo}.md")
        
        if caminho.exists():
            conteudo = caminho.read_text(encoding="utf-8")
            return [TextContent(type="text", text=conteudo)]
        else:
            return [TextContent(type="text", text=f"❌ Memória '{arquivo}' não encontrada na pasta '{pasta}'.")]

# ------------------------------------
# INICIANDO O SERVIDOR
# ------------------------------------
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
