import os, requests, chromadb

URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
EMBED = os.getenv("EMBED_MODEL", "nomic-embed-text")
CHAT = os.getenv("CHAT_MODEL", "llama3.2")

def embedding(text):
    r = requests.post(URL + "/api/embeddings", json={"model": EMBED, "prompt": text}, timeout=120)
    r.raise_for_status()
    return r.json()["embedding"]

def collection():
    return chromadb.PersistentClient(path="chroma_db").get_or_create_collection("pdf_docs")

def index_chunks(chunks, source):
    col = collection()
    old = col.get()
    if old.get("ids"): col.delete(ids=old["ids"])
    col.add(ids=[f"chunk-{i}" for i in range(len(chunks))],
            documents=chunks, embeddings=[embedding(x) for x in chunks],
            metadatas=[{"source": source} for _ in chunks])

def retrieve(question, k=4):
    col = collection()
    if col.count() == 0: return []
    result = col.query(query_embeddings=[embedding(question)], n_results=min(k, col.count()))
    return result["documents"][0]

def generate(question, context):
    prompt = ("Answer only from the context. If the answer is absent, say so.\\n\\n"
              f"Context:\\n{context}\\n\\nQuestion: {question}\\nAnswer:")
    r = requests.post(URL + "/api/generate",
        json={"model": CHAT, "prompt": prompt, "stream": False}, timeout=180)
    r.raise_for_status()
    return r.json().get("response", "")
