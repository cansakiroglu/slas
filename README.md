# 🎓 Smart Learning Assistant System (SLAS)

SLAS is a full-stack AI-powered learning assistant that helps users upload custom documents, retrieve relevant information using semantic search (RAG), and ask questions about any topic they'd like to learn related the uploaded documents using their choice of LLMs (OpenAI or Ollama).

---

## 🌟 Features

- 📂 Upload plain text `.txt` documents to build a local knowledge base
- 🔍 Retrieve relevant context with `intfloat/multilingual-e5-large-instruct` embeddings and FAISS
- 🤖 Choose between OpenAI and Ollama (local) for generation with your model of preference
- 🚀 Ask learning questions and get context-aware answers with source documents
- 🐳 Fully Dockerized backend and frontend
- 🧱 Modular Python backend using FastAPI
- 📊 Interactive frontend using Streamlit

---

## 🗂️ Project Structure

```
slas/
├── app/                    # FastAPI backend
│   ├── api/                # Endpoints
│   ├── rag/                # RAG components (retriever, generator)
│   └── ...
├── ui/                     # Streamlit frontend
│   └── ...
├── docker/                 # Dockerfiles and docker-compose.yaml
│   └── ...
└── ...
```

---

## 🚀 Quick Start (with Docker)

```bash
git clone https://github.com/cansakiroglu/slas.git
cd slas
python3 -m venv .venv
source .venv/bin/activate
# For OpenAI models, set your OPENAI_API_KEY in docker-compose.yaml
# For running models locally with Ollama, ensure your Ollama server is running and model(s) are pulled
docker-compose --file docker/docker-compose.yaml up --build --detach --wait
```

- 🌐 Frontend (Streamlit): http://localhost:8501
- 🖥️ Backend (FastAPI) Swagger: http://localhost:8000/docs

### To Clean Up
```bash
docker ps  # See the containers
docker-compose --file docker/docker-compose.yaml down -v
# docker image prune  # (optional)
```

---

## 📝 Example Usage

1. Upload `physics_notes_1.txt` ... `physics_notes_n.txt`
2. Select `OpenAI` → `gpt-4.1`
3. Enter query: `Doppler Effect`
4. Click **Run Smart Assistant**
5. See retrieved context & explanation

---
