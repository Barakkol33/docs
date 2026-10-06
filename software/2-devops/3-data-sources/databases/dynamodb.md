# Amazon DynamoDB

A fully **managed, serverless key-value / document** database from AWS. Single-digit-millisecond latency at practically any scale, with no servers, patching or capacity planning (if you want). Azure's rough equivalents: Cosmos DB; GCP: Firestore / Bigtable.

**Good for:** serverless apps (Lambda), shopping carts, sessions, gaming state, IoT, any workload with well-known access patterns that must scale unpredictably.
**Not for:** ad-hoc analytics, complex joins, or workloads whose access patterns keep changing. AWS-only (vendor lock-in).

> Like Cassandra: **design the table around your access patterns**. Often a single table holds multiple entity types.

---

## Key concepts

- **Table** – Top-level container. No fixed schema except the key.
- **Item** – A record (up to 400 KB), a set of attributes.
- **Attribute** – Name/value pair: string, number, binary, boolean, null, list, map, sets.
- **Primary key** (chosen at creation, immutable)
  - _Partition key only_ – Simple key.
  - _Partition key + sort key_ – Composite key; items with same partition key are stored together, ordered by sort key.
- **Partition** – Internal storage unit; data is spread by hashing the partition key. A "hot" key (one key getting most traffic) causes throttling, so choose high-cardinality keys.
- **Secondary indexes**
  - _LSI_ (local) – Same partition key, different sort key. Must be created with the table.
  - _GSI_ (global) – Different partition + sort key, separate throughput, eventually consistent. Can be added any time.
- **Query vs Scan**
  - `Query` – Efficient: uses the key. Always prefer.
  - `Scan` – Reads the entire table. Expensive, avoid in production paths.
- **Capacity modes**
  - _On-demand_ – Pay per request, scales automatically. Good default.
  - _Provisioned_ – Set RCU/WCU (read/write capacity units), optionally with auto scaling. Cheaper at steady load.
- **Consistency** – Reads are eventually consistent by default; request strongly consistent reads (2× cost) when needed. Transactions (`TransactWriteItems`) supported.
- **TTL** – Attribute with expiry timestamp; items auto-deleted.
- **DynamoDB Streams** – Ordered change feed; commonly triggers Lambda functions.
- **Global tables** – Multi-region, multi-active replication.
- **Backups** – On-demand and Point-in-Time Recovery (PITR). Export to S3.
- **DAX** – In-memory cache in front of DynamoDB (microsecond reads).
- **Conditional writes** – `ConditionExpression` gives optimistic locking / "insert if not exists".

---

## Run it locally

```bash
docker run -d --name ddb -p 8000:8000 amazon/dynamodb-local
export AWS_ACCESS_KEY_ID=x AWS_SECRET_ACCESS_KEY=x AWS_DEFAULT_REGION=us-east-1
```

---

## Examples (AWS CLI)

```bash
EP="--endpoint-url http://localhost:8000"   # drop for real AWS

aws dynamodb create-table $EP \
  --table-name Orders \
  --attribute-definitions AttributeName=customerId,AttributeType=S AttributeName=orderId,AttributeType=S \
  --key-schema AttributeName=customerId,KeyType=HASH AttributeName=orderId,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST

aws dynamodb put-item $EP --table-name Orders \
  --item '{"customerId":{"S":"c1"},"orderId":{"S":"o1"},"total":{"N":"42"}}'

# All orders of a customer
aws dynamodb query $EP --table-name Orders \
  --key-condition-expression "customerId = :c" \
  --expression-attribute-values '{":c":{"S":"c1"}}'
```
