# Flux Shared Platform Examples

This directory contains example configurations for deploying the flux-shared-platform across various cloud providers and environments.

## Directory Structure

```
examples/
├── aws/          # Amazon Web Services (EKS)
├── azure/        # Microsoft Azure (AKS)
├── gcp/          # Google Cloud Platform (GKE)
├── upcloud/      # UpCloud (UKS or self-managed)
├── vultr/        # Vultr (VKE or self-managed)
└── minikube/     # Local development with Minikube
```

Each provider directory contains three environment types:
- **staging/**: Development and testing configurations
- **production/**: Production-ready configurations with HA
- **operations/**: Security operations and management cluster

## Environment Types

### Staging Environment
- Cost-optimized for development
- Relaxed security for easier debugging  
- Minimal high availability
- Shorter backup retention
- Smaller instance sizes

### Production Environment
- High availability across zones/regions
- Production-grade security policies
- Comprehensive monitoring and alerting
- Automated backups with long retention
- Performance-optimized configurations

### Operations Environment
- Security monitoring and compliance tools
- Infrastructure automation platforms
- Centralized logging and metrics
- Backup and disaster recovery systems
- Isolated network with restricted access

## Cloud Provider Comparison

| Feature | AWS | Azure | GCP | UpCloud | Vultr | Minikube |
|---------|-----|-------|-----|---------|-------|----------|
| Managed K8s | EKS | AKS | GKE | UKS | VKE | N/A |
| Load Balancer | ALB/NLB | Azure LB | GCLB | UpCloud LB | Vultr LB | NodePort |
| Block Storage | EBS | Azure Disk | PD | Block Storage | Block Storage | hostPath |
| Object Storage | S3 | Blob | GCS | Object Storage | Object Storage | Local |
| Managed DB | RDS | Azure DB | Cloud SQL | Managed DB | Managed DB | Pods |
| Secrets | Secrets Manager | Key Vault | Secret Manager | Manual | Manual | K8s Secrets |
| DNS | Route53 | Azure DNS | Cloud DNS | Manual | Manual | Local |

## Common Patterns

### Authentication & Authorization
- OIDC/SAML integration with cloud identity providers
- Workload identity for pod-level cloud access
- RBAC aligned with cloud IAM

### Storage
- Cloud-native CSI drivers
- Snapshot-based backups
- Encryption at rest
- Storage classes for different performance tiers

### Networking  
- Cloud load balancers with health checks
- Private endpoints for cloud services
- Network policies for segmentation
- Ingress controllers with TLS termination

### Monitoring
- Cloud-native monitoring integration
- Prometheus for metrics collection
- Grafana for visualization
- Log aggregation to cloud logging services

## Getting Started

1. Choose your cloud provider and environment
2. Review the README in the specific directory
3. Customize the configurations for your needs
4. Apply using Kustomize:

```bash
cd <provider>/<environment>
kubectl apply -k .
```

## Customization

Each example uses Kustomize patches to customize the base platform:
- Provider-specific service annotations
- Cloud-native integrations
- Environment-specific resource limits
- Security policies per environment

## Best Practices

1. **Start with staging** to test configurations
2. **Use cloud-native services** where available
3. **Implement proper secret management** using cloud KMS
4. **Enable audit logging** for compliance
5. **Regular backup testing** for disaster recovery
6. **Monitor costs** with cloud billing alerts
7. **Use reserved instances** for production workloads

## Contributing

When adding new provider examples:
1. Follow the existing directory structure
2. Include comprehensive README files
3. Provide working Kustomization examples
4. Document provider-specific requirements
5. Include cost optimization tips