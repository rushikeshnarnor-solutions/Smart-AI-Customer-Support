import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="Smart Support Assistant", page_icon="💬")
st.title("💬 Smart AI Customer Support Assistant")
st.caption("A document-grounded FAQ assistant using transparent keyword retrieval.")

DEFAULT_KB = """Returns: Items can be returned within 30 days with the original receipt.
Shipping: Standard shipping takes 3-5 business days. Express shipping takes 1-2 business days.
Payments: We accept major credit cards and UPI.
Support: Customer support is available Monday to Friday, 9 AM to 6 PM.
Warranty: Electronics include a one-year limited warranty from the purchase date."""

def pdf_text(file):
    reader = PdfReader(file)
    return "\n".join(p.extract_text() or "" for p in reader.pages)

def split_chunks(text):
    return [x.strip() for x in text.replace("\n", " ").split(".") if x.strip()]

def retrieve(question, chunks, k=3):
    terms = {w.lower().strip(".,?!:;()") for w in question.split() if len(w) > 2}
    scored = []
    for chunk in chunks:
        words = set(chunk.lower().split())
        score = len(terms & words)
        if score:
            scored.append((score, chunk))
    return [c for _, c in sorted(scored, reverse=True)[:k]]

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Knowledge base")
    uploaded = st.file_uploader("Upload a policy / FAQ PDF", type=["pdf"])
    kb = DEFAULT_KB
    if uploaded:
        try:
            kb = pdf_text(uploaded)
            st.success("PDF loaded for this session.")
        except Exception as e:
            st.error(f"PDF could not be read: {e}")
    st.caption("Demo mode: answers are retrieved from uploaded text; no external LLM is called.")

chunks = split_chunks(kb)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask about returns, shipping, payments, warranty...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    hits = retrieve(prompt, chunks)
    answer = "\n\n".join(f"- {h}." for h in hits) if hits else "I couldn't find that in the current knowledge base. Please contact a support representative."
    with st.chat_message("assistant"):
        st.markdown(answer)
        st.caption("Sources: retrieved knowledge-base text. Verify policy details before relying on them.")
    st.session_state.messages.append({"role": "assistant", "content": answer})

if st.button("Clear conversation"):
    st.session_state.messages = []
    st.rerun()
