# Azure Examples

This directory contains example configurations for deploying the flux-shared-platform components on Microsoft Azure.

## Directory Structure

- **staging/**: Development and testing environment configurations
- **production/**: Production-ready configurations with high availability
- **operations/**: Security operations and management cluster configurations

## Azure-Specific Considerations

### Authentication
- Uses Azure AD Workload Identity for pod-level Azure access
- External DNS uses Azure DNS for DNS management
- External Secrets integrates with Azure Key Vault

### Storage
- Azure Disk CSI driver for persistent volumes
- Azure Files for shared storage requirements
- Azure Blob Storage for backup storage (CNPG, Loki, etc.)

### Networking
- Azure Load Balancer for service exposure
- Azure CNI for pod networking
- Network Security Groups for network policies
- Application Gateway Ingress Controller (AGIC) as alternative to HAProxy

### Monitoring
- Azure Monitor integration for metrics and logs
- Azure Managed Prometheus integration
- Azure Managed Grafana integration
- Log Analytics workspace for centralized logging

## Prerequisites

1. AKS cluster deployed with workload identity enabled
2. Azure AD applications and service principals configured
3. Appropriate Azure RBAC roles assigned
4. VNet and networking configured
5. Azure Key Vault for secrets management

## Usage

Each environment folder contains Kustomization overlays that patch the base configurations from the flux-shared-platform with Azure-specific values.

```bash
# Example: Deploy staging environment
cd staging
kubectl apply -k .
```

## Cost Management

- Azure Cost Management integration
- Resource tagging for cost allocation
- Azure Reservations for production workloads
- Spot instances for non-critical workloads