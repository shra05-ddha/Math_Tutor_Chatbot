import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv

# Vector DB + Embeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Prompt & RAG
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# -----------------------------------
# Load Environment
# -----------------------------------
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# -----------------------------------
# Streamlit UI Setup
# -----------------------------------
st.set_page_config(page_title="Karnataka Board 2nd PUC Maths Tutor", layout="wide")

st.markdown("""
<style>
body { background-color:#0f1117; color:white; }
.main-title { text-align:center; font-size:40px; font-weight:700; }
.chat-bubble-user {
    background:#ff9ed6; color:black; padding:12px;
    border-radius:14px; max-width:80%; margin:8px 0;
}
.chat-bubble-bot {
    background:#b3d1ff; color:black; padding:12px;
    border-radius:14px; max-width:80%; margin:8px 0;
}
.chat-container { display:flex; flex-direction:column; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>📘 Karnataka Board 2nd PUC Maths Tutor (RAG)</div>",
            unsafe_allow_html=True)

# -----------------------------------
# Sidebar Chapters
# -----------------------------------
chapters = [
    "1. Relations and Functions",
    "2. Inverse Trigonometric Functions",
    "3. Matrices",
    "4. Determinants",
    "5. Continuity and Differentiability",
    "6. Application of Derivatives",
    "7. Integrals",
    "8. Application of Integrals",
    "9. Differential Equations",
    "10. Vector Algebra",
    "11. 3D Geometry",
    "12. Linear Programming",
    "13. Probability",
]

st.sidebar.title("Chapters")
selected_chapter = st.sidebar.selectbox("Select a chapter (optional)", chapters)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# -----------------------------------
# Load Vectorstore
# -----------------------------------
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")

vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_type="similarity", k=4)

# -----------------------------------
# Prompt Template
# -----------------------------------
prompt = PromptTemplate.from_template("""
You are a Class 12 Maths Teacher AI.

CHAPTER: {chapter}

Use the following retrieved content to answer the question:

CONTEXT:
{context}

QUESTION:
{question}

Provide a clean NCERT-style step-by-step explanation with proper LaTeX.

Final Answer:
""")

# -----------------------------------
# RAG Base Chain
# -----------------------------------
def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

rag_base = RunnableParallel({
    "context": retriever | format_docs,
    "chapter": lambda _: selected_chapter,
    "question": RunnablePassthrough(),
}) | prompt

# -----------------------------------
# OpenRouter API Call
# -----------------------------------
def call_openrouter(prompt_text):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "PUC Maths Tutor"
    }

    data = {
        "model": "google/gemma-3-12b-it:free",
        "messages": [
            {
                "role": "user",
                "content": prompt_text
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()

    try:
        return result["choices"][0]["message"]["content"]
    except:
        return f"Error calling model: {result}"

# -----------------------------------
# Chat History
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    bubble = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-bot"
    st.markdown(
        f"<div class='chat-container'><div class='{bubble}'>{msg['content']}</div></div>",
        unsafe_allow_html=True
    )

# -----------------------------------
# User Input
# -----------------------------------
user_input = st.chat_input("Ask your Class 12 Maths question…")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# -----------------------------------
# Generate Answer (RAG + Gemini)
# -----------------------------------
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

    q = st.session_state.messages[-1]["content"]

    with st.chat_message("assistant"):
        with st.spinner("Solving…"):

            rag_prompt = rag_base.invoke(q)
            final_prompt = rag_prompt.to_string()

            answer = call_openrouter(final_prompt)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
