import faiss
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
import torch

torch.set_num_threads(1)
model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")
INDEX_PATH = Path("app/rag/index/faiss_index.bin")
DOCS_PATH = Path("app/rag/index/docstore.pkl")
DOCS_DIR = Path("app/rag/documents")


def get_detailed_instruct(
    task_description: str = "Given a topic as query, retrieve relevant text that is related to the topic",
    query: str = None,
) -> str:
    return f"Instruct: {task_description}\nQuery: {query}"


def load_documents():
    docs = []
    folder = Path("app/rag/documents")
    for file in folder.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            docs.append(f.read())
    return docs


def build_or_load_index():
    if INDEX_PATH.exists() and DOCS_PATH.exists():
        with open(DOCS_PATH, "rb") as f:
            documents = pickle.load(f)
        index = faiss.read_index(str(INDEX_PATH))
        return index, documents

    documents = load_documents()
    embeddings = model.encode(
        documents,
        # convert_to_tensor=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )  # .cpu().numpy()
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    Path(INDEX_PATH.parent).mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))
    with open(DOCS_PATH, "wb") as f:
        pickle.dump(documents, f)

    return index, documents


def retrieve_context(query: str, top_k: int = 3) -> str:
    if (not DOCS_DIR.exists() or not any(DOCS_DIR.glob("*.txt"))) and (
        not INDEX_PATH.exists() or not DOCS_PATH.exists()
    ):
        raise ValueError("No documents found and no prebuilt index available.")
    index, documents = build_or_load_index()
    query_embedding = model.encode(
        [get_detailed_instruct(query=query)],
        # convert_to_tensor=True,
        normalize_embeddings=True,
    )  # .cpu().numpy()
    scores, indices = index.search(query_embedding, top_k)
    return "\n---\n".join([documents[i] for i in indices[0]])
