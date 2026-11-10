# Smart AI Customer Support Assistant

A lightweight retrieval-based support chatbot. It answers questions using an included sample FAQ or a PDF uploaded during the session.

## Features
- PDF knowledge-base upload
- Sentence-level retrieval using keyword overlap
- Chat-style interface and conversation history
- Fallback response when no source is found

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Architecture
1. Extract text from the uploaded PDF.
2. Split the text into sentence-like chunks.
3. Rank chunks by shared question keywords.
4. Display the best matching source text.

## Limitations & responsible use
This starter uses lexical retrieval, not a generative LLM or a production-grade RAG pipeline. It can miss paraphrases and should not be used as the sole source for legal, financial, medical, or account-sensitive decisions.

## Suggested extensions
- Add embeddings and a vector database (FAISS / Chroma).
- Add citations with page numbers.
- Connect a hosted LLM with environment-based API key configuration.
- Add agent handoff and feedback analytics.
