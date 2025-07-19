# Minikube Staging Environment

This directory contains lightweight configurations for local development on Minikube.

## Overview

The staging environment is optimized for rapid development with:
- Minimal resource requirements
- In-memory databases where possible
- Local storage only
- Simplified networking

## Key Configurations

### Resources
- **CPU**: 2 cores allocated
- **Memory**: 4GB allocated
- **Storage**: 20GB disk
- **Driver**: Docker (recommended)

### Storage
- **Storage Class**: standard (hostPath)
- **Persistence**: Minimal (development only)
- **Backups**: None (local development)

### Networking
- **Ingress**: NGINX via addon
- **Services**: NodePort or ClusterIP
- **DNS**: CoreDNS + local /etc/hosts
- **TLS**: Self-signed certificates

### Databases
- **PostgreSQL**: Single pod, no replicas
- **Redis**: Memory-only, no persistence
- **Resource Limits**: Minimal

## Quick Start

```bash
# Start Minikube
minikube start --profile staging \
  --cpus 2 \
  --memory 4096 \
  --disk-size 20g \
  --driver docker

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server

# Apply configurations
kubectl apply -k .

# Access services
minikube service list
```

## Local Development Features

### Port Forwarding
```bash
# Grafana
kubectl port-forward svc/grafana 3000:80 -n grafana

# Prometheus
kubectl port-forward svc/prometheus 9090:9090 -n prometheus-operator
```

### Local Registry
```bash
# Enable local registry
minikube addons enable registry

# Use in deployments
# localhost:5000/myapp:latest
```

### Volume Mounts
```yaml
# Mount local directories
minikube mount ./data:/data
```

## Resource Limits

All components configured with minimal resources:
```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

## Troubleshooting

```bash
# Check Minikube status
minikube status

# View logs
minikube logs

# SSH into node
minikube ssh

# Clean up
minikube delete --profile staging
```