# GCP Staging Environment

This directory contains configurations for deploying a staging environment on Google Kubernetes Engine (GKE).

## Overview

The staging environment is optimized for development and testing with:
- Single-zone deployment for cost savings
- Preemptible nodes for non-critical workloads
- Cloud SQL with minimal HA configuration
- Relaxed security for development ease

## Key Configurations

### Compute
- **Machine Types**: e2-standard-2 for general workloads
- **Preemptible Nodes**: 80% of node pool
- **Auto-scaling**: 1-5 nodes with aggressive scale-down
- **Node Pools**: Single pool with mixed workloads

### Storage
- **Storage Classes**: standard (HDD) as default
- **Snapshots**: Daily, retained for 7 days
- **Filestore**: Basic tier for shared storage

### Networking
- **Load Balancer**: Regional TCP/UDP load balancer
- **DNS**: Cloud DNS with staging.example.com
- **TLS**: Let's Encrypt staging certificates
- **Ingress**: GCLB with basic configuration

### Database
- **Cloud SQL**: db-f1-micro PostgreSQL instance
- **Memorystore**: Basic tier Redis (1GB)
- **Backup**: On-demand backups only
- **High Availability**: Disabled

## Deployment

```bash
# Get GKE credentials
gcloud container clusters get-credentials staging-cluster \
  --zone us-central1-a --project my-project

# Apply staging configurations
kubectl apply -k .

# Verify deployment
kubectl get kustomizations -n flux-system
```

## Cost Optimization

- Preemptible instances (up to 80% savings)
- Cluster autoscaler with aggressive scale-down
- Resource quotas to prevent overspending
- Scheduled shutdown for nights/weekends
- Minimal backup retention