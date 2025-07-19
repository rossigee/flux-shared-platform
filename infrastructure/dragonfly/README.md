# Dragonfly P2P Image Distribution

Dragonfly provides P2P-based container image distribution in the Kubernetes cluster, reducing bandwidth usage and improving image pull performance.

## Architecture

- **Manager**: Manages the P2P network topology
- **Scheduler**: Schedules P2P tasks across peers
- **Seed Peer**: Acts as a super node and cache for the P2P network
- **Client (dfdaemon)**: Runs on each node and handles P2P distribution

## Deployment Options

### Option 1: Application-Level Configuration (Recommended for Flux)

Configure applications to use Dragonfly proxy explicitly:

```yaml
# In your pod spec:
spec:
  containers:
  - name: myapp
    image: dragonfly-proxy.dragonfly-system.svc.cluster.local:65001/docker.io/nginx:latest
```

Or use imagePullSecrets with registry credentials pointing to Dragonfly.

### Option 2: Node-Level Configuration (Manual Setup)

For cluster-wide transparent proxying, manually configure each node:

1. SSH to each node
2. Edit `/etc/containerd/config.toml`
3. Add mirror configuration:

```toml
[plugins."io.containerd.grpc.v1.cri".registry.mirrors]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
    endpoint = ["http://localhost:30001"]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."harbor.golder.lan"]
    endpoint = ["http://localhost:30001", "https://harbor.golder.lan"]
```

4. Restart containerd: `systemctl restart containerd`

### Option 3: Mutating Webhook (Advanced)

Deploy a mutating webhook that automatically rewrites image URLs to use Dragonfly proxy.

## Usage Examples

### Direct Proxy Usage
```bash
# Pull through Dragonfly proxy (from inside cluster)
docker pull dragonfly-proxy.dragonfly-system.svc.cluster.local:65001/docker.io/nginx:latest

# Pull through NodePort (from nodes)
docker pull localhost:30001/docker.io/nginx:latest
```

### Checking P2P Status
```bash
# Check Dragonfly pods
kubectl get pods -n dragonfly-system

# Check P2P metrics
kubectl port-forward -n dragonfly-system svc/dragonfly-metrics 8000:8000
curl http://localhost:8000/metrics | grep dragonfly
```

## Benefits

1. **Bandwidth Savings**: Up to 90% reduction in external registry traffic
2. **Faster Pulls**: Images are distributed via P2P from nearby nodes
3. **Resilience**: If external registry is down, cached images still available
4. **Rate Limit Mitigation**: Reduces hits to Docker Hub rate limits

## Monitoring

Dragonfly exposes Prometheus metrics on port 8000:
- `dragonfly_p2p_traffic_bytes_total`: P2P traffic served
- `dragonfly_proxy_traffic_bytes_total`: Proxy traffic handled
- `dragonfly_peer_count`: Number of active peers

## Troubleshooting

### Check logs
```bash
kubectl logs -n dragonfly-system -l component=dfdaemon
kubectl logs -n dragonfly-system -l component=scheduler
```

### Verify P2P network
```bash
kubectl exec -n dragonfly-system <dfdaemon-pod> -- dfget status
```
