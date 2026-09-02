import os
import json
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 1. Define onde as pastas devem ser criadas
DATA_DIR = Path(__file__).parent.parent / "data"

# 2. Lista de pastas que o Brain Bank deve ter
PASTAS_PADRAO = [
    "projetos",
    "pessoas",
    "aprendizado",
    "ideias",
    "contexto",
    "instrucoes",
    "fonte"
]

# 3. Função que cria as pastas automaticamente se não existirem
def criar_pastas_automaticamente():
    print("🧠 Verificando pastas do Brain Bank...")
    for pasta in PASTAS_PADRAO:
        caminho_pasta = DATA_DIR / pasta
        if not caminho_pasta.exists():
            caminho_pasta.mkdir(parents=True, exist_ok=True)
            # Cria um arquivo de exemplo para o GitHub não apagar a pasta
            (caminho_pasta / "README.md").write_text(f"# {pasta.capitalize()}", encoding="utf-8")
            print(f"✅ Pasta criada: {pasta}")
        else:
            print(f"📂 Pasta encontrada: {pasta}")

# Chama a função assim que o servidor ligar
criar_pastas_automaticamente()

# Inicializa o servidor MCP
server = Server("brain-bank")

# ------------------------------------
# LISTA DE FERRAMENTAS (O que a IA pode fazer)
# ------------------------------------
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="buscar_memoria",
            description="Busca (lê) uma memória salva em uma pasta específica do Brain Bank",
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
            name="salvar_memoria",
            description="Salva (escreve) uma nova memória ou atualiza uma existente no Brain Bank",
            inputSchema={
                "type": "object",
                "properties": {
                    "pasta": {"type": "string", "description": "Nome da pasta (ex: projetos)"},
                    "arquivo": {"type": "string", "description": "Nome do arquivo sem extensão"},
                    "conteudo": {"type": "string", "description": "O texto completo da memória a ser salva"}
                },
                "required": ["pasta", "arquivo", "conteudo"]
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
    
    # FERRAMENTA: Listar Pastas
    if name == "listar_pastas":
        pastas = [p.name for p in DATA_DIR.iterdir() if p.is_dir()]
        return [TextContent(type="text", text=f"📂 Pastas disponíveis: {', '.join(pastas)}")]

    # FERRAMENTA: Buscar (Ler) Memória
    elif name == "buscar_memoria":
        pasta = arguments.get("pasta")
        arquivo = arguments.get("arquivo")
        
        # Proteção contra "Path Traversal" (tentativa de acessar pastas do sistema)
        if pasta not in PASTAS_PADRAO:
            return [TextContent(type="text", text=f"🚫 Pasta inválida. Escolha uma de: {', '.join(PASTAS_PADRAO)}")]
            
        caminho = (DATA_DIR / pasta / f"{arquivo}.md")
        
        if caminho.exists():
            conteudo = caminho.read_text(encoding="utf-8")
            return [TextContent(type="text", text=conteudo)]
        else:
            return [TextContent(type="text", text=f"❌ Memória '{arquivo}' não encontrada na pasta '{pasta}'.")]

    # FERRAMENTA: Salvar (Escrever) Memória
    elif name == "salvar_memoria":
        pasta = arguments.get("pasta")
        arquivo = arguments.get("arquivo")
        conteudo = arguments.get("conteudo")
        
        # Proteção contra "Path Traversal"
        if pasta not in PASTAS_PADRAO:
            return [TextContent(type="text", text=f"🚫 Pasta inválida. Escolha uma de: {', '.join(PASTAS_PADRAO)}")]
        
        caminho = (DATA_DIR / pasta / f"{arquivo}.md")
        
        # Garante que a pasta existe (caso tenham apagado)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        
        # Escreve o arquivo
        caminho.write_text(conteudo, encoding="utf-8")
        
        return [TextContent(type="text", text=f"✅ Memória '{arquivo}' salva com sucesso na pasta '{pasta}'!")]

    else:
        return [TextContent(type="text", text="❌ Ferramenta desconhecida.")]

# ------------------------------------
# INICIANDO O SERVIDOR
# ------------------------------------
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
