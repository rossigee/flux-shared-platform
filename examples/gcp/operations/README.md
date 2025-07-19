# GCP Operations Environment

This directory contains configurations for deploying a security operations and management cluster on GKE.

## Overview

The operations environment is designed for:
- Security monitoring and threat detection
- Infrastructure automation and management
- Compliance and audit operations
- Centralized logging and monitoring

## Key Configurations

### Compute
- **Machine Types**: n2-highmem-4 for consistent performance
- **Sole-tenant Nodes**: Available for compliance needs
- **Node Pools**: Dedicated pools for security zones
- **Regional Cluster**: High availability by default

### Storage
- **Storage Classes**: ssd for high-performance logging
- **GCS Buckets**: 
  - Hot tier for recent logs
  - Nearline for 30-day retention
  - Archive for compliance (7 years)
- **Filestore**: For shared security tools

### Networking
- **Private Cluster**: No external IPs
- **Private Service Connect**: For GCP services
- **Cloud Interconnect**: To on-premises
- **VPC Service Controls**: Security perimeter
- **Cloud NAT**: Controlled egress

### Security & Compliance
- **Security Command Center**: Centralized findings
- **Cloud Asset Inventory**: Resource tracking
- **Access Transparency**: Audit GCP access
- **VPC Flow Logs**: Network monitoring
- **Cloud Audit Logs**: Comprehensive audit trail
- **Cloud KMS**: Encryption key management
- **Cloud HSM**: Hardware security modules

### Monitoring & Logging
- **Cloud Logging**: Centralized sink
- **Cloud Monitoring**: Metrics and dashboards
- **Cloud Trace**: Distributed tracing
- **Error Reporting**: Automated error tracking
- **Managed Prometheus**: Long-term metrics
- **Log Router**: Advanced log filtering

## Key Components

### Security Tools
- Kubescape for GKE security
- Kyverno policy enforcement
- Falco runtime security
- Binary Authorization
- Container Analysis API

### Operations Tools
- ArgoCD for deployments
- Crossplane with GCP Provider
- Velero with GCS backend
- Config Connector
- Anthos Config Management

## Access Control

- Cloud Identity integration
- Context-aware access
- BeyondCorp Enterprise
- Access Approval API
- Privileged Access Manager

## Deployment

```bash
# Get GKE credentials
gcloud container clusters get-credentials ops-cluster \
  --region us-central1 --project security-ops-project

# Apply operations configurations
kubectl apply -k .

# Verify security components
kubectl get pods -n security-tools
kubectl get pods -n operations
```

## Compliance Features

- PCI-DSS compliance controls
- HIPAA-eligible infrastructure
- SOC 2 audit logging
- Data residency controls
- Assured Workloads integration