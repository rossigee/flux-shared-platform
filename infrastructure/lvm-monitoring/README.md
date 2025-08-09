# LVM Storage Monitoring

This is a shared LVM storage monitoring solution for Kubernetes clusters using the CSI-Driver-LVM storage provisioner.

## Overview

The monitoring solution provides:
- Real-time metrics collection every 5 minutes
- Daily comprehensive reports
- Hourly health checks
- Prometheus metrics export
- Grafana dashboards
- Alerting for storage issues

## Components

### Base Components (in this directory)
- `namespace.yaml` - Common namespace definition
- `rbac.yaml` - ServiceAccount and RBAC permissions
- `configmap.yaml` - Monitoring scripts
- `cronjob.yaml` - Daily and hourly monitoring jobs
- `deployment.yaml` - Continuous metrics exporter
- `prometheus-rules.yaml` - Alert rules
- `grafana-dashboard.json` - Visualization dashboard

### Container Images
- `lvm-metrics-exporter.py` - Python metrics collection script
- `Dockerfile` - Container build definition

## Usage

To use this in your cluster:

1. Create a Kustomization that references this base:
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: lvm-monitoring
resources:
- github.com/your-org/flux-shared-platform/infrastructure/lvm-monitoring?ref=main

patches:
- target:
    kind: Deployment
    name: lvm-metrics-exporter
  patch: |-
    - op: replace
      path: /spec/template/spec/containers/0/env/0/value
      value: "your-cluster-name"
```

2. Customize cluster-specific values:
- Cluster name
- Prometheus Push Gateway URL
- External secrets configuration
- Resource limits

## Metrics Exported

See the full list in the individual cluster implementations.

## Building the Container

### Container Image

The monitoring scripts require a custom container image with pre-installed tools to comply with Pod Security Standards (no root access).

### Building the Container

```bash
# Build the container image
./build-and-push.sh v1.0.0

# Login to Harbor
docker login PRIVATE_REGISTRY

# Push the image
docker push PRIVATE_REGISTRY/infrastructure/lvm-monitor:v1.0.0
docker push PRIVATE_REGISTRY/infrastructure/lvm-monitor:latest
```

### Container Contents

The custom image includes:
- `kubectl` - For Kubernetes API access
- `jq` - For JSON parsing
- `mc` (MinIO Client) - For MinIO uploads
- `curl` - For Discord webhooks
- `python3` with `kubernetes` and `prometheus-client` packages
- Runs as non-root user (UID 10001)

### Security Compliance

The container and CronJobs are configured to comply with Kubernetes Pod Security Standards "restricted" profile:
- Runs as non-root user (10001)
- No privilege escalation allowed
- All capabilities dropped
- Seccomp profile enabled
- Read-only root filesystem compatible
