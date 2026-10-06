# Databases

There is no "best" database, only the best fit for a workload. This page is the map; each database has its own section or page with key concepts and examples.

## Choosing a database

| Type | Examples | Best for | Watch out for |
|---|---|---|---|
| **Relational (SQL)** | [PostgreSQL](databases/postgresql.md), [MySQL/MariaDB](databases/mysql.md), [SQLite](databases/sqlite.md), SQL Server, Oracle | Transactions, structured data, joins, integrity. **The default choice.** | Scaling writes beyond one primary needs effort |
| **Document** | [MongoDB](#mongodb), Couchbase, Firestore | Flexible/hierarchical JSON, evolving schemas | Joins and multi-document transactions are weaker |
| **Key-value** | [Redis](#redis), [DynamoDB](databases/dynamodb.md), etcd, Memcached | Caching, sessions, lookups by key at massive scale | Query only by key; limited ad-hoc queries |
| **Wide-column** | [Cassandra](databases/cassandra.md), ScyllaDB, HBase, Bigtable | Huge write-heavy, multi-DC, always-on | Must model per query; no joins |
| **Columnar / OLAP** | [ClickHouse](#clickhouse), BigQuery, Redshift, Snowflake | Analytics and aggregations over billions of rows | Poor at frequent single-row updates |
| **Search** | [Elasticsearch](#elasticsearch), OpenSearch, Solr | Full-text search, log search, faceting | Not a system of record |
| **Graph** | [Neo4j](databases/neo4j.md), Neptune | Highly connected data, recommendations, fraud | Not for plain tabular data |
| **Time-series** | [InfluxDB, TimescaleDB](databases/timeseries.md), Prometheus | Metrics, IoT, events over time | High-cardinality tags |

### Pages in this section

| Page | Type |
|---|---|
| [PostgreSQL](databases/postgresql.md) | Relational |
| [MySQL / MariaDB](databases/mysql.md) | Relational |
| [SQLite](databases/sqlite.md) | Embedded relational |
| [Cassandra](databases/cassandra.md) | Wide-column |
| [DynamoDB](databases/dynamodb.md) | Managed key-value / document (AWS) |
| [Neo4j](databases/neo4j.md) | Graph |
| [InfluxDB & TimescaleDB](databases/timeseries.md) | Time-series |
| [Elasticsearch](#elasticsearch), [MongoDB](#mongodb), [Redis](#redis), [ClickHouse](#clickhouse) | Below on this page |

### Concepts that apply to every database

- **ACID** – _Atomicity_ (all or nothing), _Consistency_ (constraints hold), _Isolation_ (concurrent transactions don't interfere), _Durability_ (committed data survives crashes). Classic relational guarantees.
- **CAP theorem** – During a network **P**artition, a distributed system must choose between **C**onsistency and **A**vailability. Many NoSQL systems pick availability (eventual consistency); many SQL systems pick consistency.
- **Eventual consistency** – Replicas may briefly disagree but converge.
- **Replication** – Copies of data on several nodes: high availability + read scaling.
- **Sharding / partitioning** – Splitting data across nodes: write scaling.
- **Indexes** – Make reads fast, writes slower, use disk. Index what you filter and join on.
- **Backups** – A replica is **not** a backup (a bad `DELETE` replicates too). Test restores, and know your **RPO** (how much data you can lose) and **RTO** (how long recovery may take).
- **Connection pooling** – Databases handle a limited number of connections; use a pooler or app-level pool.
- **Running in Kubernetes** – Stateful databases need StatefulSets, PersistentVolumes and a backup story. In production consider an operator or a managed cloud service (see [cloud](../5-cloud/cloud.md)).

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