# AWS Staging Environment

This directory contains configurations for deploying a staging environment on AWS EKS.

## Overview

The staging environment is optimized for development and testing with:
- Single-node RDS instances for databases
- Smaller instance types for cost optimization
- Relaxed security policies for easier debugging
- Integration with AWS developer tools

## Key Configurations

### Compute
- **Instance Types**: t3.medium for general workloads
- **Spot Instances**: Enabled for non-critical workloads
- **Auto-scaling**: Cluster autoscaler with 1-5 nodes

### Storage
- **EBS**: gp3 storage class as default
- **Backup**: Daily snapshots retained for 7 days

### Networking
- **Load Balancer**: Network Load Balancer for ingress
- **DNS**: Route53 with staging.example.com subdomain
- **TLS**: Let's Encrypt staging certificates

### Database
- **RDS**: Single db.t3.micro PostgreSQL instance
- **ElastiCache**: t3.micro Redis instance

## Deployment

```bash
# Apply staging-specific configurations
kubectl apply -k .

# Verify deployment
kubectl get kustomizations -n flux-system
```

## Cost Optimization

- Spot instances for workers
- Scheduled scaling (down to 1 node outside business hours)
- S3 lifecycle policies for log retention
- Reserved capacity for predictable workloads