import os
from dotenv import load_dotenv

# Text splitting + embeddings + vectorstore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()


def load_all_text_files():
    """
    Load all .txt files from:
    - data/combined_text
    - data/solutions_learncbse
    - data/solutions_kseeb
    """
    base_path = "data"

    folders = [
        "combined_text",
        "solutions_learncbse",
        "solutions_kseeb"
    ]

    all_docs = []

    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            continue

        for file in os.listdir(folder_path):
            if file.endswith(".txt"):
                file_path = os.path.join(folder_path, file)

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                        all_docs.append(text)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    print(f"Loaded {len(all_docs)} documents.")
    return all_docs


def chunk_documents(documents):
    """
    Split documents into overlapping chunks
    for better embedding retrieval.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " "]
    )

    chunks = splitter.create_documents(documents)
    print(f"Created {len(chunks)} chunks.")
    return chunks


def build_vector_db():
    """
    Build a FAISS vector store using local HF embeddings.
    Saves to /vectorstore.
    """
    print("Loading documents...")
    documents = load_all_text_files()

    print("Splitting into chunks...")
    chunks = chunk_documents(documents)

    print("Loading embeddings (BAAI/bge-small-en)...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")

    print("Building FAISS vectorstore...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs("vectorstore", exist_ok=True)
    vectorstore.save_local("vectorstore")

    print("Vector database saved at: vectorstore/")


if __name__ == "__main__":
    build_vector_db()
