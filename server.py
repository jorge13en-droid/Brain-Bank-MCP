import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# 1. Inicializa o servidor usando o FastMCP (Formato Moderno)
mcp = FastMCP("brain-bank")

# 2. Define onde as pastas devem ser criadas
DATA_DIR = Path(__file__).parent.parent / "data"

# 3. Lista de pastas que o Brain Bank deve ter
PASTAS_PADRAO = [
    "projetos",
    "pessoas",
    "aprendizado",
    "ideias",
    "contexto",
    "instrucoes",
    "fonte"
]

# 4. Função que cria as pastas automaticamente se não existirem
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

# ------------------------------------
# FERRAMENTA 1: Listar Pastas
# ------------------------------------
@mcp.tool()
def listar_pastas() -> str:
    """Lista todas as pastas de memórias disponíveis no Brain Bank."""
    pastas = [p.name for p in DATA_DIR.iterdir() if p.is_dir()]
    return f"📂 Pastas disponíveis: {', '.join(pastas)}"

# ------------------------------------
# FERRAMENTA 2: Buscar (Ler) Memória
# ------------------------------------
@mcp.tool()
def buscar_memoria(pasta: str, arquivo: str) -> str:
    """Busca (lê) uma memória salva em uma pasta específica do Brain Bank.
    
    Args:
        pasta: Nome da pasta (ex: projetos)
        arquivo: Nome do arquivo sem extensão
    """
    # Proteção contra "Path Traversal"
    if pasta not in PASTAS_PADRAO:
        return f"🚫 Pasta inválida. Escolha uma de: {', '.join(PASTAS_PADRAO)}"
        
    caminho = (DATA_DIR / pasta / f"{arquivo}.md")
    
    if caminho.exists():
        return caminho.read_text(encoding="utf-8")
    else:
        return f"❌ Memória '{arquivo}' não encontrada na pasta '{pasta}'."

# ------------------------------------
# FERRAMENTA 3: Salvar (Escrever) Memória
# ------------------------------------
@mcp.tool()
def salvar_memoria(pasta: str, arquivo: str, conteudo: str) -> str:
    """Salva (escreve) uma nova memória ou atualiza uma existente no Brain Bank.
    
    Args:
        pasta: Nome da pasta (ex: projetos)
        arquivo: Nome do arquivo sem extensão
        conteudo: O texto completo da memória a ser salva
    """
    # Proteção contra "Path Traversal"
    if pasta not in PASTAS_PADRAO:
        return f"🚫 Pasta inválida. Escolha uma de: {', '.join(PASTAS_PADRAO)}"
    
    caminho = (DATA_DIR / pasta / f"{arquivo}.md")
    
    # Garante que a pasta existe
    caminho.parent.mkdir(parents=True, exist_ok=True)
    
    # Escreve o arquivo
    caminho.write_text(conteudo, encoding="utf-8")
    
    return f"✅ Memória '{arquivo}' salva com sucesso na pasta '{pasta}'!"

# ------------------------------------
# INICIANDO O SERVIDOR
# ------------------------------------
if __name__ == "__main__":
    mcp.run()
