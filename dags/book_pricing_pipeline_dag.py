from airflow import DAG
from airflow.operators.bash import BashOperator 
from datetime import datetime, timedelta

default_args = {
    "owner" : "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id = "book_pricing_pipeline_dag",
    default_args= default_args,
    start_date = datetime(2024, 1, 1),
    schedule_interval = "@daily",
    catchup = False,
) as dag:
    
    scrape_books = BashOperator(
        task_id = "scrape_books",
        bash_command = "python /opt/airflow/scripts/scrape_books.py"
    )

    save_raw_products = BashOperator(
        task_id="save_raw_products",
        bash_command="python /opt/airflow/scripts/save_raw_products.py",
    )

    fetch_exchange_rate = BashOperator(
        task_id="fetch_exchange_rate",
        bash_command="python /opt/airflow/scripts/fetch_exchange_rate.py",
    )

    transform_products = BashOperator(
        task_id="transform_products",
        bash_command="python /opt/airflow/scripts/transform_products.py",
    )

    scrape_books >> save_raw_products >> fetch_exchange_rate >> transform_products