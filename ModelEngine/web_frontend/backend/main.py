from fastapi import FastAPI
from routers import chat_routes
from routers import model_routes

app = FastAPI()

app.include_router(chat_routes.router, prefix="/chat", tags=["chat"])
app.include_router(model_routes.router, prefix="/models", tags=["models"])
