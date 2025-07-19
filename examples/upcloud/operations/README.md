# UpCloud Operations Environment

This directory contains configurations for deploying a security operations and management cluster on UpCloud.

## Overview

The operations environment is designed for:
- Security monitoring and compliance
- Infrastructure automation
- Centralized logging and metrics
- Backup and disaster recovery

## Key Configurations

### Compute
- **Server Types**: 4 vCPU, 8GB RAM dedicated
- **Node Count**: Fixed 3-node cluster
- **Availability**: Single zone with HA
- **Isolated Network**: Separate VLAN

### Storage
- **Storage Type**: MaxIOPS for logs/metrics
- **Archive Storage**: HDD for long-term
- **Object Storage**: For backup archives
- **Encryption**: Mandatory for all volumes

### Networking
- **Private Network**: Isolated ops VLAN
- **VPN Gateway**: Site-to-site connectivity
- **Jump Hosts**: Bastion access only
- **Firewall**: Strict ingress rules
- **No Public IPs**: On cluster nodes

### Security Features
- **Network Isolation**: Dedicated VLAN
- **Access Control**: VPN-only access
- **Audit Logging**: All API calls logged
- **Encryption**: In-transit and at-rest
- **Backup Encryption**: GPG encrypted

## Key Components

### Security Tools
- Kubescape for security scanning
- Kyverno for policy enforcement
- Falco for runtime protection
- Vault for secrets management

### Operations Tools
- ArgoCD for GitOps
- Crossplane for infrastructure
- Velero for backup/restore
- Prometheus for monitoring
- Loki for log aggregation

### UpCloud Integration
- API credentials in Vault
- Terraform state in Object Storage
- Backup to Object Storage
- Monitoring via UpCloud API

## Access Control

- VPN-only cluster access
- MFA for all operations
- Audit trail to Object Storage
- Time-limited access tokens
- Regular access reviews

## Deployment

```bash
# Connect via VPN first
# Configure kubectl
export KUBECONFIG=./kubeconfig-operations.yaml

# Apply operations configurations
kubectl apply -k .

# Verify security components
kubectl get pods -n security-tools
kubectl get pods -n operations
```

## Backup Strategy

- Velero to Object Storage
- Encrypted backup archives
- Cross-region replication
- Monthly backup testing
- 1-year retention policy

## Compliance

- EU data residency
- GDPR compliance features
- Audit log retention
- Access control reports
- Security scan reports