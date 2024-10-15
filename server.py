from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymilvus import connections, Collection
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

# Neo4j connection
neo4j_driver = GraphDatabase.driver(
    "bolt://neo4j:7687",
    auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
)

class Query(BaseModel):
    query: str

def generate_react_output(prompt):
    # This is a placeholder. In a real implementation, this would call an AI model.
    thoughts = [
        "I need to determine what kind of query this is.",
        "Based on the keywords, I can decide which database to query.",
        "After getting the results, I should format them for the user."
    ]
    actions = [
        {"type": "search_milvus", "input": prompt},
        {"type": "query_neo4j", "input": prompt}
    ]
    return {"thoughts": thoughts, "actions": actions}

async def search_milvus(query):
    try:
        collection = Collection("example_collection")
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = collection.search(
            data=[[0.1, 0.2, 0.3]],  # Example vector, replace with actual query vector
            anns_field="embedding",
            param=search_params,
            limit=5
        )
        return str(results)
    except Exception as e:
        print(f"Milvus search error: {e}")
        return "Error searching Milvus"

async def query_neo4j(query):
    try:
        with neo4j_driver.session() as session:
            result = session.run("MATCH (n) RETURN n LIMIT 5")
            return str([record["n"] for record in result])
    except Exception as e:
        print(f"Neo4j query error: {e}")
        return "Error querying Neo4j"

async def execute_action(action):
    if action["type"] == "search_milvus":
        return await search_milvus(action["input"])
    elif action["type"] == "query_neo4j":
        return await query_neo4j(action["input"])
    else:
        return f"Unknown action type: {action['type']}"

@app.post("/query")
async def process_query(query: Query):
    try:
        react_output = generate_react_output(query.query)
        final_result = ""

        for thought in react_output["thoughts"]:
            final_result += f"Thought: {thought}\n"

        for action in react_output["actions"]:
            final_result += f"Action: {action['type']}[{action['input']}]\n"
            action_result = await execute_action(action)
            final_result += f"Observation: {action_result}\n"

        final_result += "Answer: Based on the observations, here's a summary..."  # You'd generate a real summary here

        return {"result": final_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)