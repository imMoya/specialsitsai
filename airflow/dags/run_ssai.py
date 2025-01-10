from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'run_ssai',
    default_args=default_args,
    description='DAG to run main.py daily',
    schedule_interval=timedelta(days=1),
    start_date=datetime.now() - timedelta(days=1),
    catchup=False,
)

# Define the task
run_ssai = BashOperator(
    task_id='run_ssai',
    bash_command='cd /***/secedgarspecial/ \
        && poetry run python main.py',
    dag=dag,
)

# Set the task in the DAG
run_ssai
