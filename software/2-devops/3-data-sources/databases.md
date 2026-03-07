# Databases

---

## Cassandra

A distributed wide-column NoSQL database designed for huge scale, high write throughput, and always-on availability. No single leader; built for multi-datacenter setups.

**Key concepts:**

- **Keyspace** – Top-level namespace (like a database).
- **Table (wide-column)** – Rows can have many columns; optimized by primary key design.
- **Partition Key** – Determines which node stores the data (critical for performance).
- **Clustering Columns** – Define sort order within a partition.
- **Replication Factor (RF)** – How many copies of data exist.
- **Consistency Level** – Tradeoff between availability and consistency (`ONE`, `QUORUM`, `ALL`, etc.).
- **Ring Architecture** – Nodes arranged logically; data distributed via consistent hashing.
- **Gossip Protocol** – Nodes share cluster state.
- **SSTables / Memtables** – Write path structures, enabling fast sequential disk writes.
- **CQL** – Cassandra Query Language (SQL-like).

**Resources:** https://www.nan.fyi/database – short tutorial highlighting Cassandra concepts.

---

## Elasticsearch

A distributed search and analytics engine built on Lucene. Optimized for full-text search, filtering, and near real-time aggregation over large datasets.

**Key concepts:**

- **Index** – Logical namespace for documents (like a DB/table).
- **Document** – JSON record you search over.
- **Field / Mapping** – Field types and how they’re indexed (text, keyword, date, numeric).
- **Inverted Index** – Core search structure enabling fast text search.
- **Analyzer** – How text is tokenized/normalized (tokenizer + filters).
- **Shard** – A partition of an index; enables horizontal scale. Each index is split into primary shards, each with multiple replicas.
  - **Primary** – Source-of-truth for the index.
  - **Replica** – Copy for availability + read scaling.
- **Query DSL** – JSON-based query language (match, bool, term, range, aggregations).
- **Aggregations** – Built-in analytics (histograms, terms, metrics).
- **Near real-time** – Data searchable shortly after indexing (refresh interval).

**Examples:**

Get all:

```json
GET <index>/_search
{
  "query": {
    "match_all": {}
  }
}
```

Search:

```json
GET <index>/_search
{
  "query": {
    "match": {
      "type": {
        "query": "process"
      }
    }
  }
}
```

---

## MongoDB

A document-oriented NoSQL database. Stores data as flexible, JSON-like documents (BSON). Great when your data schema evolves or is hierarchical.

**Key concepts:**

- **Document** – A single record, like a JSON object.
- **Collection** – Group of documents (similar to a table).
- **BSON** – Binary JSON format Mongo uses internally.
- **Schema-flexible** – Documents in the same collection can have different fields.
- **Index** – Speeds up queries; supports single-field, compound, text, geospatial.
- **Aggregation Pipeline** – Framework for analytics/transformations (stages like `$match`, `$group`, `$project`).
- **Replica Set** – High availability via primary + secondary nodes, automatic failover.
- **Sharding** – Horizontal scaling by splitting collections across servers.

---

## Redis

An in-memory key-value data store. Extremely fast; used as cache, message broker, or lightweight database. Can persist to disk but primarily memory-first.

**Key concepts:**

- **Key-Value Store** – Data accessed by key.
- **Data Structures** – Strings, hashes, lists, sets, sorted sets, streams, bitmaps, hyperloglogs.
- **TTL / Expiration** – Keys auto-expire; core to caching.
- **Persistence:**
  - RDB snapshots (periodic dump)
  - AOF – Append Only File (log of writes)
- **Replication** – Primary + replicas for read scaling / high availability.
- **Sentinel** – Monitoring + automatic failover.
- **Cluster Mode** – Sharding across nodes.
- **Pub/Sub** – Message broadcasting channel system.
- **Lua Scripting** – Atomic server-side logic.
- **Pipelining** – Batch commands to reduce network overhead.

**Resources:**

- https://try.redis.io/

---

## ClickHouse

A high-performance, columnar database for real-time analytics on huge datasets. Built for fast aggregations and scans (dashboards, logs, events), not for lots of tiny transactional updates.

**Key concepts:**

- **Columnar Storage** – Data stored by column, so analytic queries that touch a few columns fly.
- **Table Engines** – Define how data is stored/replicated:
  - _MergeTree family_ – Default for large analytic tables; supports partitioning, sorting, TTL.
  - _ReplacingMergeTree / SummingMergeTree / AggregatingMergeTree_ – Variants for dedup or pre-aggregation.
- **Partitions** – Logical data chunks (often by date). Helps pruning during queries.
- **Primary Key / ORDER BY** – Not a uniqueness constraint; defines sort order on disk for fast range scans.
- **Sparse Indexing** – Index stores marks per granule, enabling skipping big blocks quickly.
- **Granules** – Smallest unit of data read (default ~8192 rows). Important for scan efficiency.
- **Materialized Views** – Precompute/roll up data into another table automatically.
- **Distributed Tables** – Query multiple shards as one logical table.
- **Replication** – Via ReplicatedMergeTree engines (coordinated with ZooKeeper/ClickHouse Keeper).
- **Compression** – Very strong due to columnar layout; huge space savings.
- **Joins** – Supported, but performance depends on data size and join type; design to minimize heavy joins.
- **INSERT-heavy, UPDATE-light** – Updates/deletes exist but are more expensive; best used append-only.

---

## YugabyteDB

An open-source, high-performance distributed PostgreSQL database.

- **Rule of thumb:** Use it unless your data volume is very large (then use Cassandra).
- **ACID-compliant** — you can perform operations across multiple rows or even multiple nodes, and the database guarantees they will either all succeed or all fail together.

**How is it different from regular PostgreSQL?**

While Yugabyte is "PostgreSQL-compatible" (it uses the upper half of the Postgres source code for its query layer), the engine underneath is entirely different:

- **Architecture** – Postgres is monolithic (one server). Yugabyte is distributed (a cluster of servers).
- **Scalability** – Postgres write scaling requires manual sharding or primary-replica setups. Yugabyte auto-shards data across all nodes — scale writes by adding servers.
- **Availability** – Postgres has downtime during failover. Yugabyte remains active with zero data loss using Raft consensus replication.

---

## PostgreSQL vs Cassandra

### PostgreSQL

The "safe" default for most applications. Choose it when your data has strict rules and complex questions.

- **Data Integrity (ACID)** – When handling money or sensitive records where a "partial" update is a disaster.
- **Complex Relationships** – You need to JOIN five different tables to generate a report.
- **Flexible Querying** – You don’t know exactly how you’ll search your data next month. Postgres allows ad-hoc queries on any indexed column.

### Cassandra

A specialized tool. Choose it when you have so much data that a single server would literally explode.

- **Write Speed is King** – Logging billions of sensor readings (IoT), clicks, or chat messages per second. Built for "high-velocity ingestion."
- **Predictable Queries** – You already know exactly how you will query the data (e.g., "Get all messages for User X"). You model your data for the query, not for the relationship.
