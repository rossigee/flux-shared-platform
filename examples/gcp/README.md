# GCP Examples

This directory contains example configurations for deploying the flux-shared-platform components on Google Cloud Platform (GCP).

## Directory Structure

- **staging/**: Development and testing environment configurations
- **production/**: Production-ready configurations with high availability
- **operations/**: Security operations and management cluster configurations

## GCP-Specific Considerations

### Authentication
- Uses Workload Identity for pod-level GCP access
- External DNS uses Cloud DNS for DNS management
- External Secrets integrates with Secret Manager

### Storage
- GCE Persistent Disk CSI driver for block storage
- Filestore for shared NFS storage
- Cloud Storage (GCS) for object storage and backups

### Networking
- Cloud Load Balancing for service exposure
- GKE native VPC networking
- Cloud Armor for DDoS protection and WAF
- Network policies with Dataplane V2

### Monitoring
- Cloud Operations suite integration
- Managed Prometheus (beta) for metrics
- Cloud Logging for centralized logs
- Cloud Trace for distributed tracing

## Prerequisites

1. GKE cluster deployed with Workload Identity enabled
2. Service accounts configured with appropriate IAM roles
3. Cloud DNS zones created
4. VPC and firewall rules configured
5. Secret Manager API enabled

## Usage

Each environment folder contains Kustomization overlays that patch the base configurations from the flux-shared-platform with GCP-specific values.

```bash
# Example: Deploy staging environment
cd staging
kubectl apply -k .
```

## Cost Management

- GCP Cost Management exports
- Resource labeling for cost allocation
- Committed use discounts for production
- Preemptible VMs for non-critical workloads
- Autoscaling policies to optimize costs