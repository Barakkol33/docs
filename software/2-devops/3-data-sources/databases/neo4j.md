# Neo4j (Graph Databases)

A **graph database**: data is stored as nodes and relationships, and relationships are first-class citizens (stored as direct pointers, not computed by joins). Neo4j is the most popular; alternatives include Amazon Neptune, ArangoDB, JanusGraph.

**Good for:** highly connected data. Social networks, recommendations, fraud detection, knowledge graphs, network/IT topology, dependency and permission graphs.
**Not for:** simple tabular data, heavy aggregations over entire datasets, or when relationships are shallow (a SQL join is fine).

**Why not SQL?** Queries like "friends of friends of friends" need a join per hop. Cost grows with data size in SQL, but graph traversal cost depends only on the part of the graph you touch.

---

## Key concepts (Property Graph Model)

- **Node** – An entity, e.g. a Person.
- **Label** – Type tag on a node: `:Person`, `:Movie`. A node can have several.
- **Relationship** – Directed, typed connection between two nodes: `(a)-[:FOLLOWS]->(b)`.
- **Properties** – Key/value pairs on both nodes and relationships (`name`, `since`).
- **Cypher** – Declarative query language using ASCII-art patterns. (ISO **GQL** is the new standard, heavily Cypher-based.)
- **Index / Constraint** – Speed lookups of the starting nodes; `UNIQUE` constraints for IDs.
- **Traversal** – Walking relationships from a starting node.
- **Clustering** – Causal clustering with primaries and secondaries (Enterprise / Aura).
- **Graph algorithms (GDS)** – PageRank, community detection, shortest path.

---

## Run it locally

```bash
docker run -d --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password123 \
  neo4j:5
```

Browser UI: http://localhost:7474 (Bolt protocol on 7687).

---

## Examples (Cypher)

```cypher
// Create
CREATE (a:Person {name: 'Alice'})-[:FOLLOWS]->(b:Person {name: 'Bob'})
CREATE (b)-[:FOLLOWS]->(:Person {name: 'Carol'});

// Find who Alice follows
MATCH (a:Person {name: 'Alice'})-[:FOLLOWS]->(f)
RETURN f.name;

// Friends of friends (2 hops), excluding people already followed
MATCH (a:Person {name: 'Alice'})-[:FOLLOWS*2]->(fof)
WHERE NOT (a)-[:FOLLOWS]->(fof) AND a <> fof
RETURN DISTINCT fof.name;

// Shortest path
MATCH p = shortestPath((a:Person {name:'Alice'})-[:FOLLOWS*..6]-(c:Person {name:'Carol'}))
RETURN p;

// Upsert
MERGE (p:Person {name: 'Dave'}) SET p.city = 'Tel Aviv';

// Delete node and its relationships
MATCH (p:Person {name: 'Dave'}) DETACH DELETE p;
```
