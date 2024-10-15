from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymilvus import connections, Collection, utility
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Milvus connection
connections.connect("default", host="milvus", port="19530")

# Check if Milvus is healthy
def check_milvus_health():
    try:
        return utility.get_server_version()
    except Exception as e:
        print(f"Failed to connect to Milvus: {e}")
        return None

# Neo4j connection
neo4j_driver = GraphDatabase.driver(
    "bolt://neo4j:7687",
    auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
)

class Query(BaseModel):
    query: str

# TODO: Implement query processing logic here

@app.post("/query")
async def process_query(query: Query):
    # TODO: Implement query processing logic
    pass

@app.on_event("startup")
async def startup_event():
    milvus_version = check_milvus_health()
    if milvus_version:
        print(f"Successfully connected to Milvus. Server version: {milvus_version}")
    else:
        print("Failed to connect to Milvus. Please check your configuration.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)