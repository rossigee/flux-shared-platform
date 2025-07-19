# AWS Examples

This directory contains example configurations for deploying the flux-shared-platform components on Amazon Web Services (AWS).

## Directory Structure

- **staging/**: Development and testing environment configurations
- **production/**: Production-ready configurations with high availability
- **operations/**: Security operations and management cluster configurations

## AWS-Specific Considerations

### Authentication
- Uses IAM roles for service accounts (IRSA) for pod-level AWS access
- External DNS uses Route53 for DNS management
- External Secrets integrates with AWS Secrets Manager or Systems Manager Parameter Store

### Storage
- EBS CSI driver for persistent volumes (instead of LVM)
- EFS for shared storage requirements
- S3 for backup storage (CNPG, Loki, etc.)

### Networking
- AWS Load Balancer Controller for ingress (alternative to HAProxy)
- VPC CNI for pod networking (alternative to Cilium)
- Security groups for network policies

### Monitoring
- CloudWatch integration for metrics and logs
- AWS Managed Prometheus (AMP) integration options
- AWS Managed Grafana (AMG) integration options

## Prerequisites

1. EKS cluster deployed
2. OIDC provider configured for IRSA
3. Appropriate IAM roles and policies created
4. VPC and networking configured

## Usage

Each environment folder contains Kustomization overlays that patch the base configurations from the flux-shared-platform with AWS-specific values.

```bash
# Example: Deploy staging environment
cd staging
kubectl apply -k .
```