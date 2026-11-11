# Week 14 – Streamlit LLM Application

## Setup
1. Install Python 3.10+ and Ollama.
2. In a terminal run:
   ```bash
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ```
3. Open this project folder in VS Code.
4. Install packages:
   ```bash
   python -m pip install -r requirements.txt
   ```
5. Start the app:
   ```bash
   streamlit run app.py
   ```

Upload a PDF, click **Process PDF**, then enter a question.

## Files
- `app.py`: Streamlit interface
- `pdf_qa.py`: PDF extraction and question answering
- `rag_core.py`: Ollama embeddings, ChromaDB storage/retrieval and response generation
- `dataset/`: sample files
- `uploaded_files/`: folder for uploaded PDFs
- `chroma_db/`: local vector database
- `assets/` and `screenshots/`: add logo and project screenshots

Ollama must be running locally. Default chat model: `llama3.2`; embedding model: `nomic-embed-text`.
