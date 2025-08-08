---
title: "Testing Guide"
weight: 30
# bookFlatSection: false
# bookToc: true
# bookHidden: false
# bookCollapseSection: false
# bookComments: false
# bookSearchExclude: false
---

# Testing Guide

This guide provides instructions for testing the flux-shared-platform migration and components.

## Validation Script

Use the provided validation script to check migration status:

```bash
./scripts/validate-migration.sh
```

This script will:
- Check that GitRepository sources are ready
- Verify Helm repositories are available
- Validate infrastructure components are deployed
- Review HelmRelease status across namespaces
- Show recent Flux events

## Manual Testing Steps

### 1. Check Git Sources

```bash
flux get sources git
kubectl get gitrepository flux-shared-platform -n flux-system -o yaml
```

### 2. Verify Helm Repositories

```bash
flux get sources helm
helm repo list
```

### 3. Test Component Deployments

```bash
# Check shared components
kubectl get kustomizations -n flux-system | grep shared

# Check HelmReleases
kubectl get helmreleases -A

# Verify pods are running
kubectl get pods -n cert-manager
kubectl get pods -n external-secrets
kubectl get pods -n argo-workflows
```

### 4. Test Customizations

Verify that cluster-specific patches are working:

```bash
# For argo-workflows, check workflowNamespaces
kubectl get helmrelease argo-workflows -n argo-workflows -o jsonpath='{.spec.values.controller.workflowNamespaces}'

# For cert-manager, check custom values
kubectl get helmrelease cert-manager -n cert-manager -o yaml
```

### 5. Monitor Reconciliation

```bash
# Watch reconciliation status
flux get kustomizations --watch

# Check for reconciliation errors
flux logs --follow

# Specific component logs
flux logs --kind=HelmRelease --name=cert-manager
```

## Integration Tests

Create test resources to verify functionality:

```yaml
# Test cert-manager with a test certificate
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: test-cert
  namespace: default
spec:
  secretName: test-cert-tls
  issuerRef:
    name: selfsigned-issuer
    kind: ClusterIssuer
  dnsNames:
  - test.example.com

---
# Test argo-workflows with a simple workflow
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: test-workflow-
  namespace: argo-workflows
spec:
  entrypoint: hello
  templates:
  - name: hello
    container:
      image: alpine:latest
      command: [echo, "Hello from shared platform!"]
```

## Performance Testing

### Resource Usage

Monitor resource consumption after migration:

```bash
# Check resource usage by namespace
kubectl top pods -A | grep -E "(cert-manager|external-secrets|argo-workflows)"

# Check memory and CPU limits
kubectl describe pods -n cert-manager
```

### Reconciliation Performance

Monitor Flux reconciliation times:

```bash
# Check reconciliation duration
flux get kustomizations | grep -E "(shared|cert-manager|external-secrets|argo-workflows)"

# Monitor for reconciliation delays
kubectl get events -n flux-system | grep -i "reconcil"
```

## Troubleshooting Tests

### Dependency Failures

Simulate dependency failures:

```bash
# Suspend helm repositories
flux suspend source helm jetstack

# Observe impact on dependent components
flux get kustomizations | grep cert-manager

# Resume and verify recovery
flux resume source helm jetstack
```

For complete testing procedures including load testing, rollback testing, and continuous testing setup, refer to the full testing documentation in the repository.