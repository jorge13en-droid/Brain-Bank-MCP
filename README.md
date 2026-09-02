# 🧠 Brain Bank MCP

**Nunca mais comece uma conversa com IA do zero.**

O Brain Bank é um servidor de **Model Context Protocol (MCP)** que funciona como uma memória persistente para Inteligências Artificiais. Em vez de explicar tudo de novo a cada nova conversa, você salva suas informações uma única vez e as injeta como contexto em qualquer IA.

---

## 🤔 O Problema
Hoje, ao usar IAs, enfrentamos a "amnésia digital". Cada conversa nova é uma página em branco. Perdemos tempo reexplicando projetos, gostos, decisões e aprendizados.

## 💡 A Solução
O Brain Bank resolve isso. Ele organiza suas memórias em **pastas estruturadas** e as disponibiliza para qualquer IA compatível com MCP. Quando uma IA precisa de contexto, ela "puxa" a memória do banco.

---

## 📂 Estrutura de Pastas
As memórias são divididas em pastas dentro de `/data`:

| Pasta         | Para que serve                                 |
| ------------- | ---------------------------------------------- |
| `projetos`    | Memórias sobre trabalhos e tarefas em andamento |
| `pessoas`     | Informações sobre contatos e relacionamentos    |
| `aprendizado` | Lições, artigos e conhecimentos adquiridos      |
| `ideias`      | Brainstorms e pensamentos criativos             |
| `contexto`    | Memória de curto prazo (o que está acontecendo) |
| `instrucoes`  | Regras e preferências (estilo, tom de voz)      |
| `fonte`       | Documentos brutos, PDFs e referências           |

---

## 🚀 Recursos (O que ele faz?)
- **Busca de Memória:** Permite que a IA procure arquivos específicos.
- **Listagem de Pastas:** Mostra à IA quais pastas de contexto existem.
- **Formato Markdown:** Memórias legíveis por humanos e máquinas.
- **Arquitetura MCP:** Compatível com Claude Desktop, Slack Agents e outras IAs.

---

## 🛠️ Como Usar

### 1. Pré-requisitos
- Node.js (se for rodar o Frontend da Lovable)
- Python 3.10+ (para o servidor MCP)
- Uma IA compatível com MCP (ex: Claude Desktop)

### 2. Instalação
```bash
# Clone o repositório
git clone <this-repository-url>
cd <repository-name>

# Instale as dependências do servidor MCP
pip install -r requirements.txt
