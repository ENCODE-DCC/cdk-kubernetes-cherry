from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.job import KubernetesJobOperator

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

    kubernetes_job = KubernetesJobOperator(
        task_id='kubernetes-s3-test-job',
        namespace='data-stack-dev',
        image='debian:latest',
        cmds=['ls', '/mnt/s3'],
        name='test-s3-volume-job',
        wait_until_job_complete=True,
        service_account_name='airflow-logging-sa',
        volumes=[
            {
                'name': 's3-volume',
                'persistentVolumeClaim': {
                    'claimName': 's3-encode-blobs-dev-claim'
                }
            }
        ],
        volume_mounts=[
            {
                'name': 's3-volume',
                'mountPath': '/mnt/s3',
                'readOnly': True
            }
        ]
    )