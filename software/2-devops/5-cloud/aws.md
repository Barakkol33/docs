# AWS (Amazon Web Services)

The largest and oldest cloud, with 200+ services. You need only a core set to build most things.

---

## Account & global structure

- **Account** – The fundamental isolation and billing boundary. Companies use many accounts (prod, dev, security…).
- **AWS Organizations** – Groups accounts, consolidated billing, **Service Control Policies (SCPs)** to restrict what accounts may do.
- **Region** – e.g. `us-east-1`, `eu-west-1`. Most resources are regional. Some services (IAM, Route 53, CloudFront) are global.
- **Availability Zone (AZ)** – e.g. `eu-west-1a`. Isolated data centers inside a region.
- **ARN** – Amazon Resource Name, the unique ID of anything: `arn:aws:s3:::my-bucket`.

---

## IAM (Identity & Access Management)

Controls **who can do what**. Global service, free.

- **User** – A person or app with long-term credentials. Prefer SSO (IAM Identity Center) for humans.
- **Group** – Collection of users sharing policies.
- **Role** – An identity with **temporary** credentials that something *assumes*: an EC2 instance, a Lambda, a pod (IRSA / Pod Identity), another account. **Prefer roles over access keys.**
- **Policy** – JSON document listing allowed/denied actions on resources.
  - _Identity-based_ (attached to user/role) and _resource-based_ (attached to e.g. an S3 bucket).
