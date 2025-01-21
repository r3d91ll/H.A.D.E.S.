from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class ModelRequest(BaseModel):
    model_name: str

class ModelResponse(BaseModel):
    message: str
