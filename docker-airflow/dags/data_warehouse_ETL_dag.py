from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'CapstoneProject',
    'start_date': datetime(2020,1,1,0,0,0,0),
    'depends_on_past': False,
    'retries': 3, 
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}

with DAG('s3_ETL_redshift_data_warehouse_dag',\
          default_args=default_args,\
          description='Load and transform data in Redshift with Airflow',\
          schedule_interval="@monthly"\
        ) as dag:

    start_operator = DummyOperator(task_id='Begin_execution')

    WHO_COVID19_data_to_redshift = StageToRedshiftOperator(
        task_id='Stage_WHO_COVID19_data',
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="WHO_COVID19_data",
        s3_bucket="tomgt-dend-s3",
        s3_key="",
        region="us-west-2",
        sql_statement=SqlQueries.create_WHO_COVID19_data_table,
        format="gzip"
    )

    stage_country_vaccinations_to_redshift = StageToRedshiftOperator(
        task_id='Stage_country_vaccinations',
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_vaccinations",
        s3_bucket="tomgt-dend-s3",
        s3_key="",
        region="us-west-2",
        sql_statement=SqlQueries.create_staging_vaccinations_table,
        format="gzip"
    )

    stage_country_code_to_redshift = StageToRedshiftOperator(
        task_id='Stage_country_code',
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_country_code",
        s3_bucket="tomgt-dend-s3",
        s3_key="",
        region="us-west-2",
        sql_statement=SqlQueries.create_staging_country_code_table,
        format="gzip"
    )

    stage_countries_usefulFeatures_to_redshift = StageToRedshiftOperator(
        task_id='Stage_countries_usefulFeatures',
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_useful_features",
        s3_bucket="tomgt-dend-s3",
        s3_key="",
        region="us-west-2",
        sql_statement=SqlQueries.create_staging_useful_features_table,
        format="gzip"
    )

    # load_songplays_table = LoadFactOperator(
    #     task_id='Load_songplays_fact_table',
    #     dag=dag,
    #     redshift_conn_id="redshift",
    #     table="songplays",
    #     sql_create=SqlQueries.create_songplay_table,
    #     sql_insert=SqlQueries.songplay_table_insert,
    #     mode="append-only"
    # )


    # load_user_dimension_table = LoadDimensionOperator(
    #     task_id='Load_user_dim_table',
    #     dag=dag,
    #     redshift_conn_id="redshift",
    #     table="users",
    #     sql_create=SqlQueries.create_user_table,
    #     sql_insert=SqlQueries.user_table_insert,
    #     mode="delete-load"
    # )

    # load_song_dimension_table = LoadDimensionOperator(
    #     task_id='Load_song_dim_table',
    #     dag=dag,
    #     redshift_conn_id="redshift",
    #     table="songs",
    #     sql_create=SqlQueries.create_song_table,
    #     sql_insert=SqlQueries.song_table_insert,
    #     mode="delete-load"
    # )

    # load_artist_dimension_table = LoadDimensionOperator(
    #     task_id='Load_artist_dim_table',
    #     dag=dag,
    #     redshift_conn_id="redshift",
    #     table="artists",
    #     sql_create=SqlQueries.create_artist_table,
    #     sql_insert=SqlQueries.artist_table_insert,
    #     mode="delete-load"
    # )

    # load_time_dimension_table = LoadDimensionOperator(
    #     task_id='Load_time_dim_table',
    #     dag=dag,
    #     redshift_conn_id="redshift",
    #     table="time",
    #     sql_create=SqlQueries.create_time_table,
    #     sql_insert=SqlQueries.time_table_insert,
    #     mode="delete-load"
    # )

    # run_quality_checks = DataQualityOperator(
    #     task_id='Run_data_quality_checks',
    #     dag=dag,
    #     redshift_conn_id="redshift",
    #     tables=["songplays","users","songs","artists","time"]
    # )

    # end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

    # start_operator >> [stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table >> [load_song_dimension_table, load_user_dimension_table, load_artist_dimension_table, load_time_dimension_table] >> run_quality_checks >> end_operator

