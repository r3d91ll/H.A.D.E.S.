# HADES (Heuristic Adaptive Data Extraction System)

HADES is an advanced query processing and information retrieval system that combines the power of vector search (Milvus), graph database (Neo4j), and natural language processing to provide intelligent responses to user queries.

## Project Structure

- `src/`: React-based frontend application
- `server.py`: FastAPI-based backend server
- `docker-compose.yml`: Docker configuration for all services
- `Dockerfile.frontend`: Dockerfile for the frontend service
- `Dockerfile.backend`: Dockerfile for the backend service

## Technologies Used

- Frontend: React, TypeScript, Tailwind CSS
- Backend: Python, FastAPI
- Databases: Milvus (vector database), Neo4j (graph database)
- Containerization: Docker

## Prerequisites

- Docker and Docker Compose
- Node.js and npm (for local development)
- Python 3.9+ (for local development)

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

## Development

To run the services individually for development:

### Frontend

1. Navigate to the `src` directory
2. Install dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm run dev
   ```

### Backend

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the FastAPI server:
   ```
   uvicorn server:app --reload
   ```

## Usage

1. Open the HADES web interface in your browser.
2. Enter your query in the input field.
3. The system will process your query using the following steps:
   - Parse and understand the query
   - Search for relevant information in Milvus
   - Query related data in Neo4j
   - Generate a response based on the collected information
4. View the results, including thoughts, actions, and observations from the ReAct framework.

## API Endpoints

- `POST /query`: Process a user query
  - Request body: `{ "query": "Your query here" }`
  - Response: `{ "result": "Processed result here" }`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Milvus for vector similarity search
- Neo4j for graph database capabilities
- FastAPI for the efficient Python web framework
- React for the frontend user interface