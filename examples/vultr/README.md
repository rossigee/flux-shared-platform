# Vultr Examples

This directory contains example configurations for deploying the flux-shared-platform components on Vultr Kubernetes Engine (VKE) or self-managed Kubernetes on Vultr.

## Directory Structure

- **staging/**: Development and testing environment configurations  
- **production/**: Production-ready configurations with high availability
- **operations/**: Security operations and management cluster configurations

## Vultr-Specific Considerations

### Infrastructure
- Vultr Kubernetes Engine (VKE) for managed Kubernetes
- High Frequency Compute for performance-critical workloads
- Block Storage for persistent volumes
- Object Storage (S3-compatible) for backups

### Storage
- Vultr Block Storage CSI driver
- NVMe storage on High Frequency instances
- HDD block storage for cost-effective bulk storage
- Object Storage with S3-compatible API

### Networking
- Vultr Load Balancers for service exposure
- Reserved IPs for static addressing
- Private networks for secure communication
- Direct Connect for dedicated connectivity

### Additional Services
- Managed Databases (PostgreSQL, MySQL, Redis)
- DDoS Protection
- Vultr Firewall
- Snapshots and Backups

## Prerequisites

1. Vultr account with API key
2. VKE cluster or self-managed Kubernetes
3. Vultr CLI or Terraform configured
4. Load balancers provisioned
5. Object Storage configured

## Usage

Each environment folder contains Kustomization overlays that patch the base configurations from the flux-shared-platform with Vultr-specific values.

```bash
# Example: Deploy staging environment
cd staging
kubectl apply -k .
```

## Global Presence

Vultr offers deployment in 30+ locations worldwide, enabling:
- Geographic distribution
- Low latency deployments
- Data sovereignty compliance
- Disaster recovery options