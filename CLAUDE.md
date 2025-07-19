# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is a flux-shared-platform that provides reusable GitOps manifests and templates for Kubernetes infrastructure deployment using Flux CD. It serves as a centralized collection of common infrastructure components, automation templates, and monitoring patterns that can be shared across multiple clusters and organizations.

### Core Architecture

The repository follows a clear separation of concerns:
- **Infrastructure components**: Core platform services (cert-manager, external-secrets, argo-workflows, prometheus-operator, kubescape, kyverno)
- **Helm repositories**: Common Helm repository definitions for shared charts
- **Templates**: Reusable patterns for automation, monitoring, RBAC, and networking
- **Examples**: Reference implementations and usage patterns

### GitOps Integration Pattern

Components are designed to be consumed as GitRepository sources in Flux configurations:
1. Add repository as GitRepository source in flux-system namespace
2. Reference shared components via Kustomization resources
3. Apply cluster-specific patches using Kustomize overlays
4. Never include secrets or cluster-specific configurations in shared components

## Common Commands

### Validation and Testing

```bash
# Validate migration and component status
./scripts/validate-migration.sh

# Check Flux status across all components
flux get all

# Monitor reconciliation
flux get kustomizations --watch
flux logs --follow

# Check specific component logs
flux logs --kind=HelmRelease --name=cert-manager
```

### Component Verification

```bash
# Check GitRepository sources
flux get sources git
kubectl get gitrepository flux-shared-platform -n flux-system

# Verify Helm repositories
flux get sources helm
helm repo list

# Check infrastructure deployments
kubectl get kustomizations -n flux-system | grep shared
kubectl get helmreleases -A

# Verify component pods
kubectl get pods -n cert-manager
kubectl get pods -n external-secrets
kubectl get pods -n argo-workflows
```

### Testing Infrastructure Components

```bash
# Test cert-manager with test certificate
kubectl apply -f examples/test-certificate.yaml

# Test argo-workflows with simple workflow
argo submit -n argo-workflows examples/test-workflow.yaml

# Monitor resource usage
kubectl top pods -A | grep -E "(cert-manager|external-secrets|argo-workflows)"
```

## Development Guidelines

### Template Development

- Use ALL_CAPS placeholders for variables (e.g., `COMPONENT_NAME`, `NAMESPACE_NAME`)
- Include descriptive comments explaining required substitutions
- Provide reasonable defaults where possible
- Document dependencies and prerequisites in template files

### Security Requirements

- Never include secrets, API keys, or sensitive data
- Use parameterized values for all customizable fields
- Private certificates and credentials must be provided separately via External Secrets
- Review all templates before deployment to production

### Component Structure

Each infrastructure component follows standard structure:
```
infrastructure/component-name/
├── helmrelease.yaml    # Helm chart deployment
├── kustomization.yaml  # Resource aggregation
└── namespace.yaml      # Namespace definition (if needed)
```

### Customization Pattern

Shared components should be customized using Kustomize patches, not by forking:
```yaml
# In consuming cluster repository
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
spec:
  patches:
    - patch: |
        - op: replace
          path: /spec/values/controller/workflowNamespaces
          value: ["production", "staging"]
      target:
        kind: HelmRelease
        name: argo-workflows
```

## Repository Structure

- `infrastructure/`: Core platform components with HelmRelease definitions
- `helm-repos/`: Common Helm repository sources (jetstack, external-secrets, argoproj, prometheus)
- `templates/`: Reusable templates for automation, monitoring, RBAC, networking
- `examples/`: Reference cluster implementations and usage patterns
- `docs/`: Platform documentation (USAGE.md, TESTING.md, CONTRIBUTING.md)
- `scripts/`: Validation and testing utilities

## Testing Strategy

The repository includes comprehensive testing approaches:
- **validate-migration.sh**: Automated validation of component deployments
- **Health checks**: Continuous monitoring of component status
- **Integration tests**: Test certificates, workflows, and external secrets
- **Load testing**: Concurrent operations and scaling validation
- **Rollback testing**: Component and version rollback procedures

## Monitoring and Alerting

Templates include Prometheus rules for:
- Flux reconciliation failures
- Suspended resources
- Source readiness issues
- Component-specific alerts (cert-manager, DNS, etc.)

Monitor reconciliation performance and resource usage regularly to ensure healthy GitOps operations.
