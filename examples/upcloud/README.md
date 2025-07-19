# UpCloud Examples

This directory contains example configurations for deploying the flux-shared-platform components on UpCloud Kubernetes Service (UKS) or self-managed Kubernetes on UpCloud.

## Directory Structure

- **staging/**: Development and testing environment configurations
- **production/**: Production-ready configurations with high availability
- **operations/**: Security operations and management cluster configurations

## UpCloud-Specific Considerations

### Infrastructure
- UpCloud Kubernetes Service (managed) or self-managed K8s on Private Cloud
- MaxIOPS storage for high-performance workloads
- Object Storage for backups and artifacts
- Private networking with SDN

### Storage
- CSI driver for UpCloud block storage
- MaxIOPS SSD storage for databases
- HDD storage for cost-effective bulk storage
- Object Storage S3-compatible API

### Networking
- UpCloud Load Balancers for service exposure
- Floating IPs for high availability
- Private networks for secure communication
- Cloud Gateway for VPN connectivity

### Database Options
- Managed Databases (PostgreSQL, MySQL, Redis)
- Self-managed databases on Kubernetes
- MaxIOPS storage for database performance

## Prerequisites

1. UpCloud account with API credentials
2. Kubernetes cluster (UKS or self-managed)
3. UpCloud CLI or Terraform for infrastructure
4. Load balancer and floating IPs configured
5. Object Storage buckets created

## Usage

Each environment folder contains Kustomization overlays that patch the base configurations from the flux-shared-platform with UpCloud-specific values.

```bash
# Example: Deploy staging environment
cd staging
kubectl apply -k .
```

## Cost Optimization

- Simple pricing model with predictable costs
- Hourly billing for flexible scaling
- Free internal traffic between servers
- Cost-effective HDD storage for logs/backups