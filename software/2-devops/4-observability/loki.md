# Loki & LogQL

LogQL is the query language for **Grafana Loki** logs.

---

## Useful UI features (Grafana Explore)
- **Logs view** shows matching log lines for your query.
- **Sort** logs by newest/oldest.
- **Expand / Collapse** log lines to see full details.
- Tip: select text inside a log line and use **Filter** / **Exclude** to quickly refine the query.

---

## Core idea: select streams, then filter/process lines
Most LogQL queries look like:

1) Pick log streams by **labels**
2) Apply **pipeline stages** (filter, parse, format)

### 1. Stream selector (labels)
```logql
{container="myapp"}
```

---

## Common filters
### Substring match / exclude
```logql
{container="myapp"} |= "error"
```

```logql
{container="myapp"} != "healthcheck"
```

### Regex match / exclude
```logql
{container="myapp"} |~ "timeout|reset"
```

```logql
{container="myapp"} !~ "(/health|/metrics)"
```

---

## Parse JSON and filter by fields
If your log lines are JSON, you can parse them and then filter on keys:

```logql
{container="myapp"} | json | level="error"
```

---

## Format the output line
After parsing JSON, you can format the displayed log line:

```logql
{container="myapp"} | json | line_format "{{.downstream_local_address}} {{.response_code}} {{.method}} {{.path}}"
```

---

## Full example (search + parse + format)
```logql
{container="myapp"} |= "error" | json | line_format "{{.downstream_local_address}} {{.response_code}} {{.method}} {{.path}}"
```
