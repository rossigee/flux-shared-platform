# Migration Guide

This guide helps you migrate from duplicated infrastructure manifests to the shared platform components.

## Prerequisites

- Existing Flux CD installation
- Access to modify cluster GitOps repositories
- Understanding of Kustomize patches

## Migration Steps

### 1. Add Shared Platform Source

Add the shared platform as a GitRepository source:

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: flux-shared-platform
  namespace: flux-system
spec:
  interval: 20m
  ref:
    branch: main
  url: https://github.com/rossigee/flux-shared-platform
```

### 2. Deploy Helm Repositories First

Deploy shared helm repositories before infrastructure components:

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: helm-repos
  namespace: flux-system
spec:
  interval: 30m
  path: ./helm-repos
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
```

### 3. Migrate Components Gradually

For each component, follow this pattern:

#### Before (Duplicated)
```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: cert-manager
spec:
  path: ./clusters/production/cert-manager
  sourceRef:
    kind: GitRepository
    name: my-cluster-repo
```

#### After (Shared + Override)
```yaml
# Deploy shared component
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: cert-manager-shared
spec:
  dependsOn:
    - name: helm-repos
  path: ./infrastructure/cert-manager
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  targetNamespace: cert-manager

---
# Deploy cluster-specific overrides
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: cert-manager
spec:
  dependsOn:
    - name: cert-manager-shared
  path: ./clusters/production/cert-manager
  sourceRef:
    kind: GitRepository
    name: my-cluster-repo
  targetNamespace: cert-manager
```

### 4. Update Cluster-Specific Kustomizations

Remove infrastructure references from cluster kustomizations:

#### Before
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../../infrastructure/cert-manager  # Remove this
  - automation.yaml
  - namespace.yaml
```

#### After
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - automation.yaml
  - namespace.yaml
  # Shared component deployed via cert-manager-shared kustomization
```

### 5. Update Dependencies

Update all component dependencies to reference shared versions:

```yaml
# Change from:
dependsOn:
  - name: cert-manager

# To:
dependsOn:
  - name: cert-manager-shared
```

## Component-Specific Migration

### Cert-Manager
- No customization typically needed
- Keep cluster-specific automation and namespaces

### External-Secrets
- Update chart version references
- Maintain cluster-specific CA certificates and secrets

### Argo Workflows
- Customize `workflowNamespaces` using patches:

```yaml
patches:
  - patch: |
      - op: replace
        path: /spec/values/controller/workflowNamespaces
        value: ["production", "staging"]
    target:
      kind: HelmRelease
      name: argo-workflows
```

## Testing Strategy

1. **Start with staging environments**
2. **Deploy one component at a time**
3. **Verify functionality before proceeding**
4. **Monitor for reconciliation errors**
5. **Test cluster-specific customizations**

## Rollback Plan

If issues occur, you can quickly rollback by:

1. Suspending shared component kustomizations
2. Re-enabling original infrastructure references
3. Removing shared platform GitRepository source

## Troubleshooting

### Common Issues

**Reconciliation Loops**
- Ensure old infrastructure references are removed
- Check for conflicting resource ownership

**Missing Dependencies**
- Verify helm repositories are deployed first
- Check dependency chains in kustomizations

**Version Conflicts**
- Update shared platform to match your current versions
- Use patches to override specific values

### Monitoring

Watch Flux reconciliation status:

```bash
flux get kustomizations
flux get helmreleases
flux logs --follow
```

## Benefits After Migration

- **Reduced Duplication**: ~60-70% fewer manifests to maintain
- **Consistency**: Shared components ensure uniform configurations
- **Updates**: Centralized component version management
- **Community**: Contribute and benefit from shared improvements
