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

## Automated Testing

### Health Checks

Add monitoring to verify components are healthy:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: health-check
  namespace: default
spec:
  containers:
  - name: checker
    image: curlimages/curl:latest
    command:
    - /bin/sh
    - -c
    - |
      # Test cert-manager webhook
      curl -k https://cert-manager-webhook.cert-manager.svc:443/readyz

      # Test external-secrets
      curl http://external-secrets.external-secrets.svc:8080/metrics

      # Test argo-workflows
      curl http://argo-workflows-server.argo-workflows.svc:2746/api/v1/info
  restartPolicy: Never
```

### Integration Tests

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
# Test external-secrets with a dummy secret
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: test-store
  namespace: default
spec:
  provider:
    kubernetes:
      server:
        url: https://kubernetes.default.svc
      auth:
        serviceAccount:
          name: default

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
kubectl describe pods -n external-secrets
kubectl describe pods -n argo-workflows
```

### Reconciliation Performance

Monitor Flux reconciliation times:

```bash
# Check reconciliation duration
flux get kustomizations | grep -E "(shared|cert-manager|external-secrets|argo-workflows)"

# Monitor for reconciliation delays
kubectl get events -n flux-system | grep -i "reconcil"
```

## Load Testing

### Concurrent Operations

Test system behavior under load:

```bash
# Create multiple test certificates simultaneously
for i in {1..10}; do
  kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: load-test-cert-$i
  namespace: default
spec:
  secretName: load-test-cert-$i-tls
  issuerRef:
    name: selfsigned-issuer
    kind: ClusterIssuer
  dnsNames:
  - test-$i.example.com
EOF
done

# Monitor certificate creation
watch "kubectl get certificates -A"
```

### Workflow Scaling

Test argo-workflows under load:

```bash
# Submit multiple workflows
for i in {1..20}; do
  argo submit -n argo-workflows - <<EOF
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: load-test-$i-
spec:
  entrypoint: sleep-test
  templates:
  - name: sleep-test
    container:
      image: alpine:latest
      command: [sleep, "60"]
EOF
done

# Monitor workflow execution
argo list -n argo-workflows
```

## Rollback Testing

### Component Rollback

Test rollback procedures:

```bash
# Suspend shared component
flux suspend kustomization cert-manager-shared

# Verify cluster-specific component takes over
kubectl get helmreleases -n cert-manager

# Resume shared component
flux resume kustomization cert-manager-shared
```

### Version Rollback

Test component version rollback:

```bash
# Update shared component to previous version
# (This would be done via git commit to shared platform repo)

# Monitor rollback process
flux reconcile kustomization cert-manager-shared
kubectl rollout status deployment/cert-manager -n cert-manager
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

### Network Isolation

Test component behavior with network restrictions:

```yaml
# Apply restrictive network policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-isolation
  namespace: cert-manager
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress: []  # Block all egress
```

Monitor component behavior and recovery after removing the policy.

## Continuous Testing

### Automated Validation

Set up automated testing with GitHub Actions or similar:

```yaml
name: Validate Shared Platform
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup kubectl
      uses: azure/setup-kubectl@v1
    - name: Setup flux
      uses: fluxcd/flux2/action@main
    - name: Run validation
      run: ./scripts/validate-migration.sh
```

### Health Monitoring

Implement continuous health checks:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: health-check-script
  namespace: monitoring
data:
  check.sh: |
    #!/bin/bash
    # Continuous health monitoring for shared platform
    while true; do
      echo "$(date): Checking shared platform health..."
      ./validate-migration.sh
      sleep 300  # Check every 5 minutes
    done
```

This comprehensive testing approach ensures the migration is successful and the shared platform components are working correctly in your environment.
