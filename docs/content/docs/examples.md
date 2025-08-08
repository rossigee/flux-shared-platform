---
title: "Examples"
weight: 60
# bookFlatSection: false
# bookToc: true
# bookHidden: false
# bookCollapseSection: false
# bookComments: false
# bookSearchExclude: false
---

# Examples

Real-world examples of using the Flux Shared Platform components.

## Complete Cluster Setup

### Basic Production Cluster

Here's a complete example of setting up a production Kubernetes cluster with essential components:

```yaml
# 1. Add the shared platform source
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: flux-shared-platform
  namespace: flux-system
spec:
  interval: 10m
  ref:
    branch: main
  url: https://github.com/rossigee/flux-shared-platform

---
# 2. Deploy helm repositories first
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: shared-helm-repos
  namespace: flux-system
spec:
  interval: 30m
  path: ./helm-repos
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  prune: true

---
# 3. Certificate management
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
  dependsOn:
    - name: shared-helm-repos
  targetNamespace: cert-manager

---
# 4. Secrets management
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: external-secrets
  namespace: flux-system
spec:
  interval: 30m
  path: ./infrastructure/external-secrets
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  dependsOn:
    - name: shared-helm-repos
  targetNamespace: external-secrets

---
# 5. Monitoring stack
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: prometheus-operator
  namespace: flux-system
spec:
  interval: 30m
  path: ./infrastructure/prometheus-operator
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  dependsOn:
    - name: shared-helm-repos
  targetNamespace: monitoring

---
# 6. Policy enforcement
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: kyverno
  namespace: flux-system
spec:
  interval: 30m
  path: ./infrastructure/kyverno
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  dependsOn:
    - name: shared-helm-repos
  targetNamespace: kyverno
```

## Environment-Specific Customizations

### Development Environment

```yaml
# Development cluster with relaxed security for faster iteration
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: argo-workflows-dev
  namespace: flux-system
spec:
  interval: 10m  # Faster sync for development
  path: ./infrastructure/argo-workflows
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  patches:
    - patch: |
        - op: replace
          path: /spec/values/controller/workflowNamespaces
          value: ["default", "development", "testing"]
        - op: replace
          path: /spec/values/server/secure
          value: false  # Disable HTTPS for local development
      target:
        kind: HelmRelease
        name: argo-workflows
```

### Production Environment

```yaml
# Production cluster with enhanced security and monitoring
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: argo-workflows-prod
  namespace: flux-system
spec:
  interval: 30m  # Slower sync for stability
  path: ./infrastructure/argo-workflows
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  patches:
    - patch: |
        - op: replace
          path: /spec/values/controller/workflowNamespaces
          value: ["production"]
        - op: replace
          path: /spec/values/server/secure
          value: true
        - op: add
          path: /spec/values/controller/resources
          value:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 1000m
              memory: 2Gi
      target:
        kind: HelmRelease
        name: argo-workflows
```

## Multi-Cluster Deployments

### Shared Services Cluster

```yaml
# Cluster dedicated to shared services (monitoring, secrets management)
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: shared-monitoring
  namespace: flux-system
spec:
  path: ./infrastructure/prometheus-operator
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  patches:
    - patch: |
        - op: replace
          path: /spec/values/prometheus/prometheusSpec/retention
          value: "90d"  # Longer retention for central monitoring
        - op: replace
          path: /spec/values/prometheus/prometheusSpec/storage/volumeClaimTemplate/spec/resources/requests/storage
          value: "500Gi"
      target:
        kind: HelmRelease
        name: prometheus-operator
```

### Application Clusters

```yaml
# Application clusters with minimal monitoring (metrics forwarded to shared cluster)
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: lightweight-monitoring
  namespace: flux-system
spec:
  path: ./infrastructure/prometheus-operator
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  patches:
    - patch: |
        - op: replace
          path: /spec/values/prometheus/prometheusSpec/retention
          value: "7d"  # Short retention, forward to central
        - op: add
          path: /spec/values/prometheus/prometheusSpec/remoteWrite
          value:
            - url: https://shared-monitoring.example.com/api/v1/write
      target:
        kind: HelmRelease
        name: prometheus-operator
```

## Security Configurations

### High Security Environment

```yaml
# Enhanced security configuration with policy enforcement
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: security-policies
  namespace: flux-system
spec:
  path: ./infrastructure/kyverno-policies
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  patches:
    - patch: |
        - op: replace
          path: /spec/validationFailureAction
          value: enforce  # Block non-compliant resources
      target:
        kind: ClusterPolicy
        name: disallow-privileged-containers
```

### Network Security

```yaml
# Cilium with enhanced network policies
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: cilium-secure
  namespace: flux-system
spec:
  path: ./infrastructure/cilium
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  patches:
    - patch: |
        - op: replace
          path: /spec/values/hubble/enabled
          value: true
        - op: replace
          path: /spec/values/hubble/relay/enabled
          value: true
        - op: replace
          path: /spec/values/hubble/ui/enabled
          value: true
      target:
        kind: HelmRelease
        name: cilium
```

## Integration Patterns

### GitOps with External Secrets

```yaml
# External secrets integrated with HashiCorp Vault
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: external-secrets
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "external-secrets"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  refreshInterval: 15s
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: database-credentials
    creationPolicy: Owner
  data:
  - secretKey: username
    remoteRef:
      key: database/production
      property: username
  - secretKey: password
    remoteRef:
      key: database/production
      property: password
```

### Monitoring Integration

```yaml
# Custom monitoring for your applications
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: my-app-metrics
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: my-application
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics

---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: my-app-alerts
  namespace: monitoring
spec:
  groups:
  - name: my-app.rules
    rules:
    - alert: MyAppDown
      expr: up{job="my-application"} == 0
      for: 5m
      annotations:
        summary: "My application is down"
```

## Cloud Provider Specific Examples

The `examples/` directory in the repository contains detailed examples for:

- **AWS**: EKS-specific configurations with ALB ingress, EBS CSI, and IAM roles
- **Azure**: AKS-specific configurations with Azure DNS and Key Vault integration  
- **GCP**: GKE-specific configurations with Cloud DNS and Secret Manager
- **On-premises**: Bare metal Kubernetes with MetalLB and local storage

## Testing Examples

For testing and validation examples, see the [Testing Guide](testing/) which includes:

- Health check manifests
- Load testing configurations
- Rollback procedures
- Monitoring validation

## More Examples

Browse the complete examples directory in the repository:
- [Repository Examples](https://github.com/rossigee/flux-shared-platform/tree/main/examples)

Each example includes:
- Complete configuration files
- Deployment instructions  
- Customization options
- Testing procedures