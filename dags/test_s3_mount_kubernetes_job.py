from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.job import KubernetesJobOperator
from kubernetes.client import models as k8s

default_args = {
    'owner': 'me',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='test-s3-volume-job',
    default_args=default_args,
    description='A DAG to run a Kubernetes job with S3 volume mounted',
    schedule_interval=None,
    max_active_runs=1,
    catchup=False,
) as dag:

    volume = k8s.V1Volume(
        name='s3-volume',
        persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(
            claim_name='s3-encode-blobs-dev-claim'
        )
    )

    volume_mount = k8s.V1VolumeMount(
        name='s3-volume',
        mount_path='/mnt/s3',
        read_only=True
    )

    container = k8s.V1Container(
        name='base',
        image='debian:latest',
        command=['ls'],
        args=['/mnt/s3'],
        volume_mounts=[volume_mount]
    )

    pod_template = k8s.V1PodTemplateSpec(
        spec=k8s.V1PodSpec(
            containers=[container],
            volumes=[volume],
            service_account_name='airflow-logging-sa'
        )
    )

    kubernetes_job = KubernetesJobOperator(
        task_id='kubernetes-s3-test-job',
        namespace='data-stack-dev',
        name='test-s3-volume-job',
        wait_until_job_complete=True,
        pod_template=pod_template
    )