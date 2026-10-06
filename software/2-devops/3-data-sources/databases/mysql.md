# MySQL / MariaDB

A widely deployed open-source **relational** database. Powers a large share of the web (WordPress, many SaaS backends). MariaDB is a community fork that is largely drop-in compatible.

**Good for:** classic web OLTP workloads, read-heavy apps with replicas, simple operations, huge hosting/tooling ecosystem.
**Compared to Postgres:** historically simpler and very fast for basic reads; Postgres has richer SQL features, types and extensions.

---

## Key concepts

- **Storage engine** – MySQL is pluggable. Use **InnoDB** (default): transactions, row-level locking, foreign keys, crash recovery. MyISAM is legacy, don't use it.
- **Clustered index** – In InnoDB the table *is* the primary key B-tree. Rows are physically ordered by PK, so a short, monotonically increasing PK (auto-increment / UUIDv7) performs best. Secondary indexes store the PK value.
- **Transactions & isolation** – Default isolation is `REPEATABLE READ`. Uses MVCC plus gap locks.
- **Binary log (binlog)** – Log of all changes. Drives replication and point-in-time recovery.
- **Redo log / undo log** – Crash recovery and MVCC inside InnoDB.
- **Replication**
  - _Source → replica_ (async by default; semi-sync available). Replicas serve reads.
  - _GTID_ – Global transaction IDs make failover and re-pointing replicas easy.
  - _Group Replication / InnoDB Cluster_ – Built-in multi-node HA with automatic failover.
- **Character set** – Use `utf8mb4` (real UTF-8). The old `utf8` is a 3-byte subset.
- **Slow query log** – First place to look for performance problems.
- **Proxies** – ProxySQL / MySQL Router for routing reads/writes and pooling.

---

## Run it locally

```bash
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=app \
  -p 3306:3306 \
  -v mysqldata:/var/lib/mysql \
  mysql:8

docker exec -it mysql mysql -uroot -p
```

---

## Examples

```sql
CREATE TABLE users (
  id         BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  email      VARCHAR(255) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SHOW INDEX FROM users;
EXPLAIN SELECT * FROM users WHERE email = 'a@b.com';

-- Replication status
SHOW REPLICA STATUS\G
```

| Command | Purpose |
|---|---|
| `SHOW DATABASES;` | List databases |
| `USE app;` | Select database |
| `SHOW TABLES;` | List tables |
| `DESCRIBE users;` | Describe a table |
| `SHOW PROCESSLIST;` | Running queries |

## Backup & restore

```bash
mysqldump -uroot -p --single-transaction app > app.sql
mysql -uroot -p app < app.sql
```

For large datasets: Percona XtraBackup / MySQL Enterprise Backup (physical, hot backups) plus binlogs for PITR.

**Managed:** AWS RDS / Aurora MySQL, GCP Cloud SQL, Azure Database for MySQL.
