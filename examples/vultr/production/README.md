# Vultr Production Environment

This directory contains configurations for deploying a production environment on Vultr with high availability and performance.

## Overview

The production environment is optimized for reliability and performance:
- Multi-region deployment options
- High frequency compute instances
- NVMe storage for databases
- Redundant networking

## Key Configurations

### Compute
- **Instance Types**: vhf-8c-32gb (8 vCPU, 32GB RAM)
- **High Frequency**: Intel/AMD latest CPUs
- **Node Count**: 3-10 nodes with scaling
- **Locations**: Primary + DR region
- **Dedicated CPU**: No noisy neighbors

### Storage
- **NVMe Storage**: On high frequency instances
- **Block Storage**: High performance tier
- **Backup**: Hourly snapshots
- **Object Storage**: Multi-region sync
- **Encryption**: AES-256 at rest

### Networking
- **Load Balancers**: Multiple with failover
- **Reserved IPs**: Multiple static IPs
- **Private Network**: Isolated VPC
- **DDoS Protection**: Always enabled
- **Direct Connect**: Optional dedicated link

### Database
- **Managed PostgreSQL**:
  - 8 vCPU, 32GB RAM
  - 2 read replicas
  - Continuous backups
  - Point-in-time recovery
- **Managed Redis**:
  - 8GB memory
  - Persistence enabled
  - Eviction policies

## High Availability

- Geographic distribution
- Automatic failover
- Health check monitoring
- Cross-region replication
- Zero-downtime updates

## Deployment

```bash
# Get VKE credentials
export KUBECONFIG=./vke-production-kubeconfig.yaml

# Apply production configurations
kubectl apply -k .

# Verify deployment
kubectl get nodes -o wide
kubectl get pods -A
```

## Vultr-Specific Features

### High Performance Storage
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: vultr-nvme
provisioner: blk.csi.vultr.com
parameters:
  type: high-performance
  fs-type: xfs
```

### Advanced Load Balancer
```yaml
metadata:
  annotations:
    service.beta.kubernetes.io/vultr-loadbalancer-protocol: "http"
    service.beta.kubernetes.io/vultr-loadbalancer-ssl-ports: "443"
    service.beta.kubernetes.io/vultr-loadbalancer-proxy-protocol: "true"
    service.beta.kubernetes.io/vultr-loadbalancer-firewall-rules: "0.0.0.0/0"
```

### DDoS Protection
```yaml
metadata:
  annotations:
    service.beta.kubernetes.io/vultr-loadbalancer-ddos-protection: "true"
```

## Performance Optimization

- NVMe local storage for databases
- High frequency compute
- Optimized network paths
- Cache-friendly workload placement
- CPU pinning for critical pods