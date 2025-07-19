# Vultr Staging Environment

This directory contains configurations for deploying a staging environment on Vultr Kubernetes Engine (VKE).

## Overview

The staging environment is optimized for development and testing with:
- Single region deployment
- Regular compute instances
- Standard block storage
- Managed databases in basic configuration

## Key Configurations

### Compute
- **Instance Types**: vc2-2c-4gb (2 vCPU, 4GB RAM)
- **Node Count**: 1-3 nodes
- **Node Pool**: Single pool for all workloads
- **Location**: Single datacenter

### Storage
- **Block Storage**: Standard SSD volumes
- **Storage Size**: 100GB per node
- **Backup**: Daily snapshots (7-day retention)
- **Object Storage**: Single bucket

### Networking
- **Load Balancer**: Single Vultr LB
- **Reserved IP**: One static IP
- **DNS**: Via External DNS
- **TLS**: Let's Encrypt staging
- **Firewall**: Basic rules

### Database
- **Managed PostgreSQL**: 
  - 1 vCPU, 1GB RAM
  - No replicas
  - Daily backups
- **Managed Redis**:
  - 1GB memory
  - No persistence

## Deployment

```bash
# Get VKE credentials
export KUBECONFIG=./vke-staging-kubeconfig.yaml

# Apply staging configurations
kubectl apply -k .

# Verify deployment
kubectl get kustomizations -n flux-system
```

## Vultr-Specific Configuration

### Storage Class
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: vultr-block-storage
provisioner: blk.csi.vultr.com
parameters:
  type: standard
```

### Load Balancer Service
```yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
    service.beta.kubernetes.io/vultr-loadbalancer-protocol: "tcp"
    service.beta.kubernetes.io/vultr-loadbalancer-healthcheck-port: "80"
```

## Cost Optimization

- Regular compute instances
- Standard block storage
- Single-zone deployment
- Minimal backup retention
- Scheduled shutdown capability