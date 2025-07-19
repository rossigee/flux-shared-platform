# Minikube Production Environment

This directory contains production-like configurations for testing production scenarios locally on Minikube.

## Overview

The production environment simulates production configurations with:
- Maximum available local resources
- Persistent storage for all stateful services
- Full monitoring stack
- Security policies enabled

## Key Configurations

### Resources
- **CPU**: 4+ cores allocated
- **Memory**: 8GB+ allocated
- **Storage**: 50GB+ disk
- **Driver**: Docker or HyperKit

### Storage
- **Storage Classes**: Multiple for different tiers
- **Local Persistent Volumes**: For databases
- **Backup Simulation**: Local directory backups

### Networking
- **Ingress**: NGINX with TLS
- **Network Policies**: Enabled (Calico)
- **Service Mesh**: Optional (Linkerd/Istio)
- **Load Balancer**: Via minikube tunnel

### High Availability Simulation
- **Pod Replicas**: Where possible
- **Anti-affinity**: Simulated with labels
- **PDB**: PodDisruptionBudgets configured
- **Health Checks**: Comprehensive probes

## Setup

```bash
# Start Minikube with production-like resources
minikube start --profile production \
  --cpus 4 \
  --memory 8192 \
  --disk-size 50g \
  --driver docker \
  --extra-config=kubeadm.pod-network-cidr=10.244.0.0/16

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable registry
minikube addons enable dashboard

# Apply configurations
kubectl apply -k .
```

## Production Features Testing

### Monitoring Stack
- Prometheus with persistence
- Grafana with saved dashboards
- AlertManager with routing
- Loki for log aggregation

### Security Testing
- NetworkPolicies enforced
- PodSecurityStandards
- RBAC configurations
- Secret encryption at rest

### Backup Testing
```bash
# Simulate backups to local directory
minikube mount ./backups:/backups

# Velero with file backend
kubectl apply -f velero-file-backend.yaml
```

## Performance Testing

### Resource Monitoring
```bash
# Monitor resource usage
kubectl top nodes
kubectl top pods -A

# Minikube dashboard
minikube dashboard
```

### Load Testing
- Deploy load generation tools
- Monitor resource constraints
- Test autoscaling behaviors
- Verify resource limits

## Limitations vs Real Production

- Single node (no real HA)
- Local storage (no distributed storage)
- No cloud provider features
- Limited network isolation
- No real multi-zone testing

## Best Practices

- Regular cleanup of resources
- Profile isolation for different tests
- Resource monitoring
- Log rotation
- Periodic restarts