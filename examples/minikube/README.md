# Minikube Examples

This directory contains example configurations for deploying the flux-shared-platform components on Minikube for local development and testing.

## Directory Structure

- **staging/**: Lightweight development environment
- **production/**: Production-like configuration for testing
- **operations/**: Security and operations tool testing

## Minikube-Specific Considerations

### Local Development
- Single-node cluster on local machine
- Limited resources (CPU, memory, storage)
- Docker or VM-based drivers
- Local storage only

### Networking
- NodePort or LoadBalancer via minikube tunnel
- Ingress via minikube addons
- Local DNS resolution
- No external connectivity by default

### Storage
- hostPath for simple persistence
- Local PV provisioner
- No real high availability
- Limited storage capacity

### Addons
- metrics-server for resource monitoring
- ingress for HTTP routing
- dashboard for UI access
- registry for local images

## Prerequisites

1. Minikube installed (latest version)
2. Hypervisor (VirtualBox, HyperKit, Docker, etc.)
3. kubectl configured
4. Sufficient local resources (8GB RAM minimum)
5. Docker or compatible container runtime

## Usage

Each environment folder contains lightweight configurations suitable for Minikube's constraints.

```bash
# Start Minikube with sufficient resources
minikube start --cpus 4 --memory 8192 --disk-size 50g

# Enable necessary addons
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable registry

# Deploy configurations
cd staging
kubectl apply -k .
```

## Limitations

- Single node only (no real HA testing)
- Limited resources
- No cloud provider integrations
- Simplified networking
- Local storage only

## Best Practices

- Use for development and testing only
- Profile different configurations
- Clean up resources regularly
- Use minikube profiles for isolation
- Monitor resource usage