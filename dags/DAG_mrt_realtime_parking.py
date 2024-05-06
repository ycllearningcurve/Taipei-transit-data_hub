import requests
import pandas as pd
import json
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import re
from sqlalchemy import create_engine
from airflow.decorators import dag, task
from zoneinfo import ZoneInfo
from MRT_ETL_function.mrt_realtime_parking import E_mrt_realtime_parking, T_mrt_realtime_parking, L_mrt_realtime_parking
# 使用getenv拿取帳號密碼
load_dotenv()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["lala9456@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


@dag(
    dag_id="DAG_mrt_realtime_parking",
    default_args=default_args,
    description="ETL MRT realtime parking data to mysql",
    schedule_interval="*/5 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    # Optional: Add tags for better filtering in the UI
    tags=["example", "decorator"]
)
def DAG_mrt_realtime_parking():
    @task
    def DAG_E_task():
        return (E_mrt_realtime_parking())

    @task
    def DAG_T_task(df):
        return (T_mrt_realtime_parking(df=df))

    @task
    def DAG_L_task(df, port):
        return (L_mrt_realtime_parking(df, port))

    E_df = DAG_E_task()
    T_df = DAG_T_task(df=E_df)
    DAG_L_task(df=T_df, port="docker")


DAG_mrt_realtime_parking()
