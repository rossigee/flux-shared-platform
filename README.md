# Flux Shared Platform

A collection of reusable GitOps manifests and templates for Kubernetes infrastructure deployment using Flux CD.

## Overview

This repository provides a centralized library of reusable GitOps manifests and templates for:
- Common infrastructure component definitions (cert-manager, external-secrets, argo-workflows, etc.)
- Reusable automation templates and monitoring patterns  
- RBAC templates and networking configurations
- Cross-cluster shared Helm repository definitions

## Quick Start

Add as a GitRepository source in your Flux configuration:

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
  url: https://gitea.golder.tech/infrastructure/flux-shared-platform
```

Then reference shared components:

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: cert-manager
spec:
  sourceRef:
    kind: GitRepository
    name: flux-shared-platform
  path: ./infrastructure/cert-manager
  # Add cluster-specific patches as needed
```

## Documentation

📖 **Complete documentation** is available at [https://rossigee.github.io/flux-shared-platform](https://rossigee.github.io/flux-shared-platform):

- **Architecture & Design Principles**: Understanding the security-first, reusable component approach
- **Component Reference**: Detailed documentation of all infrastructure components
- **Migration Guide**: Step-by-step migration from duplicated manifests to shared components  
- **Usage Patterns**: Real-world examples and customization strategies
- **Testing & Validation**: Comprehensive testing procedures and troubleshooting guides
- **Best Practices**: Security, customization, and operational recommendations

## Repository Structure

```
flux-shared-platform/
├── infrastructure/          # Core platform components
├── helm-repos/             # Common Helm repository definitions  
├── templates/              # Reusable automation and monitoring templates
├── examples/               # Reference implementations and patterns
└── scripts/                # Validation and testing utilities
```

## Security

- **Zero embedded secrets** - all sensitive data managed through External Secrets
- **Parameterized configurations** - customize via Kustomize overlays and Helm values
- **Security-first design** - implements defense-in-depth and zero-trust principles
- **Review before deployment** - validate all templates in staging environments

## Contributing

Contributions should focus on reusable, generic components that benefit multiple clusters and organizations. See the [Contributing Guide](https://rossigee.github.io/flux-shared-platform/docs/contributing/) for detailed guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
