# HADES (Heuristic Adaptive Data Extraction System)

HADES is a powerful system that combines vector search capabilities of Milvus, graph database functionalities of Neo4j, and natural language processing to provide an advanced query processing and information retrieval system.

## Project Structure

- `frontend/`: React-based frontend application
- `backend/`: FastAPI-based backend server
- `docker-compose.yml`: Docker configuration for all services
- `Dockerfile.frontend`: Dockerfile for the frontend service
- `Dockerfile.backend`: Dockerfile for the backend service

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hades.git
   cd hades
   ```

2. Create a `.env` file in the root directory with the following content:
   ```
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password_here
   ```

3. Build and start the Docker containers:
   ```
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

## Usage

Enter your query in the input field on the frontend. The system will process your query using the following steps:

1. Parse and understand the query
2. Search for relevant information in Milvus
3. Query related data in Neo4j
4. Generate a response based on the collected information

## Development

To run the services individually for development:

- Frontend:
  ```
  cd frontend
  npm install
  npm run dev
  ```

- Backend:
  ```
  cd backend
  pip install -r requirements.txt
  uvicorn server:app --reload
  ```

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.