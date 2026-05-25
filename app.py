import streamlit as st
from openai import AzureOpenAI

# ⚙️ Configurações baseadas nos dados fornecidos
ENDPOINT = "https://ai-foundry-aluno-resource.cognitiveservices.azure.com/"
API_KEY = ""
API_VERSION = "2025-01-01-preview"
DEPLOYMENT_NAME = "gpt-4o"

st.set_page_config(page_title="Azure OpenAI Chat", page_icon="🤖")
st.title("🤖 Azure AI - Chat gpt-4o")

# 🔒 Dica: No futuro, troque o 'value=API_KEY' por algo vazio e deixe o usuário digitar
api_key = st.text_input(
    "Azure API Key", 
    type="password", 
    value=API_KEY, 
    placeholder="Cole sua chave aqui..."
)

st.divider()

if not api_key:
    st.info("Insira sua Azure API Key acima para começar.")
    st.stop()

# --- Configuração do Cliente ---
@st.cache_resource
def get_client(key: str) -> AzureOpenAI:
    return AzureOpenAI(
        api_version=API_VERSION,
        azure_endpoint=ENDPOINT,
        api_key=key,
    )

client = get_client(api_key)

# --- Gerenciamento de Histórico (Sessão) ---
if "messages" not in st.session_state:
    # Instrução inicial do sistema (opcional, define o comportamento da IA)
    st.session_state.messages = [
        {"role": "system", "content": "Você é um assistente útil e amigável."}
    ]

# Renderiza o histórico (ignorando a mensagem do sistema para não poluir a tela)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- Interação com o Usuário ---
if prompt := st.chat_input("Digite sua mensagem..."):
    
    # 1. Salva a mensagem do usuário e exibe na tela
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Chama a API da Azure (Chat Completions)
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = client.chat.completions.create(
                    model=DEPLOYMENT_NAME,
                    messages=st.session_state.messages,
                    # Opcional: ajustar parâmetros como temperatura
                    temperature=0.7 
                )
                
                # Extrai a resposta de texto
                assistant_response = response.choices[0].message.content
                st.markdown(assistant_response)
                
                # 3. Salva a resposta no histórico para manter o contexto vivo
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                
            except Exception as e:
                st.error(f"❌ Erro de conexão com a API: {e}")

# --- Barra lateral ---
with st.sidebar:
    st.header("Sessão")
    st.caption(f"**Modelo:** `{DEPLOYMENT_NAME}`")
    st.caption(f"**Versão da API:** `{API_VERSION}`")
    
    if st.button("Limpar conversa", use_container_width=True):
        st.session_state.pop("messages", None)
        st.rerun()