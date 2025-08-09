#!/bin/bash
set -euo pipefail

# Configuration
REGISTRY="PRIVATE_REGISTRY"
PROJECT="infrastructure"
IMAGE_NAME="lvm-monitor"
VERSION="${1:-v1.0.0}"

echo "Building LVM monitoring container image..."
echo "Registry: ${REGISTRY}/${PROJECT}/${IMAGE_NAME}:${VERSION}"

# Build the image
docker build -f Dockerfile.monitoring -t "${REGISTRY}/${PROJECT}/${IMAGE_NAME}:${VERSION}" .

# Also tag as latest
docker tag "${REGISTRY}/${PROJECT}/${IMAGE_NAME}:${VERSION}" "${REGISTRY}/${PROJECT}/${IMAGE_NAME}:latest"

echo ""
echo "To push to Harbor, run:"
echo "  docker push ${REGISTRY}/${PROJECT}/${IMAGE_NAME}:${VERSION}"
echo "  docker push ${REGISTRY}/${PROJECT}/${IMAGE_NAME}:latest"
echo ""
echo "Make sure you're logged in to Harbor first:"
echo "  docker login ${REGISTRY}"