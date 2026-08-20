# Airflow Orchestration

### Verify Airflow Installation

```
python3 --version
pip3 --version
java -version
airflow version
```

### Verify Airflow Configuration

```
airflow info | head -30
```

#### Output

```
Apache Airflow

version       | 3.3.1
executor      | LocalExecutor
sql_alchemy_conn | sqlite:////home/abhi/airflow/airflow.db
```

This establishes that Airflow is initialized and using `LocalExecutor` with SQLite.

### Verify Airflow Home

```
echo 'export AIRFLOW_HOME=~/airflow' >> ~/.bashrc
source ~/.bashrc

echo $AIRFLOW_HOME
ls -la ~/airflow
```

### Create DAG directory

```
mkdir -p ~/airflow/dags
cd ~/airflow/dags
```

### Create DAG

```
cat > ~/airflow/dags/seatunnel_pipeline.py <<'EOF'

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

EOF
```

### Start Airflow

```
airflow standalone
```

### Verify if DAG is picked up

```
airflow dags list | grep seatunnel
```

```
seatunnel_sales_pipeline | /home/abhi/airflow/dags/seatunnel_pipeline.py | airflow | False | dags-folder | None
```

**#### Note: If Airflow is started and then DAG is created, refresh interval may be high and Airflow needs time to pick it up. Better to create DAG then start Airflow.**

### GraphViz install

```
uv tool install --force "apache-airflow[graphviz]==3.3.1"
```

##### Verify

```
~/.local/share/uv/tools/apache-airflow/bin/python -c \
"import graphviz; print('Graphviz Python package OK')"
```

```
Graphviz Python package OK
```

### Verify the DAG

```
~/airflow/dags$ airflow dags show seatunnel_sales_pipeline
```

#### Output

```
digraph seatunnel_sales_pipeline {
    graph [label=seatunnel_sales_pipeline labelloc=t rankdir=LR]
    csv_to_hdfs [color="#000000" fillcolor="#f0ede4" label=csv_to_hdfs shape=rectangle style="filled,rounded"]
    hdfs_to_postgres [color="#000000" fillcolor="#f0ede4" label=hdfs_to_postgres shape=rectangle style="filled,rounded"]
    csv_to_hdfs -> hdfs_to_postgres
}
```
Yep — add this **before clearing PostgreSQL**, so every test starts with a clean HDFS destination too:

### Clear HDFS Output

```
hdfs dfs -rm -r /seatunnel-demo/sales
hdfs dfs -mkdir -p /seatunnel-demo/sales
hdfs dfs -ls /seatunnel-demo/sales
```

### Clear Postgres Table

```
psql -h localhost -U postgres -d seatunnel_demo \
-c "TRUNCATE TABLE sales;"

psql -h localhost -U postgres -d seatunnel_demo \
-c "SELECT COUNT(*) FROM sales;"
```

### Trigger Airflow

```
airflow dags trigger seatunnel_sales_pipeline
```

### Checks

```
airflow dags list-runs seatunnel_sales_pipeline

airflow dags list-runs seatunnel_sales_pipeline --state queued

airflow dags list-runs seatunnel_sales_pipeline --state running

airflow dags list-runs seatunnel_sales_pipeline --state success
```

### Verify HDFS Output

```
hdfs dfs -ls /seatunnel-demo/sales

hdfs dfs -cat /seatunnel-demo/sales/* | wc -l
```

```
Found 1 items
-rw-r--r--   3 abhi supergroup  ... /seatunnel-demo/sales/T_....csv
49
```

The output contains **50 CSV records**. `wc -l` reports `49` because the final CSV record does not contain a trailing newline.

### Verify PostgreSQL Output

```
psql -h localhost -U postgres -d seatunnel_demo \
-c "SELECT COUNT(*) FROM sales;"
```

#### Output

```
 count
-------
    50

(1 row)
```
