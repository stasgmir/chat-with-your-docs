# Documentation Chatbot — “Chat with Your Docs”

**Chat with your documents using AI.**  
Upload PDFs, Markdown, or TXT files and ask natural language questions — the bot will return precise answers with context, citations, and code examples.

---

## Features
-  Upload and analyze **one or multiple** documentation files (PDF, MD, TXT)
-  Ask questions in natural language
- Context-aware answers with source references
-  Chat history and memory (Redis / SQLite)

---

## Tech Stack
- **Streamlit** — for building the interactive web application UI.  
- **FastAPI** — backend framework for handling file uploads, user queries, and chat history.  
- **LangChain** — framework for building LLM-powered workflows (retrieval, prompting, memory).  
- **langchain.embeddings.OpenAIEmbeddings** — generating text embeddings using OpenAI models.  
- **langchain.vectorstores.FAISS** — efficient similarity search and vector database management.  
- **langchain.chains.RetrievalQA** and **langchain.chains.LLMChain** — orchestrating document retrieval and LLM responses.  
- **langchain_core.prompts.PromptTemplate** — defining structured prompts for OpenAI models.  
- **OpenAI API** — for GPT-4 / GPT-5 access and embedding generation.  
- **PyMuPDF** and **Markdown parser** — for extracting and parsing text from PDF and Markdown files.  
- **FAISS / Qdrant** — vector databases for storing and searching document embeddings.  
- **Redis / SQLite** — for chat history, caching, and session persistence.

## System Architecture (OpenAI-based)

###  1. User Interface (Streamlit)
- Multiple file upload support  
- Chat window  
- Display of answers and source citations  

---

###  2. Backend API (FastAPI)
- `/upload` — handle **single or multiple** file uploads and preprocessing  
- `/query` — process user questions and return model answers  
- `/history` — manage chat history (Redis / SQLite)  
- Connects to vector database for context retrieval  

---

### 3. Document Preprocessing Pipeline
1. **Text extraction:** PyMuPDF, Markdown parser
2. **Text cleaning:** Whitespace normalization, merging hyphenated words,Cleaning of Markdown/HTML artifacts,removal of : headers footers, and page numbers, artifacts.
3. **Chunking:** LangChain `TextSplitter` (~1000 tokens per chunk)  
4. **Metadata enrichment:** file name, section, page reference  
5. **Embedding generation:** OpenAI Embeddings API  

---

###  4. Vector Database (FAISS / Qdrant)
- Stores text embeddings  
- Performs similarity search  
- Returns top relevant document chunks  

---

###  5. LLM Query Module (LangChain + OpenAI API)
- Builds a context from retrieved document fragments  
- Generates natural-language answers via GPT-4 / GPT-5  
- Includes sources and references in the response  




