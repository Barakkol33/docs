# Azure (Microsoft Azure)

Microsoft's cloud. Strongest in enterprises that already use Microsoft: Windows Server, SQL Server, Active Directory, Microsoft 365, .NET.

---

## Resource hierarchy

```
Tenant (Microsoft Entra ID)
 └── Management Group (optional)
      └── Subscription          ← billing + access boundary
           └── Resource Group   ← logical container
                └── Resources
```

- **Tenant** – Your organization's identity directory (Microsoft Entra ID, formerly Azure Active Directory).
- **Management Group** – Group subscriptions to apply policy/RBAC at scale.
- **Subscription** – Billing unit and a scope for quotas and access. Common to split into prod / non-prod.
- **Resource Group (RG)** – Mandatory folder for resources that **share a lifecycle** (deploy together, delete together). Deleting an RG deletes everything inside. A resource lives in exactly one RG.
- **Resource ID** – Full path: `/subscriptions/<id>/resourceGroups/<rg>/providers/Microsoft.Compute/virtualMachines/<vm>`.
- **Region** – e.g. `westeurope`, `northeurope`. Many regions have **Availability Zones**; **region pairs** support disaster recovery.
- **Tags** – Metadata for cost and organization.
- **Azure Resource Manager (ARM)** – The control plane API behind portal, CLI, Terraform and templates.

---

## Identity & access

- **Microsoft Entra ID** – Users, groups, apps, SSO, MFA, **Conditional Access**.
- **RBAC (Role-Based Access Control)** – A **role assignment** = *who* (principal) + *role* + *scope* (management group, subscription, RG, or resource). Inherited downward.
  - Built-in roles: `Owner`, `Contributor` (everything but access management), `Reader`, plus many service-specific ones (e.g. `Storage Blob Data Reader`).
  - Note: control-plane roles vs **data-plane** roles (e.g. reading blob contents).
- **Service principal** – Identity for an application/automation (client ID + secret/certificate).
- **Managed Identity** – Azure-managed service principal attached to a resource (VM, App Service, AKS pod, Function). **No secrets to store, prefer this.** _System-assigned_ (tied to resource) or _user-assigned_ (reusable).
- **Workload identity federation** – For GitHub Actions / Kubernetes without secrets.
- **Azure Policy** – Enforce/audit rules (allowed regions, required tags, deny public IP).
- **Privileged Identity Management (PIM)** – Just-in-time elevated access.

---

## Networking

- **Virtual Network (VNet)** – Private network in a region, with address space and **subnets**.
- **Network Security Group (NSG)** – Allow/deny rules by priority, attached to a subnet or NIC.
- **Route tables (UDR)** – Custom routing. **NAT Gateway** – Outbound internet for private subnets.
- **Public IP**, **Private Endpoint / Private Link** – Private access to PaaS services (Storage, SQL…). **Service Endpoints** – lighter alternative.
- **VNet Peering**, **VPN Gateway**, **ExpressRoute** (dedicated line), **Virtual WAN** – Connectivity. **Hub-and-spoke** is the common enterprise layout.
- **Load balancing options** – (pick by layer and scope)
  - _Load Balancer_ – L4, regional.
  - _Application Gateway_ – L7 regional, WAF.
  - _Front Door_ – L7 global, CDN + WAF.
  - _Traffic Manager_ – DNS-based global routing.
- **Azure DNS**, **Azure Firewall**, **Bastion** (browser-based SSH/RDP, no public IPs).

---

## Compute

- **Virtual Machines** – IaaS. Sizes like `Standard_B2s` (burstable), `D` (general), `E` (memory), `F` (compute), `N` (GPU). Windows or Linux, managed disks, availability sets/zones, Spot VMs, Reserved Instances & Savings Plans.
- **VM Scale Sets (VMSS)** – Autoscaled groups of VMs.
- **AKS (Azure Kubernetes Service)** – Managed Kubernetes. Control plane is free (paid tier for SLA); you pay for node pools. Integrates with Entra ID, managed identities/workload identity, Azure Disk/Files CSI drivers, Azure Load Balancer.
- **ACR (Azure Container Registry)** – Private Docker/OCI registry. `az acr login`.
- **Container Apps** – Serverless containers (KEDA-based scaling, scales to zero). **Container Instances (ACI)** – run a container quickly without orchestration.
- **App Service** – PaaS for web apps/APIs (.NET, Java, Node, Python, containers) with deployment slots and autoscale. Runs on an **App Service Plan** (defines size/cost).
- **Azure Functions** – Serverless functions with triggers (HTTP, queue, timer, blob…).
- **Azure Batch**, **Logic Apps** (low-code workflows).

