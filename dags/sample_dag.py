from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.operators.postgres_operator import PostgresOperator
#from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.models import Variable
from airflow.sensors.http_sensor import HttpSensor
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.operators.bash_operator import BashOperator
from sqlalchemy import create_engine

import pandas as pd

from datetime import datetime, timedelta
import requests
import csv
import os
import json

# fetching data from API,
# and saveing it as a JSON file.
def save_posts(ti):
    base_url_api = 'https://jsonplaceholder.typicode.com/todos'  

    response = requests.get(f'{base_url_api}')
    response_data = response.json()

    with open('/opt/airflow/dags/data/api_data.json', 'w') as f:
        json.dump(response_data, f)


# json to df and df to csv(save),
# df to postgres(store)(database_url)
def json_to_csv():
    df = pd.read_json('/opt/airflow/dags/data/api_data.json')
    df_team_flattened = pd.json_normalize(df)

    df.to_csv('/opt/airflow/dags/data/api_data.csv', index=False)
    
    database_url = 'postgresql://airflow:airflow@postgres:5432/airflow'
    engine = create_engine(database_url)
    df.to_sql('airflow', engine, if_exists='replace', index=False)

# DAG 
with DAG(
    dag_id = "My_DAG",
    schedule_interval='@daily',
    start_date=datetime(2023,9,19),
    catchup=False
) as dag:
    
    is_api_active = HttpSensor(
        task_id='is_api_active',
        http_conn_id='http_local',
        endpoint='todos/'
    )

    get_posts = SimpleHttpOperator(
        task_id = 'get_posts',
        http_conn_id='http_local',
        endpoint='todos/',
        method='GET',   
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    save_posts = PythonOperator(
        task_id = 'save_posts',
        python_callable=save_posts
    )
    
    read_table_task = PostgresOperator(
        sql = "select * from airflow",
        task_id = "read_table_task",
        postgres_conn_id = "airflow_postgres",
        autocommit=True
    )
    
    def process_postgres_result(**kwargs):
        ti = kwargs['ti']
        result = ti.xcom_pull(task_ids='read_table_task')
        
        for row in result:   # process and display each item 
            print(row)       # prints each row to the console
            
    
    process_postgres_result = PythonOperator(
        task_id='process_postgres_result',
        python_callable=process_postgres_result,
        provide_context=True   # access to Airflow context & XCom data.
    )        
    
    is_api_active >> get_posts >> save_posts  >> read_table_task >> process_postgres_result
    