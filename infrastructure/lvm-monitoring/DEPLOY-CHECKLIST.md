# LVM Monitoring Deployment Checklist

## Prerequisites (Once Harbor is Available)

### 1. Push Container Images
```bash
# Push the Alpine-based image
docker push harbor.golder.lan/infrastructure/lvm-monitor:alpine-v1.0.0
docker tag harbor.golder.lan/infrastructure/lvm-monitor:alpine-v1.0.0 harbor.golder.lan/infrastructure/lvm-monitor:latest
docker push harbor.golder.lan/infrastructure/lvm-monitor:latest
```

### 2. Update Image References
Update all CronJobs and Deployments to use the new Alpine image:
- `harbor.golder.lan/infrastructure/lvm-monitor:alpine-v1.0.0`

## Deployment Steps

### SecOps Cluster (Already Deployed)
- [x] Namespace created
- [x] RBAC configured
- [x] External secrets deployed
- [x] ConfigMaps updated with mc commands
- [ ] Update CronJobs to use Alpine image
- [ ] Test mc upload functionality

### Staging Cluster
1. Create Kustomization overlay at `/home/rossg/clients/golder/infrastructure/flux-golder/clusters/golder-staging/lvm-monitoring/`
2. Configure cluster-specific values:
   - CLUSTER_NAME: "staging"
   - KUBERNETES_CONTEXT: "staging"
3. Ensure external secrets are configured for staging
4. Apply and verify deployment

### Production Cluster
1. Create Kustomization overlay at `/home/rossg/clients/golder/infrastructure/flux-golder/clusters/golder-production/lvm-monitoring/`
2. Configure cluster-specific values:
   - CLUSTER_NAME: "production"
   - KUBERNETES_CONTEXT: "production"
3. Ensure external secrets are configured for production
4. Apply and verify deployment

## Testing Procedure
1. Trigger manual job run: `kubectl create job --from=cronjob/lvm-metrics-daily test-manual -n lvm-monitoring`
2. Check logs for successful mc upload
3. Verify files in MinIO: `mcli ls assange/lvm-space-reports/<cluster>/`
4. Check Discord notifications (if configured)
5. Verify Prometheus metrics are being pushed

## Rollback Plan
If issues occur, revert to AWS CLI version:
- Image: `harbor.golder.lan/infrastructure/lvm-monitor:v1.0.0`
- ConfigMap: Revert changes in `configmap.yaml`