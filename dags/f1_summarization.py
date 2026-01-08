from airflow import DAG
from airflow.operators.python import PythonOperator
from pipeline.summarization_job import run_summarization_job
from pipeline.discovery_job import run_discovery_job
from pipeline.scraping_job import run_scraping_job
from datetime import datetime,timedelta
default_args={
    "owner":"airflow",
    "retries":1,
    "retry_delay":timedelta(minutes=5)
}

with DAG(
    dag_id="f1_summarization",
    default_args=default_args,
    start_date=datetime(2026,1,1),
    schedule="0 0 */3 * *",
    catchup=False
) as dag:
    discovery=PythonOperator(
        task_id="rss_discovery",
        python_callable=run_discovery_job
    )
    scraping = PythonOperator(
        task_id="article_scraping",
        python_callable=run_scraping_job,
    )
    summarization=PythonOperator(
        task_id="summarization",
        python_callable=run_summarization_job
    )
    discovery>>scraping>>summarization
    