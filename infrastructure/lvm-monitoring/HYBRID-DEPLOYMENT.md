# Hybrid LVM Monitoring Deployment

## Overview

This document describes how to deploy LVM monitoring with both Kubernetes-level and node-level monitoring capabilities.

## Components

### 1. Base Monitoring (Required)
- **CronJobs**: Scheduled reports and health checks
- **Deployment**: Continuous metrics collection
- **ConfigMaps**: Monitoring scripts
- **RBAC**: Service account and permissions

### 2. Node-Level Monitoring (Optional)
- **DaemonSet**: Direct LVM metrics from each node
- Requires privileged access
- Provides hardware-level visibility

## Deployment Options

### Option 1: Kubernetes-Only Monitoring (Default)
Best for environments with strict security requirements.

```yaml
# In your cluster's kustomization.yaml
resources:
  - github.com/goldertech/flux-shared-platform/infrastructure/lvm-monitoring?ref=master
```

Features:
- ✅ Pod Security Standards compliant
- ✅ No privileged containers
- ✅ PVC and namespace metrics
- ❌ No direct LVM visibility

### Option 2: Hybrid Monitoring
Best for environments needing complete storage visibility.

```yaml
# In your cluster's kustomization.yaml
resources:
  - github.com/goldertech/flux-shared-platform/infrastructure/lvm-monitoring?ref=master
  
patches:
  - target:
      kind: Kustomization
    patch: |-
      - op: add
        path: /resources/-
        value: daemonset.yaml
```

Or create a local overlay:

```yaml
# In your cluster's kustomization.yaml
resources:
  - github.com/goldertech/flux-shared-platform/infrastructure/lvm-monitoring?ref=master
  - daemonset-override.yaml  # Local daemonset configuration
```

Features:
- ✅ Complete storage visibility
- ✅ Volume group metrics
- ✅ Hardware-level monitoring
- ❌ Requires privileged containers

## Security Considerations

### DaemonSet Requirements
The DaemonSet requires:
- `privileged: true` - Access to LVM commands
- `hostPID: true` - Access to host processes
- `runAsUser: 0` - Root access for hardware

### Mitigation Strategies
1. Use Pod Security Policies to restrict DaemonSet deployment
2. Deploy only on specific nodes using node selectors
3. Use separate namespace with restricted access
4. Regular security audits

## Metrics Collection

### From CronJobs/Deployment
- PVC capacity and usage
- Namespace storage allocation
- Orphaned PVC detection
- Failed PVC alerts

### From DaemonSet
- Volume Group (VG) size and free space
- Logical Volume (LV) sizes
- Physical Volume (PV) status
- Node-specific storage health

## Integration Points

1. **Prometheus Push Gateway**
   - Both components push metrics
   - Unified dashboard in Grafana

2. **MinIO Storage**
   - Reports stored centrally
   - Historical data retention

3. **Alert Routing**
   - Critical alerts from both sources
   - Discord notifications

## Example Deployment

### Staging Environment (Hybrid)
```bash
# Update kustomization to include daemonset
cd flux-golder/clusters/golder-staging/lvm-monitoring
cat >> kustomization.yaml <<EOF

# Add node-level monitoring
resources:
  - github.com/goldertech/flux-shared-platform/infrastructure/lvm-monitoring?ref=master
  - minio-resources.yaml

patches:
  # ... existing patches ...
  - target:
      kind: Kustomization
    patch: |-
      - op: add
        path: /resources/-
        value: daemonset.yaml
EOF
```

### Production Environment (Kubernetes-Only)
```bash
# Keep default configuration for security
cd flux-golder/clusters/golder-production/lvm-monitoring
# No changes needed - daemonset not included by default
```

## Monitoring Dashboard

Access unified metrics in Grafana:
- Kubernetes PVC metrics
- Node LVM metrics (if DaemonSet deployed)
- Combined storage utilization view
- Alerting thresholds

## Troubleshooting

### DaemonSet Issues
```bash
# Check pod status on each node
kubectl get pods -n lvm-monitoring -l app=lvm-node-exporter -o wide

# View logs from specific node
kubectl logs -n lvm-monitoring -l app=lvm-node-exporter --prefix=true
```

### Missing Node Metrics
1. Verify DaemonSet is deployed
2. Check node tolerations
3. Verify LVM tools are available
4. Check privileged container permissions

## Future Enhancements
1. CSI driver integration for direct metrics
2. Operator-based deployment for better security
3. eBPF-based monitoring (no privileged required)
4. Integration with storage auto-scaling