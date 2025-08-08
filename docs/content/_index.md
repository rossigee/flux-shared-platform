---
title: "Flux Shared Platform - Reusable GitOps Components"
description: "A comprehensive library of reusable GitOps manifests and templates for Kubernetes infrastructure deployment using Flux CD"
type: docs
---

# Flux Shared Platform

A collection of reusable GitOps manifests and templates for Kubernetes infrastructure deployment using Flux CD.

## Overview

This repository provides a centralized library of reusable GitOps manifests and templates for:

- Common infrastructure component definitions
- Reusable automation templates and monitoring patterns  
- RBAC templates and networking configurations
- Cross-cluster shared Helm repository definitions

## Quick Start

Get started quickly by adding the shared platform as a GitRepository source in your Flux configuration and referencing shared components in your cluster deployments.

## Key Features

- **Security-First Design**: Zero embedded secrets, parameterized configurations
- **Reusable Components**: Common infrastructure patterns for cert-manager, external-secrets, argo-workflows, and more
- **Customizable**: Use Kustomize overlays and Helm values for environment-specific customization
- **Well-Tested**: Comprehensive validation scripts and testing procedures

## Repository Structure

```
flux-shared-platform/
├── infrastructure/          # Core platform components
├── helm-repos/             # Common Helm repository definitions  
├── templates/              # Reusable automation and monitoring templates
├── examples/               # Reference implementations and patterns
└── scripts/                # Validation and testing utilities
```