from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator


with DAG(
    dag_id="seatunnel_sales_pipeline",
    start_date=datetime(2026, 8, 21),
    schedule=None,
    catchup=False,
    tags=["seatunnel", "hdfs", "postgres"],
) as dag:

    csv_to_hdfs = BashOperator(
        task_id="csv_to_hdfs",
        bash_command=(
            "~/seatunnel/bin/seatunnel.sh "
            "--config ~/seatunnel-demo/csv_to_hdfs.conf"
        ),
    )

    hdfs_to_postgres = BashOperator(
        task_id="hdfs_to_postgres",
        bash_command=(
            "~/seatunnel/bin/seatunnel.sh "
            "--config ~/seatunnel-demo/hdfs_to_postgres.conf"
        ),
    )

    csv_to_hdfs >> hdfs_to_postgres
