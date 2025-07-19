# AWS Production Environment

This directory contains configurations for deploying a production environment on AWS EKS with high availability and security.

## Overview

The production environment is optimized for reliability, security, and performance:
- Multi-AZ deployments for all critical components
- Auto-scaling based on metrics
- Enhanced security with private endpoints
- Comprehensive monitoring and alerting

## Key Configurations

### Compute
- **Instance Types**: m5.large for general workloads, c5.xlarge for compute-intensive
- **Reserved Instances**: 70% baseline capacity
- **Auto-scaling**: Cluster autoscaler with 3-20 nodes
- **Availability Zones**: Minimum 3 AZs for HA

### Storage
- **EBS**: gp3 storage class with encryption at rest
- **Backup**: Continuous backups with point-in-time recovery
- **Snapshots**: Every 4 hours, retained for 30 days

### Networking
- **Load Balancer**: Application Load Balancer with WAF
- **DNS**: Route53 with example.com domain
- **TLS**: ACM certificates or Let's Encrypt production
- **PrivateLink**: For AWS service access

### Database
- **RDS**: Multi-AZ db.r5.xlarge PostgreSQL with read replicas
- **ElastiCache**: Multi-AZ Redis cluster mode enabled
- **Backup**: Automated backups with 35-day retention

### Security
- **Network Policies**: Strict ingress/egress rules
- **Pod Security Standards**: Enforced restricted policies
- **Secrets**: AWS Secrets Manager with automatic rotation
- **Audit Logging**: CloudTrail and EKS audit logs to S3

## High Availability

- Cross-AZ pod spreading
- PodDisruptionBudgets for all services
- Automated failover for stateful services
- Health checks and circuit breakers

## Disaster Recovery

- Cross-region backup replication
- RTO: 1 hour, RPO: 15 minutes
- Automated backup testing
- Runbook documentation

## Deployment

```bash
# Apply production configurations
kubectl apply -k .

# Verify deployment
kubectl get kustomizations -n flux-system
kubectl get pods -A
```