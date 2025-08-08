# LVM Monitoring Migration Plan

## Current State
- **SecOps**: Using shared platform components (partially deployed)
- **Staging**: Has its own implementation (not using shared platform)
- **Production**: Has its own implementation (not using shared platform)

## Migration Strategy

### Phase 1: Update Shared Platform (COMPLETED)
- [x] Updated scripts to use MinIO client (mc) instead of AWS CLI
- [x] Created Alpine-based container image for better performance
- [x] Fixed Pod Security Standards compliance
- [x] Created deployment checklist

### Phase 2: Prepare Staging Migration
1. **Review differences** between staging implementation and shared platform:
   - Staging has DaemonSet for node-level monitoring
   - Staging has different metrics collection approach
   - Staging uses different report structure

2. **Decision needed**: 
   - Option A: Migrate staging to use shared platform (standardization)
   - Option B: Keep staging implementation separate (if it has unique requirements)
   - Option C: Merge best features from both into shared platform

### Phase 3: Update Kustomizations

#### For Staging (if migrating to shared platform):
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: lvm-monitoring

resources:
  - github.com/goldertech/flux-shared-platform/infrastructure/lvm-monitoring?ref=master
  - minio-resources.yaml  # Keep local MinIO resources

patches:
  # Cluster-specific configurations
  - target:
      kind: CronJob
      name: lvm-metrics-daily
    patch: |-
      - op: replace
        path: /spec/jobTemplate/spec/template/spec/containers/0/env/0/value
        value: "golder-staging"
```

#### For Production (similar approach):
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: lvm-monitoring

resources:
  - github.com/goldertech/flux-shared-platform/infrastructure/lvm-monitoring?ref=master
  - minio-resources.yaml

patches:
  # Production-specific configurations
```

### Phase 4: Testing Strategy
1. **Staging First**:
   - Deploy shared platform version alongside existing
   - Compare metrics and reports
   - Validate all features work correctly
   - Monitor for 1 week

2. **Production Rollout**:
   - Only after staging validation
   - Blue-green deployment approach
   - Keep old implementation ready for rollback

### Phase 5: Cleanup
- Remove old implementations after successful migration
- Update documentation
- Archive old code for reference

## Risk Mitigation
1. **Data Loss**: Both implementations can run in parallel temporarily
2. **Feature Parity**: Document all features in current implementations
3. **Rollback Plan**: Keep old implementations for 30 days post-migration

## Timeline Estimate
- Phase 2: 1-2 days (analysis and decision)
- Phase 3: 1 day (configuration updates)
- Phase 4: 1-2 weeks (testing and validation)
- Phase 5: 1 day (cleanup)

## Next Steps
1. Analyze staging daemonset functionality
2. Compare metrics between implementations
3. Make architectural decision
4. Create detailed migration runbook