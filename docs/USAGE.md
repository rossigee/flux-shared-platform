# Usage Guide

## Getting Started

### 1. Add as Git Source

First, add the shared platform repository as a GitRepository source in your Flux configuration:

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: flux-shared-platform
  namespace: flux-system
spec:
  interval: 10m
  ref:
    branch: main
  url: https://github.com/your-org/flux-shared-platform
```

### 2. Use Shared Infrastructure Components

Reference shared infrastructure components in your Kustomizations:

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: cert-manager
  namespace: flux-system
spec:
  interval: 30m
  path: ./infrastructure/cert-manager
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  targetNamespace: cert-manager
```

### 3. Customize with Patches

Use Kustomize patches to customize shared components for your cluster:

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: argo-workflows
spec:
  # ... other fields ...
  patches:
    - patch: |
        - op: replace
          path: /spec/values/controller/workflowNamespaces
          value: ["production", "staging"]
      target:
        kind: HelmRelease
        name: argo-workflows
```

## Available Components

### Infrastructure Components

- **cert-manager**: Certificate management
- **external-secrets**: External secrets operator
- **argo-workflows**: Workflow engine

### Templates

- **automation/**: Image update automation and Discord notifications
- **kustomization/**: Common kustomization patterns
- **monitoring/**: Prometheus rules and scrape configs
- **rbac/**: RBAC templates for SSO and service accounts
- **networking/**: Ingress and NetworkPolicy templates

## Best Practices

### Security

1. Never include secrets in shared configurations
2. Use External Secrets or sealed secrets for sensitive data
3. Review all templates before applying to production
4. Use least-privilege RBAC configurations

### Customization

1. Use Kustomize patches instead of forking shared components
2. Keep cluster-specific configurations in your private repository
3. Version pin shared components for stability
4. Test changes in staging environments first

### Monitoring

1. Customize monitoring templates for your environment
2. Add cluster-specific alerting rules
3. Configure notification channels appropriately
4. Monitor resource usage and scaling

## Examples

See the `examples/` directory for:
- Complete cluster configurations
- Component usage patterns
- Customization examples
- Integration patterns