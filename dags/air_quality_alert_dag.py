import sys
sys.path.insert(0, '/opt/airflow')


from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from api.ingest import  fetch_data
from twitter.bot import tweet






default_args = {
    'owner': 'Umid',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='air_quality_alert_dag',
    description='A DAG that alerts about when the air quality is bad',
    start_date=datetime(2026, 5, 2, 3),
    schedule='5 * * * *',  
    default_args=default_args
) as dag:
    task1 = PythonOperator(
        task_id='fetch_insert_data',
        python_callable=fetch_data
        
    )


    task2 = SQLExecuteQueryOperator(
        task_id = 'load_silver',
        conn_id = 'supabase_postgres',
        sql='SELECT load_silver();'
    )

    task3 = SQLExecuteQueryOperator(
        task_id = 'load_gold',
        conn_id = 'supabase_postgres',
        sql='SELECT load_gold();'
    )


    task4 = PythonOperator(
        task_id ='tweet',
        python_callable=tweet
    )

    task1 >> task2>>task3>>task4