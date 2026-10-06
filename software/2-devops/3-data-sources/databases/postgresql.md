# PostgreSQL

The most popular open-source **relational** database. Full SQL, strong ACID guarantees, and a huge extension ecosystem. If you don't know which database to pick, Postgres is the safe default.

**Good for:** OLTP applications (users, orders, payments), anything needing joins and transactions, JSON + relational in one place, geospatial (PostGIS), vector search (pgvector).
**Not ideal for:** huge analytical scans (use a columnar DB like [ClickHouse](../databases.md#clickhouse)), extreme write scale across many nodes without extra tooling.

---

## Key concepts

- **Database / Schema / Table** – A server hosts many databases; each has schemas (namespaces, default `public`) that contain tables.
- **Row / Column / Types** – Strongly typed: `int`, `text`, `timestamptz`, `uuid`, `numeric`, `boolean`, arrays, `jsonb`, enums.
- **Primary key / Foreign key / Constraints** – Enforce integrity: `PRIMARY KEY`, `UNIQUE`, `NOT NULL`, `CHECK`, `REFERENCES`.
- **Index** – Speeds up reads at the cost of writes and disk. Types:
  - _B-tree_ (default) – equality and range
  - _GIN_ – `jsonb`, arrays, full-text
  - _GiST_ – geometric / range types
  - _BRIN_ – huge, naturally ordered tables (e.g. time series)
- **Transaction / ACID** – `BEGIN … COMMIT`. All-or-nothing, isolated from other transactions.
- **MVCC** – Multi-Version Concurrency Control: readers don't block writers. Updates create new row versions; old ones are cleaned up later.
- **VACUUM / autovacuum** – Reclaims dead row versions. Disabled or starved autovacuum = table bloat and slow queries.
- **WAL (Write-Ahead Log)** – Every change is logged before being applied. Basis for crash recovery, replication and point-in-time recovery.
- **Replication**
  - _Streaming (physical)_ – Replica is a byte-for-byte copy, read-only. Used for HA and read scaling.
  - _Logical_ – Replicate selected tables, can cross versions.
- **Failover** – Postgres itself doesn't elect a leader. Use Patroni, a managed service (RDS, Cloud SQL), or a Kubernetes operator (CloudNativePG, Zalando).
- **Connection pooling** – Each connection is an OS process, so connections are expensive. Put **PgBouncer** in front.
- **Extensions** – `CREATE EXTENSION ...`: `postgis`, `pgvector`, `pg_stat_statements`, `timescaledb`, `pg_trgm`.
- **EXPLAIN (ANALYZE)** – Shows the query plan and real timings. First tool for slow queries.

---

## Run it locally

```bash
docker run -d --name pg \
  -e POSTGRES_PASSWORD=secret \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16

docker exec -it pg psql -U postgres
```

---

## Examples

```sql
CREATE TABLE users (
  id         bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email      text NOT NULL UNIQUE,
  profile    jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE orders (
  id      bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id bigint NOT NULL REFERENCES users(id),
  total   numeric(10,2) NOT NULL
);

CREATE INDEX idx_orders_user ON orders(user_id);

-- Join + aggregate
SELECT u.email, count(*) AS orders, sum(o.total) AS spent
FROM users u JOIN orders o ON o.user_id = u.id
GROUP BY u.email
ORDER BY spent DESC
LIMIT 10;

-- JSON query
SELECT email FROM users WHERE profile->>'country' = 'IL';

-- Why is it slow?
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 42;
```

## psql cheat sheet

| Command | Purpose |
|---|---|
| `\l` | List databases |
| `\c mydb` | Connect to a database |
| `\dt` | List tables |
| `\d tablename` | Describe a table |
| `\du` | List roles |
| `\x` | Toggle expanded output |
| `\q` | Quit |

## Backup & restore

```bash
pg_dump -U postgres -Fc mydb > mydb.dump       # logical backup
pg_restore -U postgres -d mydb mydb.dump
pg_dumpall -U postgres > everything.sql         # all databases + roles
```

For production: continuous WAL archiving + base backups (pgBackRest, Barman) enables **point-in-time recovery**.

**Managed:** AWS RDS / Aurora PostgreSQL, GCP Cloud SQL / AlloyDB, Azure Database for PostgreSQL.
