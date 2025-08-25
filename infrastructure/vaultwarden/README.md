# Vaultwarden Flux Deployment with Prometheus Metrics

This directory contains the Kubernetes manifests for deploying Vaultwarden with Prometheus metrics enabled in your Flux GitOps infrastructure.

## Features

- **Metrics-enabled Vaultwarden**: Custom build with Prometheus metrics support
- **Secure metrics endpoint**: Token-based authentication for metrics collection
- **External Secrets integration**: Secrets managed via Vault
- **Automatic image updates**: Flux automation for image updates
- **Service monitoring**: Prometheus ServiceMonitor configuration
- **Ingress**: HAProxy ingress with TLS termination
- **Persistent storage**: LVM LocalPV for data persistence

## Prerequisites

1. **Secrets in Vault**: Configure the following secrets in your Vault instance:
   ```bash
   # Database URL (can be SQLite file path or PostgreSQL/MySQL connection string)
   vault kv put secret/vaultwarden database-url="data/db.sqlite3"
   
   # Admin token for web interface (generate with: openssl rand -hex 32)
   vault kv put secret/vaultwarden admin-token="your-admin-token-here"
   
   # Metrics token for Prometheus scraping (generate with: openssl rand -hex 32)
   vault kv put secret/vaultwarden metrics-token="your-metrics-token-here"
   ```

2. **DNS Configuration**: Ensure your domain points to your cluster ingress

3. **TLS Certificate**: The deployment uses `vault-ecdsa-clusterissuer` for TLS

## Deployment Steps

### 1. Copy Files to Flux Repository

Copy this entire directory to your Flux repository:

```bash
# Copy the deployment files to your Flux apps directory
cp -r vaultwarden/ /path/to/your/flux-repository/apps/vaultwarden
```

### 2. Update Flux Apps Kustomization

Add Vaultwarden to your main apps kustomization file:

```yaml
# In your cluster's apps kustomization file
# Add under resources:
- ../../../apps/vaultwarden
```

### 3. Configure Secrets in Vault

```bash
# Generate secure tokens
ADMIN_TOKEN=$(openssl rand -hex 32)
METRICS_TOKEN=$(openssl rand -hex 32)

# Store in Vault
vault kv put secret/vaultwarden \\
  database-url="data/db.sqlite3" \\
  admin-token="$ADMIN_TOKEN" \\
  metrics-token="$METRICS_TOKEN"

echo "Admin token: $ADMIN_TOKEN"
echo "Metrics token: $METRICS_TOKEN"
```

### 4. Commit and Push

```bash
cd /path/to/your/flux-repository
git add apps/vaultwarden/
git commit -m "feat: Add Vaultwarden deployment with Prometheus metrics"
git push origin main
```

## Accessing Vaultwarden

- **Web Interface**: https://your-domain.example.com
- **Admin Panel**: https://your-domain.example.com/admin (use admin token)
- **Metrics Endpoint**: https://your-domain.example.com/metrics (requires metrics token)

## Metrics Configuration

### Manual Metrics Testing

```bash
# Test metrics endpoint
curl -H "Authorization: Bearer your-metrics-token" \\
  https://your-domain.example.com/metrics

# Or with query parameter
curl "https://your-domain.example.com/metrics?token=your-metrics-token"
```

### Prometheus Configuration

The ServiceMonitor is automatically configured to scrape metrics. In Prometheus, you'll see metrics prefixed with `vaultwarden_`:

- `vaultwarden_http_requests_total` - HTTP request counts
- `vaultwarden_http_request_duration_seconds` - Response times
- `vaultwarden_users_total` - User counts
- `vaultwarden_vault_items_total` - Vault item counts
- `vaultwarden_uptime_seconds` - Application uptime

### Example Grafana Queries

```promql
# Request rate
rate(vaultwarden_http_requests_total[5m])

# Error rate
rate(vaultwarden_http_requests_total{status=~"4..|5.."}[5m]) / rate(vaultwarden_http_requests_total[5m]) * 100

# 95th percentile response time
histogram_quantile(0.95, rate(vaultwarden_http_request_duration_seconds_bucket[5m]))

# Active users
vaultwarden_users_total{status="enabled"}
```

## Customization

### Environment Variables

Common environment variables you might want to customize in `vaultwarden.yaml`:

```yaml
env:
- name: SIGNUPS_ALLOWED
  value: "false"                    # Disable new signups
- name: INVITATIONS_ALLOWED
  value: "true"                     # Allow invitations
- name: SMTP_HOST
  value: "smtp.example.com"         # SMTP server for emails
- name: SMTP_FROM
  value: "vault@example.com"        # From address
```

### Storage

To use PostgreSQL instead of SQLite, update the database URL in Vault:

```bash
vault kv put secret/vaultwarden \\
  database-url="postgresql://user:password@postgres-host:5432/vaultwarden"
```

### Resource Limits

Adjust CPU and memory limits in `vaultwarden.yaml` based on your usage:

```yaml
resources:
  requests:
    memory: "256Mi"      # Increase for large deployments
    cpu: "200m"          # Increase for high load
  limits:
    memory: "1Gi"        # Increase for large deployments
    cpu: "1000m"         # Increase for high load
```

## Monitoring and Alerting

The deployment includes comprehensive metrics. Consider setting up alerts for:

- High error rates (>5%)
- High response times (>5s)
- Low availability
- Failed authentication attempts

See the [MONITORING.md](../MONITORING.md) file for complete Grafana dashboards and alerting rules.

## Troubleshooting

### Check Pod Status
```bash
kubectl get pods -n vaultwarden
kubectl logs -n vaultwarden deployment/vaultwarden
```

### Check Secrets
```bash
kubectl get secrets -n vaultwarden
kubectl describe externalsecret -n vaultwarden vaultwarden-secrets
```

### Test Metrics
```bash
kubectl port-forward -n vaultwarden svc/vaultwarden-metrics 8080:80
curl -H "Authorization: Bearer your-metrics-token" http://localhost:8080/metrics
```

### Check Service Monitor
```bash
kubectl get servicemonitor -n vaultwarden
kubectl describe servicemonitor -n vaultwarden vaultwarden-metrics
```