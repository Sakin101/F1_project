from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pipeline.discovery_job import run_discovery_job
from pipeline.scraping_job import run_scraping_job
from pipeline.summarization_job import run_summarization_job
default_args={
    "owner":"airflow",
    "retries":1,
    "retry_delay":timedelta(minutes=5)
}
with DAG(
    dag_id="f1_news_pipeline",
    default_args=default_args,
    start_date=datetime(2026,1,1),
    schedule="@daily",
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

    discovery >> scraping