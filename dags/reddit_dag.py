from airflow import DAG
from datetime import datetime
import os
import sys

from airflow.operators.python import PythonOperator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.aws_s3_pipeline import upload_s3_pipeline
from pipelines.reddit_pipeline import reddit_pipeline

default_args = {
    'owner': 'Sanod Malla',
    'start_date': datetime(year=2024, month=6, day=9)
}

# The format that we're going to append our files with

file_postfix = datetime.now().strftime("%Y%m%d")


# Define the schedule using cron expression
schedule = '0 0 * * *'  # Run daily at midnight

# basic DAG

dag = DAG(
    dag_id="etl_reddit_pipeline",
    default_args=default_args,
    schedule_interval=schedule,
    catchup=False,
    tags=['reddit', 'etl', 'pipeline'],
)

# extraction from reddit

extract = PythonOperator(
    task_id='reddit_extraction',
    python_callable=reddit_pipeline,
    op_kwargs={
        'file_name': f'reddit_{file_postfix}',
        'sub_reddit': 'Dataengineering',
        'time_filter': 'day',
        'limit': 100
    },
    dag=dag
)

# upload to s3

upload_s3 = PythonOperator(
    task_id= 's3_upload',
    python_callable= upload_s3_pipeline,
    dag=dag
)

extract >> upload_s3
