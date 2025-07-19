# Azure Production Environment

This directory contains configurations for deploying a production environment on Azure AKS with high availability and security.

## Overview

The production environment is optimized for reliability, security, and performance:
- Zone-redundant deployments across availability zones
- Auto-scaling based on metrics
- Private cluster with private endpoints
- Comprehensive monitoring with Azure Monitor

## Key Configurations

### Compute
- **VM Types**: Standard_D4s_v3 for general, Standard_F8s_v2 for compute-intensive
- **Reserved Instances**: 3-year reservations for baseline capacity
- **Auto-scaling**: Cluster autoscaler with 3-20 nodes
- **Availability Zones**: Spread across 3 zones
- **Node Pools**: Separate pools for system and user workloads

### Storage
- **Azure Disk**: Premium SSD with encryption
- **Backup**: Continuous backups with Azure Backup
- **Snapshots**: Every 4 hours, retained for 30 days
- **Disaster Recovery**: Geo-redundant storage

### Networking
- **Load Balancer**: Standard SKU with multiple frontend IPs
- **Application Gateway**: With WAF for web applications
- **DNS**: Azure DNS with example.com zone
- **TLS**: Azure Key Vault certificates
- **Private Link**: For all Azure service access
- **Azure Firewall**: For egress control

### Database
- **Azure Database**: Business Critical tier PostgreSQL Flexible Server
- **High Availability**: Zone-redundant HA enabled
- **Read Replicas**: Cross-region read replicas
- **Azure Cache**: Premium tier Redis with clustering
- **Backup**: Long-term retention with PITR

### Security
- **Azure Policy**: Enforced compliance policies
- **Azure Security Center**: Advanced threat protection
- **Key Vault**: HSM-backed key storage
- **Managed Identities**: For all service authentication
- **Network Policies**: Calico network policies enforced

## High Availability

- Zone-redundant AKS control plane
- Pod topology spread constraints
- PodDisruptionBudgets enforced
- Multi-region failover capability

## Disaster Recovery

- Cross-region backup replication
- RTO: 1 hour, RPO: 15 minutes
- Automated failover procedures
- Regular DR drills

## Deployment

```bash
# Set Azure context
az aks get-credentials --resource-group prod-rg --name prod-aks

# Apply production configurations
kubectl apply -k .

# Verify deployment
kubectl get kustomizations -n flux-system
kubectl get pods -A
```