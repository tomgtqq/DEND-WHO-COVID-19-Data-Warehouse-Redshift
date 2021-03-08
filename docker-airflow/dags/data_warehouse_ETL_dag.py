from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'CapstoneProject',
    'start_date': datetime.now() - timedelta(days=2),
    'depends_on_past': False,
    'retries': 3, 
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}

dag = DAG('s3_ETL_redshift_data_warehouse_dag',\
          default_args=default_args,\
          description='Load and transform data in Redshift with Airflow',\
          schedule_interval='@daily'
        )

start_operator = DummyOperator(task_id='Begin_execution', dag=dag)

WHO_COVID19_data_to_redshift = StageToRedshiftOperator(
        task_id='Stage_WHO_COVID19_data',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="WHO_COVID19_data",
        s3_bucket=Variable.get('s3_bucket'),
        s3_key="WHO_COVID_19_global_data.csv",
        region="us-west-2",
        sql_statement=SqlQueries.create_WHO_COVID19_data_table,
        format=Variable.get('format')
    )

stage_country_vaccinations_to_redshift = StageToRedshiftOperator(
        task_id='Stage_country_vaccinations',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_vaccinations",
        s3_bucket=Variable.get('s3_bucket'),
        s3_key="country_vaccinations.csv",
        region="us-west-2",
        sql_statement=SqlQueries.create_staging_vaccinations_table,
        format=Variable.get('format')
    )

stage_country_code_to_redshift = StageToRedshiftOperator(
        task_id='Stage_country_code',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_country_code",
        s3_bucket=Variable.get('s3_bucket'),
        s3_key="country_code.csv",
        region="us-west-2",
        sql_statement=SqlQueries.create_staging_country_code_table,
        format=Variable.get('format')
    )

stage_countries_usefulFeatures_to_redshift = StageToRedshiftOperator(
        task_id='Stage_countries_usefulFeatures',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_useful_features",
        s3_bucket=Variable.get('s3_bucket'),
        s3_key="Countries_usefulFeatures.csv",
        region="us-west-2",
        sql_statement=SqlQueries.create_staging_useful_features_table,
        format=Variable.get('format')
    )

stage_GDP_per_capita_to_redshift = StageToRedshiftOperator(
        task_id='Stage_GDP_per_capita',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_GDP_per_capita",
        s3_bucket=Variable.get('s3_bucket'),
        s3_key="WORLD-DATA-by-country-2020/GDP_per_capita.csv",
        region="us-west-2",
        sql_statement=SqlQueries.create_staging_GDP_per_capita_table,
        format=Variable.get('format')
    )

stage_life_expectancy_to_redshift = StageToRedshiftOperator(
        task_id='Stage_life_expectancy',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_life_expectancy",
        s3_bucket=Variable.get('s3_bucket'),
        s3_key="WORLD-DATA-by-country-2020/Life_expectancy.csv",
        region="us-west-2",
        sql_statement=SqlQueries.create_staging_life_expectancy_table,
        format=Variable.get('format')
    )

stage_median_age_to_redshift = StageToRedshiftOperator(
        task_id='Stage_median_age',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_median_age",
        s3_bucket=Variable.get('s3_bucket'),
        s3_key="WORLD-DATA-by-country-2020/Median_age.csv",
        region="us-west-2",
        sql_statement=SqlQueries.create_staging_median_age_table,
        format=Variable.get('format')
    )

stage_population_growth_to_redshift = StageToRedshiftOperator(
        task_id='Stage_population_growth',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_population_growth",
        s3_bucket=Variable.get('s3_bucket'),
        s3_key="WORLD-DATA-by-country-2020/Population_growth.csv",
        region="us-west-2",
        sql_statement=SqlQueries.create_staging_population_growth_table,
        format=Variable.get('format')
    )

stage_urbanization_rate_to_redshift = StageToRedshiftOperator(
        task_id='Stage_urbanization_rate',
        dag=dag,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_urbanization_rate",
        s3_bucket=Variable.get('s3_bucket'),
        s3_key="WORLD-DATA-by-country-2020/Urbanization_rate.csv",
        region="us-west-2",
        sql_statement=SqlQueries.create_staging_urbanization_rate_table,
        format=Variable.get('format')
    )

load_vaccinations_fact_table = LoadFactOperator(
        task_id='load_vaccinations_fact_table',
        dag=dag,
        redshift_conn_id="redshift",
        table="vaccinations_fact",
        sql_create=SqlQueries.create_vaccinations_fact_table,
        sql_insert=SqlQueries.vaccinations_fact_table_insert,
        mode="append-only"
    )


load_country_region_dimension_table = LoadDimensionOperator(
        task_id='Load_country_region_dim_table',
        dag=dag,
        redshift_conn_id="redshift",
        table="country_region_dim",
        sql_create=SqlQueries.create_country_region_dimension_table,
        sql_insert=SqlQueries.country_region_dimension_table_insert,
        mode="delete-load"
    )

load__time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        dag=dag,
        redshift_conn_id="redshift",
        table="time_dim",
        sql_create=SqlQueries.create_time_dimension_table,
        sql_insert=SqlQueries.time_dimension_table_insert,
        mode="delete-load"
    )

load__vaccines_dimension_table = LoadDimensionOperator(
        task_id='Load_vaccines_dim_table',
        dag=dag,
        redshift_conn_id="redshift",
        table="vaccines_dim",
        sql_create=SqlQueries.create_vaccines_dimension_table,
        sql_insert=SqlQueries.vaccines_dimension_table_insert,
        mode="delete-load"
    )

load__source_dimension_table = LoadDimensionOperator(
        task_id='Load_source_dim_table',
        dag=dag,
        redshift_conn_id="redshift",
        table="source_dim",
        sql_create=SqlQueries.create_source_dimension_table,
        sql_insert=SqlQueries.source_dimension_table_insert,
        mode="delete-load"
    )

run_stage_quality_checks = DataQualityOperator(
        task_id='Run_stage_data_quality_checks',
        dag=dag,
        redshift_conn_id="redshift",
        tables=["WHO_COVID19_data",\
                "staging_vaccinations",\
                "staging_country_code",\
                "staging_useful_features",\
                "staging_GDP_per_capita",\
                "staging_life_expectancy",\
                "staging_median_age",\
                "staging_population_growth",\
                "staging_urbanization_rate"]
    )

run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        dag=dag,
        redshift_conn_id="redshift",
        tables=["vaccinations_fact","country_region_dim","time_dim","vaccines_dim","source_dim"]
    )

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> [WHO_COVID19_data_to_redshift,stage_country_vaccinations_to_redshift,stage_country_code_to_redshift,stage_countries_usefulFeatures_to_redshift,stage_GDP_per_capita_to_redshift,stage_life_expectancy_to_redshift,stage_median_age_to_redshift,stage_population_growth_to_redshift,stage_urbanization_rate_to_redshift] \
               >> run_stage_quality_checks \
               >> [load_vaccinations_fact_table,load_country_region_dimension_table,load__time_dimension_table,load__vaccines_dimension_table,load__source_dimension_table] \
               >> run_quality_checks >> end_operator