- **Permission boundary / SCP** – Upper limits on what permissions can be granted.
- **STS** – Issues temporary credentials (`AssumeRole`).
- **Evaluation rule** – Explicit **Deny** > explicit Allow > implicit deny (default).

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:PutObject"],
    "Resource": "arn:aws:s3:::my-bucket/uploads/*"
  }]
}
```

---

## Networking: VPC

A **VPC** is your private network in a region.

- **CIDR block** – IP range, e.g. `10.0.0.0/16`.
- **Subnet** – A slice of the VPC inside **one AZ**.
  - _Public_ – Route to an Internet Gateway; resources can have public IPs.
  - _Private_ – No direct inbound internet; outbound via NAT.
- **Route table** – Where traffic for a destination goes.
- **Internet Gateway (IGW)** – Two-way internet access for public subnets.
- **NAT Gateway** – Lets private subnets reach out to the internet (updates, APIs). Costs money per hour + per GB.
- **Security Group (SG)** – **Stateful** instance-level firewall, allow rules only. Can reference other SGs.
- **Network ACL (NACL)** – Stateless subnet-level firewall, allow + deny.
- **VPC Endpoints** – Private access to AWS services (S3, DynamoDB, ECR…) without going over the internet or a NAT.
- **VPC Peering / Transit Gateway** – Connect VPCs / accounts / on-prem.
- **VPN / Direct Connect** – Link to on-premises networks.
- **Elastic Load Balancing**
  - _ALB_ – Layer 7 (HTTP/HTTPS, path/host routing).
  - _NLB_ – Layer 4 (TCP/UDP, extreme performance, static IPs).
- **Route 53** – DNS + health checks + routing policies (latency, weighted, failover).
- **CloudFront** – CDN.

Typical layout: public subnets (load balancers, NAT) + private subnets (apps, databases), spread over 2–3 AZs.

---

## Compute

- **EC2** – Virtual machines.
  - _Instance type_ – Family + size, e.g. `t3.micro` (burstable), `m6i.large` (general), `c6i` (compute), `r6i` (memory), `g5` (GPU).
  - _AMI_ – Machine image (OS template).
  - _Key pair / SSM Session Manager_ – Access (SSM avoids open SSH ports).
  - _User data_ – Script run at first boot.
  - _Instance profile_ – Attaches an IAM role to the instance.
  - _Purchase options_ – On-Demand, Savings Plans/Reserved, **Spot** (up to ~90% off, can be interrupted).
- **EBS** – Network block volumes attached to an instance (one AZ). Snapshots go to S3.
- **Auto Scaling Group (ASG)** – Keeps N healthy instances from a launch template and scales on metrics.
- **Lambda** – Run functions on events (HTTP, S3 upload, queue message, schedule). Pay per ms. Limits: 15 min runtime.
- **ECS** – AWS's own container orchestrator. **Fargate** = serverless compute for ECS/EKS (no nodes to manage).
- **EKS** – Managed Kubernetes. AWS runs the control plane; you run managed node groups, Karpenter-provisioned nodes, or Fargate. Uses the AWS Load Balancer Controller for Services/Ingress and the EBS CSI driver for volumes.
- **ECR** – Private Docker registry.
- **Elastic Beanstalk / App Runner / Lightsail** – Simpler PaaS-style options.

---

## Storage

- **S3** – Object storage. Unlimited, 11 nines durability.
  - _Bucket_ (globally unique name) → _objects_ (key + data + metadata).
  - _Storage classes_ – Standard, Intelligent-Tiering, Standard-IA, Glacier tiers (cheaper, slower retrieval).
  - _Versioning_, _lifecycle rules_ (transition/expire), _replication_, _encryption_ (default on).
  - **Block Public Access** – Keep it ON. Public buckets are a classic breach cause.
  - _Presigned URLs_ – Time-limited access to a private object.
- **EFS** – Managed NFS shared file system.
- **FSx** – Managed Windows/Lustre/NetApp file systems.

---

## Databases

- **RDS** – Managed MySQL, PostgreSQL, MariaDB, SQL Server, Oracle. Multi-AZ (HA), read replicas, automated backups.
- **Aurora** – AWS-built MySQL/Postgres-compatible, storage auto-scales across 3 AZs; Serverless v2 option.
- **DynamoDB** – Serverless key-value/document. See [dynamodb.md](../3-data-sources/databases/dynamodb.md).
- **ElastiCache** – Managed Redis/Valkey/Memcached.
- **OpenSearch Service** – Managed Elasticsearch fork.
- **Redshift** – Data warehouse. **Athena** – SQL directly on S3 files.
- **DocumentDB**, **Neptune** (graph), **Keyspaces** (Cassandra), **Timestream**.

---

## Integration & messaging

- **SQS** – Queue (decouple producers/consumers).
- **SNS** – Pub/sub notifications (fan-out to queues, email, Lambda).
- **EventBridge** – Event bus and scheduler, routing events between services/SaaS.
- **Kinesis / MSK** – Streaming (MSK = managed Kafka, see [kakfa.md](../3-data-sources/kakfa.md)).
- **Step Functions** – Workflow orchestration.
- **API Gateway** – Managed HTTP/REST/WebSocket front door for APIs.

---

## Security, ops & governance

- **KMS** – Encryption keys; most services integrate ("encrypted with KMS key").
- **Secrets Manager** – Store/rotate secrets. **SSM Parameter Store** – cheaper config/secrets store.
- **ACM** – Free managed TLS certificates for ALB/CloudFront.
- **CloudWatch** – Metrics, logs, alarms, dashboards.
- **CloudTrail** – Audit log of every API call. Turn it on in every account.
- **Config / GuardDuty / Security Hub** – Compliance drift, threat detection, central findings.
- **CloudFormation / CDK** – Native IaC (CDK = write it in TypeScript/Python). Terraform is the popular alternative.
- **Cost Explorer / Budgets** – Track and alert on spend.
- **Tags** – Essential for cost allocation.

---

## CLI cheat sheet

```bash
aws configure                       # set keys/region (or use: aws configure sso)
aws sts get-caller-identity         # who am I?
aws s3 ls
aws s3 cp file.txt s3://my-bucket/
aws s3 sync ./dist s3://my-bucket/ --delete
aws ec2 describe-instances --query "Reservations[].Instances[].[InstanceId,State.Name]" --output table

# ECR login and push
aws ecr get-login-password | docker login --username AWS --password-stdin <acct>.dkr.ecr.<region>.amazonaws.com
docker tag app:1 <acct>.dkr.ecr.<region>.amazonaws.com/app:1
docker push <acct>.dkr.ecr.<region>.amazonaws.com/app:1

# Kubernetes on EKS
aws eks update-kubeconfig --name my-cluster --region eu-west-1
kubectl get nodes
```

**Typical 3-tier web app on AWS:** Route 53 → CloudFront → ALB (public subnets) → ECS/EKS/EC2 (private subnets, multi-AZ) → RDS/Aurora (private subnets, Multi-AZ), assets in S3, logs in CloudWatch, secrets in Secrets Manager, all defined in Terraform/CDK.
