from datetime import datetime, timedelta
import pandas as pd

import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


dag = DAG(
    dag_id="nytimes-bestsellers",
    description="A DAG to fetch data from NYTimes API and store it into a Postgres DB",
    start_date=datetime.now() - timedelta(days=1),
    schedule="0 3 * * THU",
    catchup=False
)

extract = BashOperator(
    task_id="extract_json",
    bash_command="curl -o /tmp/nytimes_lists.json -L https://api.nytimes.com/svc/books/v3/lists/overview.json?api-key={{ var.value.get('nytimes_api_key') }}",
    dag=dag
)


def _transform_data(**kwargs):
    json_data = pd.read_json("/tmp/nytimes_lists.json")
    book_lists = json_data["results"]["lists"]

    books_df = []
    for book_list in book_lists:
        for book in book_list["books"]:
            books_df.append({
                "title": book["title"],
                "author": book["author"],
                "description": book["description"],
                "publisher": book["publisher"],
                "book_uri": book["book_uri"],
                "amazon_url": book["amazon_product_url"],
                "category": book_list["display_name"],
                "rank": book["rank"],
                "rank_last_week": book["rank_last_week"],
                "weeks_on_list": book["weeks_on_list"]
            })

    ti = kwargs['ti']
    ti.xcom_push(key="books_df", value=books_df)


transform = PythonOperator(
    task_id="transform_data",
    python_callable=_transform_data,
    dag=dag
)


create_table = PostgresOperator(
    task_id="create_table",
    postgres_conn_id="postgres_nytimes_connection",
    sql="./sql/create_books.sql",
    dag=dag
)


def _load_data(**kwargs):
    ti = kwargs['ti']
    books_df = ti.xcom_pull(key="books_df", task_ids="transform_data")
    postgres_hook = PostgresHook(
        postgres_conn_id='postgres_nytimes_connection')

    insert = """
        INSERT INTO books (title, author, description, publisher, book_uri, 
        amazon_url, category, rank, rank_last_week, weeks_on_list)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for book in books_df:
        postgres_hook.run(insert, parameters=(
            book['title'], book['author'], book['description'], book['publisher'], book['book_uri'],
            book['amazon_url'], book['category'], book['rank'], book['rank_last_week'], book['weeks_on_list']
        ))


load = PythonOperator(
    task_id="load_data",
    python_callable=_load_data,
    dag=dag
)


# Dependencies
extract >> transform >> create_table >> load
