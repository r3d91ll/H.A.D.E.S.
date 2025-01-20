<div align="center">

# Welcome to HADES - Heuristic Adaptive Data Extraction System

## An ArangoDB server with Model Context Protocol built in

</div>

***NOTE THIS BRANCH OF THE REPO IS JUST FOR THOSE WHO WANT TO HAVE A ARANGO DB SERVER AND MCP SERVER RUNNING LOCALLY. nO FURTHER WORK OR DEVELOPMENT WILL BE DONE ON THIS BRANCH!!***

**HADES (Heuristic Adaptive Data Extraction System)** is a lightweight foundation for a multi-modal RAG (Retrieval-Augmented Generation) solution, designed to be stable and efficient for small office and home lab environments. This project focuses on integrating:

- **ArangoDB**: For document storage and vector similarity search using FAISS.
- **Model Context Protocol (MCP) Server**: Provides seamless interaction with ArangoDB via TypeScript.

---

## Objective

This project aims to provide:

- A stable, production-ready backend for RAG systems in small-scale environments.
- A flexible base for future development of multi-modal solutions.
- Integration of a locally installed or Dockerized ArangoDB instance with an MCP server.

---

## 1. Installing ArangoDB

### Option A: Local Installation (Recommended for Stability)

1. **Add the ArangoDB Repository**:

   ```bash
   wget -q https://download.arangodb.com/arangodb42/DEBIAN/Release.key -O- | sudo apt-key add -
   echo 'deb https://download.arangodb.com/arangodb42/DEBIAN/ /' | sudo tee /etc/apt/sources.list.d/arangodb.list
   ```

2. **Install ArangoDB**:

   ```bash
   sudo apt-get update
   sudo apt-get install -y arangodb3
   ```

3. **Configure ArangoDB**:
   - During installation, set a secure root password.
   - Ensure port `8529` is open and accessible.
4. **Start the ArangoDB Service**:

   ```bash
   sudo systemctl start arangodb3
   sudo systemctl enable arangodb3
   ```

5. **Verify Installation**:
   Navigate to `http://localhost:8529` and log in with the root credentials.

### Option B: Docker Installation

For containerized environments:

1. Create a `docker-compose.yml` file:

   ```yaml
   version: "3.8"
   services:
     arangodb:
       image: arangodb:3.10
       container_name: arangodb
       ports:
         - "8529:8529"
       environment:
         - ARANGO_ROOT_PASSWORD=p@$$W0rd
   ```

2. Start the container:

   ```bash
   docker-compose up -d
   ```

3. Access ArangoDB at `http://localhost:8529`.

---

## 2. Installing the ArangoDB MCP Server

This project includes a merged version of the [ArangoDB MCP Server](https://github.com/ravenwits/mcp-server-arangodb). Follow these steps to set it up:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/r3d91ll/H.A.D.E.S.git
   cd H.A.D.E.S
   ```

2. **Configure Environment Variables**:

   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit the .env file with your preferred settings
   nano .env
   ```

3. **Run the Setup Script**:

   ```bash
   # Make the setup script executable
   chmod +x setup.sh
   
   # Run the setup script
   ./setup.sh
   ```

   The setup script will:
   - Check for required dependencies (Docker, Docker Compose, npm)
   - Create a .env file if it doesn't exist
   - Build and start the ArangoDB container
   - Install npm dependencies
   - Build the TypeScript project

4. **Run the Server**:

   ```bash
   node build/index.js
   ```

### Environment Variables

The following environment variables can be configured in your `.env` file:

- `ARANGO_URL`: ArangoDB server URL (default: `http://localhost:8529`)
- `ARANGO_DATABASE`: Database name (default: `hades`)
- `ARANGO_USERNAME`: Database user (default: `root`)
- `ARANGO_PASSWORD`: Database password
- `ARANGO_CONTAINER_NAME`: Docker container name (optional)
- `ARANGO_PORT`: ArangoDB port (optional, default: `8529`)

> **Security Note**: Never commit your `.env` file to version control. The repository includes an `env.example` file as a template.

---

## 3. Integration with RAG Solutions

- Use the MCP server for AQL queries, vector searches, and database operations.
- Example queries and JSON payloads for operations like `insert`, `update`, and `remove` are included in the documentation.

---

## 4. Debugging & Troubleshooting

### TypeScript Module Compatibility

If you encounter TypeScript build errors related to ES modules (errors mentioning `CommonJS module` and `ECMAScript module`), this is due to module system compatibility. To resolve this:

1. Ensure your `package.json` includes the `"type": "module"` field:

   ```json
   {
     "name": "arango-server",
     "version": "0.4.0",
     "type": "module",
     ...
   }
   ```

2. Update build scripts in `package.json` to use ES module syntax:

   ```json
   {
     "scripts": {
       "build": "tsc && node --eval \"import('fs').then(fs => fs.chmodSync('build/index.js', '755'))\"",
       "watch": "tsc --watch && node --eval \"import('fs').then(fs => fs.chmodSync('build/index.js', '755'))\""
     }
   }
   ```

3. Verify your `tsconfig.json` has the correct module settings:

   ```json
   {
     "compilerOptions": {
       "module": "Node16",
       "moduleResolution": "Node16",
       ...
     }
   }
   ```

These settings ensure proper compatibility with ES modules used by the Model Context Protocol SDK.

### MCP Communication

- **Debugging MCP Communication**:
  Use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) for stdio-based debugging:

  ```bash
  npm run inspector
  ```

- **Logs**:
  - MCP server logs output to `stdout` by default.
  - Configure the `logging` module to redirect logs to a file for easier analysis.

- **Docker Logs**:

  ```bash
  docker logs arangodb
  ```

---

## Acknowledgments

We extend our gratitude to the team behind the original [ArangoDB MCP Server](https://github.com/ravenwits/mcp-server-arangodb). Their work has provided a robust foundation for this project, enabling seamless integration with ArangoDB.

---

## License & Support

This project is licensed under the MIT License. For support, consult your internal maintainers or the repository maintainers.

*Enjoy building your RAG workflows with the HADES MCP Server!*
