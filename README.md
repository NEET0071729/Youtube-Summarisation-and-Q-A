# 🎬 YouTube RAG — AI-Powered Q&A for YouTube Videos

A full-stack **Retrieval-Augmented Generation (RAG)** application that lets you chat with any YouTube video. Paste a YouTube URL, ingest the transcript, and ask questions in a conversational interface — powered by Google Gemini and ChromaDB.

---

## ✨ Features

- 🔗 **YouTube Ingestion** — Load any YouTube video transcript via URL
- 🧠 **Contextual Query Rewriting** — Rephrases follow-up questions using chat history for accurate retrieval
- 💬 **Multi-turn Chat** — Remembers conversation context across turns
- ⚡ **Fast Vector Search** — Uses ChromaDB for persistent local vector storage
- 🌐 **Clean Web UI** — Single-page frontend with a modern chat interface
- 🔒 **CORS Enabled** — Ready for local frontend/backend separation

---

## 🏗️ Architecture

```
YouTube URL
    │
    ▼
[Ingest Pipeline]
 YoutubeLoader → Text Splitter → Gemini Embeddings → ChromaDB

User Query + Chat History
    │
    ▼
[RAG Chain]
 Query Rewriter (Gemini) → ChromaDB Retriever → Answer Generator (Gemini)
    │
    ▼
  Answer
```

### Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| LLM         | Google Gemini 2.5 Pro               |
| Embeddings  | `gemini-embedding-001`              |
| Vector DB   | ChromaDB (local persistence)        |
| RAG Framework | LangChain                         |
| Backend     | FastAPI + Uvicorn                   |
| Frontend    | Vanilla HTML / CSS / JavaScript     |

---

## 📁 Project Structure

```
YoutubeRAG/
├── backend/
│   ├── main.py          # FastAPI app — /ingest and /chat endpoints
│   ├── ingest.py        # YouTube transcript loading, chunking & embedding
│   ├── rag_core.py      # RAG chain: query rewriting + retrieval + generation
│   └── models.py        # Pydantic request/response models
├── frontend/
│   └── index.html       # Single-page chat UI
├── data/
│   └── chroma_db/       # Persisted ChromaDB vector store (auto-generated)
├── requirements.txt
├── .env                 # API keys (not committed)
└── .gitignore
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.9+
- A [Google AI Studio](https://aistudio.google.com/) API key

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/YoutubeRAG.git
cd YoutubeRAG
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 5. Run the Backend

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### 6. Open the Frontend

Simply open `frontend/index.html` in your browser. No build step required.

---

## 🔌 API Reference

### `POST /ingest`

Ingests a YouTube video's transcript into the vector store.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "message": "Video successfully ingested into ChromaDB. Chat history cleared."
}
```

---

### `POST /chat`

Sends a message and receives an AI-generated answer grounded in the video content.

**Request Body:**
```json
{
  "message": "What is the main topic of this video?"
}
```

**Response:**
```json
{
  "answer": "The video discusses..."
}
```

---

## ⚙️ How It Works

1. **Ingestion** (`ingest.py`)
   - The YouTube transcript is fetched using `YoutubeLoader`
   - Text is split into chunks (1000 chars, 150 overlap) using `RecursiveCharacterTextSplitter`
   - Chunks are embedded with `gemini-embedding-001` and stored in ChromaDB

2. **RAG Chain** (`rag_core.py`)
   - On the **first turn**, the user's raw query is used directly for retrieval
   - On **subsequent turns**, a *query rewriting* sub-chain uses the chat history to reformulate the question as a standalone query
   - The rewritten query retrieves the top-3 relevant chunks from ChromaDB
   - Gemini 2.5 Pro generates a final answer conditioned on the retrieved context and chat history

3. **Chat Memory** (`main.py`)
   - A global `chat_history` list stores `HumanMessage` and `AIMessage` objects
   - History is cleared automatically when a new video is ingested

---

## 📦 Dependencies

```
langchain
langchain-google-genai
langchain-community
langchain-text-splitters
langchain-core
langchain-chroma
chromadb
google-generativeai
youtube-transcript-api
pytube
fastapi
uvicorn
python-dotenv
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
