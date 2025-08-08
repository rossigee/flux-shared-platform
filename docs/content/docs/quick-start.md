---
title: "Quick Start"
weight: 5
# bookFlatSection: false
# bookToc: true
# bookHidden: false
# bookCollapseSection: false
# bookComments: false
# bookSearchExclude: false
---

# Quick Start Guide

Get up and running with Flux Shared Platform in minutes.

## Prerequisites

- Kubernetes cluster with Flux CD installed
- `kubectl` and `flux` CLI tools configured
- Git repository for your cluster configuration

## Step 1: Add the Shared Platform Source

Add the flux-shared-platform repository as a GitRepository source:

```yaml
# clusters/shared-platform-source.yaml
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
```

Apply it to your cluster:

```bash
kubectl apply -f clusters/shared-platform-source.yaml
```

## Step 2: Deploy Helm Repositories

First, deploy the shared Helm repositories:

```yaml
# clusters/helm-repos.yaml
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
```

```bash
kubectl apply -f clusters/helm-repos.yaml
```

## Step 3: Deploy Your First Component

Let's deploy cert-manager as an example:

```yaml
# clusters/cert-manager.yaml
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
  prune: true
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: cert-manager
      namespace: cert-manager
```

```bash
kubectl apply -f clusters/cert-manager.yaml
```

## Step 4: Verify Deployment

Check that everything is working:

```bash
# Check Flux sources
flux get sources git
flux get sources helm

# Check kustomizations
flux get kustomizations

# Verify cert-manager pods
kubectl get pods -n cert-manager

# Check cert-manager is ready
kubectl get deployment cert-manager -n cert-manager
```

## Step 5: Customize (Optional)

If you need to customize cert-manager for your environment, use Kustomize patches:

```yaml
# clusters/cert-manager-custom.yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: cert-manager-custom
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
  patches:
    - patch: |
        - op: replace
          path: /spec/values/installCRDs
          value: true
        - op: add
          path: /spec/values/resources
          value:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 200m
              memory: 256Mi
      target:
        kind: HelmRelease
        name: cert-manager
```

## Next Steps

Now you're ready to:

1. **Explore more components** - Check out external-secrets, argo-workflows, and monitoring components
2. **Read the [Usage Guide](usage/)** - Learn about best practices and advanced configurations
3. **Follow the [Migration Guide](migration/)** - Migrate existing infrastructure to shared components
4. **Set up testing** - Use our [Testing Guide](testing/) to validate your deployments

## Common Next Components

- **external-secrets** - For secret management with HashiCorp Vault
- **argo-workflows** - For CI/CD and automation workflows  
- **prometheus-operator** - For monitoring and alerting
- **kyverno** - For policy enforcement and governance

## Need Help?

- Check the [Troubleshooting section](testing/#troubleshooting-tests) in our Testing Guide
- Review our [Best Practices](usage/#best-practices)
- Open an issue in the [GitHub repository](https://github.com/rossigee/flux-shared-platform/issues)