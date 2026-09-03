---
name: brain-bank
description: Memória persistente do usuário em markdown. Use ao salvar ou recuperar contexto de longo prazo — projetos, pessoas, preferências, decisões e aprendizados. Acione quando o usuário disser "lembra que", "guarda isso", "anota", quando perguntar sobre algo que ele contou antes, ou quando faltar contexto para responder bem.
---

# Brain Bank

O Brain Bank é a memória de longo prazo do usuário: arquivos markdown que
persistem entre conversas. Ele existe para que o usuário não precise
reexplicar as mesmas coisas toda vez.

## Quando usar

- O usuário pede para lembrar de algo ("lembra que...", "guarda isso", "anota").
- O usuário se refere a algo que contou antes ("aquele cliente", "o projeto que
  te falei") — procure antes de dizer que não sabe.
- Você precisa de contexto sobre projetos, pessoas, decisões ou preferências.
- Surgiu um fato durável sobre o usuário no meio da conversa. Salve sem
  interromper o assunto.

## Ferramentas

| Ferramenta | Quando usar |
| ---------- | ----------- |
| `procurar` | **Comece por aqui** quando tiver um termo. Busca em todas as pastas, no nome e no conteúdo. |
| `listar_pastas` | Quando não souber onde salvar ou procurar |
| `listar_memorias` | Para ver o que já existe em uma pasta |
| `buscar_memoria` | Para ler uma memória inteira, quando já souber o nome |
| `salvar_memoria` | Para criar ou atualizar. **Substitui o conteúdo anterior.** |
| `apagar_memoria` | Só quando o usuário pedir. Confirme antes. |

## Onde salvar cada coisa

- `projetos` — trabalhos e tarefas em andamento
- `pessoas` — contatos, times e relacionamentos
- `aprendizado` — lições, artigos e conhecimento adquirido
- `ideias` — brainstorms e pensamentos criativos
- `contexto` — o que está acontecendo agora (memória curta)
- `instrucoes` — preferências, tom de voz e regras de trabalho
- `fonte` — documentos brutos e material de referência

## Regras

1. **Nunca invente memórias.** Só afirme o que veio de uma ferramenta. Se a
   busca não achou nada, diga que não achou.
2. **`salvar_memoria` sobrescreve.** Para acrescentar a uma memória existente,
   leia com `buscar_memoria` primeiro, junte o conteúdo e salve o texto completo.
3. **Escreva memórias autossuficientes.** Quem ler daqui a seis meses, sem esta
   conversa, tem que entender. "Prazo 15/03" não serve; "Cliente Acme aprovou o
   escopo em 02/09, entrega 15/03" serve.
4. **Uma memória por assunto.** Atualize a existente em vez de criar
   `acme-2`, `acme-novo`.
5. **Não salve o que expira em dias** nem o que o usuário claramente não quer
   registrado.
6. Ao recuperar contexto, use a memória para melhorar a resposta — não anuncie
   que consultou a memória a cada frase.
