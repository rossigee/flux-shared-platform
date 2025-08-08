---
title: "Contributing Guide"
weight: 40
# bookFlatSection: false
# bookToc: true
# bookHidden: false
# bookCollapseSection: false
# bookComments: false
# bookSearchExclude: false
---

# Contributing Guide

## Overview

This repository contains shared GitOps manifests and templates for Kubernetes infrastructure. Contributions should focus on reusable, generic components that can benefit multiple clusters and organizations.

## What to Contribute

### ✅ Good Contributions

- Generic infrastructure component definitions
- Reusable automation templates
- Common monitoring and alerting patterns
- Documentation improvements
- Bug fixes and security improvements
- Template parameterization improvements

### ❌ What Not to Include

- Secrets or sensitive data
- Organization-specific configurations
- Hardcoded hostnames or domains
- Private certificates or keys
- Cluster-specific networking configurations

## Contribution Process

### 1. Fork and Clone

```bash
git clone https://github.com/rossigee/flux-shared-platform.git
cd flux-shared-platform
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

- Follow the existing directory structure
- Use template parameters for customizable values
- Add documentation for new components
- Test changes in a development environment

### 4. Template Guidelines

When creating templates:

- Use ALL_CAPS placeholders for variables (e.g., `COMPONENT_NAME`)
- Include comments explaining required substitutions
- Provide reasonable defaults where possible
- Document any dependencies or prerequisites

Example:
```yaml
# Replace COMPONENT_NAME with actual component name
metadata:
  name: COMPONENT_NAME
  namespace: NAMESPACE_NAME  # Replace with target namespace
```

### 5. Documentation

- Update README.md if adding new directories
- Add usage examples for new components
- Include security considerations for new features
- Update this documentation site with new patterns

### 6. Testing

Before submitting:

- Validate YAML syntax
- Test templates with actual values
- Verify no sensitive data is included
- Check for spelling and grammar errors

### 7. Submit Pull Request

- Provide clear description of changes
- Reference any related issues
- Include testing instructions
- Request review from maintainers

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and improve
- Follow security best practices

## Questions?

- Open an issue for questions
- Check existing documentation first
- Provide context when asking for help