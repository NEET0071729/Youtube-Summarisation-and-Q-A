# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage

# Import your modules
from models import ChatRequest, ChatResponse, IngestRequest
from ingest import process_youtube_url
from rag_core import get_rag_chain

app = FastAPI(title="YouTube RAG API")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize the RAG chain once at startup
try:
    rag_chain = get_rag_chain()
except Exception as e:
    print(f"Warning: Could not initialize RAG chain (did you ingest data yet?): {e}")
    rag_chain = None

# Single global memory store for the chat history
chat_history = []

@app.post("/ingest")
async def ingest_video(request: IngestRequest):
    try:
        process_youtube_url(request.url)
        
        # Re-initialize the chain and clear the chat history for the new video
        global rag_chain, chat_history
        rag_chain = get_rag_chain()
        chat_history = [] 
        
        return {"message": "Video successfully ingested into ChromaDB. Chat history cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not rag_chain:
         raise HTTPException(status_code=500, detail="RAG chain not initialized. Please ingest a video first.")

    user_message = request.message

    # Prepare inputs using the single global history
    input_dict = {
        "input": user_message,
        "chat_history": chat_history
    }

    try:
        # 1. Run the chain with the current history
        result = rag_chain.invoke(input_dict)

        # 2. Update the global history list for the next turn
        chat_history.extend([
            HumanMessage(content=user_message),
            AIMessage(content=result)
        ])
        
        # 3. Return the payload matching your ChatResponse model
        return ChatResponse(answer=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))