const express = require('express');
const cors = require('cors');
const { MilvusClient } = require('@zilliz/milvus2-sdk-node');
const neo4j = require('neo4j-driver');

const app = express();
app.use(cors());
app.use(express.json());

// Milvus client setup
const milvusClient = new MilvusClient('milvus:19530');

// Neo4j driver setup
const neo4jDriver = neo4j.driver(
  'bolt://neo4j:7687',
  neo4j.auth.basic('neo4j', 'password')
);

// ReAct-like function to generate thoughts and actions
function generateReactOutput(prompt) {
  // This is a placeholder. In a real implementation, this would call an AI model.
  const thoughts = [
    "I need to determine what kind of query this is.",
    "Based on the keywords, I can decide which database to query.",
    "After getting the results, I should format them for the user."
  ];
  const actions = [
    { type: 'search_milvus', input: prompt },
    { type: 'query_neo4j', input: prompt }
  ];
  return { thoughts, actions };
}

// Function to execute actions
async function executeAction(action) {
  switch (action.type) {
    case 'search_milvus':
      return await searchMilvus(action.input);
    case 'query_neo4j':
      return await queryNeo4j(action.input);
    default:
      return `Unknown action type: ${action.type}`;
  }
}

async function searchMilvus(query) {
  // Simulated Milvus query
  try {
    const result = await milvusClient.search({
      collection_name: 'example_collection',
      vector: [0.1, 0.2, 0.3], // Example vector
      limit: 5,
    });
    return JSON.stringify(result);
  } catch (error) {
    console.error('Milvus search error:', error);
    return 'Error searching Milvus';
  }
}

async function queryNeo4j(query) {
  // Simulated Neo4j query
  const session = neo4jDriver.session();
  try {
    const result = await session.run(
      'MATCH (n) RETURN n LIMIT 5'
    );
    return JSON.stringify(result.records.map(record => record.get('n').properties));
  } catch (error) {
    console.error('Neo4j query error:', error);
    return 'Error querying Neo4j';
  } finally {
    await session.close();
  }
}

app.post('/query', async (req, res) => {
  const { query } = req.body;

  try {
    const reactOutput = generateReactOutput(query);
    let finalResult = '';

    for (const thought of reactOutput.thoughts) {
      finalResult += `Thought: ${thought}\n`;
    }

    for (const action of reactOutput.actions) {
      finalResult += `Action: ${action.type}[${action.input}]\n`;
      const actionResult = await executeAction(action);
      finalResult += `Observation: ${actionResult}\n`;
    }

    finalResult += `Answer: Based on the observations, here's a summary...`; // You'd generate a real summary here

    res.json({ result: finalResult });
  } catch (error) {
    console.error('Error processing query:', error);
    res.status(500).json({ error: 'An error occurred while processing the query' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});