# Welcome to HADES - Heuristic Adaptive Data Extraction System

## An ArnagoDB server with Model Context Protocol built in

The **HADES MCP Server** integrates:

- **ArangoDB** for document storage
- A **TypeScript-based Model Context Protocol (MCP) server** for seamless ArangoDB integration.

This server handles **search, query execution, and other operations** via custom tools, making it extensible for various workflows, including LLM-based RAG systems.

---

## Features

### TypeScript-based MCP Server

Provides database interaction capabilities through ArangoDB, including:

- `arango_query`: Execute AQL queries with optional bind variables.
- `arango_insert`: Insert documents into collections.
- `arango_update`: Update existing documents by key.
- `arango_remove`: Remove documents from collections.
- `arango_backup`: Backup collections to JSON files.
- `arango_list_collections`: List all collections in the database.
- `arango_create_collection`: Create a new collection.

---

## Sample Docker Setup (ArangoDB)

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

1. Save the above as `docker-compose.yml`.
2. Run `docker-compose up -d`.
3. Access ArangoDB at `http://localhost:8529` (user: `root`, pass: `p@$$W0rd`).

---

## Configuration for TypeScript MCP Server

Update the server configuration for tools like Claude or Cline:

```json
{
  "mcpServers": {
    "arango": {
      "command": "node",
      "args": ["/path/to/arango-server/build/index.js"],
      "env": {
        "ARANGO_URL": "http://localhost:8529",
        "ARANGO_DATABASE": "my_database",
        "ARANGO_USERNAME": "root",
        "ARANGO_PASSWORD": "p@$$W0rd"
      }
    }
  }
}
```

### Environment Variables

- `ARANGO_URL`: ArangoDB server URL (default port is `8529`).
- `ARANGO_DATABASE`: Database name.
- `ARANGO_USERNAME`: Database user.
- `ARANGO_PASSWORD`: Database password.

---

## Cline Integration

The MCP server can be integrated with the **Cline VSCode Extension** to simplify debugging and interaction:

1. **Install the MCP server into Cline**:

   ```bash
   cline add ./build/index.js
   ```

   This command registers the MCP server from the current working directory.

2. **Verify Installation**:
   After adding the server, check Cline’s configuration file:
   - MacOS: `~/Library/Application Support/Code/User/globalStorage/cline.cline/config.json`
   - Windows: `%APPDATA%/Code/User/globalStorage/cline.cline/config.json`

   Ensure the configuration includes:

   ```json
   {
     "command": "node",
     "args": ["./build/index.js"],
     "env": {
       "ARANGO_URL": "http://localhost:8529",
       "ARANGO_DATABASE": "my_database",
       "ARANGO_USERNAME": "root",
       "ARANGO_PASSWORD": "p@$$W0rd"
     }
   }
   ```

3. **Usage in Cline**:
   - Open Cline in VSCode.
   - Issue commands like "List all collections in the database" or "Insert a document into users collection."
   - The MCP server will handle these operations seamlessly.

---

## Debugging

For stdio-based MCP communication:

- Use [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

  ```bash
  npm run inspector
  ```

---

## Acknowledgments

We extend our gratitude to the team behind the original [ArangoDB MCP Server](https://github.com/ravenwits/mcp-server-arangodb). Their work has been invaluable in providing the foundation for integrating MCP functionality with ArangoDB. This project builds upon their efforts to deliver enhanced RAG capabilities.

## License & Support

This project is licensed under the MIT License. For issues, please consult your internal support or the repository maintainers.

*Enjoy building your RAG workflows with the HADES MCP Server!*
