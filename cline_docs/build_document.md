# Build Document for HADES (Heuristic Adaptive Data Extraction System)

## 1. Prerequisites

- Node.js (LTS version recommended)
- npm (package manager)
- Docker (optional for containerized installation)
- Python 3.8+ with pip
- CUDA-compatible GPU (recommended)

## 2. Base Environment Setup

### 2.1 RAM Disk Configuration

```bash
# Create 64GB RAM Disk for model hot-swapping
sudo mkdir /mnt/ramdisk
sudo mount -t tmpfs -o size=64G tmpfs /mnt/ramdisk

# Add to /etc/fstab for persistence
echo "tmpfs /mnt/ramdisk tmpfs size=64G 0 0" | sudo tee -a /etc/fstab
```

### 2.2 Python Environment Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install base dependencies
pip install torch torchvision torchaudio
pip install transformers accelerate
pip install python-dotenv
```

## 3. Database Setup

### 3.1 Local Installation of ArangoDB

#### Dependencies

1. Add the ArangoDB repository:

```bash
wget -q https://download.arangodb.com/arangodb42/DEBIAN/Release.key -O- | sudo apt-key add -
echo 'deb https://download.arangodb.com/arangodb42/DEBIAN/ /' | sudo tee /etc/apt/sources.list.d/arangodb.list
```

2. Install ArangoDB:

```bash
sudo apt-get update
sudo apt-get install -y arangodb3
```

3. Configuration:
   - Default port: `8529`
   - Default credentials: root/root

4. Start the service:

```bash
sudo systemctl start arangodb3
sudo systemctl enable arangodb3
```

### 3.2 Docker Installation of ArangoDB (Alternative)

1. Create a `docker-compose.yml` file:

```yaml
version: "3.8"
services:
  arangodb:
    image: arangodb:latest
    environment:
      - ARANGO_ROOT_PASSWORD=root
    ports:
      - "8529:8529"
    volumes:
      - arangodb_data:/var/lib/arangodb3
volumes:
  arangodb_data:
```

2. Start the container:

```bash
docker-compose up -d
```

## 4. Model Infrastructure

### 4.1 vLLM Installation

```bash
# Install vLLM
pip install vllm
```

### 4.2 Model Configuration

```bash
# Start RAG Specialist (3B Model)
vllm serve phi-2 \
    --port 8961 \
    --max-model-len 8192 \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.3

# Start Main Processing Model
vllm serve mistral-7b \
    --port 8962 \
    --max-model-len 32768 \
    --tensor-parallel-size 2 \
    --gpu-memory-utilization 0.8
```

## 5. CrewAI Setup

### 5.1 Installation

```bash
# Install CrewAI and dependencies
pip install crewai langchain pydantic openai
pip install duckduckgo-search  # For web search capabilities
```

### 5.2 Project Structure

```bash
mkdir -p hades_crew/{agents,tasks,tools,config}
touch hades_crew/__init__.py
```

### 5.3 Components Setup

1. ArangoDB Tool (`hades_crew/tools/arango_tool.py`):

```python
from typing import Dict
from crewai.tools import BaseTool
from arangodb import ArangoClient

class ArangoDBTool(BaseTool):
    name: str = "ArangoDB Tool"
    description: str = "Tool for interacting with ArangoDB"

    def __init__(self):
        self.client = ArangoClient(hosts="http://localhost:8529")
        self.db = self.client.db("hades", username="root", password="your_password")

    async def execute(self, query: str) -> Dict:
        try:
            cursor = await self.db.aql.execute(query)
            return {"status": "success", "data": [doc for doc in cursor]}
        except Exception as e:
            return {"status": "error", "message": str(e)}
```

2. Agent Definitions (`hades_crew/agents/agents.py`):

```python
from crewai import Agent
from ..tools.arango_tool import ArangoDBTool

class HADESAgents:
    def __init__(self):
        self.arango_tool = ArangoDBTool()

    def rag_specialist(self) -> Agent:
        return Agent(
            role='RAG Specialist',
            goal='Efficiently manage and query the database',
            backstory='Expert in database operations and RAG systems',
            verbose=True,
            allow_delegation=False,
            tools=[self.arango_tool],
            model="phi-2",
            base_url="http://localhost:8961/v1"
        )

    def main_processor(self) -> Agent:
        return Agent(
            role='Main Processor',
            goal='Process and analyze complex queries',
            backstory='Advanced reasoning and analysis specialist',
            verbose=True,
            allow_delegation=True,
            model="mistral-7b",
            base_url="http://localhost:8962/v1"
        )
```

3. Task Definitions (`hades_crew/tasks/tasks.py`):

```python
from crewai import Task
from ..agents.agents import HADESAgents

class HADESTasks:
    def __init__(self):
        self.agents = HADESAgents()

    def query_database(self, query: str) -> Task:
        return Task(
            description=f"Execute and analyze the following query: {query}",
            agent=self.agents.rag_specialist(),
            expected_output="Query results with analysis"
        )

    def process_results(self, context: str) -> Task:
        return Task(
            description=f"Process and analyze the following data: {context}",
            agent=self.agents.main_processor(),
            expected_output="Processed analysis and insights"
        )
```

4. Crew Setup (`hades_crew/crew_setup.py`):

```python
from crewai import Crew
from .tasks.tasks import HADESTasks

class HADESCrew:
    def __init__(self):
        self.tasks = HADESTasks()

    def create_crew(self) -> Crew:
        return Crew(
            agents=[
                self.tasks.agents.rag_specialist(),
                self.tasks.agents.main_processor()
            ],
            tasks=[
                self.tasks.query_database("INITIAL_QUERY"),
                self.tasks.process_results("CONTEXT")
            ],
            verbose=True
        )

    async def run(self, query: str):
        crew = self.create_crew()
        result = await crew.kickoff()
        return result
```

## 6. MCP Server Setup

### 6.1 Installation

```bash
git clone https://github.com/r3d91ll/H.A.D.E.S.git
cd H.A.D.E.S
npm install
```

### 6.2 Build and Run

```bash
npm run build
node build/index.js
```

## 7. Monitoring Setup

### 7.1 Resource Monitoring

```bash
pip install psutil gputil
python scripts/monitor.py
```

### 7.2 Performance Tracking

```python
# scripts/performance_tracker.py
class PerformanceTracker:
    def __init__(self):
        self.metrics = {
            "response_times": [],
            "memory_usage": [],
            "gpu_utilization": []
        }

    def track_query(self, query_time, memory_used, gpu_util):
        self.metrics["response_times"].append(query_time)
        self.metrics["memory_usage"].append(memory_used)
        self.metrics["gpu_utilization"].append(gpu_util)
```

## 8. Usage Example

```python
# example.py
import asyncio
from hades_crew.crew_setup import HADESCrew

async def main():
    crew = HADESCrew()
    result = await crew.run("YOUR_QUERY_HERE")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## 9. Troubleshooting

### Debugging MCP Communication

```bash
npm run inspector
```

### Logs

- MCP server logs to `stdout`
- Configure logging for file output
- ArangoDB logs:

```bash
docker logs arangodb
```

## 10. License & Support

This project is MIT licensed. For support, contact internal maintainers or the repository maintainers.
