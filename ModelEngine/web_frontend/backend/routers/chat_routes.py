from fastapi import APIRouter, HTTPException

router = APIRouter()

from types.schemas import ChatRequest, ChatResponse

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Placeholder for chat logic
    raise HTTPException(status_code=501, detail="Chat functionality not implemented yet")
