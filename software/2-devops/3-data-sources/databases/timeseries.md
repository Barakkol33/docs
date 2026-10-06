# Time-Series Databases (InfluxDB & TimescaleDB)

Databases optimized for data that arrives continuously with a timestamp: metrics, sensor readings, stock ticks, events. Workload is append-heavy, queries are by time range and aggregated (avg/max per 5 min), and old data is downsampled or dropped.

> You already met one: **Prometheus** (see [metrics.md](../../4-observability/metrics.md)) is a time-series DB for infrastructure metrics. [ClickHouse](../databases.md#clickhouse) is also very popular for this.

---

## Common concepts

- **Measurement / metric** – What is measured (`cpu_usage`).
- **Tags / labels** – Indexed metadata describing the series (`host=web1`, `region=eu`).
- **Fields / values** – The actual numbers (`usage=73.2`).
- **Series** – Unique combination of metric + tags. **High cardinality** (millions of unique tag combos, e.g. a user ID as tag) is the classic way to kill a time-series DB.
- **Retention policy** – Automatically delete data older than N days.
- **Downsampling / rollups** – Store raw data short term, aggregated data long term.
- **Compression** – Time-ordered data compresses extremely well.

---

## InfluxDB

Purpose-built TSDB. Data model: `measurement,tag=value field=value timestamp` (line protocol).

- **Bucket** – Named container with a retention period (InfluxDB 2.x/3.x).
- **Organization / Token** – Multi-tenancy and auth.
- **Flux / InfluxQL / SQL** – Query languages (v3 uses SQL).
- **Tasks** – Scheduled queries for downsampling.
- Typically fed by **Telegraf** (collection agent with hundreds of plugins).

```bash
docker run -d --name influx -p 8086:8086 influxdb:2

# write (line protocol) and query (Flux)
influx write -b mybucket 'cpu,host=web1 usage=73.2'
influx query 'from(bucket:"mybucket") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "cpu") |> mean()'
```

---

## TimescaleDB

A **PostgreSQL extension**. You keep full SQL, joins, and the whole Postgres ecosystem, and get time-series superpowers.

- **Hypertable** – Looks like one table, internally auto-partitioned into time **chunks**.
- **Continuous aggregates** – Incrementally maintained materialized views (rollups).
- **Compression** – Native columnar compression of older chunks (often 90%+ savings).
- **Retention policies** – `add_retention_policy`.
- Time-bucketing: `time_bucket('5 minutes', ts)`.

```bash
docker run -d --name tsdb -e POSTGRES_PASSWORD=secret -p 5432:5432 timescale/timescaledb:latest-pg16
```

```sql
CREATE TABLE metrics (
  ts    timestamptz NOT NULL,
  host  text NOT NULL,
  cpu   double precision
);
SELECT create_hypertable('metrics', 'ts');

SELECT time_bucket('5 minutes', ts) AS bucket, host, avg(cpu)
FROM metrics
WHERE ts > now() - interval '1 day'
GROUP BY bucket, host
ORDER BY bucket;

SELECT add_retention_policy('metrics', INTERVAL '30 days');
```

## Which one?

| | InfluxDB | TimescaleDB |
|---|---|---|
| Query language | Flux / InfluxQL / SQL | Full SQL |
| Joins with relational data | Limited | Native |
| Ecosystem | Telegraf, own tooling | All of Postgres |
| Pick when | Pure metrics/IoT pipeline | You already use Postgres, or need SQL + joins |
