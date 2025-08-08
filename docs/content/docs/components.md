---
title: "Component Reference"
weight: 50
# bookFlatSection: false
# bookToc: true
# bookHidden: false
# bookCollapseSection: false
# bookComments: false
# bookSearchExclude: false
---

# Component Reference

This section provides detailed information about all available infrastructure components in the shared platform.

## Core Infrastructure Components

### Certificate Management

#### cert-manager
- **Path**: `./infrastructure/cert-manager`
- **Purpose**: Automated certificate lifecycle management
- **Dependencies**: jetstack helm repository
- **Customization**: Minimal configuration needed for most use cases

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: cert-manager
  namespace: flux-system
spec:
  path: ./infrastructure/cert-manager
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  targetNamespace: cert-manager
```

#### trust-manager (included with cert-manager)
- **Purpose**: CA bundle distribution and trust chain management
- **Integration**: Automatically deployed with cert-manager
- **Use case**: Distribute internal CA certificates across the cluster

### Secrets Management

#### external-secrets
- **Path**: `./infrastructure/external-secrets`
- **Purpose**: Kubernetes-native secret synchronization
- **Integration**: Works with HashiCorp Vault, AWS Secrets Manager, Azure Key Vault
- **Dependencies**: external-secrets helm repository

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: external-secrets
  namespace: flux-system
spec:
  path: ./infrastructure/external-secrets
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  targetNamespace: external-secrets
```

### Workflow Orchestration

#### argo-workflows
- **Path**: `./infrastructure/argo-workflows`
- **Purpose**: Kubernetes-native workflow engine
- **Use cases**: CI/CD pipelines, data processing, backup automation
- **Dependencies**: argoproj helm repository
- **Common customization**: workflowNamespaces configuration

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: argo-workflows
  namespace: flux-system
spec:
  path: ./infrastructure/argo-workflows
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  patches:
    - patch: |
        - op: replace
          path: /spec/values/controller/workflowNamespaces
          value: ["production", "staging", "default"]
      target:
        kind: HelmRelease
        name: argo-workflows
```

### Monitoring Stack

#### prometheus-operator
- **Path**: `./infrastructure/prometheus-operator`
- **Purpose**: Metrics collection and alerting infrastructure
- **Components**: Prometheus, Grafana, AlertManager
- **Dependencies**: prometheus helm repository

#### kube-state-metrics
- **Path**: `./infrastructure/kube-state-metrics`
- **Purpose**: Kubernetes cluster state metrics
- **Integration**: Works with prometheus-operator

### Policy and Security

#### kyverno
- **Path**: `./infrastructure/kyverno`
- **Purpose**: Policy enforcement and governance
- **Use cases**: Security policies, resource validation, mutation
- **Dependencies**: kyverno helm repository

#### kubescape
- **Path**: `./infrastructure/kubescape`
- **Purpose**: Kubernetes security scanning and compliance
- **Integration**: Provides security insights and compliance reports

### Networking

#### cilium
- **Path**: `./infrastructure/cilium`
- **Purpose**: Advanced networking and security for Kubernetes
- **Features**: Network policies, service mesh, observability
- **Dependencies**: cilium helm repository

#### external-dns
- **Path**: `./infrastructure/external-dns`
- **Purpose**: Automated DNS record management
- **Integration**: Works with cert-manager for automated certificate management

### Storage

#### csi-driver-lvm
- **Path**: `./infrastructure/csi-driver-lvm`
- **Purpose**: LVM-based persistent volume provisioning
- **Use case**: High-performance local storage

### Application Management

#### argocd
- **Path**: `./infrastructure/argocd`
- **Purpose**: GitOps application deployment and management
- **Separation**: Complements Flux CD for application-specific deployments

## Templates and Patterns

### Automation Templates
- **Path**: `./templates/automation/`
- **Components**: Discord notifications, image update automation, webhook receivers
- **Use case**: Extend Flux CD with custom automation workflows

### Monitoring Templates
- **Path**: `./templates/monitoring/`
- **Components**: Prometheus rules, scrape configs, alert definitions
- **Categories**: Infrastructure, application, security, and network monitoring

### RBAC Templates
- **Path**: `./templates/rbac/`
- **Components**: Service accounts, role definitions, SSO integration
- **Use case**: Standardized permission patterns

### Networking Templates
- **Path**: `./templates/networking/`
- **Components**: Ingress patterns, network policies, service definitions
- **Use case**: Secure networking configurations

## Helm Repositories

The shared platform includes definitions for common Helm repositories:

- **jetstack**: cert-manager charts
- **external-secrets**: External secrets operator charts  
- **argoproj**: Argo project charts (workflows, CD, events)
- **prometheus**: Prometheus community charts
- **kyverno**: Policy engine charts
- **cilium**: Networking charts
- **grafana**: Grafana and related charts

## Usage Patterns

### Basic Component Deployment
```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: COMPONENT_NAME
  namespace: flux-system
spec:
  interval: 30m
  path: ./infrastructure/COMPONENT_NAME
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  dependsOn:
    - name: shared-helm-repos
  targetNamespace: COMPONENT_NAMESPACE
```

### Component with Customization
```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: COMPONENT_NAME-custom
  namespace: flux-system
spec:
  interval: 30m
  path: ./infrastructure/COMPONENT_NAME
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  patches:
    - patch: |
        - op: replace
          path: /spec/values/SETTING_PATH
          value: CUSTOM_VALUE
      target:
        kind: HelmRelease
        name: COMPONENT_NAME
```

## Integration Examples

See the `examples/` directory in the repository for complete integration examples including:

- Multi-cluster deployments
- Environment-specific configurations
- Complete monitoring stacks
- Security policy implementations

## Next Steps

1. Review the [Usage Guide](usage/) for deployment best practices
2. Check the [Migration Guide](migration/) for transitioning existing infrastructure
3. Use the [Testing Guide](testing/) to validate your deployments
4. Explore the [examples directory](https://github.com/rossigee/flux-shared-platform/tree/main/examples) for real-world usage patterns