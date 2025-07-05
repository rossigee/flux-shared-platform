# Flux Shared Platform

A collection of reusable GitOps manifests and templates for Kubernetes infrastructure deployment using Flux CD.

## Overview

This repository provides:
- Common infrastructure component definitions
- Reusable automation templates
- Monitoring and alerting patterns
- RBAC templates
- Documentation and examples

## Structure

```
flux-shared-platform/
├── infrastructure/          # Core platform components
│   ├── cert-manager/       # Certificate management
│   ├── external-secrets/   # External secrets operator
│   ├── argo-workflows/     # Workflow engine
│   └── prometheus-operator/ # Monitoring stack
├── helm-repos/             # Common Helm repository definitions
│   ├── jetstack.yaml      # Cert-manager charts
│   ├── external-secrets.yaml # External secrets charts
│   ├── argoproj.yaml      # Argo project charts
│   └── prometheus.yaml    # Prometheus community charts
├── templates/
│   ├── automation/         # Flux automation templates
│   ├── kustomization/      # Common kustomization patterns
│   ├── monitoring/         # Prometheus/alerting templates
│   ├── rbac/              # RBAC templates
│   └── networking/        # Ingress/service templates
├── examples/
│   ├── clusters/          # Reference cluster implementations
│   └── patterns/          # Usage pattern examples
└── docs/                  # Platform documentation
```

## Usage

### As a Git Source

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
  url: https://github.com/your-org/flux-shared-platform
```

### Referencing Components

Use shared components in your cluster configurations:

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

## Security Considerations

- No secrets or sensitive data are included
- All configurations use parameterized values
- Private certificates and credentials must be provided separately
- Review all templates before deployment

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines on contributing to this repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.