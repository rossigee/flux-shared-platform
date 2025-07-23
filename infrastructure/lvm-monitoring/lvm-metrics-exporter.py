#!/usr/bin/env python3
"""
LVM Storage Metrics Exporter for Kubernetes
Collects storage metrics and pushes to Prometheus Push Gateway
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional

from kubernetes import client, config
from prometheus_client import CollectorRegistry, Gauge, Counter, push_to_gateway
from prometheus_client.exposition import basic_auth_handler


# Configuration
PUSH_GATEWAY_URL = os.getenv('PROMETHEUS_PUSH_GATEWAY', 'http://prometheus-pushgateway:9091')
PUSH_GATEWAY_USER = os.getenv('PUSH_GATEWAY_USER', '')
PUSH_GATEWAY_PASS = os.getenv('PUSH_GATEWAY_PASS', '')
CLUSTER_NAME = os.getenv('CLUSTER_NAME', 'kubernetes')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Set up logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LVMMetricsCollector:
    """Collects LVM and storage metrics from Kubernetes cluster"""

    def __init__(self):
        """Initialize Kubernetes client and Prometheus metrics"""
        try:
            # Try in-cluster config first
            config.load_incluster_config()
            logger.info("Loaded in-cluster Kubernetes config")
        except:
            # Fall back to kubeconfig
            config.load_kube_config()
            logger.info("Loaded kubeconfig")

        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.custom_api = client.CustomObjectsApi()

        # Initialize Prometheus metrics
        self.registry = CollectorRegistry()

        # Node metrics
        self.node_capacity_bytes = Gauge(
            'k8s_node_storage_capacity_bytes',
            'Node storage capacity in bytes',
            ['cluster', 'node', 'region'],
            registry=self.registry
        )

        self.node_allocatable_bytes = Gauge(
            'k8s_node_storage_allocatable_bytes',
            'Node allocatable storage in bytes',
            ['cluster', 'node', 'region'],
            registry=self.registry
        )

        # PVC metrics
        self.pvc_capacity_bytes = Gauge(
            'k8s_pvc_capacity_bytes',
            'PVC capacity in bytes',
            ['cluster', 'namespace', 'pvc', 'storageclass'],
            registry=self.registry
        )

        self.pvc_used_bytes = Gauge(
            'k8s_pvc_used_bytes',
            'PVC used space in bytes (if available)',
            ['cluster', 'namespace', 'pvc', 'storageclass'],
            registry=self.registry
        )

        # Aggregate metrics
        self.namespace_pvc_count = Gauge(
            'k8s_namespace_pvc_count',
            'Number of PVCs per namespace',
            ['cluster', 'namespace'],
            registry=self.registry
        )

        self.namespace_storage_allocated_bytes = Gauge(
            'k8s_namespace_storage_allocated_bytes',
            'Total storage allocated per namespace',
            ['cluster', 'namespace'],
            registry=self.registry
        )

        # Status metrics
        self.orphaned_pvc_count = Gauge(
            'k8s_orphaned_pvc_count',
            'Number of PVCs not mounted by any pod',
            ['cluster'],
            registry=self.registry
        )

        self.failed_pvc_count = Gauge(
            'k8s_failed_pvc_count',
            'Number of failed or pending PVCs',
            ['cluster'],
            registry=self.registry
        )

        self.evicted_pod_count = Gauge(
            'k8s_evicted_pod_count',
            'Number of evicted pods',
            ['cluster'],
            registry=self.registry
        )

        # CNPG metrics
        self.cnpg_cluster_instances = Gauge(
            'k8s_cnpg_cluster_instances',
            'Number of instances in CNPG cluster',
            ['cluster', 'namespace', 'cnpg_cluster'],
            registry=self.registry
        )

        self.cnpg_cluster_ready = Gauge(
            'k8s_cnpg_cluster_ready',
            'CNPG cluster ready status (1=ready, 0=not ready)',
            ['cluster', 'namespace', 'cnpg_cluster'],
            registry=self.registry
        )

    def _parse_storage_size(self, size_str: str) -> int:
        """Convert Kubernetes storage size to bytes"""
        if not size_str:
            return 0

        size_str = size_str.upper()
        multipliers = {
            'KI': 1024,
            'MI': 1024 * 1024,
            'GI': 1024 * 1024 * 1024,
            'TI': 1024 * 1024 * 1024 * 1024,
            'K': 1000,
            'M': 1000 * 1000,
            'G': 1000 * 1000 * 1000,
            'T': 1000 * 1000 * 1000 * 1000,
        }

        for suffix, multiplier in multipliers.items():
            if size_str.endswith(suffix):
                return int(float(size_str[:-len(suffix)]) * multiplier)

        # No suffix means bytes
        return int(size_str)

    def collect_node_metrics(self):
        """Collect storage metrics from nodes"""
        logger.info("Collecting node metrics...")

        nodes = self.v1.list_node()
        for node in nodes.items:
            node_name = node.metadata.name
            labels = node.metadata.labels or {}
            region = labels.get('topology.kubernetes.io/region', 'unknown')

            # Get capacity and allocatable storage
            capacity = node.status.capacity.get('storage', '0')
            allocatable = node.status.allocatable.get('storage', '0')

            capacity_bytes = self._parse_storage_size(capacity)
            allocatable_bytes = self._parse_storage_size(allocatable)

            self.node_capacity_bytes.labels(
                cluster=CLUSTER_NAME,
                node=node_name,
                region=region
            ).set(capacity_bytes)

            self.node_allocatable_bytes.labels(
                cluster=CLUSTER_NAME,
                node=node_name,
                region=region
            ).set(allocatable_bytes)

            logger.debug(f"Node {node_name}: capacity={capacity}, allocatable={allocatable}")

    def collect_pvc_metrics(self):
        """Collect PVC metrics and calculate aggregates"""
        logger.info("Collecting PVC metrics...")

        pvcs = self.v1.list_persistent_volume_claim_for_all_namespaces()

        # Track metrics
        namespace_totals = {}
        orphaned_count = 0
        failed_count = 0

        # Get all PVCs in use by pods
        pvcs_in_use = set()
        pods = self.v1.list_pod_for_all_namespaces()
        for pod in pods.items:
            if pod.spec.volumes:
                for volume in pod.spec.volumes:
                    if volume.persistent_volume_claim:
                        pvc_name = f"{pod.metadata.namespace}/{volume.persistent_volume_claim.claim_name}"
                        pvcs_in_use.add(pvc_name)

        for pvc in pvcs.items:
            namespace = pvc.metadata.namespace
            pvc_name = pvc.metadata.name
            full_name = f"{namespace}/{pvc_name}"

            # Initialize namespace tracking
            if namespace not in namespace_totals:
                namespace_totals[namespace] = {'count': 0, 'bytes': 0}

            # Check if PVC is bound
            if pvc.status.phase != 'Bound':
                failed_count += 1
                continue

            # Check if orphaned
            if full_name not in pvcs_in_use:
                orphaned_count += 1

            # Get storage info
            storage_class = pvc.spec.storage_class_name or 'unknown'
            capacity = pvc.spec.resources.requests.get('storage', '0')
            capacity_bytes = self._parse_storage_size(capacity)

            # Update metrics
            self.pvc_capacity_bytes.labels(
                cluster=CLUSTER_NAME,
                namespace=namespace,
                pvc=pvc_name,
                storageclass=storage_class
            ).set(capacity_bytes)

            # Update namespace totals
            namespace_totals[namespace]['count'] += 1
            namespace_totals[namespace]['bytes'] += capacity_bytes

            logger.debug(f"PVC {full_name}: {capacity} ({capacity_bytes} bytes)")

        # Set aggregate metrics
        for namespace, totals in namespace_totals.items():
            self.namespace_pvc_count.labels(
                cluster=CLUSTER_NAME,
                namespace=namespace
            ).set(totals['count'])

            self.namespace_storage_allocated_bytes.labels(
                cluster=CLUSTER_NAME,
                namespace=namespace
            ).set(totals['bytes'])

        self.orphaned_pvc_count.labels(cluster=CLUSTER_NAME).set(orphaned_count)
        self.failed_pvc_count.labels(cluster=CLUSTER_NAME).set(failed_count)

        logger.info(f"Found {orphaned_count} orphaned PVCs and {failed_count} failed PVCs")

    def collect_pod_metrics(self):
        """Collect pod-related storage metrics"""
        logger.info("Collecting pod metrics...")

        evicted_count = 0
        pods = self.v1.list_pod_for_all_namespaces(field_selector='status.phase=Failed')

        for pod in pods.items:
            if pod.status.reason == 'Evicted':
                evicted_count += 1

        self.evicted_pod_count.labels(cluster=CLUSTER_NAME).set(evicted_count)
        logger.info(f"Found {evicted_count} evicted pods")

    def collect_cnpg_metrics(self):
        """Collect CloudNativePG cluster metrics"""
        logger.info("Collecting CNPG metrics...")

        try:
            clusters = self.custom_api.list_cluster_custom_object(
                group='postgresql.cnpg.io',
                version='v1',
                plural='clusters'
            )

            for cluster in clusters.get('items', []):
                namespace = cluster['metadata']['namespace']
                name = cluster['metadata']['name']

                instances = cluster['spec'].get('instances', 0)
                ready = 1 if cluster['status'].get('phase') == 'Cluster in healthy state' else 0

                self.cnpg_cluster_instances.labels(
                    cluster=CLUSTER_NAME,
                    namespace=namespace,
                    cnpg_cluster=name
                ).set(instances)

                self.cnpg_cluster_ready.labels(
                    cluster=CLUSTER_NAME,
                    namespace=namespace,
                    cnpg_cluster=name
                ).set(ready)

                logger.debug(f"CNPG cluster {namespace}/{name}: instances={instances}, ready={ready}")

        except Exception as e:
            logger.warning(f"Failed to collect CNPG metrics: {e}")

    def push_metrics(self):
        """Push all collected metrics to Prometheus Push Gateway"""
        logger.info(f"Pushing metrics to {PUSH_GATEWAY_URL}...")

        try:
            # Configure auth if provided
            handler = None
            if PUSH_GATEWAY_USER and PUSH_GATEWAY_PASS:
                handler = basic_auth_handler(
                    lambda: (PUSH_GATEWAY_USER, PUSH_GATEWAY_PASS)
                )

            push_to_gateway(
                PUSH_GATEWAY_URL,
                job='lvm_storage_exporter',
                registry=self.registry,
                handler=handler
            )
            logger.info("Successfully pushed metrics to Prometheus")

        except Exception as e:
            logger.error(f"Failed to push metrics: {e}")
            raise

    def run(self):
        """Run complete metrics collection and push"""
        start_time = time.time()

        try:
            self.collect_node_metrics()
            self.collect_pvc_metrics()
            self.collect_pod_metrics()
            self.collect_cnpg_metrics()
            self.push_metrics()

            duration = time.time() - start_time
            logger.info(f"Metrics collection completed in {duration:.2f} seconds")

        except Exception as e:
            logger.error(f"Error during metrics collection: {e}")
            raise


def main():
    """Main entry point"""
    logger.info(f"Starting LVM Storage Metrics Exporter for cluster: {CLUSTER_NAME}")

    collector = LVMMetricsCollector()

    # Run once if no interval specified
    run_interval = int(os.getenv('RUN_INTERVAL_SECONDS', '0'))

    if run_interval <= 0:
        # Single run
        collector.run()
    else:
        # Continuous run
        logger.info(f"Running in continuous mode with {run_interval}s interval")
        while True:
            try:
                collector.run()
            except Exception as e:
                logger.error(f"Collection failed: {e}")

            time.sleep(run_interval)


if __name__ == '__main__':
    main()