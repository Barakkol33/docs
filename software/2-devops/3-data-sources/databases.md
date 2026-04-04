# Databases

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

- https://redis.io/try-free/

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