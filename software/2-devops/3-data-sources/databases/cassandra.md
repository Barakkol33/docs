# Apache Cassandra

A distributed **wide-column** NoSQL database built for massive write throughput, linear horizontal scaling and no single point of failure. Every node is equal (masterless). ScyllaDB is a compatible, C++ re-implementation.

**Good for:** huge write-heavy workloads (events, IoT, messaging, activity feeds), multi-datacenter replication, always-on availability.
**Not for:** ad-hoc queries, joins, aggregations, strong cross-row transactions, or small datasets (a single Postgres is simpler).

> **Mindset shift:** in relational DBs you model the data, then write queries. In Cassandra you **start from the queries** and design one table per query pattern. Denormalization and duplication are normal.

---

## Key concepts

- **Cluster / Node / Datacenter / Rack** – A ring of equal nodes, grouped by DC and rack for placement.
- **Keyspace** – Like a database. Defines the **replication strategy** and **replication factor (RF)**.
- **Table** – Rows grouped by partition. Schema is defined up front (CQL, a SQL-like language).
- **Primary key = partition key + clustering columns**
  - _Partition key_ – Hashed to decide which nodes own the data. All rows with the same partition key live together.
  - _Clustering columns_ – Sort order of rows **within** a partition.
- **Partition** – Unit of distribution. Keep partitions bounded (rough guide: < 100 MB). Unbounded partitions are the #1 modeling mistake.
- **Token ring / vnodes** – Hash space is split among nodes; adding a node moves only part of the data.
- **Replication factor** – Number of copies (typically 3 per DC).
- **Consistency level (per query)** – How many replicas must respond:
  - `ONE`, `QUORUM`, `LOCAL_QUORUM`, `ALL`
  - `R + W > RF` gives strong consistency (e.g. QUORUM reads + QUORUM writes).
- **Write path** – Commit log (durable) → memtable (memory) → flushed to immutable **SSTables**. Writes are append-only, hence fast.
- **Compaction** – Background merging of SSTables. Strategies: STCS, LCS, TWCS (time series).
- **Tombstones** – Deletes are markers, removed after `gc_grace_seconds`. Many tombstones hurt reads.
- **Gossip** – Nodes exchange state peer-to-peer.
- **Hinted handoff / read repair / anti-entropy repair** – Mechanisms that converge replicas. Run `nodetool repair` regularly.
- **Lightweight transactions (LWT)** – `IF NOT EXISTS` compare-and-set via Paxos. Slow, use sparingly.
- **TTL** – Per-row/column expiry, handy for time-bound data.

---

## Run it locally

```bash
docker run -d --name cassandra -p 9042:9042 cassandra:5
# wait ~1 min for startup
docker exec -it cassandra cqlsh
```

---

## Examples (CQL)

```sql
CREATE KEYSPACE shop WITH replication =
  {'class': 'SimpleStrategy', 'replication_factor': 1};
USE shop;

-- Query: "latest events for a user"
CREATE TABLE events_by_user (
  user_id    uuid,
  ts         timestamp,
  event_type text,
  payload    text,
  PRIMARY KEY ((user_id), ts)
) WITH CLUSTERING ORDER BY (ts DESC);

INSERT INTO events_by_user (user_id, ts, event_type, payload)
VALUES (uuid(), toTimestamp(now()), 'login', '{}');

SELECT * FROM events_by_user WHERE user_id = <uuid> LIMIT 10;
```

Queries **must** include the partition key; otherwise you'd need `ALLOW FILTERING` (full scan, avoid).

```bash
nodetool status      # cluster health (UN = Up/Normal)
nodetool repair      # anti-entropy repair
nodetool tablestats  # per-table stats
```

**Managed:** AWS Keyspaces, Azure Managed Instance for Apache Cassandra / Cosmos DB (Cassandra API), DataStax Astra DB.
