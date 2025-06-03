from datetime import datetime, timedelta
import os

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

    # Get the directory where this DAG file is located
    dag_folder = os.path.dirname(os.path.abspath(__file__))
    job_template_path = os.path.join(dag_folder, 'job-templates', 's3-volume-test-job.yaml')

    kubernetes_job = KubernetesJobOperator(
        task_id='kubernetes-s3-test-job',
        namespace='data-stack-dev',
        job_template_file=job_template_path,
        wait_until_job_complete=True
    )

    kubernetes_job.dry_run()