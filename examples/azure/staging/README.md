# Azure Staging Environment

This directory contains configurations for deploying a staging environment on Azure AKS.

## Overview

The staging environment is optimized for development and testing with:
- Single-instance Azure Database for PostgreSQL
- Smaller VM sizes for cost optimization
- Relaxed security policies for easier debugging
- Integration with Azure DevOps

## Key Configurations

### Compute
- **VM Types**: Standard_DS2_v2 for general workloads
- **Spot VMs**: Enabled for non-critical workloads
- **Auto-scaling**: Cluster autoscaler with 1-5 nodes
- **Node Pools**: Single system node pool

### Storage
- **Azure Disk**: Standard SSD as default storage class
- **Backup**: Daily snapshots retained for 7 days
- **File Shares**: Azure Files for shared storage

### Networking
- **Load Balancer**: Basic SKU Load Balancer
- **DNS**: Azure DNS with staging.example.com zone
- **TLS**: Let's Encrypt staging certificates
- **Private Endpoints**: Disabled for simplicity

### Database
- **Azure Database**: Basic tier PostgreSQL single server
- **Azure Cache**: Basic tier Redis instance
- **Backup**: Geo-redundant backup disabled

## Deployment

```bash
# Set Azure context
az aks get-credentials --resource-group staging-rg --name staging-aks

# Apply staging-specific configurations
kubectl apply -k .

# Verify deployment
kubectl get kustomizations -n flux-system
```

## Cost Optimization

- Spot instances for workers
- B-series burstable VMs where appropriate
- Auto-shutdown outside business hours
- Lifecycle management for blob storage
- Dev/Test pricing where applicable