# Setup

This repository contains Apache Airflow DAGs deployed to Kubernetes using the official Apache Airflow Helm chart.

DAGs are synced directly from this repository using Airflow's Git Sync sidecar.

## Requirements

* Kubernetes cluster
* Helm 3
* `kubectl`
* Access to the Kubernetes cluster
* Access to the Git repository from the cluster

## Configuration

Copy the example Helm values:

```bash
cp airflow-values.yaml.example airflow-values.yaml
```

Update `airflow-values.yaml` with your environment-specific configuration.

The values file configures the Airflow deployment and Git Sync, including the repository, branch/revision, and any required Git credentials.

Git Sync is configured through the Helm chart's `dags.gitSync` settings.

## Deploy

Add the official Airflow Helm repository:

```bash
helm repo add apache-airflow https://airflow.apache.org
helm repo update
```

Install or upgrade Airflow:

```bash
helm upgrade --install airflow apache-airflow/airflow \
  -f airflow-values.yaml
```

Check the deployment:

```bash
kubectl get pods
```

Once the Git Sync sidecar has pulled the repository, the DAGs under `dags/` will be available to Airflow.

## Updating DAGs

Changes pushed to the configured Git branch are automatically picked up by Git Sync. The sync interval is configurable through the Helm chart's `dags.gitSync` settings.

No DAG files need to be copied into the Kubernetes cluster manually.

## Useful commands

```bash
# Check Airflow pods
kubectl get pods

# Check Git Sync logs
kubectl logs <pod> -c git-sync

# Check Helm release
helm status airflow

# Upgrade after changing values
helm upgrade airflow apache-airflow/airflow \
  -f airflow-values.yaml
```

For more information, see the [Apache Airflow Helm Chart documentation](https://airflow.apache.org/docs/helm-chart/stable/).
