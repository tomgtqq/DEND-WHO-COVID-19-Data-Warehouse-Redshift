from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'Sparkify',
    'start_date': datetime.now() - timedelta(hours=2),
    'depends_on_past': False,
    'retries': 3, 
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}


dag = DAG('s3_ETL_redshift_data_warehouse_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval="@hourly"
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_events",
    s3_bucket="udacity-dend",
    s3_key="log_data",
    region="us-west-2",
    sql_statement=SqlQueries.create_staging_events_table,
    format_as_json="s3://udacity-dend/log_json_path.json"
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_songs",
    s3_bucket="udacity-dend",
    s3_key="song_data",
    region="us-west-2",
    sql_statement=SqlQueries.create_staging_songs_table,
    format_as_json="auto"
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="songplays",
    sql_create=SqlQueries.create_songplay_table,
    sql_insert=SqlQueries.songplay_table_insert,
    mode="append-only"
)


load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="users",
    sql_create=SqlQueries.create_user_table,
    sql_insert=SqlQueries.user_table_insert,
    mode="delete-load"
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="songs",
    sql_create=SqlQueries.create_song_table,
    sql_insert=SqlQueries.song_table_insert,
    mode="delete-load"
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="artists",
    sql_create=SqlQueries.create_artist_table,
    sql_insert=SqlQueries.artist_table_insert,
    mode="delete-load"
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="time",
    sql_create=SqlQueries.create_time_table,
    sql_insert=SqlQueries.time_table_insert,
    mode="delete-load"
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    tables=["songplays","users","songs","artists","time"]
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> [stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table >> [load_song_dimension_table, load_user_dimension_table, load_artist_dimension_table, load_time_dimension_table] >> run_quality_checks >> end_operator

