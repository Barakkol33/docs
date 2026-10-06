# SQLite

A **serverless, embedded** relational database. The whole database is a single file, and the engine is a library linked into your application. No daemon, no network, no configuration. The most widely deployed database in the world (phones, browsers, desktop apps).

**Good for:** local/dev databases, tests, mobile and desktop apps, CLI tools, small websites, edge devices, data analysis on a file.
**Not for:** many concurrent writers, multi-server access over the network, or large-scale production services.

---

## Key concepts

- **Single file** – Database lives in one `.db` file (plus `-wal`/`-shm` files in WAL mode). Backup = copy the file (safely, see below).
- **Serverless** – Runs inside your process; access is by file I/O.
- **Dynamic typing** – Column types are "affinities"; SQLite is lenient. Use `STRICT` tables to enforce types.
- **One writer at a time** – Many concurrent readers, but writes are serialized.
- **WAL mode** – `PRAGMA journal_mode=WAL;` lets readers and a writer work concurrently. Recommended for almost every app.
- **Transactions** – Fully ACID. Wrap bulk inserts in a transaction, it's orders of magnitude faster.
- **PRAGMAs** – Per-connection settings: `foreign_keys=ON` (off by default!), `journal_mode`, `synchronous`, `busy_timeout`.
- **Extensions** – FTS5 (full-text search), JSON1, R*Tree. Related tools: **Litestream** (continuous replication to S3), **LiteFS**, **libSQL/Turso**.

---

## Examples

```bash
sqlite3 app.db
```

```sql
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE notes (
  id    INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  body  TEXT
) STRICT;

INSERT INTO notes (title, body) VALUES ('hello', 'world');
SELECT * FROM notes;
```

| Command | Purpose |
|---|---|
| `.tables` | List tables |
| `.schema notes` | Show CREATE statement |
| `.mode column` / `.headers on` | Nicer output |
| `.import file.csv table` | Load CSV |
| `.backup backup.db` | Consistent online backup |
| `.quit` | Exit |

Python has it built in:

```python
import sqlite3
con = sqlite3.connect("app.db")
con.execute("CREATE TABLE IF NOT EXISTS t (x)")
con.commit()
```
