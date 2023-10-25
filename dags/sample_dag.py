from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime, timedelta
import os

# default arguments 
default_args = {
    'owner': 'team_season',
    'start_date': datetime(2023, 10, 25),  # Modify as needed
    'depends_on_past': False,
    'retries': 1,
}

# DAG 
dag = DAG('hello_world_dag',
    default_args=default_args,
    schedule_interval=None)  # Set your desired schedule interval

# Python function
def run_hello_world_script():
    import subprocess
    subprocess.call(["python", "dags/sample_dag.py"])

# PythonOperator 
run_hello_world_task = PythonOperator(
    task_id='run_hello_world',
    python_callable=run_hello_world_script,
    dag=dag,
)

run_hello_world_task

if __name__ == "__main__":
    dag.cli()
