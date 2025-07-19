# GCP Production Environment

This directory contains configurations for deploying a production environment on Google Kubernetes Engine (GKE) with high availability and security.

## Overview

The production environment is optimized for reliability, security, and performance:
- Multi-zonal deployment for high availability
- Auto-scaling based on metrics
- Private GKE cluster with authorized networks
- Comprehensive monitoring with Cloud Operations

## Key Configurations

### Compute
- **Machine Types**: n2-standard-4 general, c2-standard-8 for compute
- **Committed Use**: 3-year CUDs for 70% of capacity
- **Auto-scaling**: 3-20 nodes across zones
- **Node Pools**: Separate pools for different workload types
- **Zones**: Distributed across 3 zones in region

### Storage
- **Storage Classes**: ssd-retain for databases, standard for logs
- **Snapshots**: Every 4 hours, 30-day retention
- **Filestore**: Enterprise tier with automatic backups
- **GCS**: Multi-region buckets for critical data

### Networking
- **Load Balancer**: Global HTTPS(S) load balancer
- **Cloud CDN**: Enabled for static content
- **Cloud Armor**: DDoS protection and WAF rules
- **DNS**: Cloud DNS with DNSSEC enabled
- **TLS**: Google-managed SSL certificates
- **Private Google Access**: For GCP API access

### Database
- **Cloud SQL**: High-availability PostgreSQL
  - Machine: db-n1-highmem-4
  - Automated backups with PITR
  - Read replicas in multiple regions
- **Memorystore**: Standard tier Redis with HA
- **Cloud Spanner**: For globally distributed data

### Security
- **Binary Authorization**: Container image verification
- **Shielded GKE Nodes**: Secure boot enabled
- **Network Policies**: Enforced with Dataplane V2
- **Private Cluster**: No public IPs on nodes
- **Secret Manager**: For sensitive configuration

## High Availability

- Regional GKE cluster (multi-zone)
- PodDisruptionBudgets for all services
- Anti-affinity rules for spreading
- Automated failover testing
- Cross-region backup replication

## Disaster Recovery

- Multi-region backup strategy
- RTO: 1 hour, RPO: 15 minutes
- Automated backup verification
- Cross-region failover capability
- Regular DR exercises

## Deployment

```bash
# Get GKE credentials
gcloud container clusters get-credentials prod-cluster \
  --region us-central1 --project my-project

# Apply production configurations
kubectl apply -k .

# Verify deployment and health
kubectl get kustomizations -n flux-system
kubectl top nodes
kubectl get pods -A
```