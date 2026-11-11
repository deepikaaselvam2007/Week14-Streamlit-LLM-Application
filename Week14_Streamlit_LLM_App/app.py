import streamlit as st
from pdf_qa import process_pdf, ask_pdf

st.set_page_config(page_title="PDF LLM Assistant", page_icon="📄")
st.title("PDF Question Answering Assistant")
st.write("Upload a PDF and ask questions about its contents.")
st.sidebar.info("Ollama models required: llama3.2 and nomic-embed-text")
uploaded = st.file_uploader("Choose a PDF", type=["pdf"])
if uploaded and st.button("Process PDF"):
    try:
        count = process_pdf(uploaded)
        st.session_state.ready = True
        st.success(f"PDF processed. Indexed {count} text chunks.")
    except Exception as e:
        st.error(str(e))
if st.session_state.get("ready"):
    q = st.text_input("Ask a question")
    if st.button("Get answer") and q.strip():
        try:
            answer, sources = ask_pdf(q)
            st.subheader("Answer")
            st.write(answer)
            with st.expander("Retrieved passages"):
                for s in sources: st.write(s)
        except Exception as e: st.error(str(e))
