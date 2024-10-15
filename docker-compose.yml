import os
import re
import tempfile
import shutil
from git import Repo
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymilvus import connections, Collection, utility, DataType, CollectionSchema, FieldSchema
from neo4j import GraphDatabase
import openai
import logging
from sentence_transformers import SentenceTransformer
import time

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# LM Studio configuration
openai.api_base = os.getenv("LLM_API_BASE_URL", "http://192.168.1.69:1234/v1")
openai.api_key = os.getenv("LLM_API_KEY", "not-needed")

# Neo4j connection
neo4j_driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

class Query(BaseModel):
    query: str

def connect_to_milvus():
    max_retries = 5
    retry_interval = 5  # seconds

    for i in range(max_retries):
        try:
            connections.connect("default", host=os.getenv("MILVUS_HOST"), port=os.getenv("MILVUS_PORT"))
            logger.info("Successfully connected to Milvus")
            return
        except Exception as e:
            logger.warning(f"Failed to connect to Milvus (attempt {i+1}/{max_retries}): {e}")
            if i < max_retries - 1:
                logger.info(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                logger.error("Max retries reached. Unable to connect to Milvus.")
                raise

def check_milvus_health():
    try:
        return utility.get_server_version()
    except Exception as e:
        logger.error(f"Failed to connect to Milvus: {e}")
        return None

def create_milvus_collection():
    try:
        if not utility.has_collection("code_snippets"):
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="file_path", dtype=DataType.VARCHAR, max_length=500),
                FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=384)
            ]
            schema = CollectionSchema(fields, "Code snippets collection")
            collection = Collection("code_snippets", schema)
            index_params = {
                "index_type": "IVF_FLAT",
                "metric_type": "L2",
                "params": {"nlist": 1024}
            }
            collection.create_index("vector", index_params)
            logger.info("Created Milvus collection 'code_snippets'")
        else:
            logger.info("Milvus collection 'code_snippets' already exists")
    except Exception as e:
        logger.error(f"Error creating Milvus collection: {e}")

def generate_llm_output(prompt, use_rag=False):
    try:
        logger.debug(f"Sending prompt to LLM: {prompt}")
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Only respond to the user's query and do not generate any additional content."}
        ]
        
        if use_rag:
            rag_content = search_milvus(prompt)
            messages.append({"role": "system", "content": f"Here's some relevant information: {rag_content}"})
        
        messages.append({"role": "user", "content": prompt})
        
        response = openai.ChatCompletion.create(
            model=os.getenv("LLM_MODEL"),
            messages=messages,
            max_tokens=int(os.getenv("LLM_MAX_TOKENS")),
            temperature=float(os.getenv("LLM_TEMPERATURE")),
        )
        raw_output = response.choices[0].message['content']
        logger.debug(f"Raw LLM output: {raw_output}")
        
        # Filter out unexpected content
        filtered_output = re.sub(r'^\s*\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}.*?$', '', raw_output, flags=re.MULTILINE)
        filtered_output = re.sub(r'^\s*##.*?$', '', filtered_output, flags=re.MULTILINE)
        filtered_output = filtered_output.strip()
        
        logger.debug(f"Filtered LLM output: {filtered_output}")
        return filtered_output
    except Exception as e:
        logger.error(f"Error generating LLM output: {e}")
        raise

def search_milvus(query):
    try:
        collection = Collection("code_snippets")
        collection.load()
        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10},
        }
        vector = model.encode([query])[0].tolist()
        results = collection.search(
            data=[vector],
            anns_field="vector",
            param=search_params,
            limit=5,
            output_fields=["file_path", "content"]
        )
        
        relevant_snippets = []
        for hits in results:
            for hit in hits:
                relevant_snippets.append(f"File: {hit.entity.get('file_path')}\nContent: {hit.entity.get('content')}\n")
        
        return "\n".join(relevant_snippets)
    except Exception as e:
        logger.error(f"Milvus search error: {e}")
        return "Error searching Milvus"

async def query_neo4j(query):
    try:
        with neo4j_driver.session() as session:
            result = session.run("MATCH (n) RETURN n LIMIT 5")
            return str([record["n"] for record in result])
    except Exception as e:
        logger.error(f"Neo4j query error: {e}")
        return "Error querying Neo4j"

@app.post("/query")
async def process_query(query: Query, request: Request):
    try:
        logger.info(f"Received query: {query.query}")
        logger.debug(f"Request headers: {request.headers}")

        # Determine if RAG is needed
        use_rag = "code" in query.query.lower() or "repository" in query.query.lower()

        # Generate LLM output
        llm_output = generate_llm_output(query.query, use_rag)

        # Only perform Milvus search if RAG is used
        milvus_result = search_milvus(query.query) if use_rag else "RAG not used for this query"

        # Perform Neo4j query
        neo4j_result = await query_neo4j(query.query)

        # Combine results
        final_result = f"LLM Output: {llm_output}\n\nMilvus Result: {milvus_result}\n\nNeo4j Result: {neo4j_result}"

        return {"result": final_result}
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload_repo")
async def upload_repo(repo_url: str):
    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Clone the repository
            Repo.clone_from(repo_url, tmpdirname)

            # Process and embed the files
            collection = Collection("code_snippets")
            for root, dirs, files in os.walk(tmpdirname):
                for file in files:
                    if file.endswith(('.py', '.js', '.java', '.cpp', '.h', '.cs')):  # Add more extensions as needed
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as f:
                            content = f.read()
                        
                        # Embed the content
                        vector = model.encode([content])[0].tolist()

                        # Insert into Milvus
                        collection.insert([
                            [file_path.replace(tmpdirname, '')],  # file_path
                            [content],  # content
                            [vector]  # vector
                        ])

        return {"message": "Repository uploaded and embedded successfully"}
    except Exception as e:
        logger.error(f"Error uploading repository: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    health_status = {
        "milvus": "unhealthy",
        "neo4j": "unhealthy",
        "llm": "unhealthy"
    }
    
    # Check Milvus
    try:
        milvus_version = check_milvus_health()
        if milvus_version:
            health_status["milvus"] = "healthy"
    except Exception as e:
        logger.error(f"Milvus health check failed: {e}")

    # Check Neo4j
    try:
        with neo4j_driver.session() as session:
            result = session.run("RETURN 1")
            list(result)
            health_status["neo4j"] = "healthy"
    except Exception as e:
        logger.error(f"Neo4j health check failed: {e}")

    # Check LLM
    try:
        generate_llm_output("test")
        health_status["llm"] = "healthy"
    except Exception as e:
        logger.error(f"LLM health check failed: {e}")

    return health_status

@app.on_event("startup")
async def startup_event():
    connect_to_milvus()
    create_milvus_collection()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)