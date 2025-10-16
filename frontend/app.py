import streamlit as st
import os

from direct_chat import Direct_LLM_Chat
from pdf_qa import PDF_QA_Session
from rag_create import Create_RAG_Memory
from rag_chat import RAG_Chat
from model_setup import model_setup_page




def login():

    st.set_page_config(page_title="Login | Chat with Your Docs", page_icon="🔐", layout="centered")

    st.title("🔐 Вход в систему")

    USERS = {
        "admin": "12345",
        "user": "password"
    }

    if "authenticated" in st.session_state and st.session_state.authenticated:
        return True

    username = st.text_input("👤 Логин")
    password = st.text_input("🔑 Пароль", type="password")

    if st.button("Войти"):
        if username in USERS and USERS[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success(f" Добро пожаловать, {username}!")
            st.rerun()
        else:
            st.error(" Неверный логин или пароль")

    st.stop()



if "authenticated" not in st.session_state or not st.session_state.authenticated:
    login()

if "setup_complete" not in st.session_state or not st.session_state.setup_complete:
    model_setup_page()
    st.stop()

st.set_page_config(
    page_title="Chat with Your Documents",
    layout="wide",
    page_icon="📚"
)
if st.sidebar.button("🔄 Сменить модель"):
    st.session_state.setup_complete = False
    st.rerun()

# ------------------- SESSION STATE -------------------
DEFAULTS = {
    "pdf_processed_for_qa": False,
    "pdf_vector_store": None,
    "rag_vector_store": None,
    "rag_memory_loaded": False,
    "mode": "🏠 Home"
}

for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)

FAISS_INDEX_PATH = os.path.join(os.getcwd(), "faiss_index.bin")
RAG_DOCS_DIR = os.path.join(os.getcwd(), "rag_docs")
os.makedirs(RAG_DOCS_DIR, exist_ok=True)

temperature = 0.5


st.sidebar.image("https://em-content.zobj.net/source/microsoft-teams/363/books_1f4da.png", width=60)
st.sidebar.title("Chat with Your Docs")

st.sidebar.markdown(f"**👋 Привет, {st.session_state.username}!**")

if st.sidebar.button("🚪 Выйти"):
    st.session_state.authenticated = False
    st.rerun()


st.title("📚 Chat with Your Documents")
st.caption("Загружай документы, создавай память и общайся с ИИ как с ассистентом!")

mode = st.session_state.mode



if mode == "🏠 Home":
    st.markdown(
        """
        <style>
        .centered {
            text-align: center;
            margin-top: 50px;
        }
        .card-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 25px;
            margin-top: 40px;
        }
        .card {
            background-color: #f9f9f9;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            width: 250px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid #e6e6e6;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            background-color: #ffffff;
        }
        .emoji {
            font-size: 36px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="centered">
            <h1>👋 Добро пожаловать!</h1>
            <p style="font-size:18px;">
                Добро пожаловать в <b>Chat with Your Documents</b> — интеллектуального ассистента 
                для анализа документов, поиска информации и построения памяти 📚
            </p>
            <p style="color: gray;">Выберите режим, чтобы начать 👇</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4, gap="large")

    with col1:
        if st.button("💬 Direct Chat", use_container_width=True):
            st.session_state.mode = "💬 Direct Chat"
            st.rerun()
        st.caption("Общайся напрямую с LLM (OpenAI / Ollama).")

    with col2:
        if st.button("📄 PDF Q&A", use_container_width=True):
            st.session_state.mode = "📄 PDF Q&A"
            st.rerun()
        st.caption("Загрузи PDF и получай ответы из текста.")

    with col3:
        if st.button("🧠 Create RAG Memory", use_container_width=True):
            st.session_state.mode = "🧠 Create RAG Memory"
            st.rerun()
        st.caption("Создай долговременную базу знаний из документов.")

    with col4:
        if st.button("🔍 RAG Chat", use_container_width=True):
            st.session_state.mode = "🔍 RAG Chat"
            st.rerun()
        st.caption("Задавай вопросы на основе сохранённой памяти.")



elif mode == "💬 Direct Chat":
    Direct_LLM_Chat(temperature)
elif mode == "📄 PDF Q&A":
    PDF_QA_Session()
elif mode == "🧠 Create RAG Memory":
    Create_RAG_Memory(FAISS_INDEX_PATH, RAG_DOCS_DIR)
elif mode == "🔍 RAG Chat":
    RAG_Chat(temperature, FAISS_INDEX_PATH)



