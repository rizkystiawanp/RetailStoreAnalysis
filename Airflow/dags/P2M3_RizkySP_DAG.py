'''
=================================================
Milestone 3

Nama  : Rizky Stiawan Pratama
Batch : HCK 024

Program ini dibuat untuk melakukan otomatisasi ekstraksi, transformasi, dan load (ETL) data dari PostgreSQL ke Elasticsearch menggunakan Apache Airflow.  
Adapun dataset yang digunakan adalah dataset penjualan berbagai kategori produk di beberapa wilayah selama periode 2022-2023.  

Dashboard yang dibuat bertujuan untuk memberikan wawasan bisnis terkait:  
- Distribusi penjualan berdasarkan kategori & wilayah  
- Tren pertumbuhan transaksi dari waktu ke waktu  
- Pola permintaan produk berdasarkan musim  
- Pengaruh harga pesaing terhadap volume penjualan  
- Dampak kondisi cuaca terhadap penjualan  

Dengan analisis ini, diharapkan tim bisnis dapat mengambil keputusan yang lebih akurat dalam strategi penjualan, pengelolaan stok, serta optimasi harga dan promosi.  

=================================================

'''

from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from elasticsearch import Elasticsearch
import pandas as pd
import os
from datetime import datetime, timedelta

# Default Arguments untuk DAG
default_args = {
    'owner': 'RizkySP',
    'start_date': datetime(2024, 11, 1),
    'catchup': False
}

# Function to fetch data from PostgreSQL
def fetch_from_postgres(**context):
    """
    Fungsi ini digunakan untuk mengambil data dari PostgreSQL 
    dan menyimpannya ke dalam file CSV untuk tahap data cleaning.

    Parameters:
    context: dict - Context dari Airflow untuk komunikasi antar task menggunakan XCom.

    Returns:
    Tidak ada return, tetapi menyimpan file CSV dan mengirim path file ke XCom.
    """
    source_hook = PostgresHook(postgres_conn_id="airflow_postgres")
    source_conn = source_hook.get_conn()
    df = pd.read_sql('SELECT * FROM table_m3', source_conn)
    file_path = '/opt/airflow/dags/P2M3_RizkySP_data_raw.csv'
    df.to_csv(file_path, index=False)
    context['ti'].xcom_push(key='data_path', value=file_path)

# Function to clean data
def data_cleaning(**context):
    """
    Fungsi ini digunakan untuk membersihkan data yang telah diambil dari PostgreSQL.
    - Menghapus duplikasi
    - Membersihkan nama kolom
    - Mengisi nilai yang kosong dengan default value

    Parameters:
    context: dict - Context dari Airflow untuk komunikasi antar task menggunakan XCom.

    Returns:
    Tidak ada return, tetapi menyimpan file CSV hasil cleaning dan mengirim path file ke XCom.
    """
    ti = context['ti']
    data_path = ti.xcom_pull(task_ids='fetch_from_postgres', key='data_path')
    df = pd.read_csv(data_path)
    df.drop_duplicates(inplace=True)
    df.columns = df.columns.str.strip().str.lower().str.replace(r'[^\w\s]', '', regex=True).str.replace(' ', '_')
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('Unknown')
        else:
            df[col] = df[col].fillna(0)
    clean_file_path = '/opt/airflow/dags/P2M3_RizkySP_data_clean.csv'
    df.to_csv(clean_file_path, index=False)
    ti.xcom_push(key='clean_data_path', value=clean_file_path)

# Function to push data to Elasticsearch
def post_to_elasticsearch(**context):
    """
    Fungsi ini digunakan untuk mengirim data hasil cleaning ke Elasticsearch.

    Parameters:
    context: dict - Context dari Airflow untuk komunikasi antar task menggunakan XCom.

    Returns:
    Tidak ada return, tetapi data akan diindeks ke Elasticsearch.
    """
    es = Elasticsearch(
        "http://elasticsearch:9200",
    )
    if es.ping():
        print("Connected to Elasticsearch")
    else:
        print("Connection to Elasticsearch failed")
    
    
    ti = context['ti']

    
    data_path = ti.xcom_pull(task_ids='data_cleaning', key='clean_data_path')

    
    es = Elasticsearch(['http://elasticsearch:9200'])

    
    data_clean = pd.read_csv(data_path)

    
    index_name = "m3_data_clean"

    
    for _, row in data_clean.iterrows():  
        doc = row.to_dict()
        es.index(index=index_name, body=doc)  # uploadnya

    
    print(f"Sukses Upload dengan index, ke elasticsearch '{index_name}'.")

# DAG Definition
with DAG(
    dag_id='pipeline_milestone_3',
    default_args=default_args,
    schedule_interval='10,20,30 9 * * 6',  # Setiap Sabtu jam 09:10, 09:20, 09:30 AM
    catchup=False
) as dag:
    
    fetch_task = PythonOperator(
        task_id='fetch_from_postgres',
        python_callable=fetch_from_postgres,
        provide_context=True
    )
    
    clean_task = PythonOperator(
        task_id='data_cleaning',
        python_callable=data_cleaning,
        provide_context=True
    )
    
    post_task = PythonOperator(
        task_id='post_to_elasticsearch',
        python_callable=post_to_elasticsearch,
        provide_context=True,
        dag=dag
    )
    
    fetch_task >> clean_task >> post_task