# models.py
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    
class ChatResponse(BaseModel):
    answer: str

class IngestRequest(BaseModel):
    url: str