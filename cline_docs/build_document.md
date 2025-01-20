# Build Document for HADES (Heuristic Adaptive Data Extraction System)

## Prerequisites
- Node.js (LTS version recommended)
- npm (package manager)
- Docker (optional for containerized installation)

---

## Local Installation of ArangoDB

### Dependencies
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

3. Configure ArangoDB during installation:
   - Set a secure root password.
   - Ensure port `8529` is open and accessible.

4. Start the service:
   ```bash
   sudo systemctl start arangodb3
   sudo systemctl enable arangodb3
   ```

5. Verify installation at `http://localhost:8529`.

---

## Docker Installation of ArangoDB

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

## MCP Server Setup

1. Clone the HADES repository:
   ```bash
   git clone https://github.com/r3d91ll/H.A.D.E.S.git
   cd H.A.D.E.S
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build the server:
   ```bash
   npm run build
   ```

4. Run the server:
   ```bash
   node build/index.js
   ```

---

## Environment Variables

Configure the MCP server with these environment variables:

- `ARANGO_URL`: ArangoDB server URL (default: `http://localhost:8529`).
- `ARANGO_DATABASE`: Database name.
- `ARANGO_USERNAME`: Database user.
- `ARANGO_PASSWORD`: Database password.

---

## Integration Examples

### AQL Queries
Example query for inserting data:
```javascript
{
  "query": "INSERT INTO your-collection OBJECT { ... }"
}
```

### Vector Search
Example vector search payload:
```json
{
  "collection": "your-collection",
  "vector": [0.1, 0.2, 0.3],
  "limit": 5
}
```

---

## Troubleshooting

### Debugging MCP Communication
Use the MCP Inspector:
```bash
npm run inspector
```

### Logs
- MCP server logs to `stdout`.
- Configure logging for file output.

### Docker Logs
```bash
docker logs arangodb
```

---

## License & Support
This project is MIT licensed. For support, contact internal maintainers or the repository maintainers.
