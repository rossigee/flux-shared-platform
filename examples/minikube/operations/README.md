# Minikube Operations Environment

This directory contains configurations for testing security operations and management tools locally on Minikube.

## Overview

The operations environment is designed for testing:
- Security scanning tools
- Policy enforcement
- Monitoring and alerting
- Backup and restore procedures

## Key Configurations

### Resources
- **CPU**: 4 cores minimum
- **Memory**: 6GB minimum
- **Storage**: 40GB disk
- **Driver**: Docker recommended

### Security Tools
- **Kubescape**: Kubernetes security scanning
- **Kyverno**: Policy enforcement engine
- **Falco**: Runtime security (kernel module issues on Mac)
- **Trivy**: Vulnerability scanning

### Operations Tools
- **ArgoCD**: GitOps deployments
- **Velero**: Backup/restore testing
- **Prometheus**: Comprehensive monitoring
- **Loki**: Log aggregation

## Setup

```bash
# Start Minikube for operations
minikube start --profile operations \
  --cpus 4 \
  --memory 6144 \
  --disk-size 40g \
  --driver docker \
  --feature-gates="EphemeralContainers=true"

# Enable required addons
minikube addons enable metrics-server
minikube addons enable ingress

# Apply configurations
kubectl apply -k .
```

## Security Testing

### Policy Enforcement
```yaml
# Test Kyverno policies
kubectl apply -f test-policies/
kubectl apply -f test-violations/
```

### Vulnerability Scanning
```bash
# Scan images with Trivy
kubectl get pods -A -o jsonpath="{..image}" | \
  tr -s '[[:space:]]' '\n' | \
  sort -u | \
  xargs -I {} trivy image {}
```

### Security Benchmarks
```bash
# Run Kubescape
kubescape scan framework nsa --exclude-namespaces kube-system,kube-public
```

## Operations Testing

### Backup and Restore
```bash
# Install Velero with file backend
velero install --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.2.0 \
  --bucket-name minikube-backups \
  --backup-location-config region=minio,s3ForcePathStyle="true",s3Url=http://minio.velero.svc:9000 \
  --use-restic

# Test backup
velero backup create test-backup --include-namespaces default

# Test restore
velero restore create --from-backup test-backup
```

### Monitoring Stack
- Prometheus with all exporters
- Grafana with security dashboards
- AlertManager with test routes
- Log analysis with Loki

### GitOps Testing
```bash
# Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Login (get password)
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

## Compliance Testing

### CIS Benchmarks
```bash
# Run CIS benchmark tests
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
kubectl logs job/kube-bench
```

### Policy Reports
- Kyverno policy reports
- Kubescape compliance scores
- Trivy vulnerability reports

## Resource Optimization

Due to limited resources:
- Stagger tool deployments
- Use resource limits
- Clean up after testing
- Monitor memory usage

## Known Limitations

- Falco kernel module (use eBPF mode)
- Limited storage for logs
- Single node security testing
- No real network segmentation
- Performance constraints

## Cleanup

```bash
# Delete specific tools
kubectl delete namespace security-tools

# Full cleanup
minikube delete --profile operations
```