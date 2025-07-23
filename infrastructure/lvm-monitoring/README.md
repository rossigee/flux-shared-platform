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

```bash
docker build -t your-registry/lvm-metrics-exporter:latest .
docker push your-registry/lvm-metrics-exporter:latest
```