---

## Storage & databases

- **Storage Account** – The parent resource (globally unique name) containing:
  - **Blob Storage** – Object storage. _Container_ → _blobs_. Tiers: Hot, Cool, Cold, Archive. Lifecycle management, SAS tokens for delegated access.
  - **Azure Files** – SMB/NFS file shares.
  - **Queue Storage**, **Table Storage**.
  - _Redundancy_: LRS (local), ZRS (zones), GRS/GZRS (geo), RA-GRS (geo + read access).
- **Managed Disks** – Block storage for VMs (Standard HDD/SSD, Premium SSD, Ultra).
- **Azure SQL Database** – Managed SQL Server (single DB, elastic pool, serverless, Hyperscale). **SQL Managed Instance** for near-full SQL Server compatibility.
- **Azure Database for PostgreSQL / MySQL (Flexible Server)** – See [postgresql.md](../3-data-sources/databases/postgresql.md), [mysql.md](../3-data-sources/databases/mysql.md).
- **Cosmos DB** – Globally distributed multi-model NoSQL (NoSQL/JSON, MongoDB, Cassandra, Gremlin, Table APIs). Throughput measured in **RU/s**, tunable consistency levels (five of them), multi-region writes.
- **Azure Cache for Redis**, **Synapse / Fabric** (analytics), **Data Lake Storage Gen2**, **Data Factory** (ETL).

---

## Messaging & integration

- **Service Bus** – Enterprise queues and topics (ordering, sessions, dead-letter).
- **Event Hubs** – Big-data streaming, Kafka-compatible endpoint (see [kakfa.md](../3-data-sources/kakfa.md)).
- **Event Grid** – Event routing/pub-sub for Azure events.
- **API Management** – API gateway, throttling, policies.

---

## Security & operations

- **Key Vault** – Secrets, keys and certificates. Access via RBAC and managed identity.
- **Microsoft Defender for Cloud** – Posture management and threat protection. **Microsoft Sentinel** – SIEM.
- **Azure Monitor** – Metrics, alerts, **Log Analytics** workspaces (query with **KQL**, Kusto Query Language), Application Insights (APM), Container Insights. Managed Prometheus & Grafana available.
- **Activity Log** – Audit of control-plane operations. **Diagnostic settings** route logs/metrics to Log Analytics / storage / Event Hub.
- **Cost Management + Billing**, **Budgets**, **Advisor** (recommendations).
- **IaC** – **Bicep** (readable ARM replacement), ARM templates, Terraform. Azure DevOps or GitHub Actions for CI/CD.

---

## CLI cheat sheet

```bash
az login
az account list -o table
az account set --subscription "<name-or-id>"

az group create -n my-rg -l westeurope
az group list -o table
az group delete -n my-rg --yes        # deletes EVERYTHING in the group

az vm list -o table
az vm create -g my-rg -n vm1 --image Ubuntu2204 --size Standard_B2s --admin-username azureuser --generate-ssh-keys

az storage account create -g my-rg -n mystorageacct123 --sku Standard_LRS
az storage blob upload --account-name mystorageacct123 -c mycontainer -f file.txt -n file.txt --auth-mode login

# Containers
az acr create -g my-rg -n myregistry123 --sku Basic
az acr login -n myregistry123
docker push myregistry123.azurecr.io/app:1

# AKS
az aks create -g my-rg -n my-aks --node-count 2 --generate-ssh-keys --attach-acr myregistry123
az aks get-credentials -g my-rg -n my-aks
kubectl get nodes

az role assignment list --assignee <principal-id> -o table
```

**Typical web app on Azure:** Front Door (+ WAF) → App Service / Container Apps / AKS in a VNet → Azure SQL or PostgreSQL via Private Endpoint, assets in Blob Storage, secrets in Key Vault via managed identity, monitoring in Azure Monitor, all described in Bicep or Terraform.

---

## Name mapping gotchas

- **Resource Group** has no direct AWS equivalent (closest: a CloudFormation stack / tagging); GCP's **Project** plays a similar but stronger role.
- **Subscription** ≈ AWS Account ≈ roughly GCP Project (billing/isolation).
- **Managed Identity** ≈ AWS IAM Role for a resource ≈ GCP attached Service Account.
- **NSG** ≈ AWS Security Group + NACL; **VNet** ≈ VPC.
