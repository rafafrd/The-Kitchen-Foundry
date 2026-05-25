# Culinario RAG — Agente Culinário com Azure AI Foundry

Chat de IA especializado em **alta gastronomia e ciência culinária**, construído sobre **Azure AI Foundry (GPT-4o)** com padrão **RAG (Retrieval-Augmented Generation)**. O projeto serve como prova de conceito para validar o uso do AI Foundry em aplicações conversacionais com base de conhecimento estruturada.

---

## Visão Geral da Arquitetura

```mermaid
graph TB
    subgraph Usuario["Usuário"]
        U[/"Pergunta culinária"/]
    end

    subgraph Frontend["Frontend — Streamlit (app.py)"]
        UI["Interface de Chat"]
        HIST["Histórico de Sessão\n(st.session_state)"]
        SIDE["Sidebar\n(Modelo / Versão API)"]
    end

    subgraph AzureAI["Azure AI Foundry"]
        EP["Endpoint\nai-foundry-aluno-resource\n.cognitiveservices.azure.com"]
        GPT["GPT-4o\nDeployment"]
    end

    subgraph RAGBase["Base de Conhecimento RAG"]
        SP["System Prompt\nAgente Culinário"]
        V1["Volume 1\nFundações e Clássicos\n(Glossário MD)"]
        V2["Volume 2\nPanificação, Garde Manger e Ásia\n(Glossário MD)"]
        V3["Volume 3\nVanguarda, Fermentação e Plant-Based\n(Glossário MD + PDF)"]
    end

    U --> UI
    UI --> HIST
    HIST -->|"messages[]"| EP
    SP -->|"role: system"| EP
    EP --> GPT
    GPT -->|"Chat Completion"| UI
    V1 & V2 & V3 --> SP
    SIDE -.->|"info"| UI
```

---

## Fluxo de uma Mensagem

```mermaid
sequenceDiagram
    actor Usuário
    participant Streamlit as app.py (Streamlit)
    participant AzureClient as AzureOpenAI Client
    participant Foundry as Azure AI Foundry<br/>(GPT-4o)

    Usuário->>Streamlit: digita pergunta culinária
    Streamlit->>Streamlit: append {role: user} no histórico
    Streamlit->>AzureClient: chat.completions.create(messages, model, temperature=0.7)
    Note over AzureClient,Foundry: messages inclui o System Prompt RAG<br/>com os 3 volumes como contexto
    AzureClient->>Foundry: POST /chat/completions
    Foundry-->>AzureClient: resposta técnica (Markdown)
    AzureClient-->>Streamlit: response.choices[0].message.content
    Streamlit->>Streamlit: append {role: assistant} no histórico
    Streamlit-->>Usuário: renderiza resposta com st.markdown()
```

---

## Estrutura do Projeto

```mermaid
graph LR
    ROOT["rag/"]

    ROOT --> APP["app.py\nChat Streamlit"]
    ROOT --> API["api.py\nTeste direto de API"]
    ROOT --> REQ["requirements.txt"]
    ROOT --> SP["system_prompt_rag_culinario.md\nSystem Prompt do Agente"]
    ROOT --> RAGDIR["rag/\nBase de Conhecimento"]

    RAGDIR --> V1["glossario_culinario\n_livro_receitas.md\n(Volume 1)"]
    RAGDIR --> V2["glossario_culinario\n_livro_receitas_vol2.md\n(Volume 2)"]
    RAGDIR --> V3["glossario_culinario\n_livro_receitas_vol3.md\n(Volume 3)"]
    RAGDIR --> PDF["livro14.pdf"]

    style APP fill:#1f6feb,color:#fff
    style SP fill:#388bfd,color:#fff
    style RAGDIR fill:#2d333b,color:#cdd9e5
```

---

## Base de Conhecimento (Volumes RAG)

O agente busca respostas nos três volumes do **Grande Guia Culinário**:

```mermaid
graph TD
    RAG["Agente RAG Culinário"]

    RAG --> V1["Volume 1 — Fundações e Clássicos"]
    RAG --> V2["Volume 2 — Panificação, Garde Manger e Ásia"]
    RAG --> V3["Volume 3 — Vanguarda, Fermentação e Plant-Based"]

    V1 --> V1A["Técnicas de corte (Brunoise, Mise en place)"]
    V1 --> V1B["Métodos de cocção (Maillard, Poché, Selar)"]
    V1 --> V1C["Receitas clássicas (Risoto, Béchamel, Petit Gâteau)"]

    V2 --> V2A["Desenvolvimento de glúten / Autólise"]
    V2 --> V2B["Fermentação (Biga / Poolish)"]
    V2 --> V2C["Técnicas Wok — Wok Hei / Dashi / Umami"]
    V2 --> V2D["Cura de carnes e peixes (Gravlax)"]

    V3 --> V3A["Gastronomia molecular (Esferificação, Espumas)"]
    V3 --> V3B["Hidrocoloides (Ágar-Ágar, Alginato, Xantana)"]
    V3 --> V3C["Fermentação microbiológica (Koji, Lactofermentação)"]
    V3 --> V3D["Sous-Vide e substituições veganas"]
```

---

## Lógica de Inferência do Agente (Chain of Thought)

```mermaid
flowchart TD
    Q["Query do usuário"] --> I["1. Compreensão da Intenção\nReceita? Técnica? Troubleshooting?"]
    I --> B["2. Busca Cruzada entre Volumes\nVol1 + Vol2 + Vol3"]
    B --> P["3. Foco em Precisão\nTemperaturas, proporções e\ntabelas de hidrocoloides"]
    P --> R{"Informação encontrada\nna base RAG?"}
    R -->|Sim| G["Gera resposta técnica\nem Markdown com\nReferências aos Volumes"]
    R -->|Não| F["Fallback: 'Não consta nos\nmanuais atuais, mas com base\nem [Técnica Similar]...'"]
```

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Frontend | Streamlit |
| Modelo | GPT-4o (Azure AI Foundry) |
| SDK | `openai` (AzureOpenAI client) |
| API Version | `2025-01-01-preview` |
| Base de Conhecimento | Markdown (3 volumes) + PDF |
| Autenticação | Azure API Key via `st.text_input` |

---

## Como Executar

```bash
# 1. Criar e ativar ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar o chat
streamlit run app.py
```

Insira sua **Azure API Key** no campo da interface e comece a conversar com o agente culinário.

---

## Exemplos de Uso do Agente

| Pergunta | Volume Consultado | Resposta esperada |
|---|---|---|
| "Meu molho de queijo separou, o que fazer?" | Vol 1 + Vol 3 | Química da emulsão + uso de Xantana |
| "Como fazer pão do zero?" | Vol 2 | Autólise, Ponto de Véu, Focaccia Genovesa |
| "O que é esferificação?" | Vol 3 | Técnica molecular com Alginato + Cloreto de Cálcio |
| "Qual a temperatura para Sous-Vide de frango?" | Vol 3 | Temperatura exata + regras de segurança alimentar |
