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
    dag_id='test-kubernetes-job',
    default_args=default_args,
    description='A DAG to run a Kubernetes job',
    schedule_interval=None,
    max_active_runs=1,
    catchup=False,
) as dag:

    kubernetes_job = KubernetesJobOperator(
        task_id='kubernetes-test-job',
        namespace='data-stack-dev',
        image='debian:latest',
        cmds=['bash', '-c', 'echo "Hello, World!"'],
        name='test-kubernetes-job',
        wait_until_job_complete=True,
    )
