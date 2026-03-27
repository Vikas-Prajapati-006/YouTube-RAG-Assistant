
#  YouTube Transcript RAG Chatbot

An end-to-end **Retrieval-Augmented Generation (RAG)** application built with a modular architectural approach. This project allows users to perform semantic searches and have natural conversations based on any YouTube video's content using **Llama-3** and **FAISS**.

---

##  Key Features
* **Automated Ingestion:** Fetches transcripts directly from YouTube URLs using `yt-dlp`.
* **Modular Transformation:** Cleans raw text, removes timestamps, and generates recursive character chunks for better context retrieval.
* **Vector Search:** Utilizes `HuggingFaceEmbeddings` and `FAISS` for high-performance similarity mapping.
* **LLM Integration:** Powered by **Meta Llama-3-8B-Instruct** via HuggingFace Inference API for accurate, context-aware responses.
* **Streamlit UI:** A clean, user-friendly dashboard for real-time processing and chatting.

---

##  Project Architecture
The project follows professional software engineering practices with a decoupled folder structure:

1. **Data Ingestion:** Extracts transcript data from YouTube.
2. **Data Transformation:** Processes text and saves serialized chunk objects.
3. **Vector Store:** Creates and saves the FAISS index in the `artifacts/` directory.
4. **RAG Pipeline:** Integrates the retriever with the LLM using LangChain.

---

##  Tech Stack
* **Language:** Python 3.10+
* **Frameworks:** LangChain, Streamlit
* **Embeddings:** `all-MiniLM-L6-v2` (Sentence-Transformers)
* **Vector Database:** FAISS (Facebook AI Similarity Search)
* **LLM:** Meta Llama-3-8B-Instruct (HuggingFace API)

---

