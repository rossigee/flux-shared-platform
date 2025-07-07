#!/bin/bash
# Validation script for flux-shared-platform migration
# This script helps validate that the migration is working correctly

set -e

echo "🔍 Validating Flux Shared Platform Migration..."

# Check if flux CLI is available
if ! command -v flux &> /dev/null; then
    echo "❌ Flux CLI not found. Please install flux CLI: https://fluxcd.io/flux/installation/"
    exit 1
fi

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl"
    exit 1
fi

echo "✅ Prerequisites checked"

# Function to check resource status
check_resource() {
    local resource_type=$1
    local resource_name=$2
    local namespace=${3:-flux-system}

    echo "🔍 Checking $resource_type/$resource_name in namespace $namespace..."

    if kubectl get $resource_type $resource_name -n $namespace &> /dev/null; then
        local status=$(kubectl get $resource_type $resource_name -n $namespace -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')
        if [[ "$status" == "True" ]]; then
            echo "✅ $resource_type/$resource_name is Ready"
        else
            echo "⚠️  $resource_type/$resource_name is not Ready"
            kubectl get $resource_type $resource_name -n $namespace -o yaml | grep -A5 -B5 conditions || true
        fi
    else
        echo "❌ $resource_type/$resource_name not found"
    fi
}

echo ""
echo "📦 Checking GitRepository sources..."
check_resource "gitrepository" "flux-shared-platform"

echo ""
echo "📦 Checking Helm Repositories..."
check_resource "helmrepository" "jetstack"
check_resource "helmrepository" "external-secrets"
check_resource "helmrepository" "argoproj"
check_resource "helmrepository" "prometheus"

echo ""
echo "🏗️  Checking Infrastructure Components..."
check_resource "kustomization" "cert-manager-shared"
check_resource "kustomization" "external-secrets-shared"
check_resource "kustomization" "argo-workflows-shared"

echo ""
echo "📋 Checking HelmReleases..."
check_resource "helmrelease" "cert-manager" "cert-manager"
check_resource "helmrelease" "external-secrets" "external-secrets"
check_resource "helmrelease" "argo-workflows" "argo-workflows"

echo ""
echo "🔧 Checking Flux Status..."
flux get all

echo ""
echo "📊 Recent Flux Events..."
kubectl get events -n flux-system --sort-by='.lastTimestamp' | tail -10

echo ""
echo "🎉 Migration validation complete!"
echo ""
echo "💡 If you see any issues:"
echo "   - Check flux logs: flux logs --follow"
echo "   - Review specific resources: kubectl describe <resource-type> <name> -n <namespace>"
echo "   - Verify dependency order in your kustomizations"
