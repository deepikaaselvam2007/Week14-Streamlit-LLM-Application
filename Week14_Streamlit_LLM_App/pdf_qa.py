import tempfile
from pathlib import Path
from pypdf import PdfReader
from rag_core import index_chunks, retrieve, generate

def process_pdf(upload):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(upload.getvalue()); name = f.name
    try:
        text = "\n".join(p.extract_text() or "" for p in PdfReader(name).pages)
        chunks = [text[i:i+900] for i in range(0, len(text), 750) if text[i:i+900].strip()]
        if not chunks: raise ValueError("No readable text found in this PDF.")
        index_chunks(chunks, upload.name)
        return len(chunks)
    finally: Path(name).unlink(missing_ok=True)

def ask_pdf(question):
    docs = retrieve(question)
    return generate(question, "\n\n".join(docs)), docs
