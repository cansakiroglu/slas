import streamlit as st
import requests

root_url = "http://backend:8000/"
st.set_page_config(page_title="Smart Learning Assistant", layout="wide")
st.title("🎓 Smart Learning Assistant System (SLAS)")

# === Document Upload Section ===
st.markdown("## 📂 Upload Documents for RAG")
with st.expander("Upload plain text files to build the knowledge base", expanded=True):
    uploaded_files = st.file_uploader(
        "Choose .txt files", type=["txt"], accept_multiple_files=True
    )

    if uploaded_files:
        uploaded_filenames = [file.name for file in uploaded_files]
        if st.session_state.get("uploaded_filenames") != uploaded_filenames:
            with st.spinner("Uploading files and updating the knowledge base..."):
                response = requests.delete(f"{root_url}reset-knowledge-base")
                if response.status_code == 200:
                    st.success("Knowledge base reset successful.")
                for file in uploaded_files:
                    f = {"file": (file.name, file, "text/plain")}
                    response = requests.post(f"{root_url}upload", files=f)
                    if response.status_code == 200:
                        st.success(f"✅ {file.name} uploaded.")
                    else:
                        st.error(f"❌ Failed to upload {file.name}: {response.text}")
            st.session_state["uploaded_filenames"] = uploaded_filenames

# === Load model lists if not already loaded ===
if "openai_models" not in st.session_state:
    response = requests.get(f"{root_url}openai-models")
    if response.status_code == 200:
        st.session_state.openai_models = response.json()["models"]

if "ollama_models" not in st.session_state:
    response = requests.get(f"{root_url}ollama-models")
    if response.status_code == 200:
        st.session_state.ollama_models = response.json()["models"]

# === Select Provider and Model ===
st.markdown("## 🤖 Choose Model")
col1, col2 = st.columns(2)
with col1:
    provider = st.selectbox("LLM Provider", ["openai", "ollama"], key="provider")

if provider == "openai":
    models = st.session_state.get("openai_models", [])
else:
    models = st.session_state.get("ollama_models", [])

with col2:
    model_name = st.selectbox(
        "Model", models if models else ["No models available"], key="model"
    )

# === LLM Form ===
st.markdown("## 🧠 Ask the Smart Assistant")

with st.form("smart_assistant_form"):
    topic = st.text_input("🔍 Topic you'd like to learn about")
    run = st.form_submit_button("🚀 Run Smart Assistant")

if run:
    if not topic:
        st.warning("Please enter a topic.")
    elif not model_name or model_name.startswith("No models"):
        st.warning("Please select a valid model.")
    else:
        with st.spinner("Thinking... Generating explanation..."):
            try:
                response = requests.get(
                    f"{root_url}topic",
                    params={"query": topic, "provider": provider, "model": model_name},
                    timeout=120,
                )
                if response.status_code == 200:
                    data = response.json()
                    st.markdown("### 📖 Retrieved Context")
                    st.info(data["context"])
                    st.markdown("### 📘 Explanation")
                    st.success(data["explanation"])
                elif response.json().get("detail", "").startswith("No documents found"):
                    st.warning(
                        "⚠️ Knowledge base is empty. Please upload documents first."
                    )
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"❌ Connection error: {e}")
