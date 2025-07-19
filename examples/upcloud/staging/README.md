# UpCloud Staging Environment

This directory contains configurations for deploying a staging environment on UpCloud.

## Overview

The staging environment is optimized for development and testing with:
- Single availability zone deployment
- Standard SSD storage for general use
- Managed database in development configuration
- Simplified networking setup

## Key Configurations

### Compute
- **Server Types**: 2 vCPU, 4GB RAM general purpose
- **Node Count**: 1-3 nodes with manual scaling
- **Availability**: Single zone (Helsinki/Frankfurt)

### Storage
- **Storage Type**: Standard SSD (100 IOPS/GB)
- **Backup**: Daily snapshots, 7-day retention
- **Object Storage**: Single bucket for all backups

### Networking
- **Load Balancer**: Single UpCloud LB instance
- **Public IPs**: Direct assignment to LB
- **DNS**: External DNS with staging subdomain
- **TLS**: Let's Encrypt staging certificates

### Database
- **Managed PostgreSQL**: 1 vCPU, 2GB RAM
- **Managed Redis**: 1GB memory plan
- **Backup**: Daily automated backups
- **High Availability**: Disabled

## Deployment

```bash
# Configure kubectl for UpCloud cluster
export KUBECONFIG=./kubeconfig-staging.yaml

# Apply staging configurations
kubectl apply -k .

# Verify deployment
kubectl get kustomizations -n flux-system
```

## UpCloud-Specific Configuration

### Storage Classes
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: upcloud-ssd
parameters:
  tier: standard  # standard or maxiops
```

### Load Balancer Annotations
```yaml
metadata:
  annotations:
    service.beta.kubernetes.io/upcloud-load-balancer-plan: "development"
```

## Cost Optimization

- Development-tier managed services
- Standard SSD instead of MaxIOPS
- Single-zone deployment
- Shutdown during off-hours
- Minimal backup retention