# UpCloud Production Environment

This directory contains configurations for deploying a production environment on UpCloud with high availability.

## Overview

The production environment is optimized for reliability and performance:
- Multi-zone deployment across data centers
- MaxIOPS storage for critical workloads
- Managed databases with HA configuration
- Redundant networking with failover

## Key Configurations

### Compute
- **Server Types**: 8 vCPU, 16GB RAM for workers
- **Node Count**: 3-10 nodes with auto-scaling
- **Availability**: Multi-zone (Helsinki + Frankfurt)
- **Dedicated CPU**: For consistent performance

### Storage
- **Storage Type**: MaxIOPS SSD (100k IOPS)
- **Backup**: Continuous with 30-day retention
- **Object Storage**: Geo-replicated buckets
- **Encryption**: At-rest encryption enabled

### Networking
- **Load Balancers**: Multiple LBs with failover
- **Floating IPs**: For service availability
- **Private Network**: Isolated production VLAN
- **Gateway**: VPN for secure access
- **DDoS Protection**: Enabled on LBs

### Database
- **Managed PostgreSQL**: 
  - 4 vCPU, 8GB RAM
  - High availability mode
  - Read replicas
  - Point-in-time recovery
- **Managed Redis**:
  - 4GB memory plan
  - Persistence enabled
  - Automatic failover

## High Availability

- Servers distributed across zones
- Floating IPs for quick failover
- Load balancer health checks
- Automated backup verification
- Cross-zone data replication

## Deployment

```bash
# Configure kubectl for production
export KUBECONFIG=./kubeconfig-production.yaml

# Apply production configurations
kubectl apply -k .

# Verify deployment health
kubectl get nodes
kubectl get pods -A
```

## UpCloud-Specific Features

### MaxIOPS Configuration
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: upcloud-maxiops
parameters:
  tier: maxiops
  iops: "100000"
```

### Multi-Zone Load Balancing
```yaml
metadata:
  annotations:
    service.beta.kubernetes.io/upcloud-load-balancer-plan: "production"
    service.beta.kubernetes.io/upcloud-load-balancer-frontend-rule: |
      {
        "name": "https",
        "mode": "tcp",
        "port": 443,
        "target_port": 443
      }
```

## Monitoring

- UpCloud monitoring API integration
- Custom metrics to Prometheus
- Alerts for resource utilization
- Automated scaling triggers